#!/usr/bin/env python

from __future__ import print_function
from __future__ import division

import bchlib
import binascii
from binascii import unhexlify

import os
import random

def bytes5_to_int(bytes):
    a = 0
    a = a + int(bytes[4])
    a = a << 8
    a = a + int(bytes[3])
    a = a << 8
    a = a + int(bytes[2])
    a = a << 8
    a = a + int(bytes[1])
    a = a << 8
    a = a + int(bytes[0])

    return a

def bytes3_to_int(bytes):
    a = 0
    a = a + int(bytes[2])
    a = a << 8
    a = a + int(bytes[1])
    a = a << 8
    a = a + int(bytes[0])

    return a

def long_to_bytes (val, endianness='big'):
    """
    Use :ref:`string formatting` and :func:`~binascii.unhexlify` to
    convert ``val``, a :func:`long`, to a byte :func:`str`.

    :param long val: The value to pack

    :param str endianness: The endianness of the result. ``'big'`` for
      big-endian, ``'little'`` for little-endian.

    If you want byte- and word-ordering to differ, you're on your own.

    Using :ref:`string formatting` lets us use Python's C innards.
    """

    # one (1) hex digit per four (4) bits
    width = val.bit_length()

    # unhexlify wants an even multiple of eight (8) bits, but we don't
    # want more digits than we need (hence the ternary-ish 'or')
    width += 8 - ((width % 8) or 8)

    # format width specifier: four (4) bits per hex digit
    fmt = '%%0%dx' % (width // 4)

    # prepend zero (0) to the width, to zero-pad the output
    s = unhexlify(fmt % val)

    if endianness == 'little':
        # see http://stackoverflow.com/a/931095/309233
        s = s[::-1]

    return s
    

# Initialize the BCH to BCH(63,24,7)
bch = bchlib.BCH(0x43,7)

# A bch table to look up the ecc
bchtable = [0 for _ in range(2**24)]

for i in range(2**24):
    if (i % 1000000)==0:
        print(i)

    byte1 = i & 0xff;
    byte2 = (i >> 8) & 0xff
    byte3 = (i >> 16) & 0xff
    
    bytes = bytearray([byte1, byte2, byte3])
    ecc = bch.encode(bytes)
    ecci = bytes5_to_int(ecc)
    
    bchtable[i] = ecci

# Make some PUFs    
eccis = list()
eccs = list()
for i in range(10):
    puf = random.getrandbits(24)
    byte1 = puf & 0xff;
    byte2 = (puf >> 8) & 0xff
    byte3 = (puf >> 16) & 0xff
    
    pufbytes = bytearray([byte1,byte2,byte3])
    pufi = bytes3_to_int(pufbytes)

    ecc = bch.encode(pufbytes)
    ecci = bytes5_to_int(ecc) 

    eccs.append(ecc)
    eccis.append(ecci)

    print("PUF %06x  ECC %010x" % (pufi,ecci))
     

# Use the ECCs to predict the PUF
for ecc,ecci in zip(eccs,eccis):
    for tablepuf,tableecc in enumerate(bchtable):
        if (tableecc == ecci):
            print(" Found ECC %010x ==> PUF %06x" % (ecci,tablepuf))
    
