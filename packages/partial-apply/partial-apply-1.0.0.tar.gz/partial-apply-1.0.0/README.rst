partial-apply
=============

Partial application of functions and method names, supporting placeholder values for positional arguments.

Unlike `functools.partial() <https://docs.python.org/3/library/functools.html#functools.partial>`_, placeholder values are supported so that positional arguments for partial application do not need to be supplied solely from left to right. Keyword arguments are handled equivalently to ``functools.partial()``. It is also possible to "partially apply" a method name, producing a function which looks up the method to call on the object supplied as its first argument.

**Dependencies:**

- Python 2.7 or 3.4+.

**Installation:**

- ``$ pip install partial-apply``

**Documentation:**

- Sphinx generated API documentation is available in the ``docs`` subdirectory of this repository and is also published on `GitHub Pages <https://crowsonkb.github.io/partial-apply/>`_.

Examples
--------

An example of placeholder use:
``````````````````````````````

.. code:: python

   from partial_apply import Empty, PartialFn, PartialMethod

   isint = PartialFn(isinstance, Empty, int)

This makes a function ``isint()`` that takes one positional argument and returns ``True`` if it is an ``int`` and ``False`` otherwise. That is, calling ``isint(1)`` is equivalent to calling ``isinstance(1, int)``. The supplied positional arguments fill in ``Empty`` placeholder slots from left to right before reverting to ``functools.partial()``-style appending.

An example of ``PartialMethod`` use:
````````````````````````````````````

.. code:: python

   count_true = PartialMethod('count', True)
   count_true((False, True))  # returns 1
   count_true([False, True])  # returns 1

This makes a function ``count_true()`` that counts the number of ``True`` values in a sequence. It looks up the sequence method ``count`` on the first argument and calls it with the single argument ``True``. The calls shown are equivalent to ``(False, True).count(True)`` and ``[False, True].count(True)``. Since ``count_true()`` only stores the method name and not the method itself, it works on any type with a ``count()`` method.

Like ``PartialFn``, ``PartialMethod`` supports placeholder positional arguments and ``functools.partial()``-like keyword arguments.
