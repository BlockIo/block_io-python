
from Crypto.Cipher import AES
import base64
import sys
import hmac
import vbuterin
import pbkdf2
from binascii import hexlify, unhexlify
from struct import pack
from hashlib import sha256
import json
import requests

VERSION="1.0.6"

class BlockIo(object):

    class Key:

        def __init__(self, privkey, pubkey = None):
            self.private_key = privkey
            self.public_key = vbuterin.compress(vbuterin.privkey_to_pubkey(privkey))

        def sign(self, data_to_sign):
            # returns the signed data using secp256k1
            raw_sig = vbuterin.ecdsa_raw_sign(data_to_sign,self.private_key)
            return vbuterin.der_encode_sig(*raw_sig)

        @staticmethod
        def from_passphrase(passphrase):
            # use the sha256 of the given passphrase as the private key
            
            private_key = vbuterin.sha256(unhexlify(passphrase))
            
            return BlockIo.Key(private_key)

    class Helper:

        @staticmethod
        def pinToAesKey(pin):
            # use pbkdf2 magic
            ret = pbkdf2.pbkdf2(pin, 16)
            ret = pbkdf2.pbkdf2(hexlify(ret), 32)
            
            return hexlify(ret) # the encryption key

        @staticmethod
        def extractKey(encrypted_data, enc_key_hex):
            # encryption key is in hex
            
            decrypted = BlockIo.Helper.decrypt(encrypted_data, enc_key_hex)
            
            return BlockIo.Key.from_passphrase(decrypted)

        @staticmethod
        def encrypt(data, key):
            # key in hex, data as string
            # returns ciphertext in base64
            
            key = unhexlify(key) # get bytes
            
            BS = 16
            pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
            unpad = lambda s : s[0:-ord(s[-1])]
            
            obj = AES.new(key, AES.MODE_ECB, "")
            ciphertext = obj.encrypt(pad(message))
            
            return base64.b64encode(ciphertext)
            
        @staticmethod
        def decrypt(b64data, key):
            # key in hex, b64data as base64 string
            # returns utf8 string

            message = None

            try:
                key = unhexlify(key) # get bytes
                
                BS = 16
                pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
                unpad = lambda s : s[0:-ord(s[-1])]
                
                data = base64.b64decode(b64data) # decode from base64
                obj = AES.new(key, AES.MODE_ECB, "")
                message = unpad(obj.decrypt(data))
            except:
                # error decrypting? must be an invalid secret pin
                raise Exception('Invalid Secret PIN provided.')

            return message

    def __init__(self, api_key, pin, version = 2):
        # initiate the object
        self.api_key = api_key
        self.pin = pin
        self.version = version
        self.clientVersion = VERSION
        self.encryption_key = None
        self.base_url = 'https://block.io/api/v'+str(version)+'/API_CALL/?api_key='+api_key
        self.withdraw_calls = ['withdraw', 'withdraw_from_address', 'withdraw_from_addresses', 'withdraw_from_label', 'withdraw_from_labels', 'withdraw_from_user_id', 'withdraw_from_users']

    def __getattr__(self, attr, *args, **kwargs):
        
        def hook(*args, **kwargs):
            return self.api_call(attr, **kwargs)

        def withdraw_hook(*args, **kwargs):
            return self.withdraw_meta(attr, **kwargs)

        if any(attr in s for s in self.withdraw_calls):
            return withdraw_hook
        else:
            return hook

    def withdraw_meta(self, method, **kwargs):
        # withdraw call meta

        if (self.version == 1):
            # we'll use the pin if we're using version 1
            kwargs['pin'] = self.pin

        response = self.api_call(method, **kwargs)

        if 'reference_id' in response['data'].keys():
            # we need to sign some stuff, let's get to it

            if self.encryption_key is None:
                self.encryption_key = self.Helper.pinToAesKey(self.pin)

            key = self.Helper.extractKey(response['data']['encrypted_passphrase']['passphrase'], self.encryption_key)

            # sign all the data we can

            for inputobj in response['data']['inputs']:
                for signer in inputobj['signers']:
                    # we have the required pubkey? sign it!
                    if (signer['signer_public_key'] == key.public_key):
                        signer['signed_data'] = key.sign(inputobj['data_to_sign'])
            
            args = { 'signature_data': json.dumps(response['data']) }

            response = self.api_call('sign_and_finalize_withdrawal', **args)

            if ('reference_id' in response['data'].keys()):
                # this is a 2 of 2 address, it should've accepted our signature
                raise Exception('Invalid Secret PIN or insufficient signatures for withdrawal.')

            return response
        else:
            # withdrawal processed
            return response

    def api_call(self, method, **kwargs):
        # the actual API call
        
        # http parameters
        payload = {}

        if self.api_key is not None:
            payload["api_key"] = self.api_key
            
        payload.update(kwargs)

        # update the parameters with the API key
        response = requests.post(self.base_url.replace('API_CALL',method), params = payload)

        response = response.json()

        if ('error_message' in response['data'].keys()):
            raise Exception('Failed: '+response['data']['error_message'])

        return response

