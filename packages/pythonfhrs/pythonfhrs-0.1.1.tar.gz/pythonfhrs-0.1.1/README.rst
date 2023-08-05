========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |appveyor|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-fhrs/badge/?style=flat
    :target: https://readthedocs.org/projects/python-fhrs
    :alt: Documentation Status


.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/ayushjsh/python-fhrs?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/ayushjsh/python-fhrs

.. |codecov| image:: https://codecov.io/github/ayushjsh/python-fhrs/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/gl/deeprd/python-fhrs

.. |version| image:: https://img.shields.io/pypi/v/pythonfhrs.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pythonfhrs

.. |commits-since| image:: https://img.shields.io/github/commits-since/ayushjsh/python-fhrs/v0.1.1.svg
    :alt: Commits since latest release
    :target: https://gitlab.com/deeprd/python-fhrs/commits?since=2018-12-01

.. |wheel| image:: https://img.shields.io/pypi/wheel/pythonfhrs.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/pythonfhrs

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pythonfhrs.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/pythonfhrs

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pythonfhrs.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/pythonfhrs


.. end-badges

A python wrapper around the UK FHRS api.

* Free software: MIT license

Installation
============

::

    pip install pythonfhrs

Documentation
=============


https://python-fhrs.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
