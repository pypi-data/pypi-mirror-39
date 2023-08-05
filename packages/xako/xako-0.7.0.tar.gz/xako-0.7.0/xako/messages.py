#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------
# xako.messages
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

from xoutil.future.collections import opendict
from xako.utils.settings import get_transport_backend


class Message(object):
    DEFAULT_SUBJECT = None

    def __init__(self, sender, recipients, priority=1, payload=None, **kwargs):
        self.sender = sender
        self.recipients = recipients
        self.priority = priority
        self.payload = payload
        self.data = opendict(kwargs)

    def send(self):
        get_transport_backend().send(
            sender=self.sender,
            recipients=self.recipients,
            subject=self.DEFAULT_SUBJECT,
            priority=self.priority,
            data=self.data,
            files=[self.payload] if self.payload else [],
        )

    @classmethod
    def receive(cls):
        messages = get_transport_backend().receive(cls.DEFAULT_SUBJECT)
        try:
            for message in messages:
                yield cls(
                    sender=message.sender,
                    recipients=message.recipients,
                    payload=message.file,
                    **message.data
                )
        except GeneratorExit:
            pass
        finally:
            messages.close()

    def __getattr__(self, name):
        return getattr(self.data, name)


class FragmentReceivedConfirmation(Message):
    DEFAULT_SUBJECT = 'fragment-received'


class FragmentRetransmissionRequest(Message):
    DEFAULT_SUBJECT = 'fragment-retransmission-request'


class FragmentMessage(Message):
    DEFAULT_SUBJECT = 'fragment'
