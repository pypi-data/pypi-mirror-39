.. This file is a part of the AnyBlok / Attachment project
..
..    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. image:: https://travis-ci.org/AnyBlok/anyblok_attachment.svg?branch=master
    :target: https://travis-ci.org/AnyBlok/anyblok_attachment
    :alt: Build status

.. image:: https://coveralls.io/repos/github/AnyBlok/anyblok_attachment/badge.svg?branch=master
    :target: https://coveralls.io/github/AnyBlok/anyblok_attachment?branch=master
    :alt: Coverage

.. image:: https://img.shields.io/pypi/v/anyblok_attachment.svg
   :target: https://pypi.python.org/pypi/anyblok_attachment/
   :alt: Version status

.. image:: https://readthedocs.org/projects/anyblok-attachment/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://doc.anyblok-attachment.anyblok.org/?badge=latest


AnyBlok attachment
==================

Improve `AnyBlok <http://doc.anyblok.org>`_ to add attachment and report
system.

+-----------------------+-------------------+---------------------------------------------------------+
| Blok                  | Dependancies      | Description                                             |
+=======================+===================+=========================================================+
| **attachment**        |                   | Stock and historize Document                            |
+-----------------------+-------------------+---------------------------------------------------------+
| **report**            | **attachment**    | Core of the reporting engine for AnyBlok. This blok     |
|                       |                   | add helper to generate a Document, but it is not a      |
|                       |                   | templating engine.                                      |
+-----------------------+-------------------+---------------------------------------------------------+
| **report-format**     | **attachment**    | Simple templating engine, based on ``str.format(...)``  |
|                       | **report**        |                                                         |
+-----------------------+-------------------+---------------------------------------------------------+
| **wkhtml2pdf**        | **attachment**    | Add Model add method to convert HTML 2 PDF.             |
|                       | **report**        |                                                         |
+-----------------------+-------------------+---------------------------------------------------------+


AnyBlok / Attachment is released under the terms of the `Mozilla Public License`.

See the `latest documentation <http://doc.anyblok-attachment.anyblok.org/>`_
