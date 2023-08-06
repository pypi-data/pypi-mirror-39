==========
exceptbool
==========

.. image:: https://img.shields.io/pypi/v/exceptbool.svg
        :target: https://pypi.python.org/pypi/exceptbool

.. image:: https://pepy.tech/badge/exceptbool
        :target: https://pepy.tech/badge/exceptbool

.. image:: https://travis-ci.org/konrad-kocik/exceptbool.svg?branch=master
        :target: https://travis-ci.org/konrad-kocik/exceptbool.svg?branch=master

.. image:: https://readthedocs.org/projects/exceptbool/badge/?version=latest
        :target: https://exceptbool.readthedocs.io/en/latest/?badge=latest

Converts caught exception into bool value.

* Free software: MIT license
* Documentation: https://exceptbool.readthedocs.io.

Features
--------

How many of those have you written in your life?

.. code-block:: python

    def is_something_possible():
        try:
            do_something()
            return True
        except DoingSomethingError:
            return False

Ugh! A perfect example of six-line boilerplate code. With exceptbool you can shorten that into only three lines!

.. code-block:: python

 @except_to_bool(exc=DoingSomethingError)
 def is_something_possible():
     do_something()

Exceptbool makes decorated function return bool instead of raising an exception by converting given exception(s) into given bool value. If no exception will be raised, then negation of given bool will be returned. If exception different than given one will be raised, then it will not be caught.

============
Installation
============

Stable release
--------------

To install exceptbool, run this command in your terminal:

.. code-block:: console

    $ pip install exceptbool

This is the preferred method to install exceptbool, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

From sources
------------

The sources for exceptbool can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/konrad-kocik/exceptbool

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/konrad-kocik/exceptbool/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/konrad-kocik/exceptbool
.. _tarball: https://github.com/konrad-kocik/exceptbool/tarball/master

=====
Usage
=====

First, import ``except_to_bool`` decorator into current namespace:

.. code-block:: python

     from exceptbool import except_to_bool

To catch any exception and convert it into False:

.. code-block:: python

    @except_to_bool
    def decorated_function():
        error_raising_function()

Now ``decorated_function`` will return False if ``error_raising_function`` raises Exception, True otherwise.

To catch given exception and convert it into given bool value:

.. code-block:: python

    @except_to_bool(exc=ValueError, to=True)
    def decorated_function():
       error_raising_function()

Now ``decorated_function`` will return True if ``error_raising_function`` raises ValueError, False otherwise.

To catch any of multiple exceptions:

.. code-block:: python

    @except_to_bool(exc=(TypeError, TimeoutError))
    def decorated_function():
       error_raising_function()

Now ``decorated_function`` will return False if ``error_raising_function`` raises TypeError or TimeoutError, True otherwise.

Function decorated with ``except_to_bool`` is perfectly capable of accepting positional and keyword arguments:

.. code-block:: python

    @except_to_bool
    def decorated_function(*args, **kwargs):
        error_raising_function(*args, **kwargs)

    decorated_function("foo", bar="baz")  # no error