#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------
# xako.backends.email
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

import smtplib
import json

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders
from email import message_from_string

from poplib import POP3, POP3_SSL

from xoutil.objects import smart_copy
from xoutil.future.collections import opendict
from xoutil.future.codecs import safe_decode

from xako.utils.settings import get_peer_emails, get_peer_email
from xako.utils.priority import Priority

import logging
logger = logging.getLogger(__name__)

Required = KeyError

_BACKEND_DEFAULTS = dict(
    smtp_host=Required,
    smtp_port=25,
    smtp_user=None,
    smtp_password=None,
    starttls=False,
    pop3_host=Required,
    pop3_port=110,
    pop3_user=None,
    pop3_password=None,
    pop3_ssl=False,
    smtp_debug=False,
    pop3_debuglevel=0,
)


class Email(object):
    MESSAGE_NAME = 'MESSAGE'

    def __init__(self,  **options):
        smart_copy(options, self, defaults=_BACKEND_DEFAULTS)
        if bool(self.smtp_user) != bool(self.smtp_password):
            raise TypeError('Provide both SMTP user and password or none')
        if bool(self.pop3_user) != bool(self.pop3_password):
            raise TypeError('Provide both POP3 user and password or none')

    def send(self, sender, recipients, subject='', priority=1, data=None,
             files=()):
        msg = MIMEMultipart()
        sender_email = get_peer_email(sender)
        recipient_emails = get_peer_emails(recipients)
        msg['From'] = sender_email
        msg['To'] = COMMASPACE.join(recipient_emails)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg['Auto-Submitted'] = 'auto-generated'
        priority = Priority.email.get(priority)
        if priority:
            msg['X-Priority'] = priority

        encoded_data = MIMEBase('application', 'json')
        encoded_data.set_payload(json.dumps(data))
        encoders.encode_base64(encoded_data)
        encoded_data.add_header(
            'Content-Disposition',
            'attachment; filename="%s"' % self.MESSAGE_NAME
        )
        msg.attach(encoded_data)

        for f in files:
            part = MIMEBase('application', 'octet-stream')
            f.seek(0)
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition', 'attachment; filename="%s"' % f.name
            )
            msg.attach(part)

        smtp = smtplib.SMTP(host=self.smtp_host, port=self.smtp_port)
        smtp.set_debuglevel(self.smtp_debug)
        try:
            smtp.ehlo_or_helo_if_needed()
            if self.starttls:
                smtp.starttls()
                # After STARTTLS you must issue another HELO/EHLO command.
                smtp.ehlo_or_helo_if_needed()
            if self.smtp_user:
                smtp.login(self.smtp_user, self.smtp_password)
            smtp.sendmail(sender_email, recipient_emails, msg.as_string())
        finally:
            smtp.close()

    def receive(self, subject):
        if self.pop3_ssl:
            server = POP3_SSL(self.pop3_host, port=self.pop3_port)
        else:
            server = POP3(self.pop3_host, port=self.pop3_port)
        server.set_debuglevel(self.pop3_debuglevel)
        try:
            server.user(self.pop3_user)
            server.pass_(self.pop3_password)
            _response, messages, _ = server.list()
            for raw_message in messages:
                # TODO:  Be safer! i.e: If the message is does not comply with
                # specs, ignored it and raise a log.
                i, _size = raw_message.split()
                _, lines, _ = server.retr(int(i))
                msg = message_from_string('\n'.join(
                                              [safe_decode(l) for l in lines]
                                          ))
                if msg['Subject'] == subject:    # TODO: Better use a regexp.
                    message = opendict(
                        # TODO: email.utils.getaddresses
                        sender=msg['From'],
                        recipients=msg['To'].split(COMMASPACE),
                        data=None,
                        file=None,
                    )
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == 'application/json':
                            payload = part.get_payload(decode=True)
                            try:
                                message['data'] = opendict(
                                    json.loads(safe_decode(payload))
                                )
                            except ValueError as error:
                                logger.error(error.message)
                                logger.debug('Payload %r', payload)
                                raise
                        if content_type == 'application/octet-stream':
                            message['file'] = part.get_payload(decode=True)
                    try:
                        yield message
                    except GeneratorExit:
                        logger.warn('Interrupted at message %r', i)
                        logger.debug('Deleting message %r', i)
                        server.dele(int(i))
                        raise
                    else:
                        # Only remove the message when no error or
                        # GeneratorExit.
                        logger.debug('Deleting message %r', i)
                        server.dele(int(i))
        finally:
            logger.debug('Closing the connection to the POP3 server')
            server.quit()

    def delete_incoming_messages(self):
        server = POP3(self.pop3_host, port=self.pop3_port)
        try:
            server.user(self.pop3_user)
            server.pass_(self.pop3_password)
            _response, messages, _ = server.list()
            for raw_message in messages:
                # TODO:  Be safer! i.e: If the message is does not comply with
                # specs, ignored it and raise a log.
                i, _size = raw_message.split()
                logger.debug('Deleting message %r', i)
        finally:
            logger.debug('[delete] Closing the connection to the POP3 server')
            server.quit()
