# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------
# xako.scripts.utils
# ----------------------------------------------------------------------
# Copyright (c) 2014 Merchise Autrement and Contributors
# All rights reserved.
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the LICENCE attached (see LICENCE file) in the distribution
# package.
#
# Created on 2014-07-18

'''doc

'''

from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        unicode_literals as _py3_unicode,
                        absolute_import as _py3_abs_import)


def print_fingerprint():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('filename', type=str, action='store')
    options = p.parse_args()
    from xako.utils.fingerprint import get_fingerprint
    print(get_fingerprint(options.filename))
