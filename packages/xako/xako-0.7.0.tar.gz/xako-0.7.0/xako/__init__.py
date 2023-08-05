#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------
# xako
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

from datetime import timedelta


def main(global_config, **settings):
    """Return the Xako WSGI application."""
    from pyramid.settings import asbool
    from pyramid.config import Configurator
    from sqlalchemy import engine_from_config
    from pyramid_jinja2 import renderer_factory

    from xako.utils.settings import aslist, asdict, asdictset
    from .models import DBSession, Base

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    # custom settings
    fragment_size = int(settings.get('xako.fragment_size', 1048576))  # 1Mb
    settings['xako.fragment_size'] = fragment_size

    transmission_band = int(settings.get('xako.transmission_band', 0))
    settings['xako.transmission_band'] = transmission_band

    seconds = int(settings.get('xako.transmission_interval', 60))
    settings['xako.transmission_interval'] = timedelta(seconds=seconds)

    local_domains = aslist(settings.get('xako.local_domains', ''))
    settings['xako.local_domains'] = local_domains

    domain_emails = asdict(settings.get('xako.domain_emails'))
    settings['xako.domain_emails'] = domain_emails

    routes = asdictset(settings.get('xako.routes'), delimiter='->')
    settings['xako.routes'] = routes

    config = Configurator(settings=settings)
    config.include('pyramid_storage')
    config.include('pyramid_jinja2')
    config.include('pyramid_tm')

    # Renderers
    config.add_renderer('.html', renderer_factory)

    # Routes
    #   HTML views
    config.add_route('index', '/')
    config.add_route('domain_human_interface', '/web/{domain}/')

    #   REST API
    config.add_route('get_states', '/state/{sender}/')
    config.add_route('get_state', '/state/{sender}/{fingerprint}/')
    config.add_route('send', '/send/')
    config.add_route('inbox', '/inbox/{domain}/')
    config.add_route('download', '/download/{domain}/{fingerprint}/',
                     request_method='GET')
    config.add_route('delete', '/inbox/{domain}/{fingerprint}/',
                     request_method='DELETE')

    #   Static services
    if asbool(settings.get('pyramid.serve_statics')):
        url = settings.get('storage.base_url') + '{file_name}'
        config.add_route('static_files', url)
        config.add_view('xako.views.static_files', route_name='static_files')
        config.add_static_view('static', 'static', cache_max_age=3600)

    config.scan()
    return config.make_wsgi_app()
