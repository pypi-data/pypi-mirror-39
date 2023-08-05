#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from .connector import Connector as Ipfs

class TestCases(unittest.TestCase):

    def test_base(self):
        ipfs = Ipfs()
        hash = ipfs.add('somedata')
        #tofix : warning return str in python2, bytes in python2
        assert bytes( ipfs.cat(hash)  )== b'somedata'

    """
    def test_account(self):
        ipfs = Ipfs()
        account = ipfs.account(private_key='somekey')
        assert account.address
    """


if __name__ == '__main__':

    unittest.main()












  





