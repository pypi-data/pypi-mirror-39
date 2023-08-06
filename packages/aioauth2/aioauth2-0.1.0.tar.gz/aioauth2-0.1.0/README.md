# aioauth2 - asynchronous OAuth Python library
[![License](https://img.shields.io/pypi/l/aioauth2.svg)](https://www.apache.org/licenses/LICENSE-2.0)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aioauth2.svg)
[![PyPI](https://img.shields.io/pypi/v/aioauth2.svg)](https://pypi.org/project/aioauth2/)

Asynchronous OAuth Python library - asynchronous wrapper for [oauth2](https://github.com/joestump/python-oauth2)

## Installation
To install from [PyPI](https://pypi.org/project/aioauth2/) run:
```shell
$ pip install https://github.com/yifeikong/aioify/archive/master.zip
$ pip install aioauth2
```

## Usage
For documentation refer to https://github.com/joestump/python-oauth2, because `aioauth2` uses the same API as `oauth2` with 2 exceptions:
1. All functions are converted to coroutines, that means you have to add `await` keyword before all function calls.
2. To asynchronously create classes from `aioauth2` use static method `create`.
