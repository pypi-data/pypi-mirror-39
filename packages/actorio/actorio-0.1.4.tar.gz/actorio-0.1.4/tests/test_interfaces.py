from typing import Type

import pytest

from actorio.interfaces import Identified


@pytest.fixture(params=[Identified])
def identified_class(request) -> Type[Identified]:
    return request.param


def test_identified_simple(identified_class):
    o = identified_class(identifier="abcd")
    assert o.identifier == "abcd"


def test_has_same_identifier(identified_class):
    i1 = identified_class()
    i2 = identified_class()
    assert i1.has_same_identifier(i1)
    assert not i1.has_same_identifier(i2)


def test_two_identified_objects_with_same_identifier_have_same_hash(identified_class):
    i1 = identified_class()
    i2 = identified_class(identifier=i1.identifier)

    assert hash(i1) == hash(i2)


def test_has_same_hash_as_identifier(identified_class):
    o = identified_class()
    assert hash(o) == hash(o.identifier)


def test_identified_objects_are_findable_in_sets(identified_class):
    o1 = identified_class()
    o2 = identified_class(identifier=o1.identifier)

    s = set()
    s.add(o1)
    assert o2 in s


def test_identified_objects_are_findable_in_dicts(identified_class):
    o1 = identified_class()
    o2 = identified_class(identifier=o1.identifier)
    sentinel = object()

    d = dict()
    d[o1] = sentinel
    assert o2 in d
    assert d[o2] == sentinel

def test_identifier_equality(identified_class):
    o1 = identified_class()
    o2 = identified_class(identifier=o1.identifier)
    assert o1 == o2

def test_identifier_inequality(identified_class):
    o1 = identified_class()
    o2 = identified_class()
    assert o1 != o2

def test_identifier_inequality_with_not_identified(identified_class):
    o1 = identified_class()
    assert o1 != object()