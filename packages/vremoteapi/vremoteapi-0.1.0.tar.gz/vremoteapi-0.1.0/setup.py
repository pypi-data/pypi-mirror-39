# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['vremoteapi', 'vremoteapi.OLD_']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'vremoteapi',
    'version': '0.1.0',
    'description': 'Mecanismo para permitir chamada de funcao do backend remotamente',
    'long_description': None,
    'author': 'Flavio',
    'author_email': 'fvilante1@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
