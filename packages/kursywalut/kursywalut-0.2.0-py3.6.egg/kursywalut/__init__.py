# -*- coding: utf-8 -*-
"""Top-level package for KursyWalut."""

import logging

from .version import __version__
from . import funcs, handlers, parsers, interface


__author__ = 'Bart Grzybicki'
__email__ = 'bgrzybicki@gmail.com'

__all__ = ('__version__')


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# # create console handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('kursywalut.log')
handler.setLevel(logging.WARN)

# set logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console.setFormatter(formatter)

# add the handler to the logger
logger.addHandler(handler)
logger.addHandler(console)
