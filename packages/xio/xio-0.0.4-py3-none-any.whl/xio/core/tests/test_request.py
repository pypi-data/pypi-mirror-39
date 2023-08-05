#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import xio
import sys
from pprint import pprint


class TestCases(unittest.TestCase):

    def test_base(self):
        req = xio.request('POST', '/')
        assert req.POST
        assert not req.GET
        assert req.data == {}

if __name__ == '__main__':

    unittest.main()
