# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['vserialport']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.4,<4.0']

setup_kwargs = {
    'name': 'vserialport',
    'version': '0.1.1',
    'description': 'Uma livraria de controle das portas seriais',
    'long_description': None,
    'author': 'Flavio Vilante',
    'author_email': 'fvilante1@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
