#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
python2.7
 pip install bitcoin cffi

"""
try:
    from gevent import monkey
    monkey.patch_all()  # @ TO FIX ! pb segmentationfault
except:
    # gevent only required for server use@
    pass

__version__ = "0.0.4"

from .core.env import env, context, __PATH__ as path, register

from .core.lib.crypto.crypto import key
from .core.lib.logs import log
from .core.lib.data.data import data
from .core.lib.db.db import db

from .core.request import request
from .core.resource import resource, client, bind
from .core.user import user
from .core.app.app import app
from .core.network.network import network
from .core.node.node import node
from .core import handlers

context.init()
