# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aioetherscan', 'aioetherscan.tests']

package_data = \
{'': ['*'], 'aioetherscan': ['modules/*']}

install_requires = \
['aiohttp>=3.4,<4.0', 'asyncio_throttle>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'aioetherscan',
    'version': '0.1.3',
    'description': 'Etherscan API async Python wrapper',
    'long_description': None,
    'author': 'ape364',
    'author_email': 'ape364@gmail.com',
    'url': 'https://github.com/ape364/aioetherscan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
