import sys
import struct

# path = '/home/framgia/Downloads/sec-exercises-master/0x06/encrypt/'
path = '/home/lkintheend/Desktop/CyberSercurity/encrypt/'
enc_bytes = bytearray(open(path + "encrypt.enc", "rb").read())
cipher_bytes = bytearray(open(path + "encrypt.cpp", "rb").read())
size = 2600
xord_byte_array = bytearray(size)
for i in range(size):
    xord_byte_array[i] = enc_bytes[i + 4] ^ cipher_bytes[i]
open(path + "test.key", 'wb').write(xord_byte_array)
enc_bytes = bytearray(open(path + "encrypt.enc", "rb").read())
cipher_bytes = bytearray(open(path + "encrypt.cpp", "rb").read())
size = 2600
xord_byte_array = bytearray(size)
for i in range(size):
    xord_byte_array[i] = enc_bytes[i + 4] ^ cipher_bytes[i]

open(path + "encypt.key", 'wb').write(xord_byte_array)

N = 624
M = 397
MATRIX_A = 0x9908b0df
UPPER_MASK = 0x80000000
LOWER_MASK = 0x7fffffff

mt = [0 for i in xrange(624)]
mti = N + 1


def init_genrand(s):
    global mti
    global mt
    mt[0] = s & 0xffffffff
    for mti in range(1, N, 1):
        mt[mti] = 1812433253 * (mt[mti - 1] ^ (mt[mti - 1] >> 30)) + mti
        mt[mti] &= 0xffffffff


def init_by_array(init_key, key_length):
    init_genrand(19650218)
    i = 1
    j = 0
    k = N if N > key_length else key_length
    for k in range(k, 0, -1):
        mt[i] = (mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1664525)) + init_key[j] + j
        mt[i] &= 0xffffffff
        i += 1
        j += 1
        if i >= N:
            mt[0] = mt[N - 1]
            i = 1
        if j >= key_length:
            j = 0

    for k in range(N - 1, 0, -1):
        mt[i] = (mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1566083941)) - i
        mt[i] &= 0xffffffff
        i += 1
        if i >= N:
            mt[0] = mt[N - 1]
            i = 1

    mt[0] = 0x80000000


def genrand_int32():
    global mti
    y = 0
    mag01 = [0x0, 0x9908b0df]

    if mti >= N:
        kk = 0

        if mti == N + 1:
            init_genrand(5489)

        for kk in range(kk, N - M):
            y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK)
            mt[kk] = mt[kk + M] ^ (y >> 1) ^ mag01[y & 0x1]
        kk += 1

        for kk in range(kk, N - 1, 1):
            y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK)
            mt[kk] = mt[kk + (M - N)] ^ (y >> 1) ^ mag01[y & 0x1]
        y = (mt[N - 1] & UPPER_MASK) | (mt[0] & LOWER_MASK)
        mt[N - 1] = mt[M - 1] ^ (y >> 1) ^ mag01[y & 0x1]
        mti = 0
    y = mt[mti]
    mti += 1
    y ^= (y >> 11)
    y ^= (y << 7) & 0x9d2c5680
    y ^= (y << 15) & 0xefc60000
    y ^= (y >> 18)

    return y


def unshiftRight(x, shift):
    res = x
    for i in range(32):
        res = x ^ res >> shift
    return res


def unshiftLeft(x, shift, mask):
    res = x
    for i in range(32):
        res = x ^ (res << shift & mask)
    return res


def untemper(v):
    v = unshiftRight(v, 18)
    v = unshiftLeft(v, 15, 0xefc60000)
    v = unshiftLeft(v, 7, 0x9d2c5680)
    v = unshiftRight(v, 11)
    return v


def genrand_int32_fake(mt_fake):
    y = mt_fake
    y ^= (y >> 11)
    y ^= (y << 7) & 0x9d2c5680
    y ^= (y << 15) & 0xefc60000
    y ^= (y >> 18)
    return y


encypt_key = open(path + "encypt.key", 'rb').read()
temp = []

for x in range(0, len(encypt_key), 4):
    number = struct.unpack("<I", bytearray(encypt_key[x:x + 4]))[0]
    if x / 4 < 624:
        mt[x / 4] = untemper(number)
    temp.append(number)

mti = 0
print temp

test = []
for x in range(0, len(temp)):
    test.append(genrand_int32())

print test
key_data = bytearray(78560 - 4)

with open(path + "flag.key", 'wb') as flag_key:
    for x in range(0, 78560 - 4, 4):
        flag_key.write(struct.pack("<I", genrand_int32()))

enc_bytes = bytearray(open(path + "flag.enc", "rb").read())
cipher_bytes = bytearray(open(path + "flag.key", "rb").read())
size = 78560 - 4
print len(enc_bytes)
print len(cipher_bytes)
xord_byte_array = bytearray(size)
for i in range(size):
    xord_byte_array[i] = enc_bytes[i + 4] ^ cipher_bytes[i]

# Write the XORd bytes to the output file
open(path + "test.key", 'wb').write(xord_byte_array)

path = '/home/lkintheend/Desktop/CyberSercurity/encrypt/'

enc_bytes = bytearray(open(path + "flag.enc", "rb").read())
cipher_bytes = bytearray(open(path + "flag.key", "rb").read())
size = 78560 - 4
xord_byte_array = bytearray(size)
for i in range(size):
    xord_byte_array[i] = enc_bytes[i + 4] ^ cipher_bytes[i]

open(path + "flag.jpg", 'wb').write(xord_byte_array)
