# Cortex ML Models Python Library

The Cortex Python Library provides an SDK to easily integrate and deploy ML algorithms into Cortex. 
Refer to the Cortex documentation for details on how to use the SDK: 

- Developer guide: https://docs.cortex.insights.ai/docs/developer-guide/overview/
- Python SDK references: https://docs.cortex.insights.ai/docs/developer-guide/reference-guides


## Installation
To install the Cortex Client: 
```
  > pip install cortex-client
```

or from source code:
```
  > python setup.py install
```

## Development 

### Setup

Install for development:

`cd` to the root directory of the Python SDK project:
```
  > cd <cortex-python-sdk source dir>
```
Create a virtual environment:
```
  > virtualenv --python=python3 _venv3
  > source _venv3/bin/activate
```
Install Python SDK in editable mode, and all developer dependencies:
```
  > make dev.install
```

There's a convenience `Makefile` that has commands to common tasks, such as build, test, etc. Use it!

### Documentation

The Python client documentation is built with Sphinx. To build the documentation:

`cd` to the root directory of the Python SDK project:
```
  > cd <cortex-python-sdk source dir>
```

Activate your virtual environment:
```
> source _venv3/bin/activate
```

Setup your environment, if you have not done so:
```
> make dev.install 
```

Build the docs:
```
> make docs.build
```

The documentation will be rendered in HTML format under the `docs/_build/html` directory.
