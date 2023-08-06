import os

HOSTNAME = os.environ.get('HOSTNAME')
SERVICE_NAME = '-'.join(HOSTNAME.split('-')[:2])
SLACK_ERR_CHANNEL = 'backend-err-' + os.environ.get('APP_CONTEXT','local')
SLACK_PERFORMANCE_CHANNEL = 'backend-perf-' + os.environ.get('APP_CONTEXT','local')


#TOPICS
TOPIC_PERFORMANCE_SUCCESS = "performance/success/backend"
TOPIC_PERFORMANCE_SUBSCRIBE = "performance/sub/backend"
TOPIC_PERFORMANCE = "performance/+/backend"
TOPIC_BACKEND_EXCEPTION = "exceptions/backend"

