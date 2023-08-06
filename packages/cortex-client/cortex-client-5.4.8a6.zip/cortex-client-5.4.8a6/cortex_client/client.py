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
from typing import Dict, TypeVar, Type, Optional
from urllib.parse import urlparse
from pathlib import Path

import requests

from .serviceconnector import ServiceConnector
from .types import InputMessage, JSONType
from .utils import get_logger
from functools import lru_cache

log = get_logger(__name__)


T = TypeVar('T', bound='_Client')


class _Client:

    URIs = {} # type: Dict[str, str]

    def __init__(self, url, version, token):
        self._serviceconnector = ServiceConnector(url, version, token)

    def _post_json(self, uri, obj: JSONType):
        body_s = json.dumps(obj)
        headers = {'Content-Type': 'application/json'}
        r = self._serviceconnector.request('POST', uri, body_s, headers)
        if r.status_code != requests.codes.ok:
            log.info(r.text)
        r.raise_for_status()
        return r.json()

    def _get_json(self, uri):
        r = self._serviceconnector.request('GET', uri)
        r.raise_for_status()
        return r.json()

    def _request_json(self, uri, method='GET'):
        r = self._serviceconnector.request(method, uri)
        r.raise_for_status()
        return r.json()

    @classmethod
    @lru_cache(maxsize=100)
    def from_current_cli_profile(cls: Type[T], version:str="3") -> Optional[T]:
        # TODO Make the path configurable to cortex config
        cortex_config_file = Path("{}/.cortex/config".format(Path.home()))
        if not cortex_config_file.is_file():
            return None
        cortex_config = json.loads(cortex_config_file.read_bytes().decode('utf-8'))
        current_profile = cortex_config["currentProfile"]
        current_profile_config = cortex_config["profiles"][current_profile]
        url, token = current_profile_config["url"], current_profile_config["token"]
        return cls(url, version, token)


def build_client(type, input_message: InputMessage, version):
    return type(input_message.api_endpoint, version, input_message.token)
