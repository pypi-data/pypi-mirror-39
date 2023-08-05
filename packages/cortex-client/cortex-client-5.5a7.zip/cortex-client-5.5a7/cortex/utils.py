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

import base64
import hashlib
import logging
import json
from pathlib import Path
from collections import namedtuple


def md5sum(file_name, blocksize=65536):
    md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            md5.update(block)
    return md5.hexdigest()


def is_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or console
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False


def log_message(msg: str, log: logging.Logger, level=logging.INFO, *args, **kwargs):
    if is_notebook():
        print(msg)
        log.debug(msg, *args, **kwargs)
    else:
        log.log(level, msg, *args, **kwargs)


def get_cortex_profile(profile_name=None):
    cortex_config_path = Path.home() / '.cortex/config'

    if cortex_config_path.exists():
        with cortex_config_path.open() as f:
            cortex_config = json.load(f)

        if profile_name is None:
            profile_name = cortex_config.get('currentProfile')

        return cortex_config.get('profiles', {}).get(profile_name, {})
    return {}


def b64encode(b: bytes)->str:
    encoded = base64.b64encode(b)
    return encoded.decode('utf-8')


def b64decode(s: str)->bytes:
    return base64.decodebytes(s.encode('utf-8'))


def named_dict(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = named_dict(value)
        return namedtuple('NamedDict', obj.keys())(**obj)
    elif isinstance(obj, list):
        return [named_dict(item) for item in obj]
    else:
        return obj
