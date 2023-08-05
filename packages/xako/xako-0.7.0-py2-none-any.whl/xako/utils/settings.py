#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ---------------------------------------------------------------------
# xako.utils.settings
# ---------------------------------------------------------------------
# Copyright (c) 2014-2016 Merchise Autrement and Contributors
#
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

from collections import defaultdict

from pyramid.settings import aslist, asbool
from pyramid.threadlocal import get_current_registry


def ident(f):
    return f


def get_settings(key, default=None, prefix='xako', type=ident):
    key = '%s.%s' % (prefix, key)
    return type(get_current_registry().settings.get(key, default))


def get_routes(sender):
    return get_settings('routes').get(sender, [])


def are_routes_valid(sender, recipients):
    posible_recipients = get_routes(sender)
    return (
        posible_recipients and
        all(r in posible_recipients for r in recipients)
    )


def get_peer_email(domain):
    return get_settings('domain_emails')[domain]


def get_peer_emails(domains):
    emails = get_settings('domain_emails')
    return [emails[domain] for domain in domains]


def resolve_python_object(path):
    from pyramid.path import DottedNameResolver
    resolver = DottedNameResolver(None)
    return resolver.resolve(path)


def get_transport_backend():
    Backend = resolve_python_object(get_settings('transport_backend'))
    return Backend(
        smtp_host=get_settings('smtp_host', 'localhost'),
        smtp_port=int(get_settings('smtp_port', 25, type=int)),
        smtp_user=get_settings('smtp_user'),
        smtp_password=get_settings('smtp_pass'),
        pop3_host=get_settings('pop3_host', 'localhost'),
        pop3_port=int(get_settings('pop3_port', 110, type=int)),
        pop3_user=get_settings('pop3_user'),
        pop3_password=get_settings('pop3_pass'),
        starttls=get_settings('smtp_starttls', 'false', type=asbool),
        pop3_ssl=get_settings('pop3_ssl', 'false', type=asbool),
        smtp_debug=get_settings('smtp_debug', 'false', type=asbool),
        pop3_debuglevel=get_settings('pop3_debuglevel', '0', type=int),
    )


def asdict(value, delimiter=':'):
    r"""
    Convert a list settings to a dictionary.

    >>> asdict('settings:value\nother:value')
    {u'other': u'value', u'settings': u'value'}

    """
    result = {}
    for item in aslist(value or ''):
        key, v = item.split(delimiter)
        result[key] = v
    return result


def asdictset(value, delimiter=':'):
    r"""
    Convert a list settings to a dictionary with sets as values.

    >>> asdictset('settings:value\nsettings:another\nother:value')
    {u'other': set([u'value']), u'settings': set([u'another', u'value'])}

    """
    result = defaultdict(set)
    for item in aslist(value or ''):
        key, v = item.split(delimiter)
        result[key].add(v)
    return dict(result)
