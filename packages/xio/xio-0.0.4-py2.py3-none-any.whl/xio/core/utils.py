#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .lib.utils import *
import os


def about(src):
    from xio.core.resource import extractAbout
    return extractAbout(src)
