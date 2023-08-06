# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['vmongodb']

package_data = \
{'': ['*']}

install_requires = \
['pymongo>=3.7.2,<4.0.0']

setup_kwargs = {
    'name': 'vmongodb',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Flavio',
    'author_email': 'fvilante1@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
