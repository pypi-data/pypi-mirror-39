# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['slackperson']
install_requires = \
['attrs>=18.2,<19.0', 'nameparser>=1.0,<2.0']

setup_kwargs = {
    'name': 'slackperson',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Rick Henry',
    'author_email': 'fredericmhenry@gmail.com',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
