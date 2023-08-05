#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------
# xako.client
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

import json

from xoutil.objects import memoized_property

import requests

from xako.utils.priority import Priority
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class Client(object):
    def __init__(self, domain, url):
        self._domain = domain
        self._url = url

    def _get_url(self, path):
        return urljoin(self._url, path)

    def _make_request(self, path, method='get', data=None, files=None,
                      stream=False):
        url = self._get_url(path)
        method = getattr(requests, method)
        # This raises IOError subclasses if xako is down.
        response = method(url, data=data, files=files, stream=stream)
        if stream:
            return response.raw
        else:
            try:
                return json.loads(response.text)
            except ValueError:
                raise ValueError("Can't decode response: " + response.text)


class Sender(Client):
    def get_state(self, fingerprint=None):
        """Return the state of the documents with fingerprints."""
        path = '/state/{sender}/'.format(sender=self._domain)
        if fingerprint:
            path += fingerprint + '/'
        return self._make_request(path)

    def send(self, recipients, file_path=None, priority=Priority.NORMAL,
             metadata=None):
        """Send a file with `file_path` to `recipients`.

        :return: {'fingerprint': '<document fingerprint>'}

        """
        return self._make_request(
            '/send/',
            method='post',
            files={'payload': open(file_path, 'rb')} if file_path else {},
            data={
                'sender': self._domain,
                'recipients': ','.join(recipients),
                'priority': str(priority),
                'metadata': json.dumps(metadata),
            }
        )


class Receiver(Client):
    @property
    def inbox(self):
        """Return the received documents metadata and information."""
        path = '/inbox/{domain}/'.format(domain=self._domain)
        messages = self._make_request(path)
        return [
            Document(self._get_document_payload, self._delete, **m)
            for m in messages
        ]

    def _get_document_payload(self, fingerprint):
        """Return the document payload given a `fingerprint`.

        :rtype: `Document`:obj:
        """
        path = '/download/{domain}/{fingerprint}/'.format(
            domain=self._domain,
            fingerprint=fingerprint
        )
        return FileWrapper(self._make_request(path, stream=True))

    def _delete(self, fingerprint):
        path = '/inbox/{domain}/{fingerprint}/'.format(
            domain=self._domain,
            fingerprint=fingerprint
        )
        return self._make_request(path, method='delete')


class FileWrapper(object):
    def __init__(self, file_response):
        self._response = file_response

    def chunks(self, chunk_size=1024 * 4):
        eof = False
        while not eof:
            chunk = self._response.read(chunk_size)
            if chunk:
                yield chunk
            eof = not chunk

    def __getattr__(self, name):
        return getattr(self._response, name)


class Xako(Sender, Receiver):
    pass


class Document(object):
    def __init__(self, get_peyload_function, delete_function, **kwargs):
        self._delete = delete_function
        self._get_payload = get_peyload_function
        self.__dict__.update(kwargs)
        try:
            metadata = json.loads(kwargs.get('metadata'))
        except ValueError:
            metadata = {}
        self.metadata = metadata

    @memoized_property
    def file(self):
        return self._get_payload(self.fingerprint)

    def delete(self):
        return self._delete(self.fingerprint)
