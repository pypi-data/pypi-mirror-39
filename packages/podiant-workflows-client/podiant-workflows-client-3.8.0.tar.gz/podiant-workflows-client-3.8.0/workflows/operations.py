from importlib import import_module
from .exceptions import NamespaceError, OperationError, ProgrammingError
from .files import FileEncoder
from .transport import RequestsTransport
import json
import logging


class Operation(object):
    def __init__(self, workflow, data):
        self.workflow = workflow
        self.id = data['id']
        self.name = data['attributes']['name']

        namespace, func = self.name.rsplit('.', 1)

        try:
            module = import_module(namespace)
        except ImportError:
            raise NamespaceError(
                'Not equipped to run this operation.',
                {
                    'namespace': namespace
                }
            )

        try:
            self.func = getattr(module, func)
        except AttributeError:
            raise OperationError(
                'Operation does not exist.',
                {
                    'namespace': namespace,
                    'operation': func
                }
            )

        self.can_fail = data['attributes']['can-fail']
        self.url = data['links']['self']

        self.verbose_name = getattr(
            self.func,
            '_process_name',
            None
        ) or func.replace('_', ' ').capitalize()

        self.description = getattr(
            self.func,
            '_process_description',
            ''
        )

        self.takes_context = getattr(self.func, '_takes_context', False)
        self.progress = 0
        self.status = 'scheduled'

    def update(
        self,
        status='running',
        progress=None,
        force_update=False,
        message=None,
        **result
    ):
        attributes = {
            'status': status
        }

        nc = self.workflow.new_result(result)
        if status == 'failed' and message:
            nc['message'] = message

        advanced = force_update

        if any(nc.keys()):
            attributes['result'] = nc

        if progress is not None:
            p = float(progress)

            if p > self.progress:
                if p < 100 and status == 'running':
                    remainder = int(round(p, 0)) % 10
                    if remainder == 0:
                        attributes['progress'] = p
                        advanced = True

                self.progress = progress

            if status == 'running' and self.status == 'running':
                if not advanced:
                    return

        self.status = status
        data = json.dumps(
            {
                'data': {
                    'type': 'operations',
                    'id': self.id,
                    'attributes': attributes
                },
                'meta': {
                    'verbose-name': (
                        message or self.verbose_name or ''
                    )[:100],
                    'description': self.description
                }
            },
            cls=FileEncoder(self.workflow),
            indent=4
        )

        RequestsTransport().patch(
            self.url,
            data=data
        )

    def run(self):
        logger.debug(
            'Running operation %s ("%s")' % (
                self.id,
                self.name
            )
        )

        self.update()
        args = []

        if self.takes_context:
            args.append(self)

        try:
            result = self.func(*args, **self.workflow.context)
        except Exception as ex:
            logger.error('Error running operation', exc_info=True)
            self.update('failed', message=str(ex))
            return self.can_fail
        else:
            if isinstance(result, dict):
                self.workflow.context.update(result)
                self.update('successful', **result)
            elif result is not None and result is not False:
                raise ProgrammingError('Invalid response')  # pragma: no cover
            else:
                self.update('successful')

            return True


logger = logging.getLogger('podiant.workflows')
