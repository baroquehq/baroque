import pytest
from baroque.datastructures.registries import EventTypesRegistry
from baroque.defaults.eventtypes import GenericEventType, MetricEventType, \
    DataOperationEventType


def test_register():
    reg = EventTypesRegistry()
    assert reg.count() == 0
    reg.register(GenericEventType())  # with a concrete instance
    assert reg.count() == 1
    reg.register(GenericEventType)   # with a type object
    assert reg.count() == 1
    reg.register(MetricEventType())
    assert reg.count() == 2
    with pytest.raises(AssertionError):
        reg.register('not-a-reactor')
        pytest.fail()


def test_remove():
    reg = EventTypesRegistry()
    reg.register(GenericEventType())
    reg.register(MetricEventType())
    reg.register(DataOperationEventType())
    assert reg.count() == 3
    reg.remove(DataOperationEventType())  # with a concrete instance
    assert reg.count() == 2
    assert DataOperationEventType() not in reg.registered_types
    reg.remove(GenericEventType)  # with a type object
    assert reg.count() == 1
    assert DataOperationEventType() not in reg.registered_types
    with pytest.raises(AssertionError):
        reg.remove(123)
        pytest.fail()


def test_remove_all():
    reg = EventTypesRegistry()
    reg.register(GenericEventType())
    reg.register(MetricEventType())
    reg.register(DataOperationEventType())
    assert reg.count() == 3
    reg.remove_all()
    assert reg.count() == 0


def test_magic_len():
    reg = EventTypesRegistry()
    reg.register(GenericEventType())
    assert len(reg) == 1


def test_magic_contains():
    reg = EventTypesRegistry()
    reg.register(GenericEventType())
    assert GenericEventType() in reg
    assert MetricEventType() not in reg


def test_print():
    print(EventTypesRegistry())
