import pytest
from baroque.entities.eventtype import EventType
from baroque.entities.event import Event
from baroque.defaults.eventtypes import GenericEventType


def test_constructor_failures():
    with pytest.raises(AssertionError):
        EventType(None)
        pytest.fail()
    with pytest.raises(AssertionError):
        EventType(123)
        pytest.fail()


def test_constructor():
    et = EventType('{}', description='hello', owner=1234)
    assert et.jsonschema == '{}'
    assert not et.tags
    assert et.owner == 1234
    assert et.description == 'hello'


def test_md5():
    et = EventType('{}', description='hello', owner=1234)
    assert et.md5() is not None


def test_validate():
    jsonschema = '''{
        "type": "object",
        "properties": {
            "payload": {
                "type": "object",
                "properties": {
                    "foo": { "type": "string" },
                    "bar": { "type": "number" }
                },
                "required": ["foo", "bar"]
            }
        },
        "required": ["payload"]
    }'''
    eventtype = EventType(jsonschema)

    # event is conforming to JSON schema of its type
    event = Event(eventtype, payload=dict(foo='value', bar=123))
    assert EventType.validate(event, eventtype)

    # event is of another type
    event = Event(GenericEventType(), payload=dict(foo='value', bar=123))
    assert not EventType.validate(event, eventtype)

    # event is of the same type but not conforming
    event = Event(eventtype, payload=dict(x=1, y=2))
    assert not EventType.validate(event, eventtype)


def test_print():
    print(EventType('{}'))

