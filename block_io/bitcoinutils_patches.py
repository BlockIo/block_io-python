from decimal import Decimal
from binascii import hexlify, unhexlify
import hashlib
import ecdsa
import struct
import bitcoinutils.constants
import bitcoinutils.bech32
import base58check

bitcoinutils.constants.NETWORK_WIF_PREFIXES = { 'BTC': b'\x80',
                                                'LTC': b'\xb0',
                                                'DOGE': b'\x9e',
                                                'BTCTEST': b'\xef',
                                                'DOGETEST': b'\xf1',
                                                'LTCTEST': b'\xef'
                                               }

bitcoinutils.constants.NETWORK_P2PKH_PREFIXES = { 'BTC': b'\x00',
                                                  'BTCTEST': b'\x6f',
                                                  'LTC': b'\x30',
                                                  'DOGE': b'\x1e',
                                                  'LTCTEST': b'\x6f',
                                                  'DOGETEST': b'\x71'
                                                 }

bitcoinutils.constants.NETWORK_P2SH_PREFIXES = { 'BTC': b'\x05',
                                                 'BTCTEST': b'\xc4',
                                                 'LTC': b'\x32',
                                                 'DOGE': b'\x16',
                                                 'LTCTEST': b'\x3a',
                                                 'DOGETEST': b'\xc4'
                                                }

bitcoinutils.constants.NETWORK_SEGWIT_PREFIXES = { 'BTC': 'bc',
                                                   'BTCTEST': 'tb',
                                                   'LTC': 'ltc',
                                                   'LTCTEST': 'tltc',
                                                   'DOGE': 'doge',
                                                   'DOGETEST': 'tdge'
                                                  }

bitcoinutils.constants.DEFAULT_TX_VERSION =  b'\x01\x00\x00\x00' # little-ended version 1

from bitcoinutils.setup import setup as bitcoinutils_setup
from bitcoinutils.setup import get_network as bitcoinutils_get_network
from bitcoinutils.keys import P2pkhAddress, PrivateKey, PublicKey, P2shAddress, P2wshAddress, Address
from bitcoinutils.script import Script
from bitcoinutils.transactions import Transaction, TxInput, TxOutput

# override the method in bitcoinutils so it doesn't use floats anymore
def fixed_to_satoshis(num):
    
    if (isinstance(num, str) == False):
        raise Exception("Must specify a string for to_satoshis")

    return int(Decimal(num) * Decimal("100000000"))

bitcoinutils.utils.to_satoshis = fixed_to_satoshis
####

# add p2sh_address.to_script_pub_key()
def added_p2sh_to_script_pub_key(self):
    return Script(['OP_HASH160', self.to_hash160(), 'OP_EQUAL'])

bitcoinutils.keys.P2shAddress.to_script_pub_key = added_p2sh_to_script_pub_key
####

# override to use low R signatures
def low_r_sign_input(self, tx_digest, sighash=bitcoinutils.constants.SIGHASH_ALL):
    # unlike the overriden method, this does not append SIGHASH_ALL,
    # so we'll do it ourselves if we add signatures to serialize the transaction
    counter = 0
    der_sig = None
    
    while True:
        extra_entropy = b""
        if (counter > 0):
            extra_entropy = bytearray.fromhex(hex(counter).split("x")[1].rjust(64,"0"))[::-1]
        der_sig = hexlify(self.key.sign_digest_deterministic(tx_digest, hashlib.sha256, ecdsa.util.sigencode_der_canonize, extra_entropy))
        if (int(der_sig[6:8],16) == 32 and int(der_sig[8:10],16) < 128):
            break
        counter = counter + 1
            
    return der_sig
        
bitcoinutils.keys.PrivateKey._sign_input = low_r_sign_input
####

# return output script given address
def get_output_script(address):

    # try to see if this a valid bech32 address
    decoded_bech32 = bitcoinutils.bech32.decode(bitcoinutils.constants.NETWORK_SEGWIT_PREFIXES[bitcoinutils_get_network()], address)
    output_script = None
    
    if (decoded_bech32[0] is None or decoded_bech32[1] is None):
        # failed to decode information for bech32 address, so let's try decoding it as legacy addresses
        addr_encoded = address.encode('ascii')
        decoded_hex = hexlify(base58check.b58decode( addr_encoded ))
        network_prefix = decoded_hex[:2]
        address_hash160 = decoded_hex[2:len(decoded_hex)-8]
        decoded_checksum = decoded_hex[-8:]
        network_prefix_and_hash160 = decoded_hex[:len(decoded_hex)-8]
        correct_checksum = hexlify(hashlib.sha256(hashlib.sha256(unhexlify(network_prefix_and_hash160)).digest()).digest())

        if (correct_checksum[:8] != decoded_checksum):
            raise Exception("Invalid P2SH/P2PKH address checksum")

        # the address is fine, let's figure out if it's P2SH or P2PKH format
        if (bitcoinutils.constants.NETWORK_P2SH_PREFIXES[bitcoinutils_get_network()] == unhexlify(network_prefix)):
#            print("P2SH=",address)
            output_script = Script(['OP_HASH160', address_hash160, 'OP_EQUAL'])
        elif (bitcoinutils.constants.NETWORK_P2PKH_PREFIXES[bitcoinutils_get_network()] == unhexlify(network_prefix)):
#            print("P2PKH=",address)
            output_script = Script(['OP_DUP', 'OP_HASH160', address_hash160, 'OP_EQUALVERIFY', 'OP_CHECKSIG'])
        else:
            raise Exception("Invalid address provided")
        #checksum = data_checksum[-4:]
#        return hexlify(data).decode('utf-8') 
    elif decoded_bech32[0] == 0:
        # only support witness v0 addresses for now
        # it's a bech32 address
#        print(decoded_bech32)
#        print(hexlify(bytearray(decoded_bech32[1])))
#        print("bech32 address:", address)
        output_script = Script(["OP_" + str(decoded_bech32[0]), hexlify(bytearray(decoded_bech32[1]))])
#        print(output_script.to_hex())
    else:
        raise Exception("Unsupported address provided")

    return output_script

####

# returns signature with sighash
def signature_with_sighash(signature, sighash = bitcoinutils.constants.SIGHASH_ALL):
    # takes signature as a hex
    return hexlify(unhexlify(signature) + struct.pack('B', sighash))
####

def debug_txin_stream(self):
    """Converts to bytes"""
    
    # Internally Bitcoin uses little-endian byte order as it improves
    # speed. Hashes are defined and implemented as big-endian thus
    # those are transmitted in big-endian order. However, when hashes are
    # displayed Bitcoin uses little-endian order because it is sometimes
    # convenient to consider hashes as little-endian integers (and not
    # strings)
    # - note that we reverse the byte order for the tx hash since the string
    #   was displayed in little-endian!
    # - note that python's struct uses little-endian by default
    txid_bytes = unhexlify(self.txid)[::-1]
    txout_bytes = struct.pack('<L', self.txout_index)
    script_sig_bytes = self.script_sig.to_bytes()
#        struct.pack('B', len(script_sig_bytes)) + \
    data = txid_bytes + txout_bytes + self.encode_var_int(len(script_sig_bytes)) + script_sig_bytes + self.sequence # modified to use varints
    return data

bitcoinutils.transactions.TxInput.stream = debug_txin_stream

from bitcoinutils.utils import prepend_compact_size
from bitcoinutils.script import OP_CODES

def debug_to_bytes(self, segwit = False):
    #Converts the script to bytes
    #    If an OP code the appropriate byte is included according to:
    #    https://en.bitcoin.it/wiki/Script
    #    If not consider it data (signature, public key, public key hash, etc.) and
    #    and include with appropriate OP_PUSHDATA OP code plus length
    #    """
    script_bytes = b''
    for token in self.script:
        # add op codes directly
        if token in OP_CODES:
            script_bytes += OP_CODES[token]
            # if integer between 0 and 16 add the appropriate op code
        elif type(token) is int and token >= 0 and token <= 16:
            script_bytes += OP_CODES['OP_' + str(token)]
            # it is data, so add accordingly
        else:
            if type(token) is int:
                script_bytes += self._push_integer(token)
            else:
                if segwit:
                    # probably add TxInputWitness which will know how to serialize
                    script_bytes += self._segwit_op_push_data(token)
                else:
                    script_bytes += self._op_push_data(token)
                    
    return script_bytes

bitcoinutils.script.Script.to_bytes = debug_to_bytes

def debug_op_push_data(self, data):

    data_bytes = unhexlify(data)

    if len(data_bytes) < 0x4c:
        print("<0x4c")
        return struct.pack('B', len(data_bytes)) + data_bytes # modified
#        return chr(len(data_bytes)).encode() + data_bytes
    elif len(data_bytes) < 0xff:
        print("<0xff")
        print("chr(len(data_bytes))=",chr(len(data_bytes)))
        print("chr(len(data_bytes)).encode()=",hexlify(chr(len(data_bytes)).encode()))
        return b'\x4c' + struct.pack('B', len(data_bytes)) + data_bytes # modified
#        return b'\x4c' + chr(len(data_bytes)).encode() + data_bytes
    elif len(data_bytes) < 0xffff:
        print("<0xffff")
        return b'\x4d' + struct.pack('<H', len(data_bytes)) + data_bytes
    elif len(data_bytes) < 0xffffffff:
        print("<0xffffffff")
        return b'\x4e' + struct.pack('<I', len(data_bytes)) + data_bytes
    else:
        raise ValueError("Data too large. Cannot push into script")

bitcoinutils.script.Script._op_push_data = debug_op_push_data

def encode_var_int(self,i):
    """ Encodes integers into variable length integers, which are used in
        Bitcoin in order to save space.
    """
    if not isinstance(i, int) and not isinstance(i, long):
        raise Exception('i must be an integer')

    if i <= 0xfc:
        return (i).to_bytes(1, byteorder="little")
    elif i <= 0xffff:
        return b'\xfd' + (i).to_bytes(2, byteorder="little")
    elif i <= 0xffffffff:
        return b'\xfe' + (i).to_bytes(4, byteorder="little")
    elif i <= 0xffffffffffffffff:
        return b'\xff' + (i).to_bytes(8, byteorder="little")
    else:
        raise Exception('Integer cannot exceed 8 bytes in length.')

bitcoinutils.transactions.TxInput.encode_var_int = encode_var_int
