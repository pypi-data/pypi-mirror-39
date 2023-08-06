from . import settings
from .entities import Entity
from .exceptions import ServiceError
from .files import DownloadedFile
from .operations import Operation
from .queues import get_queue
from .transport import RequestsTransport
from .utils import check_function_exists
import logging
import os
import time


class Workflow(object):
    def __init__(self, workflow, operations, objects):
        self.id = workflow['id']
        self.url = workflow['links']['self']
        self.__workflow = workflow
        self.__objects = objects
        self.context = {}
        self.cleanup = []

        for operation in operations:
            check_function_exists(
                operation['attributes']['name']
            )

        logger = logging.getLogger('podiant.workflows')
        logger.debug('New workflow: %(id)s' % workflow)

        for obj in objects:
            if obj['type'] == 'workflows':
                if obj['id'] == workflow['attributes']['parent']:
                    self.context.update(
                        obj['attributes'].get('result', {})
                    )

        args = workflow['attributes'].get('args', {})
        self.context.update(args)

        if 'object' in self.context:
            for obj in objects:
                if obj['type'] == args['object']['type']:
                    if obj['id'] == args['object']['id']:
                        self.context['object'] = Entity(obj)
                        break

        if 'media' in self.context:
            self.context['media'] = DownloadedFile(
                self.context['media']
            )

        self.__original_context = sorted(set(self.context.keys()))
        self.__operations = operations

    def enqueue(self):
        logger = logging.getLogger('podiant.workflows')
        logger.debug(
            'Enqueuing workflow',
            extra={
                'workflow': self.id
            }
        )

        queue = get_queue()
        queue.enqueue(self.work, timeout='1h')

    def requeue(self, reason):
        rqc = getattr(self, 'requeue_count', 0) + 1
        logger = logging.getLogger('podiant.workflows')

        if rqc == settings.REQUEUE_COUNT_LIMIT:
            logger.warning(
                (
                    'Workflows has been requeued too many times. '
                    'Abandoned after %d attempt%s'
                ) % (
                    rqc,
                    rqc != 1 and 's' or '',
                ),
                extra={
                    'workflow': self.id
                }
            )

            try:
                RequestsTransport(self).patch(
                    self.url,
                    data={
                        'type': 'workflows',
                        'id': self.id,
                        'attributes': {
                            'status': 'failed',
                            'result': {
                                'message': reason
                            }
                        }
                    }
                )
            except Exception:  # pragma: no cover
                logger.warning(
                    'Error communicating abandonment of workflow',
                    exc_info=True
                )

            return

        new = Workflow(
            self.__workflow,
            self.__operations,
            self.__objects
        )

        new.requeue_count = rqc

        sleep = int(os.getenv('WORKFLOW_REQUEUE_SLEEP', '5'))
        logger.warning(
            (
                'Requeuing workflow due to service failure. '
                'Waiting %d second%s; '
                'attempt %d'
            ) % (
                sleep,
                sleep != 1 and 's' or '',
                rqc + 1
            ),
            extra={
                'workflow': self.id
            }
        )

        time.sleep(sleep)
        queue = get_queue()
        queue.enqueue(new.work, timeout='1h')

    def _cleanup(self):
        while len(self.cleanup):
            self.cleanup.pop()()

    def work(self):
        transport = RequestsTransport(self)

        try:
            for description in self.__operations:
                operation = Operation(self, description)
                result = operation.run()

                if result is False:
                    try:
                        transport.patch(
                            self.url,
                            data={
                                'type': 'workflows',
                                'id': self.id,
                                'attributes': {
                                    'status': 'failed',
                                    'result': {
                                        'message': '%s operation failed.' % (
                                            operation.verbose_name
                                        )
                                    }
                                }
                            }
                        )
                    finally:
                        self._cleanup()

                    return

            try:
                transport.patch(
                    self.url,
                    data={
                        'type': 'workflows',
                        'id': self.id,
                        'attributes': {
                            'status': 'successful',
                            'result': dict(
                                [
                                    (key, value)
                                    for (key, value) in self.context.items()
                                    if key != 'object'
                                ]
                            )
                        }
                    }
                )
            finally:
                self._cleanup()
        except ServiceError as ex:
            self.requeue(ex.args[0])

    @property
    def operations(self):
        return [o for o in self.__operations]

    def new_result(self, result):
        nr = {}

        for key, value in result.items():
            if key in self.__original_context:
                continue

            nr[key] = value

        return nr
