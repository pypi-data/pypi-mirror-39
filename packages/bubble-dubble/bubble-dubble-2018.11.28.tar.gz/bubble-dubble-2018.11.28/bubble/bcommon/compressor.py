#!/usr/bin/python
# -*- coding: utf-8 -*-

import io
import zlib
import base64
import binascii
import numpy as np


class CompressError(Exception):
    pass


def compress(s, text=True):
    if isinstance(s, str):
        s = s.encode()
    s = zlib.compress(s, 9)
    if text:
        s = base64.b64encode(s).decode()
    return s


def compressFile(f, text=True):
    try:
        return compress(open(f).read(), text)
    except (IOError, UnicodeDecodeError):
        return ''


def decompress(bts, text=True):
    try:
        if text:
            bts = base64.b64decode(bts)
        return zlib.decompress(bts)
    except (binascii.Error, zlib.error):
        raise CompressError('The string does not seem to be compressed')


def compressNumpyArray(array, text=True):
    buf = io.BytesIO()
    # noinspection PyTypeChecker
    np.save(buf, np.ascontiguousarray(array), False)
    return compress(buf.getvalue(), text)


def decompressNumpyArray(array, text=True):
    try:
        decompressed = decompress(array, text)
    except CompressError:
        return None
    buf = io.BytesIO(decompressed)
    try:
        return np.load(buf)
    except (TypeError, OSError):
        return None
