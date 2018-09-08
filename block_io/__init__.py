from Crypto.Cipher import AES
import base64
import base58
from binascii import hexlify, unhexlify
import json
import requests
import pkg_resources

from ecdsa import SigningKey, SECP256k1, util
from hashlib import sha256
from . import pbkdf2

import six

VERSION=pkg_resources.get_distribution("block-io").version

class BlockIoInvalidResponseError(Exception):
    """Thrown when we receive an unexpected/unparseable response from Block.io"""

class BlockIoUnknownError(Exception):
    """Thrown when response status codes are outside of 200-299, 419-420, 500-599."""

class BlockIoAPIThrottleError(Exception):
    """Thrown when API call gets throttled at Block.io."""

class BlockIoAPIInternalError(Exception):
    """Thrown on 500-599 errors."""

class BlockIoAPIError(Exception):
    """Thrown when block.io API call fails."""


class BlockIo(object):

    class Key:

        def __init__(self, privkey, pubkey = None, compressed = True):
            self.private_key = SigningKey.from_string(privkey, SECP256k1, sha256)

            if (compressed):
                # use the compressed public key
                self.public_key = BlockIo.Helper.compress_pubkey(self.private_key.get_verifying_key().to_string())
            else:
                # use the uncompressed public key
                self.public_key = unhexlify('04' + hexlify(self.private_key.get_verifying_key().to_string()))

        def sign(self, data_to_sign):
            der_sig = self.private_key.sign_digest_deterministic(data_to_sign, sha256, util.sigencode_der_canonize)
            return der_sig

        def sign_hex(self, hex_data):
            return hexlify(self.sign(unhexlify(hex_data)))

        def pubkey_hex(self):
            return hexlify(self.public_key)

        @staticmethod
        def from_passphrase(passphrase):
            # use the sha256 of the given passphrase as the private key
            private_key = sha256(passphrase).digest()
            return BlockIo.Key(private_key)

        @staticmethod
        def from_wif(privkey):
            # extract the secret exponent from the given coin-formatted private key
            private_key = ""

            try:
                extended_key_bytes = base58.b58decode_check(privkey)
            except ValueError as e:
                # Invalid checksum!
                raise Exception("Invalid Private Key provided. Must be in Wallet Import Format.")

            # is this a compressed WIF or not?
            is_compressed = len(hexlify(extended_key_bytes)) == 68 and hexlify(extended_key_bytes)[-2:] == "01"

            # Drop the network bytes
            extended_key_bytes = extended_key_bytes[1:]

            private_key = extended_key_bytes

            if (len(private_key) == 33):
                private_key = extended_key_bytes[:-1]

            return BlockIo.Key(private_key, None, is_compressed)

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
            return BlockIo.Key.from_passphrase(unhexlify(decrypted))

        @staticmethod
        def encrypt(data, key):
            # key in hex, data as string
            # returns ciphertext in base64

            key = unhexlify(key) # get bytes

            BS = 16
            pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
            unpad = lambda s : s[0:-s[-1]]

            obj = AES.new(key, AES.MODE_ECB)
            ciphertext = obj.encrypt(pad(data).encode('latin-1'))

            return base64.b64encode(ciphertext)

        @staticmethod
        def decrypt(b64data, key):
            # key in hex, b64data as base64 string
            # returns utf-8 string

            message = None

            try:
                key = unhexlify(key) # get bytes

                BS = 16
                if (six.PY2):
                    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
                    unpad = lambda s : s[0:-ord(s[-1])]
                else:
                    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
                    unpad = lambda s : s[0:-s[-1]]

                data = base64.b64decode(b64data) # decode from base64
                obj = AES.new(key, AES.MODE_ECB)
                message = unpad(obj.decrypt(data))
            except:
                # error decrypting? must be an invalid secret pin
                raise Exception('Invalid Secret PIN provided.')

            return message

        @staticmethod
        def compress_pubkey(pubkey):
            x = pubkey[:32]
            y = pubkey[33:64]
            y_int = 0;
            for c in six.iterbytes(y):
                y_int = 256 * y_int + c
            return six.int2byte(2+(y_int % 2)) + x

    def __init__(self, api_key, pin, version = 2):
        # initiate the object
        self.api_key = api_key
        self.pin = pin
        self.version = version
        self.clientVersion = VERSION
        self.encryption_key = None
        self.base_url = 'https://block.io/api/v'+str(version)+'/API_CALL/?api_key='+api_key
        self.withdraw_calls = ['withdraw', 'withdraw_from_address', 'withdraw_from_addresses', 'withdraw_from_label', 'withdraw_from_labels', 'withdraw_from_user_id', 'withdraw_from_users']
        self.sweep_calls = ['sweep_from_address']

    def __getattr__(self, attr, *args, **kwargs):

        def hook(*args, **kwargs):
            return self.api_call(attr, **kwargs)

        def withdraw_hook(*args, **kwargs):
            return self.withdraw_meta(attr, **kwargs)

        def sweep_hook(*args, **kwargs):
            return self.sweep_meta(attr, **kwargs)

        if any(attr in s for s in self.withdraw_calls):
            return withdraw_hook
        elif any(attr in s for s in self.sweep_calls):
            return sweep_hook
        else:
            return hook


    def sweep_meta(self, method, **kwargs):
        # sweep call meta

        if (self.version == 1):
            # only available for API v2 users
            raise Exception("Current version (API V1) does not support the Sweep functionality.")

        key = self.Key.from_wif(kwargs['private_key'])

        del kwargs['private_key'] # remove the key, we're not going to pass it on
        kwargs['public_key'] = key.pubkey_hex()

        response = self.api_call(method, **kwargs)

        if 'reference_id' in response['data'].keys():
            # we need to sign some stuff, let's get to it

            # sign all the data we can

            for inputobj in response['data']['inputs']:
                for signer in inputobj['signers']:
                    # we have the required pubkey? sign it!
                    if (signer['signer_public_key'] == key.pubkey_hex().decode('utf-8')):
                        signer['signed_data'] = key.sign_hex(inputobj['data_to_sign']).decode('utf-8')

            args = { 'signature_data': json.dumps(response['data']) }

            response = self.api_call('sign_and_finalize_sweep', **args)

            if ('network_fee' not in response['data'].keys()):
                # we didn't get the transaction ID as proof of sweep, something went wrong
                raise Exception('Sweep failed:', response['data']['error_message'])

            return response
        else:
            # sweep processed
            return response

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
                    if (signer['signer_public_key'] == key.pubkey_hex().decode('utf-8')):
                        signer['signed_data'] = key.sign_hex(inputobj['data_to_sign']).decode('utf-8')

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
        session = requests.session()
        response = session.post(self.base_url.replace('API_CALL',method), data = payload)
        status_code = response.status_code
        
        try:
            response = response.json() # convert response to JSON
        except:
            response = {}

        session.close() # we're done with it, let's close it

        if not ('status' in response.keys()):
            # unexpected response
            raise BlockIoInvalidResponseError("Failed, invalid response received from Block.io, method %s" % method)
        elif ('status' in response.keys()) and (response['status'] == 'fail'):

            if 'data' in response.keys() and 'error_message' in response['data'].keys():
                # call failed, and error_message was provided
                raise BlockIoAPIError('Failed: '+response['data']['error_message'])
            else:
                # call failed, and error_message was NOT provided
                raise BlockIoAPIError("Failed, error_message was not provided, method %s" % method)

        elif 500 <= status_code <= 599:
            # using the status_code since a JSON response was not provided
            raise BlockIoAPIInternalError("API call to Block.io failed externally, method %s" % method)
        elif 419 <= status_code <= 420:
            # using the status_code since a JSON response was not provided
            raise BlockIoAPIThrottleError("API call got throttled by rate limits at Block.io, method %s" % method)
        elif not (200 <= status_code <= 299):
            # using the status_code since a JSON response was not provided
            raise BlockIoUnknownError("Unknown error occurred when querying Block.io, method %s" % method)

        return response
