from typing import Type

import pytest

from actorio.interfaces import Identified


@pytest.fixture(params=[Identified])
def identified_class(request) -> Type[Identified]:
    return request.param


def test_identified_simple(identified_class):
    o = identified_class(identifier="abcd")
    assert o.identifier == "abcd"
