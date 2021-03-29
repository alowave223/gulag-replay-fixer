# -*- coding: utf-8 -*-

import struct

__all__ = (
    'write_uleb128',
    'write_string'
)

def write_uleb128(num: int) -> bytearray:
    """ Write `num` into an unsigned LEB128. """
    if num == 0:
        return bytearray(b'\x00')

    ret = bytearray()
    length = 0

    while num > 0:
        ret.append(num & 0b01111111)
        num >>= 7
        if num != 0:
            ret[length] |= 0b10000000
        length += 1

    return ret

def write_string(s: str) -> bytearray:
    """ Write `s` into bytes (ULEB128 & string). """
    if s:
        encoded = s.encode()
        ret = bytearray(b'\x0b')
        ret += write_uleb128(len(encoded))
        ret += encoded
    else:
        ret = bytearray(b'\x00')

    return ret