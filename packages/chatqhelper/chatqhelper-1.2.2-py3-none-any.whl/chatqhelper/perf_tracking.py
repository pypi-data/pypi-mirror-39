from functools import wraps
from chatqhelper.common import constants
import time
import json


class PerformanceTracking:
    """Caculate time to completion for a task will publish to performance-report/backend topic
    """
    @staticmethod
    def subscribe(client, topic):
        client.publish(
            'topic_sub_perf_tracking/backend',
            json.dumps({'topic':topic})
        )
    
    @staticmethod
    def track(func):
        @wraps(func)
        def _wraper(client, message):  
            start_time = time.process_time()
            func(client, message)
            end_time = time.process_time()
            report = {'topic': message.topic, 'start_time': start_time, 'end_time': end_time}
            client.publish(
                'performance-report/backend',
                json.dumps(report)
            )
        return _wraper