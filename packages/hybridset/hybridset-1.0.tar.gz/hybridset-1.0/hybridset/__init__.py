"""HybridSets module.

This module contains:

* HybridSet   : MutableSet storing non hashables values separately
* HybridCache : HybridSet storing non hashables values using copy.deepcopy
"""

from copy import deepcopy
from collections.abc import Hashable, MutableSet


__all__ = ['HybridSet', 'HybridCache']


class HybridSet(MutableSet):
    """Mutable Set storing unhashable values separately."""

    def __init__(self, iterable=None, *, hashables=None, unhashables=None):
        """An iterable containing either hashables and unhashables
        values mixed values can be supplied as fisrt argument.

        If you know already the hashabilty of the values in an iterable,
        you should use the two keyword arguments `hashables` and
        `unhashables`.
        """
        self._list = list()
        self._set = set()
        if iterable:
            self |= iterable
        if hashables:
            assert all(isinstance(val, Hashable) for val in hashables)
            self._set |= set(hashables)
        if unhashables:
            assert not any(isinstance(val, Hashable) for val in unhashables)
            for val in unhashables:
                self._add_unhashable(val)

    @property
    def hashables(self):
        """Read only property returing a copy of the hashable values
        as a set."""
        return self._set.copy()

    @property
    def unhashables(self):
        """Read only property returing a copy of the unhashable values
        as a list."""
        return self._list.copy()

    def __len__(self):
        return len(self._list) + len(self._set)

    def __contains__(self, val):
        if isinstance(val, Hashable):
            return val in self._set
        return val in self._list

    def __iter__(self):
        yield from self._set
        yield from self._list

    def add(self, val):
        if isinstance(val, Hashable):
            self._set.add(val)
        else:
            self._add_unhashable(val)

    def discard(self, val):
        if isinstance(val, Hashable):
            self._set.discard(val)
        else:
            self._discard_unhashable(val)

    def _add_unhashable(self, val):
        if val not in self._list:
            self._list.append(val)

    def _discard_unhashable(self, val):
        if val in self._list:
            self._list.remove(val)
            assert val not in self._list

    def __repr__(self):
        # ex: HybridCache(hashables={1, 2, 3}, unhashables=[[4, 5], {6, 7}])
        hashables, unhashables = self._set, self._list
        hashables = f'hashables={hashables!r}' if hashables else ''
        unhashables = f'unhashables={unhashables!r}' if unhashables else ''
        args = ', '.join(val for val in (hashables, unhashables) if val)
        clsname = self.__class__.__name__
        return f"{clsname}({args})"

    def copy(self):
        """Return a shallow copy of an HybridSet."""
        return type(self)(hashables=self._set, unhashables=self._list)

    # For copy.copy
    __copy__ = copy

    def clear(self):
        self._set.clear()
        self._list.clear()

    def pop(self):
        if self._list:
            return self._list.pop()
        return self._set.pop()

    # The two next methods may raise a TypeError when dealing with classic sets
    # because of the precense of unhashable values, so an override of the
    # default implementation in MutableSet is needed for both.

    def __le__(self, other):
        try:
            return super().__le__(other)
        except TypeError:
            # If there are unhashables, its not a subset of a regular one
            if self._list:
                return False
            raise

    def __sub__(self, other):
        try:
            return super().__sub__(other)
        except TypeError:
            # Only substract other from the hashables
            subset = self._set - other
            return type(self)(hashables=subset, unhashables=self._list)


class HybridCache(HybridSet):
    """Mutable set storing unhashable values separately.

    Implemetation detail:
    the unhashable values are stored using copy.deepcopy."""

    def _add_unhashable(self, val):
        if val not in self._list:
            self._list.append(deepcopy(val))

