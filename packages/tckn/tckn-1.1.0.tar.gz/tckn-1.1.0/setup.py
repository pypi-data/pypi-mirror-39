# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['tckn']
setup_kwargs = {
    'name': 'tckn',
    'version': '1.1.0',
    'description': 'A library for generating and validating Republic of Turkey identity numbers',
    'long_description': "# tckn\n[![PyPI version](https://badge.fury.io/py/tckn.svg)](https://badge.fury.io/py/tckn)\n \n*tckn* is a library for generating and validating Republic of Turkey identity numbers.\nIt exposes two functions: `generate` and `validate`.\n\n## Installation\n```bash \npoetry add tckn\n```\nor\n```bash\npip install tckn\n```\n\n## Usage\n```python3\n>>> import tckn\n>>> tckn.generate()\n'21862110720'\n>>> tckn.validate('43650391326')\nTrue\n```\n",
    'author': 'Ekin Dursun',
    'author_email': 'ekindursun@gmail.com',
    'url': 'https://github.com/sdispater/poetry',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
