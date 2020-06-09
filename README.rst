.. image:: https://github.com/Dominik1123/arguable/workflows/Tests/badge.svg
   :target: https://github.com/Dominik1123/arguable/actions?workflow=Tests

.. image:: https://codecov.io/gh/Dominik1123/arguable/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Dominik1123/arguable

.. image:: https://img.shields.io/pypi/v/arguable.svg
   :target: https://pypi.org/project/arguable/


Arguable
========

"arguable" stands for "argparse configurable". This project enables class-level configuration via argparse and the command line interface.


Installation
------------

.. code-block::

   pip install arguable


Usage
-----

Classes inheriting from ``arguable.Arguable`` define a class-level
``argparse.Namespace`` object ``config`` which holds relevant
parameters and their defaults. The corresponding argument parser is
created automatically from these parameters and is stored as the
``config_parser`` class attribute.

For example:

.. code-block:: python

   from argparse import Namespace
   from arguable import Arguable


   class Example(Arguable):
       config = Namespace(language='en')


   print(Example().config.language)

When the class is created, the ``Example.config_parser`` attribute holds
an argument parser with an argument ``--example-language`` with
``type=str`` and ``default='en'``.

When the class is instantiated it automatically configures its instances
by assigning an instance-level attribute ``config`` which picks up the
provided command line arguments and shadows the class-level ``config`` defaults.

So invoking the above script via ``python example.py --example-language=de`` prints ``de`` while omitting the parameter uses the default ``en``.


Parameter types
~~~~~~~~~~~~~~~

Other supported parameter types are sequences (e.g. tuples) which will
use the following argument definition:

.. code-block:: python

   # `par` is the tuple parameter default.
   parser.add_argument(name, type=type(par[0]), nargs=len(par), default=par)

``bool``:

.. code-block:: python

   # `par` is the bool parameter default.
   parser.add_argument(name, action=f'store_{"false" if par else "true"}')

and of course all the numeric types.


Customization
~~~~~~~~~~~~~

By default the class name in lowercase will be used as a prefix for
parameter names. This can be configured by two class variables:

* ``config_prefix`` -- If provided then this is used directly as the prefix.
* ``config_removesuffix`` -- If ``config_prefix`` is not provided,
  the class name in lowercase is used and reduced by this suffix
  (if provided).

These variables can also be provided during class creation without
the ``config_`` prefix, e.g.:

.. code-block:: python

   class ExampleA(Arguable, prefix='test'):
       config_prefix = 'text'  # similar


   class ExampleB(Arguable, removesuffix='b'):
       config_removesuffix = 'b'  # similar


Showing the full help text
~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to make the application aware of all registered parameters,
the ``Arguable`` class has a ``super_parser`` attribute which is an
instance of ``argparse.ArgumentParser``. Whenever a class registers
new parameters, not only the class-level parser ``config_parser`` gets
updated, but also the application-level ``super_parser``. This parser
can be used to show the help text involving all parameters.

This package provides a helper parser class, ``arguable.ArgumentParser``,
which automatically falls back on ``super_parser`` when ``--help``
is requested.

This ``super_parser`` can also be used used to verify the correctness of
all given parameters. Since every class is only concerned with their own
parameters, excess arguments are simply ignored (using ``parse_known_args``).
Using the ``super_parser`` one can verify that all provided arguments
are supported by the application:

.. code-block:: python

   from arguable import Arguable


   if __name__ == '__main__':
       # The following will report any excess arguments.
       Arguable.super_parser.parse_args()
