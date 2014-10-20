from block_io import BlockIo

import os
import unittest
import time

from struct import pack
from types import *
from binascii import hexlify, unhexlify

API_KEY = os.environ.get("BLOCK_IO_API_KEY")
PIN = os.environ.get("BLOCK_IO_PIN")
API_VERSION = os.getenv("BLOCK_IO_VERSION", 2)

# Hardcoded dogetest for now
MIN_BALANCE = 6;
WITHDRAW_AMOUNT = 2;
NETWORK_FEE = 1;

gNewAddressLabel = hexlify(pack('d', int(time.time())))
gWithdrawAddress = ""

if (API_KEY is None) or (PIN is None):
    raise Exception("NEED env: BLOCK_IO_API_KEY && BLOCK_IO_PIN")

block_io = BlockIo(API_KEY, PIN, API_VERSION)

class BlockIoAPITest(unittest.TestCase):
    def setUp(self):
        self.client = block_io

    def result_assertions(self, result):
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result["data"], dict)
        self.assertEqual(result["status"], "success")
        self.assertNotIn("error", result)

class TestBasicInteractions(BlockIoAPITest):

    def test_get_new_address(self):
        result = self.client.get_new_address(label=gNewAddressLabel)
        self.result_assertions(result)

        self.assertEqual(result["data"]["label"], gNewAddressLabel.decode('utf-8'))
        self.assertIsInstance(result["data"]["address"], str);

    def test_get_my_addresses(self):
        global gWithdrawAddress

        result = self.client.get_my_addresses()
        self.result_assertions(result)

        self.assertIsInstance(result["data"]["addresses"], list)
        addresses = result["data"]["addresses"]

        for address in addresses:
            self.assertIsInstance(address, dict)
            self.assertIsInstance(address["address"], str)
            self.assertIsInstance(address["available_balance"], str)
            valueInAddress = int(float(address["available_balance"]))
            if valueInAddress >= MIN_BALANCE:
                gWithdrawAddress = address["address"]

        if gWithdrawAddress == "":
            raise Exception("Not enough balance to continue")

    def result_assertions(self, result):
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result["data"], dict)
        self.assertEqual(result["status"], "success")
        self.assertNotIn("error", result)

class TestWithdrawInteractions(BlockIoAPITest):

    def test_withdraw_from_address(self):
        self.assertNotEqual(gWithdrawAddress, "")
        result = self.client.withdraw_from_address(from_address=gWithdrawAddress, to_label=gNewAddressLabel, amount=WITHDRAW_AMOUNT)
        self.result_assertions(result)

        self.assertEqual(int(float(result["data"]["network_fee"])), NETWORK_FEE)
        self.assertEqual(int(float(result["data"]["blockio_fee"])), 0)
        self.assertEqual(int(float(result["data"]["amount_sent"])), WITHDRAW_AMOUNT)
        self.assertEqual(int(float(result["data"]["amount_withdrawn"])), WITHDRAW_AMOUNT + NETWORK_FEE)

        self.assertIsInstance(result["data"]["txid"], str)


class TestDeterministicSignatures(unittest.TestCase):

    def setUp(self):
        self.key = BlockIo.Key(unhexlify("6b0e34587dece0ef042c4c7205ce6b3d4a64d0bc484735b9325f7971a0ead963"))

    def test_signature(self):
        sig = self.key.sign(unhexlify("feedfacedeadbeeffeedfacedeadbeeffeedfacedeadbeeffeedfacedeadbeef"))
        self.assertEqual(sig, "3045022100b633aaa7cd5b7af455211531f193b61d34d20fe5ea19d23dd40d6074126150530220676617cd427db7d85923ebe4426ccecc47fb5826e3e24b60e62244e2a4811086")

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
    def test_key_init(self):
        key = BlockIo.Key(self.priv)
        self.assertEqual(key.public_key, "029c06f988dc6b44696e002e8abf496a13c73c2f1db3bde2dfb69be129f3711b01")

basicTest = unittest.TestLoader().loadTestsFromTestCase(TestBasicInteractions)
witdrawTest = unittest.TestLoader().loadTestsFromTestCase(TestWithdrawInteractions)
sigTest = unittest.TestLoader().loadTestsFromTestCase(TestDeterministicSignatures)
helperTest = unittest.TestLoader().loadTestsFromTestCase(TestHelpers)
keyTest = unittest.TestLoader().loadTestsFromTestCase(TestKeys)

# run dat shiznit
print("TESTING BLOCK-IO, api: v{av}; client: v{cv}".format(av=block_io.version, cv=block_io.clientVersion))
unittest.TextTestRunner(verbosity=2).run(helperTest)
unittest.TextTestRunner(verbosity=2).run(keyTest)
unittest.TextTestRunner(verbosity=2).run(sigTest)
#unittest.TextTestRunner(verbosity=2).run(basicTest)
#unittest.TextTestRunner().run(witdrawTest)

