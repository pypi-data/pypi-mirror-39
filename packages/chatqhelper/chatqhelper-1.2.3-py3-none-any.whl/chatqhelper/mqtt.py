import os, threading
import json
from  chatqhelper import debug
import paho.mqtt.client as mqtt
import uuid
from chatqhelper import exceptions, utils
from chatqhelper.common import constants
from chatqhelper.perf_tracking import  PerformanceTracking


logger = debug.logger("chatqhelper.mqtt")


class MqttClient(mqtt.Client):
    def __init__(self,**kwargs):
        self._publish_exception = kwargs.pop('publish_exception', True)
        self._handle_in_thread = kwargs.pop('handle_in_thread', False)
        self._publish_performance = kwargs.pop('publish_performance', False)
        super(MqttClient, self).__init__(**kwargs)
        self.is_log_request = False
        if self._publish_exception:
            self._error_publisher = MqttErrorPublisher(mqtt_client=self)

    def log_request(self, is_log=True):
        self.is_log_request = is_log

    def _handle_on_message(self, message):
        try:
            payload = message.payload
            payload = payload.decode('utf-8') if isinstance(payload, bytes) else payload
            message.payload = json.loads(payload)
            if self.is_log_request:
                logger.info("request: " + message.topic.strip() + " -- " + str(message.payload))

            self._custom_call_callback_list(message)
        except Exception as e:
            self.publish_exception(e, message)

    def _custom_call_callback_list(self, message):
        """
            This method is use to replace the default behavior of _handle_on_message
            We need this class to call not one but a list of callback.
            We also do some custom variable as well. Like split topic out of message...
        """
        with self._callback_mutex:
            try:
                iterator = self._on_message_filtered.iter_match(message.topic)
            except Exception:
                logger.info("TOPIC NOT FOUND")
            else:
                for callback_dict in iterator:
                    for callback in list(callback_dict.values()):
                        with self._in_callback:
                            if self._handle_in_thread:
                                MqttThread(
                                    target=callback,
                                    args=(self, message)
                                ).start()
                            else:
                                callback(self, message)

            if self.on_message:
                with self._in_callback:
                    self.on_message(self, message)

    def message_callback_add(self, sub, callback):
        """
            To allow multiple callback on a single topic, we need to do a few custom.
            This method will replace _on_message_filtered map from single callback map
            to a list of callback
        """
        self.subscribe(sub)
        if callback is None or sub is None:
            raise ValueError("sub and callback must both be defined.")

        if self._publish_performance:
            PerformanceTracking.subscribe(self, sub)
            callback = PerformanceTracking.track(callback)

        callback_id = str(uuid.uuid4())
        with self._callback_mutex:
            try:
                self._on_message_filtered[sub][callback_id] = callback
            except Exception:
                self._on_message_filtered[sub] = {
                    callback_id: callback
                }

        return callback_id

    def message_callback_remove(self, callback_id_list):
        """
            Because we now allow multiple call back on a single topic. We need a way to remove it
            using a unique id that is generated during callback registration
        """
        for sub, callback_id in callback_id_list:
            with self._callback_mutex:
                try:
                    del self._on_message_filtered[sub][callback_id]
                except KeyError:  # no such subscription
                    pass

    def publish_exception(self, exception, message):
        logger.error(
            'exception from message: {0} {1}'.format(
                message.topic,
                str(message.payload)
            )
        )

        error = utils.err_to_dict(exception)
        #remove traceback from reply to frontend
        tb = error.pop('traceback', None)

        logger.error(error)
        debug.log_traceback(logger)
        if not self._publish_exception:
            return
        try:
            correlation_id = message.payload.get('correlation_id', None)
            # reply
            if correlation_id is not None:
                self.reply(message, error)

            # publish to exceptions/ topics
            if self._error_publisher:
                source_payload = message.payload
                if 'auth_key' in source_payload:
                    source_payload['auth_key'] = '---'
                error.update({
                    'source_topic': message.topic,
                    'source_payload': message.payload,
                    # add back traceback
                    'traceback': tb
                })
                self._error_publisher.publish(error)
        except Exception as e:
            # nothing we can do here except for logging
            logger.error(e)
            debug.log_traceback(logger)

    def reply(self, msg, data, log_response=False, qos=1):
        """ reply to topic with corresponding correlation_id
        default qos is 1
        return _context if it exists
        """
        topic = msg.topic + "/reply-to/" + str(msg.payload.get('correlation_id'))
        # update context
        context = msg.payload.get('_context', {})
        if context:
            data.update({'_context': context})
        payload = json.dumps(data)
        if log_response:
            logger.info("reply: " + topic + " -- " + payload)

        self.publish(topic, payload, qos=qos)

    def setup_message_callbacks(self, *args):
        for topic, callback in args:
            self.message_callback_add(topic, callback)

    @classmethod
    def create(cls, on_connect, is_log_request=False, **kwargs):
        if not 'post_fix' in kwargs:
            kwargs['post_fix'] = 'main'
        post_fix = kwargs.pop('post_fix')
        post_fix = '-' + post_fix if not post_fix[0] == '-' else post_fix
        kwargs['post_fix'] = post_fix

        if 'client_id' not in kwargs:
            kwargs['client_id'] = constants.HOSTNAME + kwargs.pop('post_fix','')+ '-pid{}'.format(str(os.getpid()))
            logger.info('Chatq MqttClient initalized with default client id {}'.format(kwargs['client_id']))

        username = os.environ.get('SOL_USERNAME', '')
        password = os.environ.get('SOL_PASSWORD', '')
        host = os.environ.get('SOL_URI', '')
        port = int(os.environ.get('SOL_MQTT_PORT', '0'))
        keepalive = 60
        if 'username' in kwargs:
            username = kwargs.pop('username')

        if 'password' in kwargs:
            password = kwargs.pop('password')

        if 'host' in kwargs:
            host = kwargs.pop('host')

        if 'port' in kwargs:
            port = kwargs.pop('port')

        if 'keepalive' in kwargs:
            keepalive = kwargs.pop('keepalive')

        client = cls(**kwargs)
        client.log_request(is_log_request)
        client.on_connect = on_connect
        client.username_pw_set(username=username, password=password)
        client.connect_async(host, port, keepalive)
        return client


class MqttErrorPublisher():
    """ error publisher will publish error to exceptions/backend
    """
    def __init__(self, mqtt_client=None):
        self._mqtt_client = mqtt_client
        if not self._mqtt_client:
            mqtt_client = MqttClient.create(self._on_connect, post_fix='err-publisher')
            mqtt_client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        print("connect with code " + str(rc))
        self._mqtt_client = client

    def publish(self, error_msg):
        """
        publish error with added info
         - trace_back
         - service
         - hostname
        """
        client = self._mqtt_client
        if client:
            client.publish(
                'exceptions/backend',
                json.dumps(error_msg)
            )
        else:
            logger.warning('invalid mqtt client, not publishing error')


class MqttThread(threading.Thread):
    """ used in MqttClient to catch thread's exceptions
    """
    def run(self):
        # NOTE: args must follow the Chatq Mqtt handler signature (client, message)
        mqtt_client, message = self._args
        try:
            super(MqttThread, self).run()
        except Exception as e:
            mqtt_client.publish_exception(e, message)
