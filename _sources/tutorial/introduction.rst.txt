Introduction
============

This guide will cover some common PyCC functions their basic use cases.

The biggest structural difference between older versions of PyCC and v4.0.0 and
later is that the client is divided into sub-clients which each handle a specific
set of functionality. Specifically, an instance of ``CitrinationClient`` will
have as members ``data``, ``data_views``, ``models``, and ``search``, which
each expose subsets of the functionality.
