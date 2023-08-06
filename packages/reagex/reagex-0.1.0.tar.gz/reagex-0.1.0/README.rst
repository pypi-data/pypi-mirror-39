========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-reagex/badge/?style=flat
    :target: https://readthedocs.org/projects/python-reagex
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/janluke/python-reagex.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/janluke/python-reagex

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/janluke/python-reagex?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/janluke/python-reagex

.. |codecov| image:: https://codecov.io/github/janluke/python-reagex/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/janluke/python-reagex

.. |version| image:: https://img.shields.io/pypi/v/reagex.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/reagex

.. |commits-since| image:: https://img.shields.io/github/commits-since/janluke/python-reagex/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/janluke/python-reagex/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/reagex.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/reagex

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/reagex.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/reagex

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/reagex.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/reagex

.. end-badges


The goal of ``reagex`` (from `"readable regular expression"`)
is to suggest a way for writing complex regular expressions with
many capturing groups in a readable way.

At the moment, it contains just one very simple function
(called ``reagex``) and an utility function, but any function
which could be useful for writing readable patterns is welcome.

**Note:** Publishing this ridiculously small project is an excuse to familiarize
with python packaging, DevOps tools and the entire workflow behind the publication
of an open-source project.
The project template was generated using https://github.com/ionelmc/cookiecutter-pylibrary/
which is obviously an overkill for a "one-function-project".

* Free software: BSD 2-Clause License

Usage
=====
The core function ``reagex`` is just a wrapper of ``str.format`` and it works
in the same way. See the example

.. code-block:: python

    import re
    from reagex import reagex

    # A sloppy pattern for an italian address (just to show how it works)
    pattern = reagex(
        '{_address}, {postcode} {city} {province}',
        # groups starting with "_" are non-capturing
        _address = reagex(
            '{street} {number}',
            street = '(via|contrada|c/da|c.da|piazza|p.za) [a-zA-Z]+',
            number = 'snc|[0-9]+'
        ),
        postcode = '[0-9]{5}',
        city = '[A-Za-z]+',
        province = '[A-Z]{2}'
    )

    matcher = re.compile(pattern)
    match = matcher.fullmatch('via Roma 123, 12345 Napoli NA')
    print(match.groupdict())

    # prints:
    #   {'city': 'Napoli',
    #    'number': '123',
    #    'postcode': '12345',
    #    'province': 'NA',
    #    'street': 'via Roma'}


Groups starting by ``'_'`` are non-capturing. The rest are all named capturing
groups.

Why not...
===========
Why not using just re.VERBOSE?
------------------------------
I think ``reagex`` is easier to write and to read:

* with reagex, you first describe the structure of the pattern in terms of groups,
  `then` you provide a pattern for each group;
  with re.VERBOSE you have to define the groups in the exact position they
  must be matched: to get the high-level structure of the pattern you may need
  to read multiple lines at the same indentation level
* with re.VERBOSE you just write a big string; with reagex you get
  syntax highlighting which helps readability
* white-spaces don't need any special treatment
* "{group_name}" is nicer than "(?P<group_name>)"


Installation
============
::

    pip install reagex


Documentation
=============

https://python-reagex.readthedocs.io/


Development
===========
Possible improvements:

1. make some meaningful use of the ``format_spec``
   in ``{group_name:format_spec}``

2. add utility functions like ``repeated`` to help writing
   common patterns in a readable way


Testing
-------
To run all the tests::

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
