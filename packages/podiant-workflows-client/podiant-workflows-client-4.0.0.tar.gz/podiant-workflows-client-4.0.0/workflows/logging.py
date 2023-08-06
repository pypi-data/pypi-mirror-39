import logging
import os


def setup_logging(**context):
    dsn = os.getenv('SENTRY_DSN')
    handler = None

    if not dsn:
        if context.get('worker'):
            console = logging.StreamHandler()
            logger = logging.getLogger('podiant.workflows')
            logger.setLevel(logging.DEBUG)
            logger.addHandler(console)

        return

    from raven import Client
    from raven.transport.http import HTTPTransport
    from raven.handlers.logging import SentryHandler
    from raven.conf import setup_logging as sl

    client = Client(dsn, transport=HTTPTransport)
    if context.get('app'):
        from raven.contrib.flask import Sentry

        Sentry(
            client=client,
            logging=True,
            level=logging.WARN
        ).init_app(
            context['app']
        )
    elif context.get('worker'):
        from rq.contrib.sentry import register_sentry
        register_sentry(client, context['worker'])

    handler = SentryHandler(client)
    handler.setLevel(logging.WARN)
    sl(handler)
