import os

HOSTNAME = os.environ.get('HOSTNAME')
SERVICE_NAME = '-'.join(HOSTNAME.split('-')[:2])
SLACK_ERR_CHANNEL = 'backend-err-' + os.environ.get('APP_CONTEXT','local')
SLACK_PERFORMANCE_CHANNEL = 'backend-perf-' + os.environ.get('APP_CONTEXT','local')