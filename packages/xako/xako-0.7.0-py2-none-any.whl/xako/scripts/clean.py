#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------
# xako.scripts.clean
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

from itertools import chain
from xoutil.annotate import annotate

from xako.models import Document, Domain
from xako.utils.settings import get_transport_backend
from .base import synchronized_cmd


# TODO: Arguments are not used! Improve and adapt help.
@synchronized_cmd
@annotate(
    domains=dict(
        nargs='*',
        help='The domains to deal clean. You may provide many. If none are '
             'provided all domains are cleaned.'),
    all='Indicate that all incoming messages are to be cleaned no matter what.'
)
def clean(domains=None, all=False):
    get_transport_backend().delete_incoming_messages()
    for item in chain(Document.query.all(), Domain.query.all()):
        item.delete()
