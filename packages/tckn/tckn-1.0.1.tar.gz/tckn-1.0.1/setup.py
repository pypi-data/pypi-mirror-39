# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['tckn']
setup_kwargs = {
    'name': 'tckn',
    'version': '1.0.1',
    'description': 'A library for generating and validating Republic of Turkey identity numbers',
    'long_description': "tckn\n====\n\n*tckn* is a library for generating and validating Republic of Turkey identity numbers.\nIt exposes two functions: `generate` and `validate`.\n\nUsage\n-----\n>>> import tckn\n>>> tckn.generate()\n'21862110720'\n>>> tckn.validate('43650391326')\nTrue\n\n",
    'author': 'Ekin Dursun',
    'author_email': 'ekindursun@gmail.com',
    'url': 'https://github.com/sdispater/poetry',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
