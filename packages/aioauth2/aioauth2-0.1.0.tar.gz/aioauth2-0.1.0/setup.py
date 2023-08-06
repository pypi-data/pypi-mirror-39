# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aioauth2']

package_data = \
{'': ['*']}

install_requires = \
['aioify', 'oauth2>=1.9,<2.0', 'poetry-version>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'aioauth2',
    'version': '0.1.0',
    'description': 'Asynchronous OAuth Python library',
    'long_description': '# aioauth2 - asynchronous OAuth Python library\n[![License](https://img.shields.io/pypi/l/aioauth2.svg)](https://www.apache.org/licenses/LICENSE-2.0)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aioauth2.svg)\n[![PyPI](https://img.shields.io/pypi/v/aioauth2.svg)](https://pypi.org/project/aioauth2/)\n\nAsynchronous OAuth Python library - asynchronous wrapper for [oauth2](https://github.com/joestump/python-oauth2)\n\n## Installation\nTo install from [PyPI](https://pypi.org/project/aioauth2/) run:\n```shell\n$ pip install https://github.com/yifeikong/aioify/archive/master.zip\n$ pip install aioauth2\n```\n\n## Usage\nFor documentation refer to https://github.com/joestump/python-oauth2, because `aioauth2` uses the same API as `oauth2` with 2 exceptions:\n1. All functions are converted to coroutines, that means you have to add `await` keyword before all function calls.\n2. To asynchronously create classes from `aioauth2` use static method `create`.\n',
    'author': 'Roman Inflianskas',
    'author_email': 'infroma@gmail.com',
    'url': 'https://github.com/rominf/aioauth2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
