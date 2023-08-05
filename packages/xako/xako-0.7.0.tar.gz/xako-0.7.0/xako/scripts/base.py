#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------
# xako.scripts.base
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
from functools import wraps

import transaction

from pyramid.paster import bootstrap, setup_logging
from pyramid.scripts.common import parse_vars


def lock(*resources, **options):
    '''Context manager for locking named-resources.

    `resources` are simple case-insentitive names that must contain only
    chars in ``a-z0-9@.-_:/``.

    This lock guarrants that resources are always acquired in the same order
    (to prevent deadlocks: process A needs resources R1, R2 and process B
    needs resources R2, R1; process A takes R1 and process B takes R2, so
    neither can proceed.

    '''
    import sys
    from contextlib import contextmanager

    assert 'linux' in sys.platform, 'Lock with AF_UNIX only works on linux'

    def _find_resources(resources):
        if not resources:
            raise TypeError('At least a resource must be given')
        import re
        validrexp = re.compile(r'^[-a-z0-9@\._/:+]+$')
        result = []
        for res in resources:
            res = res.lower()
            if not validrexp.match(res):
                raise ValueError("Invalid resource name '%s'" % res)
            result.append(res)
        result.sort()  # avoid silly deadlocks
        return result

    def acquire(res):
        import socket
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        try:
            sock.bind('\0'+res)
        except socket.error:
            raise RuntimeError('Cannot acquire resource "%s"' % res)
        else:
            return sock

    def release(takenres):
        takenres.close()

    resources = _find_resources(resources)

    @contextmanager
    def mngr():
        taken = [acquire(resource) for resource in resources]
        try:
            yield
        finally:
            for resource in taken:
                release(resource)

    return mngr()


def command(function):
    """Decorate a function as a command."""
    def infer_argtype(val):
        from xoutil.eight import string_types
        if isinstance(val, bool):
            if val:
                return 'store_false', None
            else:
                return 'store_true', None
        elif isinstance(val, string_types):
            return 'store', str
        elif val is not None:
            return 'store', type(val)  # TODO: generalize numbers
        else:
            return 'store', None
    import argparse
    from xoutil.eight import string_types
    from inspect import signature
    parser = argparse.ArgumentParser()
    parser.add_argument('inifile', help='The configuration file')
    parser.add_argument('options', help='Many a=b for Pyramid', nargs='*')
    argv = ()
    signature = signature(function)
    annotations = getattr(function, '__annotations__', {})
    argv = ((arg, val.default) + infer_argtype(val.default)
            for arg, val in signature.parameters.items())

    for arg, val, action, argtype in argv:
        argspec = dict(dest=arg, default=val, action=action)
        if argtype:
            argspec.update(type=argtype)
        argsp = annotations.get(arg)
        if argsp:
            if isinstance(argsp, dict):
                argspec.update(argsp)
            elif isinstance(argsp, string_types):
                argspec.update(help=argsp)
            else:
                raise TypeError('Invalid argument annotation %r' % argsp)
        parser.add_argument('--%s' % arg, **argspec)

    @wraps(function)
    def wrapper():
        options = parser.parse_args()
        config_uri = options.inifile
        pyramid_options = parse_vars(options.options)
        kwargs = vars(options)
        kwargs.pop('inifile', None)
        kwargs.pop('options', None)
        setup_logging(config_uri)
        env = bootstrap(config_uri, request=None, options=pyramid_options)
        with transaction.manager:
            try:
                function(**kwargs)
            except:
                import sys, logging, traceback
                logger = logging.getLogger(__name__)
                exctype, excval, exctb = sys.exc_info()
                logger.error(traceback.format_exception_only(exctype, excval))
                logger.debug('\n'.join(traceback.format_tb(exctb)))
                raise
            finally:
                env['closer']()
    return wrapper


def synchronized_cmd(function):
    '''Lock resources before executing a command.

    Locked resources are: POP3 and SMTP accounts and the DB connection.

    '''
    from xako.utils.settings import get_settings
    from xoutil.decorator.meta import flat_decorator

    def replacement(fnct, *args, **kwargs):
        pop3_user = get_settings('pop3_user')
        smtp_user = get_settings('smtp_user', pop3_user)
        db = get_settings('url', prefix='sqlalchemy')
        resources = tuple({pop3_user, smtp_user, db})
        with lock(*resources):
            fnct(*args, **kwargs)

    cmd = flat_decorator(replacement, function)
    return command(cmd)
