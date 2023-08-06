from rq import Worker
from .logging import setup_logging


class LoggedWorker(Worker):
    def work(self, *args, **kwargs):
        setup_logging(worker=self)
        super().work(*args, **kwargs)
