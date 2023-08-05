from logging.config import dictConfig


__version__ = '1.2.1'
__all__ = [
    'endpoint',
    'operation',
    'setup_logging',
]


def setup_logging():
    dictConfig(
        {
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
    )
