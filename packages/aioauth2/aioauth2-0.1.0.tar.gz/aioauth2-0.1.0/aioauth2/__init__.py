import sys

from aioify import aioify
import oauth2
import poetry_version


__version__ = poetry_version.extract(source_file=__file__)


aioauth2 = aioify(obj=oauth2, name=__name__)

sys.modules[__name__] = aioauth2
from aioauth2 import *
