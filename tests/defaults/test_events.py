from baroque.defaults.events import EventFactory
from baroque.defaults.eventtypes import GenericEventType


def test_new():
    payload = dict(test='value')
    description = 'a test event'
    owner = 'me'
    evt = EventFactory.new(payload=payload, description=description, owner=owner)
    assert isinstance(evt.type, GenericEventType)
    assert evt.payload == payload
    assert evt.owner == owner
    assert evt.description == description
