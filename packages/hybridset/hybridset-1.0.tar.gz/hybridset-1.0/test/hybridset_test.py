from collections.abc import MutableSet
from hybridset import HybridSet, HybridCache
from copy import copy
import pytest


SKIPPING_ASSERTS = False


@pytest.fixture(params=[HybridSet, HybridCache])
def EveryHybridSet(request):
    return request.param


OtherOrSameHybridSet = EveryHybridSet


@pytest.fixture(params=[set, frozenset, HybridSet, HybridCache])
def EverySet(request):
    return request.param


def test_EveryHybridSet_is_MutableSet(EveryHybridSet):
    assert issubclass(EveryHybridSet, MutableSet)
    hs = EveryHybridSet()
    assert isinstance(hs, MutableSet)


def test_EveryHybridSet_hashables_unhashables_properties(EveryHybridSet):
    hs = EveryHybridSet([42, 'thing', [3, 4], {4, 5}])
    assert hs.hashables == {42, 'thing'}
    assert hs.unhashables == [[3, 4], {4, 5}]


def test_EveryHybridSet_hashables_unhashables_kwargs(EveryHybridSet):
    hs = EveryHybridSet(hashables={3, 4}, unhashables=[[4], [5]])
    assert hs == EveryHybridSet([3, 4, [4], [5]])
    hs = EveryHybridSet(hashables=[3, 3, 3], unhashables= [[4], [4], [4]])
    assert hs == EveryHybridSet([3, [4]])


def test_EveryHybridSet_bad_instantiation(EveryHybridSet):
    if SKIPPING_ASSERTS:
        EveryHybridSet(hashables=[3, 4, 5, [6, 7], 8, 9])
        EveryHybridSet(unhashables=[3, 4, 5, [6, 7], 8, 9])
    else:
        with pytest.raises(AssertionError):
            EveryHybridSet(hashables=[3, 4, 5, [6, 7], 8, 9])
        with pytest.raises(AssertionError):
            EveryHybridSet(unhashables=[3, 4, 5, [6, 7], 8, 9])


def test_EveryHybridSet_equality(EveryHybridSet, OtherOrSameHybridSet):
    hs1 = EveryHybridSet()
    assert hs1 == OtherOrSameHybridSet()
    hs2 = OtherOrSameHybridSet([3, [4]])
    assert hs2 == EveryHybridSet([3, [4]])
    assert hs1 != hs2


def test_EveryHybridSet_equality_with_builtin_sets(EveryHybridSet):
    hs1 = EveryHybridSet()
    assert hs1 == set()
    assert hs1 == frozenset()
    assert hs1 != {1}
    assert hs1 != frozenset({1})
    hs2 = EveryHybridSet([3, 4])
    assert hs2 == {3, 4}
    assert hs2 == frozenset({3, 4})
    assert hs2 != set()
    assert hs2 != frozenset()


def test_EveryHybridSet_len(EveryHybridSet):
    hs = EveryHybridSet([42, [3, 4]])
    assert len(hs) == 2
    assert bool(hs) is True
    assert hs
    hs = EveryHybridSet()
    assert len(hs) == 0
    assert bool(hs) is False
    assert not hs


def test_EveryHybridSet_in(EveryHybridSet):
    hs = EveryHybridSet([42, [3, 4]])
    assert 42 in hs
    assert [3, 4] in hs
    assert 0 not in hs


def test_EveryHybridSet_iter(EveryHybridSet):
    hs = EveryHybridSet([42, [3, 4]])
    it = iter(hs)
    a = next(it)
    b = next(it)
    assert (a == 42 and b == [3, 4]) or (a == [3, 4] and b == 42)
    with pytest.raises(StopIteration):
        next(it)


def test_EveryHybridSet_union(EveryHybridSet, EverySet):
    hs1 = EveryHybridSet([1, 2, [3], [4]])
    hs2 = EveryHybridSet([2, [3], [5]])
    hs3 = EveryHybridSet([0, 1])
    s4 = EverySet([1, 3, 5])
    assert hs1 | hs2 == EveryHybridSet([1, 2, [3], [4], [5]])
    assert s4 | hs1 == EveryHybridSet([1, 2, 3, 5, [3], [4]])
    assert s4 | hs3 == EverySet([0, 1, 3, 5])


def test_EveryHybridSet_intersection(EveryHybridSet, EverySet):
    hs1 = EveryHybridSet([1, 2, [3], [4]])
    hs2 = EveryHybridSet([2, [3], [5]])
    hs3 = EveryHybridSet([0, 1, 3])
    s4 = EverySet([1, 3, 5])
    assert hs1 & hs2 == EveryHybridSet([2, [3]])
    assert s4 & hs1 == EverySet([1])
    assert s4 & hs3 == EverySet([1, 3])


def test_EverySet_difference(EveryHybridSet, EverySet):
    hs1 = EveryHybridSet([1, 2, [3], [4]])
    hs2 = EveryHybridSet([2, [3], [5]])
    hs3 = EveryHybridSet([0, 1])
    s4 = EverySet([1, 3, 5])
    assert hs1 - hs2 == EveryHybridSet([1, [4]])
    assert hs2 - hs1 == EveryHybridSet([[5]])
    assert s4 - hs1 == EverySet([3, 5])
    assert hs1 - s4 == EveryHybridSet([2, [3], [4]])
    assert s4 - hs3 == EverySet([3, 5])
    assert hs3 - s4 == EverySet([0])


def test_EverySet_Symetric_difference(EveryHybridSet, EverySet):
    hs1 = EveryHybridSet([1, 2, [3], [4]])
    hs2 = EveryHybridSet([2, [3], [5]])
    hs3 = EveryHybridSet([0, 1])
    s4 = EverySet([1, 3, 5])
    assert hs1 ^ hs2 == EveryHybridSet([1, [4], [5]])
    assert s4 ^ hs1 == EveryHybridSet([2, 3, 5, [3], [4]])
    assert s4 ^ hs3 == EverySet([0, 3, 5])


def test_EverySet_subset_superset(EveryHybridSet, EverySet):
    hs1 = EveryHybridSet([1, 2, [3], [4]])
    hs2 = EveryHybridSet([1, 2, [3]])
    hs3 = EveryHybridSet([1, 2])
    s4 = EverySet([1])
    assert hs1 >= hs2 and hs1 > hs2
    assert hs2 >= hs3 and hs2 > hs3
    assert hs3 >= s4  and hs3 > s4
    assert hs2 <= hs1 and hs2 < hs1
    assert hs3 <= hs2 and hs3 < hs2
    assert s4  <= hs3 and s4  < hs3


def test_EverySet_proper_subset_superset(EveryHybridSet, EverySet):
    hs1 = EveryHybridSet([1, 2, [3]])
    hs2 = EveryHybridSet([1, 2, [3]])
    hs3 = EveryHybridSet([1, 2])
    s4 = EverySet([1, 2])
    assert hs1 >= hs2 and not hs1 > hs2
    assert hs3 >= s4  and not hs3 > s4
    assert hs2 <= hs1 and not hs2 < hs1
    assert s4  <= hs3 and not s4  < hs3


def test_EverySet_isdisjoint(EveryHybridSet, EverySet):
    hs1 = EveryHybridSet([1, 2, [3], [4]])
    hs2 = EveryHybridSet([2, [3], [5]])
    hs3 = EveryHybridSet([0, 1])
    s4 = EverySet([1, 3, 5])
    hs5 = EveryHybridSet([2])
    assert not hs1.isdisjoint(hs2)
    assert hs2.isdisjoint(hs3)
    assert not hs3.isdisjoint(s4)
    assert not s4.isdisjoint(hs1)
    assert not s4.isdisjoint(hs3)
    assert s4.isdisjoint(hs5)
    if isinstance(s4, (set, frozenset)):
        assert s4.isdisjoint(hs2.hashables)
    else:
        assert s4.isdisjoint(hs2)
    assert hs2 & s4 == set()
    assert len(hs2 & s4) == 0
    assert not hs2 & s4


def test_EveryHybridSet_add_hashable(EveryHybridSet):
    hs = EveryHybridSet()
    assert len(hs) == 0
    assert 3 not in hs
    hs.add(3)
    assert len(hs) == 1
    assert 3 in hs
    hs.add(3)
    assert len(hs) == 1
    assert 3 in hs


def test_EveryHybridSet_discard_hashable(EveryHybridSet):
    hs = EveryHybridSet([4])
    assert len(hs) == 1
    assert 4 in hs
    hs.discard(4)
    assert len(hs) == 0
    assert 4 not in hs
    hs.discard(4)
    assert len(hs) == 0
    assert 4 not in hs


def test_EveryHybridSet_add_unhashables(EveryHybridSet):
    hs = EveryHybridSet()
    assert len(hs) == 0
    assert [3] not in hs
    hs.add([3])
    assert len(hs) == 1
    assert [3] in hs
    hs.add([3])
    assert len(hs) == 1
    assert [3] in hs


def test_EveryHybridSet_discard_unhashables(EveryHybridSet):
    hs = EveryHybridSet([3, [4]])
    assert len(hs) == 2
    assert [4] in hs
    hs.discard([4])
    assert len(hs) == 1
    assert [4] not in hs
    hs.discard([4])
    assert len(hs) == 1
    assert [4] not in hs


def test_EveryHybridSet_inplace_union(EveryHybridSet, EverySet):
    hs1 = EveryHybridSet([1, 3, [5], [7]])
    hs2 = EveryHybridSet([2, 3, 4, [5], [6]])
    s3  = EverySet([3, 4, 5])
    hs1 |= hs2
    assert hs1 == EveryHybridSet([1, 2, 3, 4, [5], [6], [7]])
    s3 |= hs2
    assert s3 == EveryHybridSet([2, 3, 4, 5, [5], [6]])


def test_EveryHybridSet_inplace_intersection(EveryHybridSet, EverySet):
    hs1 = EveryHybridSet([1, 3, [5], [7]])
    hs2 = EveryHybridSet([2, 3, 4, [5], [6]])
    s3  = EverySet([3, 4, 5])
    hs1 &= hs2
    assert hs1 == EveryHybridSet([3, [5]])
    s3 &= hs2
    assert s3 == EverySet([3, 4])


def test_EveryHybridSet_inplace_difference(EveryHybridSet, EverySet):
    hs1 = EveryHybridSet([1, 3, [5], [7]])
    hs2 = EveryHybridSet([2, 3, 4, [5], [6]])
    s3  = EverySet([3, 4, 5])
    hs1 -= hs2
    assert hs1 == EveryHybridSet([1, [7]])
    s3 -= hs2
    assert s3 == {5} == EveryHybridSet([5])


def test_EveryHybridSet_inplace_symetric_difference(EveryHybridSet, EverySet):
    hs1 = EveryHybridSet([1, 3, [5], [7]])
    hs2 = EveryHybridSet([2, 3, 4, [5], [6]])
    s3  = EverySet([3, 4, 5])
    hs1 ^= hs2
    assert hs1 == EveryHybridSet([1, 2, 4, [6], [7]])
    s3 ^= hs2
    assert s3 == EveryHybridSet([2, 5, [5], [6]])


def test_EveryHybridSet_pop(EveryHybridSet):
    hs1 = EveryHybridSet([1, 3, [5], [7]])
    l = []
    assert len(hs1) == 4
    for i in reversed(range(4)):
        val = hs1.pop()
        assert val not in hs1
        assert len(hs1) == i
        l.append(val)
    assert hs1 == EveryHybridSet()
    with pytest.raises(KeyError):
        hs1.pop()
    assert EveryHybridSet(l) == EveryHybridSet([1, 3, [5], [7]])


def test_EveryHybridSet_repr(EveryHybridSet):
    clsname = EveryHybridSet.__name__
    hs1 = EveryHybridSet()
    exec(f"hs2 = {hs1!r}", globals())
    assert repr(hs1)== f"{clsname}()"
    assert hs1 == hs2
    hs1 = EveryHybridSet([0])
    exec(f"hs2 = {hs1!r}", globals())
    assert repr(hs1) == f"{clsname}""(hashables={0})"
    assert hs1 == hs2
    hs1 = EveryHybridSet([[1]])
    exec(f"hs2 = {hs1!r}", globals())
    assert repr(hs1) == f"{clsname}""(unhashables=[[1]])"
    assert hs1 == hs2
    hs1 = EveryHybridSet([0, [1]])
    exec(f"hs2 = {hs1!r}", globals())
    assert repr(hs1) == f"{clsname}""(hashables={0}, unhashables=[[1]])"
    assert hs1 == hs2


def test_EveryHybridSet_copy(EveryHybridSet):
    hs = EveryHybridSet([0, 'string', [2, 3, 4]])
    copy = hs.copy()
    assert copy == hs
    assert copy is not hs
    assert copy.hashables == hs.hashables
    assert copy.unhashables == hs.unhashables
    lcopy = sorted(copy, key=repr)
    lhs = sorted(hs, key=repr)
    for elemcopy, elemhs in zip(lcopy, lhs):
        assert elemcopy == elemhs


def test_EveryHybridSet_clear(EveryHybridSet):
    hs = EveryHybridSet([3, 4, {5, 6}])
    hs.clear()
    hs == EveryHybridSet()


def test_HybridSet_add_unhashable_as_reference():
    hs = HybridSet()
    l = [0]
    hs.add(l)
    l.append(1)
    assert [0] not in hs
    assert [0, 1] in hs
    assert l in hs


def test_HybridCache_add_unhashable_as_copy():
    hc = HybridCache()
    l = [0]
    hc.add(l)
    l.append(1)
    assert [0] in hc
    assert [0, 1] not in hc
    assert l not in hc


def test_HybridCache_add_unhashable_as_deepcopy():
    hc = HybridCache()
    l = [0]
    l2 = [1]
    l.append(l2)
    hc.add(l)
    l2.append(2)
    assert l == [0, [1, 2]]
    assert [0, [1]] in hc
    assert [0, [1], 1] not in hc
    assert l not in hc

