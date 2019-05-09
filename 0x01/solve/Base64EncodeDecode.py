import string
import base64

STANDARD_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
CUSTOM_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789=~.'
ENCODE_TRANS = string.maketrans(STANDARD_ALPHABET, CUSTOM_ALPHABET)
DECODE_TRANS = string.maketrans(CUSTOM_ALPHABET, STANDARD_ALPHABET)


def encode(input):
    return base64.b64encode(input).translate(ENCODE_TRANS)


def decode(input):
    return base64.b64decode(input.translate(DECODE_TRANS))


print encode('flag')
print decode(encode('flag'))

