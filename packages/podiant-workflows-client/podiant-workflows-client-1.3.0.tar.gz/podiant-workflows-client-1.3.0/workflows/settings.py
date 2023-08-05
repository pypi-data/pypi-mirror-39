import os


AWS_S3_ENDPOINT_URL = 'http%s://%s/' % (
    os.getenv('AWS_S3_SSL') != 'false' and 's' or '',
    os.getenv('AWS_S3_HOST', 's3-eu-west-1.amazonaws.com')
)

AWS_S3_ADDRESSING_STYLE = os.getenv('AWS_S3_ADDRESSING_STYLE', 'auto')
AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET', 'workflows')

API_KEY = os.getenv('WORKFLOW_API_KEY')
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379')
RQ_QUEUE = os.getenv('RQ_QUEUE')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console']
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'boto3': {
            'level': 'CRITICAL',
            'handlers': [],
            'propagate': False
        },
        'rq.worker': {
            'level': 'WARNING'
        },
        'podiant.workflows': {
            'level': 'DEBUG'
        }
    }
}

try:
    import timber  # NOQA
except ImportError:
    pass
else:
    if os.getenv('TIMBER_API_KEY'):
        LOGGING['handlers']['timber'] = {
            'level': 'DEBUG',
            'class': 'timber.TimberHandler',
            'api_key': os.getenv('TIMBER_API_KEY')
        }
