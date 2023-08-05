#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------
# xako.scripts.send_messages
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

from xoutil.annotate import annotate
from xoutil.bound import timed, accumulated

from xako.models import Document, Fragment
from xako.utils.settings import get_settings

from .base import synchronized_cmd, command

import logging
logger = logging.getLogger(__name__)

@synchronized_cmd
@annotate(force='Forces document sending')
def transmit_documents(force=False):
    from itertools import chain
    transmission_interval = get_settings('transmission_interval')
    transmission_band = get_settings('transmission_band')
    logger.debug('%s - %s', transmission_band, transmission_interval)

    def receiving():
        logger.debug('Receiving')
        try:
            for _ in Document.receive_all():
                yield 0
        except GeneratorExit:
            logger.warn('Interrupted receiving of messages')

    def sending():
        logger.debug('Sending')
        try:
            for fragment in Document.send_all(force=force):
                yield fragment
        except GeneratorExit:
            logger.warn('Interrupted sending of fragments')

    if transmission_band:
        sending = accumulated(
            transmission_band - Fragment.size_in_transit,
            "size"
        )(sending).generate

    list(timed(transmission_interval)(
        _ for _ in chain(receiving(), sending())
    ).generate())


@synchronized_cmd
def transmit_control_messages():
    bound = get_settings('transmission_interval', 60)
    timed(bound)(Document.check_sent)()


@command
@annotate(force='Removes all documents disregarding the deprecation time.')
def remove_old_documents(force=False):
    from .base import lock
    from xako.utils.settings import get_settings
    db = get_settings('url', prefix='sqlalchemy')
    from datetime import datetime, timedelta
    when = None
    if force:
        when = datetime.now() + timedelta(days=365)
    with lock(db):
        Document.delete_deprecated(when=when)
