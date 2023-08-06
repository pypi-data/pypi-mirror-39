from redis import StrictRedis
from rq import queue
from . import settings


def get_queue():
    connection = StrictRedis.from_url(settings.REDIS_URL)
    return queue.Queue(settings.RQ_QUEUE, connection=connection)
