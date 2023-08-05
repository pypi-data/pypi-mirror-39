#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------
# xako.views
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

from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.response import FileResponse
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from xako.models import Document, Domain, Fragment
from xako.utils.priority import Priority
from xako.utils.settings import get_settings


# Human Interface

@view_config(route_name='index', renderer='xako:templates/index.html')
def index(request):
    return {
        'local_domains': request.registry.settings.get('xako.local_domains'),
    }


@view_config(route_name='domain_human_interface',
             renderer='xako:templates/domain.html')
def domain_human_interface(request):
    domain_name = request.matchdict['domain']
    if domain_name in request.registry.settings.get('xako.local_domains'):
        domain = Domain.get_or_create(name=domain_name)
        recipients = request.registry.settings.get('xako.routes')[domain_name]
        return {
            'domain': domain,
            'size_in_transit': Fragment.size_in_transit,
            'transmission_band': get_settings('transmission_band'),
            'recipients': recipients,
        }
    else:
        return HTTPNotFound()


# REST API

@view_defaults(renderer='json')
class RestApi(object):
    def __init__(self, request):
        self.request = request
        self.matchdict = request.matchdict
        self.form = getattr(self.request, self.request.method, {})

    @view_config(route_name='get_states')
    def get_states(self):
        documents = Document.outgoing(self.request.matchdict['sender'])
        return [d.reception_state for d in documents]

    @view_config(route_name='get_state')
    def get_state(self):
        document = (
            Document.outgoing(self.matchdict['sender']).
            filter(Document.fingerprint == self.matchdict['fingerprint']).
            first()
        )
        return document.reception_state if document else {}

    @view_config(route_name='send', request_method='POST')
    def send(self):
        try:
            sender = self.form['sender']
            recipients = self.form['recipients']
            priority = int(self.form.get('priority', Priority.NORMAL))
            payload = self.form.get('payload')
            metadata = self.form.get('metadata')
        except (KeyError, ValueError) as e:
            raise HTTPBadRequest(explanation='Invalid request data: "%s".' % e)

        document = Document.new(
            sender=sender,
            recipients=recipients,
            payload=payload,
            priority=priority,
            payload_metadata=metadata,
            to_be_send=True,
            built=True,
        )
        if document:
            document.save(flush=True)
            return {'fingerprint': document.fingerprint}
        else:
            msg = 'Invalid message, there is no route for it.'
            raise HTTPBadRequest(explanation=msg)

    @view_config(route_name='inbox')
    def inbox(self):
        documents = Document.incoming(self.matchdict['domain'])
        for document in documents:
            document.deprecate_if_payload_is_empty()
        return [d.inbox_information for d in documents]

    @view_config(route_name='delete')
    def delete(self):
        document = Document.incoming(
            self.matchdict['domain'],
            Document.fingerprint == self.request.matchdict['fingerprint']
        )
        if document:
            document[0].delete()
        else:
            return HTTPNotFound()


@view_config(route_name='download')
def download(request):
    document = Document.incoming(
        request.matchdict['domain'],
        Document.fingerprint == request.matchdict['fingerprint']
    )
    if document:
        document = document[0]
        document.extend_deprecation()
        return HTTPFound(location=document.payload_url)
    else:
        return HTTPNotFound()


def static_files(request):
    path = request.storage.path(request.matchdict['file_name'])
    return FileResponse(path)
