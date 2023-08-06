"""Partial application of functions and method names, supporting placeholder
values for positional arguments.

Unlike :func:`functools.partial`, placeholder values are supported so that
positional arguments for partial application do not need to be supplied solely
from left to right. Keyword arguments are handled equivalently to
:func:`functools.partial()`. It is also possible to "partially apply" a method
name, producing a function which looks up the method to call on the object
supplied as its first argument.
"""

# pylint: disable=useless-object-inheritance

__all__ = ['Empty', 'PartialFn', 'PartialMethod']


class EmptyType(object):
    """A placeholder for arguments which will be supplied later."""
    __slots__ = ()

    def __repr__(self):
        return 'Empty'

Empty = EmptyType()


class PartialFn(object):
    """A function partially applied to positional and keyword arguments.

    Keyword arguments are handled equivalently to :func:`functools.partial`, but
    arbitrary sets of positional arguments can be partially applied.

    :Examples:

    Skipping partial application of positional arguments using the
    :data:`Empty` placeholder:

    Create a partially applied function from ``fn`` where the third argument
    is ``'thing'``.

    >>> def fn(*args):
    >>>     return args

    >>> p = PartialFn(fn, Empty, Empty, 'thing')
    >>> p
    PartialFn(<function fn at 0x11b29a598>, Empty, Empty, 'thing')

    With two placeholders, you must call ``p`` with at least two positional
    arguments. They fill in the placeholders from left to right.

    >>> p(1, 2)
    (1, 2, 'thing')

    Subsequent positional arguments to ``p`` are applied after the third
    parameter.

    >>> p(1, 2, 3)
    (1, 2, 'thing', 3)

    :ivar func: The wrapped function.
    :vartype func: callable
    :ivar args: Positional arguments for the wrapped function.
    :vartype args: tuple
    :ivar kwargs: Keyword arguments for the wrapped function.
    :vartype kwargs: dict[str, any]
    """

    def __init__(self, func, *args, **kwargs):
        """Creates a new partially applied function.

        :param callable func: The function to wrap.
        :param args: Positional arguments for the wrapped function.
        :param kwargs: Keyword arguments for the wrapped function.
        :raises TypeError: If the first argument is not callable.
        """
        if not callable(func):
            raise TypeError('the first argument must be callable')
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        """Calls the partially applied function.

        :param args: Additional positional arguments for the wrapped
            function.
        :param kwargs: Additional keyword arguments for the wrapped
            function.
        :return: The return value of the wrapped function.
        :rtype: any
        :raises TypeError: If less positional arguments are supplied than
            placeholders.
        """
        i = 0
        new_args = []
        for arg in self.args:
            if arg is Empty:
                if i < len(args):
                    new_args.append(args[i])
                else:
                    expected = sum(map(lambda x: x is Empty, self.args))
                    msg = 'expected at least {} values for placeholders, got {}'
                    raise TypeError(msg.format(expected, len(args)))
                i += 1
            else:
                new_args.append(arg)
        new_args.extend(args[i:])
        new_kwargs = self.kwargs.copy()
        new_kwargs.update(kwargs)
        return self.func(*new_args, **new_kwargs)

    def __repr__(self):
        fmt_kwargs = ['{}={!r}'.format(k, v) for k, v in self.kwargs.items()]
        fmt_all_args = [repr(self.func)]
        fmt_all_args.extend(map(repr, self.args))
        fmt_all_args.extend(fmt_kwargs)
        return '{}({})'.format(type(self).__name__, ', '.join(fmt_all_args))


class PartialMethod(object):
    """A method name partially applied to positional and keyword arguments.

    Keyword arguments are handled equivalently to :func:`functools.partial`, but
    arbitrary sets of positional arguments can be partially applied (see
    :class:`PartialFn` for an example). When an instance of
    :class:`PartialMethod` is called, the object to look up the method on is
    supplied as the first argument.

    :Examples:

    Setting up some example classes.

    >>> class SomeClass:
    >>>     def method(self, *args):
    >>>         return args

    >>> some_instance = SomeClass()

    >>> class OtherClass:
    >>>     def method(self, *args):
    >>>         return sum(args)

    >>> other_instance = OtherClass()

    Create a partially applied function where the method name is ``method`` and
    the second positional argument is 1.

    >>> p = PartialMethod('method', Empty, 1)
    >>> p
    PartialMethod('method', Empty, 1)

    The partially applied function takes the object to look up the method on as
    the first argument. Subsequent positional arguments are handled as in
    :class:`PartialFn`. Apply the function to different objects of different
    types (they must all have a method named ``method``).

    >>> p(some_instance, 2, 3)
    (2, 1, 3)

    >>> p(other_instance, 2, 3)
    6

    :ivar name: The method name.
    :vartype name: str
    :ivar args: Positional arguments for the method.
    :vartype args: tuple
    :ivar kwargs: Keyword arguments for the method.
    :vartype kwargs: dict[str, any]
    """

    def __init__(self, name, *args, **kwargs):
        """Creates a new partially applied method name.

        :param str name: The method name.
        :param args: Positional arguments for the method.
        :param kwargs: Keyword arguments for the method.
        :raises TypeError: If the first argument is not a string.
        """
        if not isinstance(name, str):
            raise TypeError('the first argument must be a string')
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def __call__(self, obj, *args, **kwargs):
        """Looks up and calls the method.

        :param any obj: The object to look up the method on.
        :param args: Additional positional arguments for the method.
        :param kwargs: Additional keyword arguments for the method.
        :return: The return value of the method.
        :rtype: any
        :raises TypeError: If less positional arguments are supplied than
            placeholders.
        """
        i = 0
        new_args = []
        for arg in self.args:
            if arg is Empty:
                if i < len(args):
                    new_args.append(args[i])
                else:
                    expected = sum(map(lambda x: x is Empty, self.args))
                    msg = 'expected at least {} values for placeholders, got {}'
                    raise TypeError(msg.format(expected, len(args)))
                i += 1
            else:
                new_args.append(arg)
        new_args.extend(args[i:])
        new_kwargs = self.kwargs.copy()
        new_kwargs.update(kwargs)
        func = getattr(obj, self.name)
        return func(*new_args, **new_kwargs)

    def __repr__(self):
        fmt_kwargs = ['{}={!r}'.format(k, v) for k, v in self.kwargs.items()]
        fmt_all_args = [repr(self.name)]
        fmt_all_args.extend(map(repr, self.args))
        fmt_all_args.extend(fmt_kwargs)
        return '{}({})'.format(type(self).__name__, ', '.join(fmt_all_args))
