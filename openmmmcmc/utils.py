#!/usr/bin/env python

# =============================================================================
# MODULE DOCSTRING
# =============================================================================

"""
General utility functions for the repo.

"""


# =============================================================================
# GLOBAL IMPORTS
# =============================================================================

import abc


# =============================================================================
# METACLASS UTILITIES
# =============================================================================

# TODO Remove this when we drop Python 2 support.
def with_metaclass(metaclass, *bases):
    """Create a base class with a metaclass.

    Imported from six (MIT license): https://pypi.python.org/pypi/six.
    Provide a Python2/3 compatible way to create an metaclass.

    """
    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class Metaclass(metaclass):
        def __new__(cls, name, this_bases, d):
            return metaclass(name, bases, d)
    return type.__new__(Metaclass, 'temporary_class', (), {})


class SubhookedABCMeta(with_metaclass(abc.ABCMeta)):
    """Abstract class with an implementation of __subclasshook__.

    The __subclasshook__ method checks that the instance implement the
    abstract properties and methods defined by the abstract class. This
    allow classes to implement an abstraction without explicitly
    subclassing.

    Examples
    --------
    >>> class MyInterface(SubhookedABCMeta):
    ...     @abc.abstractmethod
    ...     def my_method(self): pass
    >>> class Implementation(object):
    ...     def my_method(self): return True
    >>> isinstance(Implementation(), MyInterface)
    True

    """
    @classmethod
    def __subclasshook__(cls, subclass):
        for abstract_method in cls.__abstractmethods__:
            if not any(abstract_method in C.__dict__ for C in subclass.__mro__):
                return False
        return True
