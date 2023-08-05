=========================================
 Xako - Document sharing transport layer
=========================================

Overview
========

Xako is document sharing transport layer system with a simple REST API.  It
allows application to send files to other peers.  Xako handles the job of
communicating with the peers and make the dispatch.

Xako ensures data integrity at delivery/arrival of documents.

See the documentation for more information.

Backends
========

Xako uses backends to send the documents fragments.  At this moment xako only
has a single backend: email.  This means you must provide each xako domain a
POP/SMTP pair to send and receive documents.

See the email backend documentation.
