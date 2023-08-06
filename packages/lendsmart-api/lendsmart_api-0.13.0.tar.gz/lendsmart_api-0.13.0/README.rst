lendsmart_api
===========

.. highlight:: python

The official python library for the `Lendsmart API v1`_ in python.

**This library is currently in beta.**


.. image:: https://travis-ci.org/linode/lendsmart_api-python.svg?branch=master
    :target: https://travis-ci.org/linode/lendsmart_api-python

.. image:: https://badge.fury.io/py/lendsmart-api.svg
   :target: https://badge.fury.io/py/lendsmart-api


Installation
------------
::

    pip install lendsmart_api


Building from Source
--------------------

To build and install this package:

- Clone this repository
- ``./setup.py install``

Usage
-----





Contributing
============

Tests
-----

Tests live in the ``tests`` directory.  When invoking tests, make sure you are
in the root directory of this project.  To run the full suite across all
supported python versions, use tox_:

.. code-block:: shell

   tox

Running tox also runs pylint and coverage reports.

The test suite uses fixtures stored as JSON in ``test/fixtures``.  These files
contain sanitized JSON responses from the API - the file name is the URL called
to produce the response, replacing any slashes with underscores.

Test classes should extend ``test.base.ClientBaseCase``.  This provides them
with ``self.client``, a ``LinodeClient`` object that is set up to work with
tests.  Importantly, any GET request made by this object will be mocked to
retrieve data from the test fixtures.  This includes lazy-loaded objects using
this client (and by extension related models).

When testing against requests other than GET requests, ``self.mock_post`` (and
equivalent methods for other HTTP verbs) can be used in a ``with`` block to
mock out the intended request type.  These functions accept the relative path
from the api base url that should be returned, for example::

   # this should return the result of GET /linode/instances/123
   with self.mock_post('/linode/instances/123'):
     linode = self.client.linode.instance_create('g6-standard-2', 'us-east')
     self.assertEqual(linode.id, 123) # passes

.. _tox: http://tox.readthedocs.io



