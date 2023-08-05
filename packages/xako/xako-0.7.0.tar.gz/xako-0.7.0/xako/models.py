#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#

import os
from shutil import move
from tempfile import mkstemp
from os.path import splitext, getsize
from datetime import datetime, timedelta

from typing import Any

from xoutil.fs import concatfiles
from xoutil.objects import classproperty
from xoutil.eight import string_types

from pyramid.threadlocal import get_current_request

from sqlalchemy import (
    Column,
    Integer,
    Text,
    Table,
    ForeignKey,
    String
)
from sqlalchemy import UniqueConstraint, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.orm.query import Query
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property

from zope.sqlalchemy import ZopeTransactionExtension

from xako.utils.fingerprint import get_fingerprint, has_fingerprint
from xako.utils.allofthem import AllOfThem
from xako.utils.file import File
from xako.utils.settings import get_settings, get_routes
from xako.utils.settings import are_routes_valid
from xako.utils.alchemy import base_model
from xako.utils.priority import Priority
from xako.messages import FragmentMessage, FragmentReceivedConfirmation
from xako.messages import FragmentRetransmissionRequest


import logging
logger = logging.getLogger(__name__)


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base: Any = declarative_base(cls=base_model(DBSession))


def _calculate_fingerprint(context):
    payload = context.current_parameters.get('payload')
    if payload:
        payload_path = get_current_request().storage.path(payload)
    else:
        payload_path = None
    metadata = context.current_parameters.get('payload_metadata')
    return get_fingerprint(payload_path, metadata)


document_domain = Table(
    'document_domain',
    Base.metadata,
    Column('document_id', Integer, ForeignKey('document.id')),
    Column('domain_id', Integer, ForeignKey('domain.id')),
    UniqueConstraint('document_id', 'domain_id'),
)


fragment_domain = Table(
    'fragment_domain',
    Base.metadata,
    Column('fragment_id', Integer, ForeignKey('fragment.id')),
    Column('domain_id', Integer, ForeignKey('domain.id')),
    UniqueConstraint('fragment_id', 'domain_id'),
)


class FileModel(Base):
    __abstract__ = True

    payload = Column(Text)
    fingerprint = Column(Text, default=_calculate_fingerprint, index=True)

    @classproperty
    def storage(self):
        return get_current_request().storage

    @property
    def payload_path(self):
        if self.payload:
            return self.storage.path(self.payload)

    @property
    def payload_url(self):
        if self.payload:
            return self.storage.url(self.payload)

    @property
    def payload_file(self):
        if self.payload:
            return open(self.payload_path, 'rb')

    @property
    def size(self):
        if self.payload:
            return getsize(self.payload_path)
        else:
            return 0

    @classmethod
    def new_payload(cls, payload=None, file_name=None):
        if payload is not None:
            if isinstance(payload, bytes) or isinstance(payload, string_types):
                payload = File(payload, file_name=file_name)
            payload = cls.storage.save(
                payload, extensions=AllOfThem(), randomize=True,
            )
        return payload or ''

    def delete_payload(self):
        if self.payload:
            self.storage.delete(self.payload)

    def delete(self, *args, **kwargs):
        self.delete_payload()
        super(FileModel, self).delete(*args, **kwargs)


class Domain(Base):
    __tablename__ = 'domain'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), index=True)

    def __str__(self):
        return self.name

    @property
    def remote_domains(self):
        domain_names = get_routes(self.name)
        return [Domain.get_or_create(name=name) for name in domain_names]


class Document(FileModel):
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True)
    file_name = Column(Text)
    sender_id = Column(Integer, ForeignKey(Domain.id))
    sender = relationship(Domain, backref='documents_sender')
    recipients = relationship(
        Domain,
        secondary=document_domain,
    )
    payload_metadata = Column(Text)
    total_fragments = Column(Integer, default=0)
    deprecation = Column(DateTime, index=True, nullable=True)
    fragments = relationship('Fragment', order_by='Fragment.number')

    def __repr__(self):
        return '<Document from: {sender}/{id}[{frags}]>'.format(
            sender=self.sender,
            id=self.id,
            frags=self.total_fragments,
        )

    @hybrid_method
    def deprecated_after(self, when):
        return self.deprecation and self.deprecation <= when

    @deprecated_after.expression
    def deprecated_after(cls, when):
        return cls.deprecation <= when

    @classmethod
    def delete_deprecated(cls, when=None):
        when = when or datetime.now()
        for document in cls.query.filter(cls.deprecated_after(when)):
            logger.debug("Removing deprecated document. FP: '%s'",
                          document.fingerprint)
            document.delete()

    def delete(self, *args, **kwargs):
        for fragment in self.fragments:
            fragment.delete()
        super(Document, self).delete(*args, **kwargs)

    @classmethod
    def new(cls, sender, recipients, payload=None, file_name=None, **kwargs):
        if isinstance(recipients, string_types):
            recipients = recipients.split(',')

        if are_routes_valid(sender, recipients):
            return cls(
                sender=Domain.get_or_create(name=sender),
                recipients=[Domain.get_or_create(name=r) for r in recipients],
                payload=cls.new_payload(payload=payload, file_name=file_name),
                file_name=file_name or getattr(payload, 'filename', None),
                **kwargs
            )

    @classmethod
    def get_or_create(cls, fingerprint, sender, recipients, **kwargs):
        document = cls.query.filter_by(
            fingerprint=fingerprint,
            sender=Domain.get_or_create(name=sender)
        ).first()
        if document:
            document.add_to(
                'recipients',
                [Domain.get_or_create(name=r) for r in recipients]
            )
            document.save()
        else:
            document = cls.new(
                sender=sender,
                fingerprint=fingerprint,
                recipients=recipients,
                **kwargs
            )
        return document

    # Sender Interface

    priority = Column(Integer, default=Priority.NORMAL, index=True)
    to_be_send = Column(Boolean, index=True, default=False)

    @classmethod
    def send_all(cls, force=False):
        """Send all pending documents to the recipients."""
        if force:
            documents = cls.query
        else:
            documents = cls.query.filter(cls.to_be_send)
        documents = documents.order_by(cls.priority)
        for document in documents:
            fragments = document.send(force=force)
            try:
                for fragment in fragments:
                    yield fragment
            except GeneratorExit:
                fragments.close()
                raise

    @property
    def size_in_transit(self):
        return sum(
            f.size
            for f in self.fragments
            if not f.to_be_send and not f.received
        )

    def send(self, force=False):
        """Send the document to the recipients."""
        if self.to_be_send or force:
            self.split()
            try:
                for frag in self.fragments:
                    if frag.to_be_send or force:
                        frag.send(force=force)
                        yield frag
            except GeneratorExit:
                logger.debug('GeneratorExit exit Document.send')
                pass
            else:
                self.to_be_send = False
            finally:
                self.save()

    @classmethod
    def check_sent(cls):
        frags = Fragment.check_sent()
        try:
            for _ in frags:
                yield
        except GeneratorExit:
            frags.close()
            raise
        for document in cls.query.filter(cls.received):
            if not document.local_recipients:
                document.deprecate()
            yield

    @classmethod
    def outgoing(cls, domain):
        return (
            cls.query.
            join(cls.sender).
            filter(Domain.name == domain)
        )

    @property
    def reception_state(self):
        """"Return the state of the document reception in remote domains."""
        domains = dict.fromkeys([r.name for r in self.recipients], 0)
        for fragment in self.fragments:
            for domain in fragment.received_by:
                domains[domain.name] += 1
        info = {
            'id': self.id,
            'file_name': self.file_name,
            'fingerprint': self.fingerprint,
            'fragments': self.total_fragments,
            'domains': domains,
        }
        if self.received and not self.local_recipients:
            self.deprecate()
        return info

    @hybrid_property
    def received(self):
        """Return True if document recipients confirmed the reception."""
        return bool(self.fragments) and all(f.received for f in self.fragments)

    @received.expression
    def received(cls):
        return cls.id.in_(Query(FullyReceivedDocument.id))

    def split(self):
        """Split the document in fragments."""
        if not self.fragments:
            total_fragments = 0
            if self.payload_path:
                fragment_size = get_settings('fragment_size')
                with open(self.payload_path, 'rb') as payload:
                    fragment_payload = payload.read(fragment_size)
                    while fragment_payload:
                        total_fragments += 1
                        self.fragments.append(Fragment(
                            payload=self.new_payload(
                                payload=fragment_payload,
                                file_name=self.payload
                            ),
                            number=total_fragments,
                            to_be_send=True,
                        ))
                        fragment_payload = payload.read(fragment_size)
            if not total_fragments:
                total_fragments = 1
                if self.payload_path:
                    payload = self.new_payload(
                        payload='',
                        file_name=self.payload
                    )
                else:
                    payload = ''
                self.fragments.append(Fragment(
                    number=total_fragments,
                    to_be_send=True,
                    payload=payload
                ))
            self.total_fragments = total_fragments
            DBSession.flush()

    # Recipient Interafece

    built = Column(Boolean, default=False, index=True)

    @property
    def inbox_information(self):
        return {
            'id': self.id,
            'fingerprint': self.fingerprint,
            'sender': self.sender.name,
            'metadata': self.payload_metadata,
            'file_name': self.file_name,
        }

    @property
    def local_recipients(self):
        """Return the recipients that belongs to local domains."""
        local_recipients = []
        recipients = [r.name for r in self.recipients]
        for local_domain in get_settings('local_domains'):
            if local_domain in recipients:
                local_recipients.append(local_domain)
        return local_recipients

    def build(self):
        """Construct the document payload from its fragments."""
        if not self.built and self.is_complete:
            if all(fragment.payload for fragment in self.fragments):
                self.payload = self.new_payload(
                    payload='',
                    file_name=self.file_name
                )
                name, ext = splitext(self.file_name)
                filedesc, file_path = mkstemp(suffix=ext)
                try:
                    fragment_paths = [
                        f.payload_path for f in self.fragments
                    ]
                    concatfiles(fragment_paths, file_path)
                    move(file_path, self.payload_path)
                finally:
                    os.close(filedesc)
            self.built = True
            logger.debug('Built document "%s"', self.fingerprint)
            self.save()

    @property
    def is_complete(self):
        return self.total_fragments == len(self.fragments)

    def extend_deprecation(self, delta=None):
        if delta is None:
            delta = timedelta(minutes=60)
        self.deprecation = datetime.now() + delta
        self.save()

    def deprecate(self):
        self.extend_deprecation(timedelta(seconds=0))

    def deprecate_if_payload_is_empty(self):
        if not self.payload and not self.deprecation:
            self.extend_deprecation()

    @classmethod
    def receive_all(cls):
        fragments = FragmentMessage.receive()
        try:
            for message in fragments:
                document = cls.get_or_create(**message.data.document)
                fragment = Fragment.get_or_create(
                    document=document,
                    number=message.data.fragment['number'],
                    payload=message.payload,
                    file_name=document.file_name,
                )
                fragment.validate(message.data.fragment['fingerprint'])
                yield
        finally:
            fragments.close()
        for document in cls.query.filter_by(built=False):
            try:
                document.build()
                yield
            except Exception:
                import traceback
                import json
                metadata = json.loads(document.payload_metadata)
                print('%r' % metadata)
                traceback.print_exc()

    @classmethod
    def incoming(cls, domain, *args):
        return cls.query \
            .join(cls.recipients) \
            .filter(cls.built, Domain.name == domain) \
            .filter(*args)


class Fragment(FileModel):
    __tablename__ = 'fragment'

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    document_id = Column(Integer, ForeignKey(Document.id), nullable=False)
    document = relationship(
        Document,
    )

    def __repr__(self):
        return '<Frag: {n}/{tot}: {payload}>'.format(
            n=self.number,
            tot=self.document.total_fragments,
            payload=self.payload,
        )

    @classmethod
    def get_or_create(cls, document, number, payload, file_name=None):
        fragment = cls.query.filter_by(
            document=document,
            number=number,
        ).first()
        if not fragment:
            fragment = cls(
                document=document,
                number=number,
                payload=cls.new_payload(payload=payload, file_name=file_name),
            )
            logger.debug("Created new fragment %d for document '%s'",
                          number, document.fingerprint)
        else:
            logger.debug("Fragment %d/'%s' already here",
                          number, document.fingerprint)
        return fragment

    # Sender Interface

    to_be_send = Column(Boolean, index=True, default=False)
    received_by = relationship(
        Domain,
        secondary=fragment_domain,
    )
    received = Column(Boolean, default=False, index=True)

    @classproperty
    def size_in_transit(cls):
        return sum(fragment.size for fragment in cls.in_transit)

    @classproperty
    def in_transit(cls):
        return cls.query.filter_by(received=False, to_be_send=False)

    @classproperty
    def received_fragments(cls):
        return ReceivedFragment.query

    @classmethod
    def check_sent(cls):
        messages = FragmentReceivedConfirmation.receive()
        try:
            for message in messages:
                for fragment in cls.get_from_control_message(message):
                    recipients = [
                        Domain.get_or_create(name=name)
                        for name in message.local_recipients
                    ]
                    fragment.add_to('received_by', recipients)
                    fragment.save()
                    yield
        except GeneratorExit:
            messages.close()
            raise
        messages = FragmentRetransmissionRequest.receive()
        try:
            for message in messages:
                for fragment in cls.get_from_control_message(message):
                    msg = 'Request retransmission for fragment: %r'
                    logger.debug(msg % fragment)
                    fragment.send(recipients=message.local_recipients)
                    yield
        except GeneratorExit:
            messages.close()

    @classmethod
    def get_from_control_message(cls, message):
        return (
            cls.query.
            join(cls.document).
            join(Document.sender).
            filter(Document.fingerprint == message.document_fingerprint).
            filter(Domain.name == message.recipient).
            filter(cls.number == message.fragment_number)
        )

    def send(self, recipients=None, force=False):
        """Return True if the fragment was sent successfully."""
        if self.to_be_send or recipients or force:
            logger.debug('Sending %r', self)
            recipients = recipients or self.document.recipients
            recipient_names = [recipient.name for recipient in recipients]
            FragmentMessage(
                sender=self.document.sender.name,
                recipients=recipient_names,
                priority=self.document.priority,
                payload=self.payload_file,
                **{
                    'fragment': {
                        'number': self.number,
                        'fingerprint': self.fingerprint,
                    },
                    'document': {
                        'file_name': self.document.file_name,
                        'sender': self.document.sender.name,
                        'recipients': recipient_names,
                        'priority': self.document.priority,
                        'fingerprint': self.document.fingerprint,
                        'total_fragments': self.document.total_fragments,
                        'payload_metadata': self.document.payload_metadata,
                   },
                }
            ).send()
            self.to_be_send = False
            self.save()
        return self

    # Recipient Interface

    def validate(self, fingerprint):
        is_valid = (
            self.fingerprint == fingerprint or
            has_fingerprint(self.payload_path, fingerprint)
        )
        if is_valid:
            self.fingerprint = fingerprint
            self.confirm_reception()
            self.save()
        elif self.is_corrupt:
            self.request_retransmission()
            self.delete()

    @property
    def is_corrupt(self):
        """Return True if the payload really has the fingerprint."""
        return not has_fingerprint(self.payload_path, self.fingerprint)

    def confirm_reception(self):
        self._send_control_message(FragmentReceivedConfirmation)

    def request_retransmission(self):
        self._send_control_message(FragmentRetransmissionRequest)

    def _send_control_message(self, klass):
        klass(
            sender=self.document.local_recipients[0],
            recipients=[self.document.sender.name],
            recipient=self.document.sender.name,
            local_recipients=self.document.local_recipients,
            document_fingerprint=self.document.fingerprint,
            fragment_number=self.number,
        ).send()

    def save(self, *args, **kwargs):
        self.received = len(self.document.recipients) == len(self.received_by)
        return super(Fragment, self).save(*args, **kwargs)


class ReceivedFragment(Base):
    '''Basically a view-like of Fragments that are received.'''
    def get_table():
        from sqlalchemy import select
        # XXX: Don't use the Fragment.query, to avoid sessions to be created
        where = Fragment.received == True
        return select([Fragment], whereclause=where).alias()

    __table__ = get_table()
    del get_table


class FullyReceivedDocument(Base):
    '''A view for received documents'''

    def received_document_table():
        # TODO: Understand!
        from sqlalchemy import join, select
        count = func.count
        docid = Document.id.label('docid')
        received = select([count(ReceivedFragment.id).label('amount'),
                           docid],
                          from_obj=join(Document,
                                        ReceivedFragment)).\
            group_by(docid).alias('r')
        frags = select([count(Fragment.id).label('amount'),
                        Document.id.label('docid')],
                       from_obj=join(Document, Fragment)).\
            group_by(docid).alias('f')
        fullyreceived = (received.c.amount == frags.c.amount).label('rec')
        full = select([received.c.docid.label('docid')],
                      whereclause=fullyreceived,
                      from_obj=join(received, frags,
                                    received.c.docid == frags.c.docid))
        return select([Document],
                      whereclause=Document.id.in_(full)).alias()

    __table__ = received_document_table()
    del received_document_table
