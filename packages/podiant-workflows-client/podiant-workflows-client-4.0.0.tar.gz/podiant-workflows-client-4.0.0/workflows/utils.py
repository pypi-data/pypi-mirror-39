from importlib import import_module
from mimetypes import guess_extension, guess_type
from urllib.parse import urlparse
from .exceptions import NamespaceError, OperationError


def get_extension_from_mimetype(mimetype):
    if 'audio/mpeg' in mimetype:
        return '.mp3'

    if 'image/jpeg' in mimetype or 'image/pjpeg' in mimetype:
        return '.jpg'

    if 'application/octet-stream' not in mimetype:
        return guess_extension(mimetype)


def get_mimetype_from_url(url):
    urlparts = urlparse(url)
    mimetype, encoding = guess_type(urlparts.path)
    return mimetype


def check_function_exists(name):
    namespace, func = name.rsplit('.', 1)

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
        return getattr(module, func)
    except AttributeError:
        raise OperationError(
            'Operation does not exist.',
            {
                'namespace': namespace,
                'operation': func
            }
        )
