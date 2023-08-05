#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------
# xako.utils.alchemy
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

from xoutil.objects import classproperty


def base_model(DBSession):
    class BaseModel(object):

        @classproperty
        def query(cls):
            return DBSession.query(cls)

        def save(self, flush=False):
            DBSession.add(self)
            if flush:
                DBSession.flush()

        def delete(self):
            DBSession.delete(self)

        def add_to(self, collection_attr, items):
            collection = getattr(self, collection_attr)
            for item in items:
                if item not in collection:
                    collection.append(item)
            return collection

        @classmethod
        def get_or_create(cls, **kwargs):
            domain = cls.query.filter_by(**kwargs).first()
            if domain is None:
                domain = cls(**kwargs)
                domain.save()
            return domain

    return BaseModel
