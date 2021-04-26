from block_io import BlockIo

import os
import unittest
import time

from struct import pack
from types import *
from binascii import hexlify, unhexlify
from ecdsa import rfc6979, SECP256k1, util
from hashlib import sha256
from decimal import Decimal, getcontext

getcontext().prec = 8

class TestDeterministicSignatures(unittest.TestCase):

    def setUp(self):
        self.key = BlockIo.Key(unhexlify("6b0e34587dece0ef042c4c7205ce6b3d4a64d0bc484735b9325f7971a0ead963"))
        self.hex_data = "feedfacedeadbeeffeedfacedeadbeeffeedfacedeadbeeffeedfacedeadbeef"

    def test_deterministic_k_no_extra_entropy(self):
        k = rfc6979.generate_k(SECP256k1.generator.order(), self.key.private_key.key.privkey.secret_multiplier, sha256, unhexlify(self.hex_data))
        self.assertEqual(hexlify(util.number_to_string(k, self.key.private_key.key.privkey.order)), b'ab56733dc6b9cf8fbecd9af7ba64ee5b658b8a1def2f4c4c510a2996d2761d6f')

    def test_deterministic_k_extra_entropy_1(self):
        extra_entropy = (1).to_bytes(32, byteorder="little")
        k = rfc6979.generate_k(SECP256k1.generator.order(), self.key.private_key.key.privkey.secret_multiplier, sha256, unhexlify(self.hex_data), 0, extra_entropy)
        self.assertEqual(hexlify(util.number_to_string(k, self.key.private_key.key.privkey.order)), b'f24f24e2e6510071c86da612ef04ccc21664a3801e0e06a227023b9c513a8290')

    def test_deterministic_k_extra_entropy_16(self):
        extra_entropy = (16).to_bytes(32, byteorder="little")
        k = rfc6979.generate_k(SECP256k1.generator.order(), self.key.private_key.key.privkey.secret_multiplier, sha256, unhexlify(self.hex_data), 0, extra_entropy)
        self.assertEqual(hexlify(util.number_to_string(k, self.key.private_key.key.privkey.order)), b'f42eeee9d30ec008d58ce23b2ff08fac85127e87390bccccbecc68a537da3d47')

    def test_deterministic_k_extra_entropy_255(self):
        extra_entropy = (255).to_bytes(32, byteorder="little")
        k = rfc6979.generate_k(SECP256k1.generator.order(), self.key.private_key.key.privkey.secret_multiplier, sha256, unhexlify(self.hex_data), 0, extra_entropy)
        self.assertEqual(hexlify(util.number_to_string(k, self.key.private_key.key.privkey.order)), b'a2c913d48ca5d18c62126a90059a552f4cafeab85b55e9acdc6848473910f150')

    def test_deterministic_k_extra_entropy_256(self):
        extra_entropy = (256).to_bytes(32, byteorder="little")
        k = rfc6979.generate_k(SECP256k1.generator.order(), self.key.private_key.key.privkey.secret_multiplier, sha256, unhexlify(self.hex_data), 0, extra_entropy)
        self.assertEqual(hexlify(util.number_to_string(k, self.key.private_key.key.privkey.order)), b'39c9dc355f042b24fe44184119c31b62ff9d8a3d0c5a26bada674d9595e6988d')

    def test_signature_with_low_r(self):
        sig = self.key.sign_hex(self.hex_data)
        self.assertEqual(sig, b'3044022042b9b4d673c85798f226c85f55ea6e114a0805bd5a0efba35f14c05235bb67b2022016333edae230c0ab607e948b48ceaefb5cab07300fb869d9da0a1b0f6bb53f65')

class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.pin = "123456";

    def test_pin_derivation(self):
        key = BlockIo.Helper.pinToAesKey(self.pin)
        self.assertEqual(key, b'd0478c395b66e588a1518cdd08d8257aa2145a4c20bcd05c466afb334b7d18e7')

    def test_aes_encryption(self):
        clear = "I\'m a little tea pot short and stout"
        key = BlockIo.Helper.pinToAesKey(self.pin)
        ciphertext = BlockIo.Helper.encrypt(clear, key)
        self.assertEqual(ciphertext, b'7HTfNBYJjq09+vi8hTQhy6lCp3IHv5rztNnKCJ5RB7cSL+NjHrFVv1jl7qkxJsOg')
        cleartext = BlockIo.Helper.decrypt(ciphertext, key)
        self.assertEqual(cleartext, clear.encode('utf-8'))

class TestKeys(unittest.TestCase):
    def setUp(self):
        self.priv = "6b0e34587dece0ef042c4c7205ce6b3d4a64d0bc484735b9325f7971a0ead963"
        self.passphrase = "deadbeeffeedface";

    def test_key_init(self):
        key = BlockIo.Key(unhexlify(self.priv))
        self.assertEqual(key.pubkey_hex(), b'029c06f988dc6b44696e002e8abf496a13c73c2f1db3bde2dfb69be129f3711b01')

    def test_from_passphrase(self):
        key = BlockIo.Key.from_passphrase(unhexlify(self.passphrase))
        self.assertEqual(key.pubkey_hex(), b'029023d9738c623cdd7e5fdd0f41666accb82f21df5d27dc5ef07040f7bdc5d9f5')

