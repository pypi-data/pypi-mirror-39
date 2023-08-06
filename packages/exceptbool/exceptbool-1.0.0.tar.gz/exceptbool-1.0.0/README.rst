==========
exceptbool
==========


.. image:: https://img.shields.io/pypi/v/exceptbool.svg
        :target: https://pypi.python.org/pypi/exceptbool

.. image:: https://readthedocs.org/projects/exceptbool/badge/?version=latest
        :target: https://exceptbool.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Converts caught exception into bool value.


* Free software: MIT license
* Documentation: https://exceptbool.readthedocs.io.


Features
--------

How many of those have you written in your life? ::

 def is_something_possible():
     try:
         do_something()
         return True
     except DoingSomethingError:
         return False

Ugh! A perfect example of six-line boilerplate code. With exceptbool you can shorten that into only three lines! ::

 @except_to_bool(exc=DoingSomethingError, to=False)
 def is_something_possible():
     do_something()

Exceptbool makes decorated function return bool instead of raising an exception by converting given exception(s) into given bool value. If no exception will be raised, then negation of given bool will be returned. If exception different than given one will be raised, then it will not be caught.

Installation
------------

To install exceptbool into your Python environment run following pip command::

 $ pip install exceptbool

Usage
-----
First import ``except_to_bool`` decorator into current namespace::

 from exceptbool import except_to_bool

|

To catch any exception and convert it into False::

 @except_to_bool
 def decorated_function():
    error_raising_function()

Now ``decorated_function`` will return False if ``error_raising_function`` raises Exception, True otherwise.

|

To catch given exception and convert it into given bool value::

 @except_to_bool(exc=ValueError, to=True)
 def decorated_function():
    error_raising_function()

Now ``decorated_function`` will return True if ``error_raising_function`` raises ValueError, False otherwise.

|

To catch any of multiple exceptions::

 @except_to_bool(exc=(TypeError, TimeoutError))
 def decorated_function():
    error_raising_function()

Now ``decorated_function`` will return False if ``error_raising_function`` raises TypeError or TimeoutError, True otherwise.

|

Function decorated with ``except_to_bool`` is perfectly capable of accepting positional and keyword arguments::

 @except_to_bool
 def decorated_function(*args, **kwargs):
    error_raising_function(*args, **kwargs)

 decorated_function("foo", bar="baz")  # no error

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
