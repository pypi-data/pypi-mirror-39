from logging import getLogger
from . import settings
import os
import requests
import time


class RequestsTransport(object):
    def __method(self, method, *args, **kwargs):
        logger = getLogger('podiant.workflows')
        func = getattr(requests, method)
        sleep = int(os.getenv('WORKFLOW_TIMEOUT_SLEEP', '5'))

        while True:
            try:
                response = func(
                    headers={
                        'Authorization': 'Bearer %s' % settings.API_KEY,
                        'Content-Type': 'application/vnd.api+json'
                    },
                    timeout=5,
                    verify=False,
                    *args,
                    **kwargs
                )
            except requests.exceptions.ReadTimeout:
                time.sleep(sleep)
            except Exception:  # pragma: no cover
                logger.error(
                    'Error communicating with Podiant API',
                    exc_info=True,
                    response=response
                )

                raise
            else:
                logger.debug(
                    '%s %s %d' % (
                        method.upper(),
                        args[0],
                        response.status_code
                    )
                )

                response.raise_for_status()
                return response

    def patch(self, *args, **kwargs):
        return self.__method('patch', *args, **kwargs)
