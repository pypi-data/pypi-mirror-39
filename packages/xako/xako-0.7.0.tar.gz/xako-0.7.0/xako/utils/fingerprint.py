#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------
# xako.utils
# ----------------------------------------------------------------------
# Copyright (c) 2014 Merchise Autrement and Contributors
# All rights reserved.
#
# Author: Eddy Ernesto del Valle Pino <eddy@merchise.org>
# Contributors: see CONTRIBUTORS and HISTORY file
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the LICENCE attached (see LICENCE file) in the distribution
# package.


from __future__ import (absolute_import as _py3_abs_imports,
                        division as _py3_division,
                        print_function as _py3_print,
                        unicode_literals as _py3_unicode)

from os.path import getsize
from hashlib import md5
from binascii import hexlify, crc32
from xoutil.future.codecs import safe_encode


BLOCK_SIZE = 1024 * 4
CHUNK_SIZE = 4
NULL_FINGERPRINT = '0' * 16


def get_fingerprint(file_path, metadata=None):
    """Return the file fingerprint, string representation of a tuple with...

    - The size of the file.

    - An integer that represent the first 32 bits of the file.

    - An integer that represent the first 32 bits in the file page 1.

    - And integer that represents the last 32 bits of the file.

    - The Cyclic Redundancy Check (CRC) of the file.

    """
    size, start, mid, end, crc = [0] * 5
    if file_path:
        size = getsize(file_path)
        if size:
            with open(file_path, 'rb') as f:
                # sampling
                start = bytes_to_int(f.read(CHUNK_SIZE))
                f.seek(BLOCK_SIZE)
                mid = bytes_to_int(f.read(CHUNK_SIZE))
                f.seek(size - CHUNK_SIZE)
                end = bytes_to_int(f.read())
        crc = get_crc32(file_path)
    meta = md5(safe_encode(metadata) or b'').hexdigest()
    fingerprint = (size, start, mid, end, crc)
    fingerprint = '-'.join([str(i) for i in fingerprint])
    fingerprint += ':' + meta
    return fingerprint


def get_crc32(file_path):
    with open(file_path, 'rb') as f:
        crc = crc32(b'')
        while True:
            page = f.read(BLOCK_SIZE)
            if page:
                crc = crc32(page, crc) & 0xffffffff
            else:
                break
    return crc


def has_fingerprint(file_path, fingerprint, metadata=None):
    """Verify the file fingerprint progressively."""
    try:
        fingerprint, f_meta = fingerprint.split(':')
        f_size, f_start, f_mid, f_end, f_crc = [
            int(i) for i in fingerprint.split('-')
        ]
    except (TypeError, ValueError):
        return False
    if md5(safe_encode(metadata) or b'').hexdigest() != f_meta:
        return False
    if file_path:
        size = getsize(file_path)
        if size != f_size:
            return False
        with open(file_path, 'rb') as f:
            start = bytes_to_int(f.read(CHUNK_SIZE))
            if start != f_start:
                return False
            f.seek(BLOCK_SIZE)
            mid = bytes_to_int(f.read(CHUNK_SIZE))
            if mid != f_mid:
                return False
            f.seek(size - CHUNK_SIZE)
            end = bytes_to_int(f.read())
            if end != f_end:
                return False
        return get_crc32(file_path) == f_crc
    else:
        return f_size == f_start == f_mid == f_end == f_crc == 0


def bytes_to_int(string):
    """Return the integer representation of the `string`.

    Examples::

      >>> bytes_to_int(b'ab')
      24930

      >>> bytes_to_int(b'ac')
      24931

      >>> bytes_to_int(b'bc')
      25187

      >>> bytes_to_int(b'')
      0

    """
    return int(hexlify(string), 16) if string else 0
