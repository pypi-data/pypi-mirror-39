from .exceptions import ProgrammingError, ServiceError
from .transport import RequestsTransport
from .utils import check_function_exists
import logging


class Operation(object):
    def __init__(self, workflow, data):
        self.workflow = workflow
        self.id = data['id']
        self.name = data['attributes']['name']
        self.func = check_function_exists(self.name)
        self.can_fail = data['attributes']['can-fail']
        self.url = data['links']['self']
        self.verbose_name = getattr(
            self.func,
            '_process_name',
            None
        ) or (
            self.name.split('.')[-1].replace('_', ' ').capitalize()
        )

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
        transport = RequestsTransport(self.workflow)
        logger = logging.getLogger('podiant.workflows')

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
                logger.debug('Progress = %s%%' % progress)

            if status == 'running' and self.status == 'running':
                if not advanced:
                    return

        self.status = status
        transport.patch(
            self.url,
            data={
                'type': 'operations',
                'id': self.id,
                'attributes': attributes
            },
            meta={
                'verbose-name': (
                    message or self.verbose_name or ''
                )[:100],
                'description': self.description
            }
        )

        logger.debug(
            'Set status of operation "%s" to "%s"' % (
                self.name,
                status
            )
        )

    def run(self):
        logger = logging.getLogger('podiant.workflows')
        logger.debug('Running operation "%s"' % self.name)

        self.update()
        args = []

        if self.takes_context:
            args.append(self)

        try:
            result = self.func(*args, **self.workflow.context)
        except ServiceError:
            raise
        except Exception as ex:
            logger.error('Error running operation', exc_info=True)
            self.update('failed', message=str(ex))
            return self.can_fail

        if isinstance(result, dict):
            self.workflow.context.update(result)
            self.update('successful', **result)
            return True

        if result is not None and result is not False:
            raise ProgrammingError('Invalid response')  # pragma: no cover

        self.update('successful')
        return True
