# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['tckn']
setup_kwargs = {
    'name': 'tckn',
    'version': '1.0.0',
    'description': 'A library for generating and validating Republic of Turkey identity numbers',
    'long_description': None,
    'author': 'Ekin Dursun',
    'author_email': 'ekindursun@gmail.com',
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
