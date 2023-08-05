===========
Added Value
===========

A Sphinx extension for embedding Python object *values* into documentation as text, lists
or tables.

This is achieved by adding new roles and directives which refer to Python objects which contain
the values to be represented. The extension provides roles for embedded single and lists of values,
and a sophisticated directive for rendering complex data structures like lists of dictionaries as
tables.


Status
======

Build status:

.. image:: https://travis-ci.org/sixty-north/added-value.svg?branch=master
    :target: https://travis-ci.org/sixty-north/added-value

.. image:: https://readthedocs.org/projects/added-value/badge/?version=latest
    :target: https://added-value.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/sixty-north/added-value/badge.svg?branch=master
    :target: https://coveralls.io/github/sixty-north/added-value?branch=master



Installation
============

The ``added-value`` package is available on the Python Package Index (PyPI):

.. image:: https://badge.fury.io/py/added-value.svg
    :target: https://badge.fury.io/py/added-value

The package supports Python 3 only. To install::

  $ pip install added-value



Development
===========

Maintenance
-----------

::

  $ pip install -e .



Testing
-------

::

  $ pip install -e .[test]
  $ pytest --cov=source tests


Documentation
-------------

  $ pip install -e .[docs]
  $ cd docs
  $ make html


Release
-------

  $ pip install -e .[deploy]
  $ bumpversion minor
  $ python setup.py sdist bdist_wheel
  $ twine upload --config-file <path>/sixty-north.pypirc dist/*
  $ git push origin
