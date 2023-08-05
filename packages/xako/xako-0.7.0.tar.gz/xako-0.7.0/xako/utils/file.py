#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------
# xako.utils.file
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


from __future__ import (
    absolute_import as _py3_abs_imports,
    division as _py3_division,
    print_function as _py3_print,
    unicode_literals as _py3_unicode
)


class File(object):
    def __init__(self, content, file_name=None):
        self._pointer = 0
        self._content = content
        self.name = self.filename = file_name or 'file'

    @property
    def file(self):
        return self

    def seek(self, pointer):
        self._pointer = pointer

    def read(self, chunk_size=None):
        if chunk_size is None:
            return self._content
        else:
            final_pointer = self._pointer + chunk_size
            chunk = self._content[self._pointer:final_pointer]
            self._pointer = final_pointer
            return chunk
