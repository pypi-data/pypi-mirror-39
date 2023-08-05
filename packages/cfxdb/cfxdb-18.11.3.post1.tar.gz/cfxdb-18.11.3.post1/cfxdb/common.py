##############################################################################
#
#                        Crossbar.io Fabric
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

import struct


def unpack_uint256(data):
    w3, w2, w1, w0 = struct.unpack('>QQQQ', data)
    return w3 << 24 + w2 << 16 + w1 << 8 + w0


def pack_uint256(value):
    assert(type(value) == int and value >= 0 and value < 2**256)
    w0 = value % 2**64
    value = value >> 8
    w1 = value % 2**64
    value = value >> 8
    w2 = value % 2**64
    value = value >> 8
    w3 = value % 2**64
    return struct.pack('>QQQQ', w3, w2, w1, w0)


class uint256(object):
    def __init__(self, data=None):
        self._data = data or b'\x00' * 32

    @property
    def value(self):
        w3, w2, w1, w0 = struct.unpack('>QQQQ', self._data)
        # return w3 << 24 + w2 << 16 + w1 << 8 + w0
        return w3, w2, w1, w0

    @value.setter
    def value(self, value):
        assert(type(value) == int and value >= 0 and value < 2**256)
        w0 = value % 2**64
        value = value >> 8
        w1 = value % 2**64
        value = value >> 8
        w2 = value % 2**64
        value = value >> 8
        w3 = value % 2**64
        self._data = struct.pack('>QQQQ', w3, w2, w1, w0)
        return w3, w2, w1, w0

    def serialize(self):
        return self._data


class address(object):
    def __init__(self, data=None):
        self._data = data or b'\x00' * 20

    @property
    def value(self):
        w2, w1, w0 = struct.unpack('>LQQ', self._data)
        return w2 << 16 + w1 << 8 + w0

    @value.setter
    def value(self, value):
        assert(type(value) == int and value >= 0 and value < 2**160)
        w0 = value % 2**64
        value = value >> 8
        w1 = value % 2**64
        value = value >> 8
        w2 = value % 2**32
        self._data = struct.pack('>LQQ', w2, w1, w0)

    def serialize(self):
        return self._data
