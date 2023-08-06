from chatqhelper.mqtt import MqttClient
from chatqhelper import scheduler
from chatqhelper import debug
import time


logger = debug.logger(__name__)


class MqttHandler:
    def __init__(self, interval=1):
        self._mqtt_client = MqttClient.create(self._on_mqtt_connect, handle_in_thread=True)
        self._interval = interval

    @property
    def mqtt(self):
        return self._mqtt_client

    def start(self):
        self._mqtt_client.loop_start()
        self.loop()

    def loop(self):
        while True:
            time.sleep(self._interval)
            self._loop_imp()

    def _loop_imp(self):
        pass

    def stop(self):
        self._mqtt_client.loop_stop()

    def restart(self):
        self.stop()
        self.start()

    def _on_mqtt_connect(self, client, userdata, flags, rc):
        logger.info('connected to solace with code ' + str(rc))


class MqttAndScheduleHandler(MqttHandler):
    def __init__(self):
        super().__init__()
        self._scheduler = scheduler.UTCScheduler()

    @property
    def scheduler(self):
        return self._scheduler

    def start(self):
        self._scheduler.loop_start()
        super().start()

    def stop(self):
        self._scheduler.loop_stop()
        super().stop()
