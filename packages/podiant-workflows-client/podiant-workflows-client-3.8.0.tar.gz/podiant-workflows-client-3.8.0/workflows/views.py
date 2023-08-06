from flask import request, jsonify
from hashlib import sha512
from . import settings
from .exceptions import NamespaceError, OperationError
from .workflows import Workflow
import logging


logger = logging.getLogger('podiant.workflows')


def endpoint():
    try:
        body = request.get_json()
        assert isinstance(body, dict)
    except Exception:
        logger.warning('Request rejected as not JSON', exc_info=True)

        return (
            jsonify(
                {
                    'error': {
                        'status': 400,
                        'title': 'Bad Request',
                        'detail': 'Invalid JSON data.'
                    }
                }
            ),
            400
        )

    try:
        assert 'meta' in body
        assert 'digest' in body['meta']
        digest = body['meta']['digest']

        assert 'signed-digest' in body['meta']
        supplied_digest = body['meta']['signed-digest']
    except AssertionError:
        logger.warning(
            'Request rejected as not authorised',
            exc_info=True
        )

        return (
            jsonify(
                {
                    'error': {
                        'status': 401,
                        'title': 'Unauthorized',
                        'detail': 'Missing digest and/or signed digest.'
                    }
                }
            ),
            401
        )

    correct_digest = sha512(
        (digest + settings.API_KEY).encode('utf-8')
    ).hexdigest()

    if supplied_digest != correct_digest:
        return (
            jsonify(
                {
                    'error': {
                        'status': 401,
                        'title': 'Unauthorized',
                        'detail': 'Signed digest is invalid.'
                    }
                }
            ),
            401
        )

    operations = []

    try:
        assert 'data' in body
        data = body['data']

        assert 'type' in data
        assert data['type'] == 'workflows'

        assert 'id' in data
        assert 'attributes' in data

        assert 'included' in body
        for included in body['included']:
            assert 'id' in included
            assert 'type' in included

    except AssertionError:
        logger.warning(
            'Request rejected as not conformant with API spec',
            exc_info=True
        )

        return (
            jsonify(
                {
                    'error': {
                        'status': 400,
                        'title': 'Bad Request',
                        'detail': (
                            'Data does not conform to Podiant Factory '
                            'spec.'
                        )
                    }
                }
            ),
            400
        )

    objects = []
    for included in body['included']:
        if included['type'] == 'operations':
            operations.append(included)
        else:
            objects.append(included)

    if not any(operations):
        logger.warning(
            'Request rejected as missing operations'
        )

        return (
            jsonify(
                {
                    'error': {
                        'status': 400,
                        'title': 'Bad Request',
                        'detail': 'Missing included operation objects.'
                    }
                }
            ),
            400
        )

    try:
        workflow = Workflow(data, operations, objects)
    except (NamespaceError, OperationError) as ex:
        return (
            jsonify(
                {
                    'error': {
                        'status': 400,
                        'title': 'Bad Request',
                        'detail': ex.args[0],
                        'meta': ex.args[1]
                    }
                }
            ),
            400
        )

    workflow.enqueue()

    return (
        jsonify(True),
        200
    )
