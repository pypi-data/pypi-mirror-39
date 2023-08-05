#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from xio.core.lib.crypto.common import *

assert sha3_keccak_256  # tofix, this line is to prevent uwsgi error on python2.7 (sha3_keccak_256 == None)


try:
    import ethereum
    ETHEREUM_AVAILABLE = True
except Exception as err:
    ETHEREUM_AVAILABLE = False

try:
    import web3
    WEB3_AVAILABLE = True
except Exception as err:
    WEB3_AVAILABLE = False


def account(*args, **kwargs):

    if sys.version_info.major == 2:
        ACCOUNT_HANDLER = EthereumHandler
    else:
        ACCOUNT_HANDLER = Web3Handler

    handler = ACCOUNT_HANDLER
    return handler(*args, **kwargs)

Account = account


class _Account:

    def __init__(self, *args, **kwargs):
        self.ethereum = kwargs.get('ethereum')
        try:
            self.address = to_string(self.address)
            import web3
            self.address = web3.Web3('').toChecksumAddress(self.address)
        except Exception as err:
            print('ETHEREUM ERROR', err)

    def getBalance(self):
        return self.ethereum.getBalance(self.address)

    def send(self, dst, value):
        transaction = {
            'from': self.address,
            'to': dst,
            'value': value,
            'data': ''
        }
        print(transaction)
        transaction = self.ethereum.transaction(transaction)
        transaction.sign(self.private)
        tx = transaction.send()
        print(tx)
        return tx


class Web3Handler(_Account):

    def __init__(self, private=None, seed=None):

        self._web3 = web3.Web3('')

        if private:
            self._account = self._web3.eth.account.privateKeyToAccount(private)
            self.private = private
            self.address = account.address
        elif seed:
            priv = sha3_keccak_256(seed)
            priv = decode_hex(priv)
            self._account = self._web3.eth.account.privateKeyToAccount(priv)
            self.private = self._account.privateKey.hex()[2:]
        else:
            self._account = self._web3.eth.account.create()
            self.private = self._account.privateKey.hex()[2:]

        self.address = self._account.address
        self.address = self._web3.toChecksumAddress(self.address)

    def sign(self, message):
        from eth_account.messages import defunct_hash_message
        message_hash = defunct_hash_message(text=message)
        signed_message = self._web3.eth.account.signHash(message_hash, private_key=self.private)
        return signed_message.signature.hex()

    @staticmethod
    def recover(message, sig):
        from eth_account.messages import defunct_hash_message
        message_hash = defunct_hash_message(text=message)
        address = web3.Web3('').eth.account.recoverHash(message_hash, signature=sig)
        return address


class EthereumHandler(_Account):

    def __init__(self, private=None, seed=None):

        from ethereum.utils import privtoaddr, sha3

        if private:
            self.private = private
            priv = decode_hex(self.private)
        elif seed:
            priv = sha3_keccak_256(seed)
            self.private = priv
        else:
            import os
            from ethereum import utils
            priv = utils.sha3(os.urandom(4096))  # TO fix - not secure -  for test only
            self.private = encode_hex(priv)

        self.address = '0x' + encode_hex(privtoaddr(priv))

    def sign(self, message):
        # https://github.com/ethereum/eth-account/blob/master/eth_account/_utils/signing.py
        from ethereum.utils import sha3, ecsign

        message_hash = sha3(message)
        print(message, message_hash)
        v, r, s = ecsign(message_hash, decode_hex(self.private))
        print(v, r, s)
        sig = '/'.join([str(value) for value in (v, r, s)])
        check = self.recover(message, sig)
        assert check == self.address
        return sig

    @staticmethod
    def recover(message, sig):
        print('recover... from', sig)
        from ethereum.utils import sha3, ecsign
        from ethereum.utils import ecrecover_to_pub
        message_hash = sha3(message)
        (v, r, s) = sig.split('/')
        print(v, r, s)
        pub = ecrecover_to_pub(message_hash, int(v), int(r), int(s))

        assert len(pub) == 64
        address = decode_hex(sha3_keccak_256(pub))[12:]
        address = "0x" + encode_hex(address)
        print('address', address)
        return address
