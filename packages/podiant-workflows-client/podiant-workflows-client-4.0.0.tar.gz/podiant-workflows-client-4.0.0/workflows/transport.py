from logging import getLogger
from .files import FileEncoder
from . import settings
import json
import os
import requests
import time


class RequestsTransport(object):
    def __init__(self, workflow):
        self.workflow = workflow

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
                    timeout=sleep or None,
                    verify=False,
                    *args,
                    **kwargs
                )
            except requests.exceptions.ReadTimeout:
                logger.warning('Podiant server timed out')
                time.sleep(sleep)
            else:
                response.raise_for_status()
                return response

    def patch(self, url, data, meta={}):
        jd = {
            'data': data
        }

        if any(meta):
            jd['meta'] = meta

        jd = json.dumps(
            jd,
            cls=FileEncoder(self.workflow)
        )

        return self.__method('patch', url, data=jd)
