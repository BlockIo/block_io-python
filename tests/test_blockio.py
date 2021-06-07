from block_io import BlockIo, BlockIoAPIError

import os
import unittest
import time
import json

from struct import pack
from types import *
from binascii import hexlify, unhexlify
from ecdsa import rfc6979, SECP256k1, util
from hashlib import sha256
from decimal import Decimal

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

    def test_pin_derivation_with_salt(self):
        key = BlockIo.Helper.pinToAesKey("deadbeef", "922445847c173e90667a19d90729e1fb", 500000)
        self.assertEqual(key, b'f206403c6bad20e1c8cb1f3318e17cec5b2da0560ed6c7b26826867452534172')
        
    def test_aes256ecb_encryption(self):
        clear = "I\'m a little tea pot short and stout"
        key = BlockIo.Helper.pinToAesKey(self.pin)
        encrypted_data = BlockIo.Helper.encrypt(clear, key)
        self.assertEqual(encrypted_data['aes_cipher_text'], b'7HTfNBYJjq09+vi8hTQhy6lCp3IHv5rztNnKCJ5RB7cSL+NjHrFVv1jl7qkxJsOg')
        cleartext = BlockIo.Helper.decrypt(encrypted_data['aes_cipher_text'], key)
        self.assertEqual(cleartext, clear.encode('utf-8'))

    def test_aes256cbc_encryption(self):
        clear = "beadbeef"
        key = BlockIo.Helper.pinToAesKey("deadbeef", "922445847c173e90667a19d90729e1fb", 500000)
        result = BlockIo.Helper.encrypt(clear, key, "11bc22166c8cf8560e5fa7e5c622bb0f", "AES-256-CBC")
        self.assertEqual(result['aes_cipher_text'], b'LExu1rUAtIBOekslc328Lw==')
        cleartext = BlockIo.Helper.decrypt(result['aes_cipher_text'], key, result['aes_iv'], result['aes_cipher'])
        self.assertEqual(cleartext, clear.encode('utf-8'))

    def test_aes256gcm_encryption(self):
        clear = "beadbeef"
        key = BlockIo.Helper.pinToAesKey("deadbeef", "922445847c173e90667a19d90729e1fb", 500000)
        result = BlockIo.Helper.encrypt(clear, key, "a57414b88b67f977829cbdca", "AES-256-GCM")
        self.assertEqual(result['aes_cipher_text'], b'ELV56Z57KoA=')
        self.assertEqual(result['aes_auth_tag'], b'adeb7dfe53027bdda5824dc524d5e55a')
        cleartext = BlockIo.Helper.decrypt(result['aes_cipher_text'], key, result['aes_iv'], result['aes_cipher'], result['aes_auth_tag'])
        self.assertEqual(cleartext, clear.encode('utf-8'))

    def test_dynamic_extract_key_aes256ecb(self):
        
        user_key = json.loads('{"encrypted_passphrase":"3wIJtPoC8KO6S7x6LtrN0g==","public_key":"02f87f787bffb30396984cb6b3a9d6830f32d5b656b3e39b0abe4f3b3c35d99323","algorithm":{"pbkdf2_salt":"","pbkdf2_iterations":2048,"pbkdf2_hash_function":"SHA256","pbkdf2_phase1_key_length":16,"pbkdf2_phase2_key_length":32,"aes_iv":null,"aes_cipher":"AES-256-ECB","aes_auth_tag":null,"aes_auth_data":null}}')

        key = BlockIo.Helper.dynamicExtractKey(user_key, "deadbeef")
        self.assertEqual(key.pubkey_hex(), BlockIo.Key.from_passphrase(unhexlify("beadbeef")).pubkey_hex())
        
    def test_dynamic_extract_key_aes256cbc(self):

        user_key = json.loads('{"encrypted_passphrase":"LExu1rUAtIBOekslc328Lw==","public_key":"02f87f787bffb30396984cb6b3a9d6830f32d5b656b3e39b0abe4f3b3c35d99323","algorithm":{"pbkdf2_salt":"922445847c173e90667a19d90729e1fb","pbkdf2_iterations":500000,"pbkdf2_hash_function":"SHA256","pbkdf2_phase1_key_length":16,"pbkdf2_phase2_key_length":32,"aes_iv":"11bc22166c8cf8560e5fa7e5c622bb0f","aes_cipher":"AES-256-CBC","aes_auth_tag":null,"aes_auth_data":null}}')

        key = BlockIo.Helper.dynamicExtractKey(user_key, "deadbeef")
        self.assertEqual(key.pubkey_hex(), BlockIo.Key.from_passphrase(unhexlify("beadbeef")).pubkey_hex())
        
    def test_dynamic_extract_key_aes256gcm(self):
        
        user_key = json.loads('{"encrypted_passphrase":"ELV56Z57KoA=","public_key":"02f87f787bffb30396984cb6b3a9d6830f32d5b656b3e39b0abe4f3b3c35d99323","algorithm":{"pbkdf2_salt":"922445847c173e90667a19d90729e1fb","pbkdf2_iterations":500000,"pbkdf2_hash_function":"SHA256","pbkdf2_phase1_key_length":16,"pbkdf2_phase2_key_length":32,"aes_iv":"a57414b88b67f977829cbdca","aes_cipher":"AES-256-GCM","aes_auth_tag":"adeb7dfe53027bdda5824dc524d5e55a","aes_auth_data":""}}')

        key = BlockIo.Helper.dynamicExtractKey(user_key, "deadbeef")
        self.assertEqual(key.pubkey_hex(), BlockIo.Key.from_passphrase(unhexlify("beadbeef")).pubkey_hex())
        
    
class TestKeys(unittest.TestCase):
    def setUp(self):
        self.priv = "6b0e34587dece0ef042c4c7205ce6b3d4a64d0bc484735b9325f7971a0ead963"
        self.passphrase = "deadbeeffeedface";
        self.dtrust_keys = ["b515fd806a662e061b488e78e5d0c2ff46df80083a79818e166300666385c0a2",
                            "1584b821c62ecdc554e185222591720d6fe651ed1b820d83f92cdc45c5e21f",
                            "2f9090b8aa4ddb32c3b0b8371db1b50e19084c720c30db1d6bb9fcd3a0f78e61",
                            "6c1cefdfd9187b36b36c3698c1362642083dcc1941dc76d751481d3aa29ca65"]

        self.dtrust_pubkeys = ["02510e29d51e9a4268e6a5253c1fbd8144857945b82acb0accfc235cc7ca36da11",
                               "0201a819bf549c253c4397bdd1535374de39e9bc278f637afdc27642d52cf79139",
                               "039e3aa9ea182ccdaff2d8d150010b27cc4765c1d55ce674e52631af7376354d62",
                               "03ee980e6334142342fcd9e6facfecfa139981e2276584c91d6a9739d533ac99fc"]
        
    def test_key_init(self):
        key = BlockIo.Key.from_privkey_hex(self.priv)
        self.assertEqual(key.pubkey_hex(), b'029c06f988dc6b44696e002e8abf496a13c73c2f1db3bde2dfb69be129f3711b01')

    def test_from_passphrase(self):
        key = BlockIo.Key.from_passphrase(unhexlify(self.passphrase))
        self.assertEqual(key.pubkey_hex(), b'029023d9738c623cdd7e5fdd0f41666accb82f21df5d27dc5ef07040f7bdc5d9f5')

    def test_dtrust_keys(self):
        for i in range(len(self.dtrust_keys)):
             self.assertEqual(BlockIo.Key.from_privkey_hex(self.dtrust_keys[i]).pubkey_hex().decode("utf-8"), self.dtrust_pubkeys[i])
        
class TestBlockIoAPIError(unittest.TestCase):
    def setUp(self):
        self.blockio = BlockIo("","",2)

    def test_throws_blockio_api_error(self):
        try:
            self.blockio.get_balance()
            self.assertEquals(True,False) # will fail if we get here
        except BlockIoAPIError as e:
            self.assertEqual(e.get_raw_data()['data']['error_message'], "API Key invalid or you have not enabled API access for this machine's IP address(es). Check that your API Keys are correct, and that you have enabled API access for this machine's IP Address(es) on your account's Settings page.")
            
