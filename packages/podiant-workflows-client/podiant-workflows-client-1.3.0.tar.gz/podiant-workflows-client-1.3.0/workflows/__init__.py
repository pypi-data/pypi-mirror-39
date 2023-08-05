from logging.config import dictConfig
from . import settings


__version__ = '1.3.0'
__all__ = [
    'endpoint',
    'operation',
    'setup_logging',
]


def setup_logging():
    dictConfig(settings.LOGGING)
