import pytest
from baroque.persistence.inmemory import DictBackend
from baroque.entities.event import Event
from baroque.defaults.eventtypes import GenericEventType, MetricEventType


def test_create():
    bck = DictBackend()
    assert len(bck._db) == 0

    # adding nothing leads to an exception
    with pytest.raises(AssertionError):
        bck.create(None)
        pytest.fail()

    # adding events with null id
    evt0 = Event(GenericEventType(), dict(foo='bar'))
    evt0.id = None
    bck.create(evt0)
    assert len(bck._db) == 0

    # fresh add
    evt1 = Event(GenericEventType(), dict(foo='bar'))
    bck.create(evt1)
    assert len(bck._db) == 1

    # adding twice the same event is idempotent
    bck.create(evt1)
    assert len(bck._db) == 1


def test_read():
    bck = DictBackend()
    evt = Event(GenericEventType(), dict(foo='bar'))
    bck.create(evt)
    result = bck.read(evt.id)
    assert result == evt

    # reading nothing
    assert bck.read('unexistent') is None


def test_update():
    bck = DictBackend()
    evt = Event(GenericEventType(), dict(foo='bar'))
    bck.create(evt)
    assert len(bck._db) == 1

    # updating nothing leads to an exception
    with pytest.raises(AssertionError):
        bck.update(None)
        pytest.fail()

    # updating events with null id is idempotent
    former_evt0_id = evt.id
    evt.id = None
    bck.update(evt)
    assert len(bck._db) == 1
    result = bck.read(former_evt0_id)
    assert result == evt  # event was unchanged
    assert result.owner is None

    # actual update
    evt.owner = 'me'
    bck.update(evt)
    assert len(bck._db) == 1
    result = bck.read(former_evt0_id)
    assert result.owner == 'me'


def test_delete():
    bck = DictBackend()
    evt1 = Event(GenericEventType(), dict(foo='bar'))
    evt2 = Event(MetricEventType(), dict(bar='baz'))
    bck.create(evt1)
    bck.create(evt2)
    assert len(bck._db) == 2

    # deleting nothing
    bck.delete(None)
    assert len(bck._db) == 2

    # deleting an actual event
    bck.delete(evt1.id)
    assert len(bck._db) == 1
    result = bck.read(evt2.id)
    assert result == evt2


def test_magic_methods():
    bck = DictBackend()
    evt1 = Event(GenericEventType(), dict(foo='bar'))
    evt2 = Event(MetricEventType(), dict(bar='baz'))
    bck.create(evt1)
    bck.create(evt2)

    assert len(bck) == 2
    assert evt1 in bck
    assert evt2 in bck
    for event_id in bck:
        assert isinstance(bck[event_id], Event)

    keys = bck.keys()
    assert len(keys) == 2
    assert evt1.id in keys
    assert evt2.id in keys

    values = bck.values()
    assert len(values) == 2
    assert evt1 in values
    assert evt2 in values

    bck.clear()
    assert len(bck) == 0


def test_print():
    print(DictBackend())
