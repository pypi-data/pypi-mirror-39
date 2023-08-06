from botocore.client import Config
from datetime import timedelta
from json import JSONEncoder
from logging import getLogger
from mimetypes import guess_type
from os import path, write, close, remove
from rq_scheduler import Scheduler
from shutil import copyfile
from tempfile import mkstemp
from . import settings, utils
from .exceptions import ServiceError
from .queues import get_queue
import boto3
import os
import requests
import time
import uuid


class DownloadedFile(object):
    def __init__(self, url):
        self.url = url
        self.__filename = None

    @property
    def mimetype(self):
        if not hasattr(self, '__mimetype'):
            self.__mimetype = utils.get_mimetype_from_url(
                self.url
            )

        return self.__mimetype

    def read(self, mode=''):
        filename = self.download()
        with open(filename, 'r%s' % mode) as f:
            return f.read()

    def __download(self):
        response = requests.get(
            self.url,
            headers={
                'User-Agent': (
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac '
                    'OS X) AppleWebKit/602.1.38 (KHTML, like Gecko) '
                    'Version/10.0 Mobile/14A300 Safari/602.1'
                )
            },
            stream=True,
            verify=False
        )

        if response.status_code < 500:
            response.raise_for_status()
            return response

    def download(self):
        logger = getLogger('podiant.workflows')

        if self.__filename is None:
            logger.debug(
                'Downloading file',
                extra={
                    'url': self.url
                }
            )

            sleep = int(os.getenv('WORKFLOW_DOWNLOAD_RETRY_SLEEP', '15'))

            while True:
                try:
                    response = self.__download()
                except Exception:
                    logger.error(
                        'Error downloading media',
                        exc_info=True,
                        extra={
                            'url': self.url
                        }
                    )

                    raise ServiceError('Error obtaining media file')

                time.sleep(sleep)
                if response is not None:
                    break

            self.__mimetype = response.headers['Content-Type']
            ext = None

            if self.__mimetype:
                ext = utils.get_extension_from_mimetype(
                    self.__mimetype
                )

            if not ext:
                self.__mimetype = utils.get_mimetype_from_url(self.url)
                ext = utils.get_extension_from_mimetype(self.__mimetype)

            handle, self.__filename = mkstemp(suffix=ext)

            try:
                for chunk in response.iter_content(chunk_size=1024):
                    write(handle, chunk)
            finally:
                close(handle)

        return self.__filename

    def copy(self):
        filename = self.download()
        return UploadedFile.from_file(filename)


class UploadedFile(object):
    def __init__(self, mimetype):
        if mimetype is None:
            raise TypeError('MIME type cannot be null.')

        ext = utils.get_extension_from_mimetype(mimetype)
        handle, self.filename = mkstemp(suffix=ext)
        close(handle)

        self.mimetype = mimetype
        self.__uploaded = None

    def download(self):
        return self.filename

    def copy(self):
        return self

    @property
    def filesize(self):
        return path.getsize(self.filename)

    def write(self, content):
        if isinstance(content, bytes):
            open(self.filename, 'wb').write(content)
        else:
            open(self.filename, 'w').write(content)

    def upload(self, key=None):
        if self.__uploaded is None:
            if key is None:
                key = '%s%s' % (
                    str(uuid.uuid4()),
                    path.splitext(self.filename)[-1]
                )

            client = boto3.client(
                's3',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                config=Config(
                    s3={
                        'addressing_style': settings.AWS_S3_ADDRESSING_STYLE
                    }
                )
            )

            with open(self.filename, 'rb') as f:
                try:
                    client.put_object(
                        Bucket=settings.AWS_S3_BUCKET,
                        Key=key,
                        Body=f,
                        ContentType=self.mimetype
                    )
                except Exception:
                    raise ServiceError('Error saving media file')

            self.__uploaded = client.generate_presigned_url(
                'get_object',
                Params=dict(
                    Bucket=settings.AWS_S3_BUCKET,
                    Key=key
                ),
                ExpiresIn=3600
            )

            try:
                Scheduler(
                    connection=get_queue().connection
                ).enqueue_in(
                    timedelta(hours=1),
                    'os.remove',
                    self.filename
                )
            except Exception:  # pragma: no cover
                pass

        return self.__uploaded

    @staticmethod
    def from_file(filename):
        mimetype, encoding = guess_type(filename)
        obj = UploadedFile(mimetype)
        copyfile(filename, obj.filename)

        return obj


def FileEncoder(workflow):
    class Encoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, DownloadedFile):
                return obj.url

            if isinstance(obj, UploadedFile):
                value = obj.upload()
                workflow.cleanup.append(
                    lambda: path.exists(obj.filename) and remove(obj.filename)
                )

                return value

            return super().default(obj)  # pragma: no cover

    return Encoder
