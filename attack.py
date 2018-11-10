#!/usr/bin/env python

from __future__ import print_function
from __future__ import division

import bchlib
import binascii
from binascii import unhexlify

import os
import random

def bytes_to_int(bytes):
    a = 0
    for x in bytes[::-1]:
        a = a << 8
        a = a+int(x)
    return a

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
    ecci = bytes_to_int(ecc)
    
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
    pufi = bytes_to_int(pufbytes)

    ecc = bch.encode(pufbytes)
    ecci = bytes_to_int(ecc) 

    eccs.append(ecc)
    eccis.append(ecci)

    print("PUF %06x  ECC %010x" % (pufi,ecci))
     

# Use the ECCs to predict the PUF
for ecc,ecci in zip(eccs,eccis):
    for tablepuf,tableecc in enumerate(bchtable):
        if (tableecc == ecci):
            print(" Found ECC %010x ==> PUF %06x" % (ecci,tablepuf))
    
