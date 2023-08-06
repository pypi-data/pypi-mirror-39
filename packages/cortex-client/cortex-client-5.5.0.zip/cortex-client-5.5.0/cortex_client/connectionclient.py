
"""
Copyright 2018 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

from .serviceconnector import ServiceConnector
from .types import InputMessage
from .client import build_client

class ConnectionClient:
    """
    A client used to manage connections.
    """
    URIs = {'content':  'content',
            'connections': 'connections'}

    def __init__(self, url, version, token):
        self._serviceconnector = ServiceConnector(url, version, token)

    def save_connection(self, connection: object):
        """
        Posts the connection client information.
        """
        uri  = self.URIs['connections']
        data = json.dumps(connection)
        headers = {'Content-Type': 'application/json'}
        r = self._serviceconnector.request('POST', uri, data, headers)
        r.raise_for_status()
        return r.json()

    def upload(self, key: str, stream_name: str, stream: object, content_type: str):
        """
        Stores a `stream` file in S3.

        :param key: the path where the file is stored
        :param stream_name: the name under which the `stream` is saved
        :param stream: the file object
        :param content_type: the type of the file to store (e.g., `text/csv`)
        :return: a dict with the response to request upload

        .. NOTE: This method uses a multi-part form request; to upload very large files, use `uploadStreaming` instead.
        .. seealso: uploadStreaming()
        """
        uri = self.URIs['content']
        fields = {'key': key, 'content': (stream_name, stream, content_type)}
        data = MultipartEncoder(fields=fields)
        headers = {'Content-Type': data.content_type}
        r = self._serviceconnector.request('POST', uri, data, headers)
        r.raise_for_status()
        return r.json()

    def uploadStreaming(self, key: str, stream: object, content_type: str):
        """
        Stores a `stream` file in S3.

        :param key: the path where the file is stored
        :param stream: the file object
        :param content_type: the type of the file to store (e.g., `text/csv`)
        :return: A dict with the response to request upload
        """
        uri = self._make_content_uri(key)
        headers = {'Content-Type': content_type}
        r = self._serviceconnector.request('POST', uri, stream, headers)
        r.raise_for_status()
        return r.json()

    def download(self, key: str) :
        """
        Downloads a file from managed content (S3).

        :param key: the path of the file to retrieve
        :return: a generator
        """
        uri = self._make_content_uri(key)
        r = self._serviceconnector.request('GET', uri, stream=True)
        r.raise_for_status()
        return r.raw

    def exists(self, key: str) :
        """
        Verifies that a file from managed content (S3) exists.

        :param key: the path of the file to check
        :return: a boolean value (True or False)
        """
        uri = self._make_content_uri(key)
        r = self._serviceconnector.request('HEAD', uri)
        return r.status_code is 200

    ## Private ##

    def _bootstrap(self):
        uri  = self.URIs['connections'] + '/_/bootstrap'
        r = self._serviceconnector.request('GET', uri)
        r.raise_for_status()
        return r.json()

    def _make_content_uri(self, key: str):
        return self.URIs['content'] + '/' + key.lstrip('/')


def build_connectionclient(input_message: InputMessage, version) -> ConnectionClient:
    """
    Builds a ConnectionClient.
    """
    return build_client(ConnectionClient, input_message, version)
