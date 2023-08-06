README
######

.. image:: https://travis-ci.org/mlenzen/lenzm_utils.svg?branch=master
	:target: https://travis-ci.org/mlenzen/lenzm_utils
	:alt: Build Status


.. image:: https://coveralls.io/repos/mlenzen/lenzm_utils/badge.svg?branch=master
	:target: https://coveralls.io/r/mlenzen/lenzm_utils?branch=master
	:alt: Coverage


Overview
========

This package includes one module - ``lenzm_utils``.


Getting Started
===============

.. code:: python

	 >>> import lenzm_utils

Installation
============

``pip install git+https://github.com/mlenzen/lenzm_utils.git#egg=lenzm_utils``

Usage
=====
	``import lenzm_utils``

Features
========

* TODO

Running Tests
=============

Some tests require a postgres db to be set up with username/password/dbname all "test"

On Ubuntu:

.. code-block:: sh

	$ sudo -u postgres createuser -P test
	$ sudo -u postgres createdb -O test test
	$ sudo -u postgres psql test -c "create extension citext"


:Author: Michael Lenzen
:Copyright: 2018 Michael Lenzen
:License: MIT
:GitHub: https://github.com/mlenzen/lenzm_utils
