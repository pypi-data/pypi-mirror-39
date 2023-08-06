from .entities import Entity
from .files import DownloadedFile, FileEncoder
from .operations import Operation
from .queues import get_queue
from .transport import RequestsTransport
import json
import logging


class Workflow(object):
    def __init__(self, workflow, operations, objects):
        self.id = workflow['id']
        self.url = workflow['links']['self']
        self.context = {}
        self.cleanup = []

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

        self.operations = [
            Operation(self, operation)
            for operation in operations
        ]

    def enqueue(self):
        logger = logging.getLogger('podiant.workflows')
        logger.debug('Enqueuing')

        queue = get_queue()
        queue.enqueue(self.work, timeout='1h')

    def _cleanup(self):
        while len(self.cleanup):
            self.cleanup.pop()()

    def work(self):
        transport = RequestsTransport()

        for operation in self.operations:
            if operation.run() is False:
                data = json.dumps(
                    {
                        'data': {
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
                    },
                    indent=4
                )

                try:
                    transport.patch(
                        self.url,
                        data=data
                    )
                finally:
                    self._cleanup()

                return

        data = json.dumps(
            {
                'data': {
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
            },
            cls=FileEncoder(self),
            indent=4
        )

        try:
            transport.patch(
                self.url,
                data=data
            )
        finally:
            self._cleanup()

    def new_result(self, result):
        nr = {}

        for key, value in result.items():
            if key in self.__original_context:
                continue

            nr[key] = value

        return nr
