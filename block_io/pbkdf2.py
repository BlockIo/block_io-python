
#from Crypto.Protocol.KDF import PBKDF2
#>>> PBKDF2("alpha","",64,1,hmac_sha256) (returns hex)
# hmac_256 pseudo-random function

import base64
import sys
import hmac
import six
from binascii import hexlify, unhexlify
from struct import pack
from hashlib import sha256

def pbkdf2( password, keylen, salt = "", itercount = 1024, hashfn = sha256 ):
    # native pbkdf2, no external libs

    try:
        # depending whether the hashfn is from hashlib or sha/md5
        digest_size = hashfn().digest_size
    except TypeError:
        digest_size = hashfn.digest_size
    # l - number of output blocks to produce
    l = keylen // digest_size
    if keylen % digest_size != 0:
        l += 1

    if type(password) is not bytes:
        password = password.encode('utf-8')
    
    h = hmac.new( password, None, hashfn )

    T = b''
    for i in range(1, l+1):
        T += pbkdf2_F( h, salt.encode('utf-8'), itercount, i )

    return T[0: keylen]

def xorbytes( a, b ):
    if len(a) != len(b):
        raise "xorstr(): lengths differ"

    ret = b''
    for i in range(len(a)):
        ret += bytes([a[i] ^ b[i]])

    return ret

def xorstr( a, b ):
    if len(a) != len(b):
        raise "xorstr(): lengths differ"
    ret = ''
    for i in range(len(a)):
        ret += chr(ord(a[i]) ^ ord(b[i]))
    return ret

def prf( h, data ):
    hm = h.copy()
    hm.update( data )
    return hm.digest()

# Helper as per the spec. h is a hmac which has been created seeded with the
# password, it will be copy()ed and not modified.
def pbkdf2_F( h, salt, itercount, blocknum ):
    U = prf( h, salt + pack('>i',blocknum ) )
    T = U

    xor_func = xorstr if six.PY2 else xorbytes

    for i in range(2, itercount+1):
        U = prf( h, U )
        T = xor_func( T, U )

    return T

