import pytest
from baroque.entities.event import Event, EventStatus
from baroque.defaults.eventtypes import GenericEventType


def test_constructor_failures():
    with pytest.raises(TypeError):
        Event()
        pytest.fail()
    with pytest.raises(AssertionError):
        Event(None)
        pytest.fail()
    with pytest.raises(AssertionError):
        Event(123)
        pytest.fail()
    with pytest.raises(AssertionError):
        Event(GenericEventType(), payload=123)
        pytest.fail()


def test_constructor():
    e = Event(GenericEventType(), payload=dict(a=1, b=2), description='hello',
              owner=1234)
    assert isinstance(e.type, GenericEventType)
    assert e.id is not None
    assert not e.tags
    assert e.status == EventStatus.UNPUBLISHED
    assert e.timestamp is not None


def test_constructor_with_type_objects():
    e1 = Event(GenericEventType(), payload=dict(a=1, b=2), description='hello',
               owner=1234)
    e2 = Event(GenericEventType, payload=dict(a=1, b=2), description='hello',
               owner=1234)
    assert isinstance(e1.type, GenericEventType)
    assert isinstance(e2.type, GenericEventType)


def test_touch():
    e = Event(GenericEventType(), payload=dict(a=1, b=2), description='hello',
              owner=1234)
    ts1 = e.timestamp
    e = Event(GenericEventType(), payload=dict(a=1, b=2), description='hello',
              owner=1234)
    ts2 = e.timestamp
    assert ts2 > ts1


def test_md5():
    e = Event(GenericEventType(), payload=dict(a=1, b=2), description='hello',
              owner=1234)
    assert e.md5() is not None


def test_print():
    print(Event(GenericEventType()))
