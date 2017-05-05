import pytest
from baroque import Baroque, EventType
from baroque.defaults.config import DEFAULT_CONFIG
from baroque.entities.reactor import Reactor
from baroque.entities.topic import Topic
from baroque.datastructures.counters import EventCounter
from baroque.datastructures.bags import ReactorsBag
from baroque.datastructures.registries import EventTypesRegistry, \
    ReactorsRegistry, TopicsRegistry
from baroque.entities.event import Event, EventStatus
from baroque.defaults.eventtypes import GenericEventType, MetricEventType
from baroque.defaults.reactors import ReactorFactory
from baroque.exceptions.eventtypes import InvalidEventSchemaError
from baroque.exceptions.topics import UnregisteredTopicError
from baroque.utils.importer import class_from_dotted_path


class Box:
    reacted_on_test_eventtype = False
    reacted_on_any_eventtype = False
    called = False

    def any_eventtype(self):
        self.reacted_on_any_eventtype = True

    def test_eventtype(self):
        self.reacted_on_test_eventtype = True

    def mark_called(self):
        self.called = True


def test_on():
    brq = Baroque()
    eventtype = GenericEventType()
    result = brq.on(eventtype)
    assert isinstance(result, ReactorsBag)

    brq.reactors.registered_types[type(eventtype)] = ReactorsBag()
    result = brq.on(eventtype)
    assert isinstance(result, ReactorsBag)


def test_on_any_event_run():
    brq = Baroque()
    assert len(brq.reactors.jolly_bag) == 0
    r = ReactorFactory.stdout()
    result = brq.on_any_event_run(r)
    assert isinstance(result, Reactor)
    assert r in brq.reactors.jolly_bag


def test_reactors():
    brq = Baroque()
    result = brq.reactors
    assert isinstance(result, ReactorsRegistry)


def test_events():
    brq = Baroque()
    result = brq.events
    assert isinstance(result, EventCounter)


def test_eventtypes():
    brq = Baroque()
    result = brq.eventtypes
    assert isinstance(result, EventTypesRegistry)


def test_topics():
    brq = Baroque()
    result = brq.topics
    assert isinstance(result, TopicsRegistry)


def test_reset():
    brq = Baroque()

    class MyEventType1(EventType):
        def __init__(self, owner=None):
            EventType.__init__(self,
                               '''{
                                 "$schema": "http://json-schema.org/draft-04/schema#"
                               }''',
                               description='test',
                               owner=owner)

    class MyEventType2(EventType):
        def __init__(self, owner=None):
            EventType.__init__(self,
                               '''{
                                 "$schema": "http://json-schema.org/draft-04/schema#"
                               }''',
                               description='test',
                               owner=owner)

    eventtype1 = MyEventType1()
    eventtype2 = MyEventType2()
    brq.on(eventtype1).run(ReactorFactory.stdout())
    brq.on(eventtype2).run(ReactorFactory.stdout())
    brq.publish(Event(eventtype1))
    brq.publish(Event(eventtype2))
    assert brq.events.count_all() == 2
    assert brq.eventtypes.count() == 2 + len(DEFAULT_CONFIG['eventtypes']['pre_registered'])
    assert len(brq.reactors.registered_types) == 2
    brq.reset()
    assert brq.events.count_all() == 0
    assert brq.eventtypes.count() == 0
    assert len(brq.reactors.registered_types) == 0


def test_publish():
    # using a databox to keep state and make assertions
    box = Box()
    r1 = ReactorFactory.call_function(box, 'test_eventtype')
    r2 = ReactorFactory.call_function(box, 'any_eventtype')
    brq = Baroque()
    eventtype = GenericEventType()
    brq.on(eventtype).run(r1)
    brq.on_any_event_run(r2)
    evt = Event(eventtype)

    assert not box.reacted_on_test_eventtype
    assert not box.reacted_on_any_eventtype
    assert brq.events.count_all() == 0
    brq.publish(evt)
    assert box.reacted_on_test_eventtype
    assert box.reacted_on_any_eventtype
    assert brq.events.count_all() == 1
    assert evt.status == EventStatus.PUBLISHED

    with pytest.raises(AssertionError):
        brq.publish('not-an-event')
        pytest.fail()


def test_fire():
    # using a databox to keep state and make assertions
    box = Box()
    r1 = ReactorFactory.call_function(box, 'test_eventtype')
    r2 = ReactorFactory.call_function(box, 'any_eventtype')
    brq = Baroque()
    eventtype = GenericEventType()
    brq.on(eventtype).run(r1)
    brq.on_any_event_run(r2)
    evt = Event(eventtype)

    assert not box.reacted_on_test_eventtype
    assert not box.reacted_on_any_eventtype
    assert brq.events.count_all() == 0
    brq.fire(evt)
    assert box.reacted_on_test_eventtype
    assert box.reacted_on_any_eventtype
    assert brq.events.count_all() == 1


def test_count_event():
    brq = Baroque()
    eventtype = GenericEventType()
    evt = Event(eventtype, payload=dict())
    assert brq.events.count(eventtype) == 0
    assert brq.events.count_all() == 0
    brq._count_event(evt)
    assert brq.events.count(eventtype) == 1
    assert brq.events.count_all() == 1


def test_persist_event():
    brq = Baroque()
    assert len(brq._persistance_backend) == 0
    evt = Event(GenericEventType(), payload=dict(test=123))
    brq._persist_event(evt)
    assert len(brq._persistance_backend) == 1
    assert evt in brq._persistance_backend


def test_update_event_status():
    eventtype = GenericEventType()
    evt = Event(eventtype, payload=dict())
    assert evt.status == EventStatus.UNPUBLISHED
    brq = Baroque()
    brq._update_event_status(evt)
    assert evt.status == EventStatus.PUBLISHED


def test_load_preregistered_eventtypes():
    brq = Baroque()
    assert brq.eventtypes.count() == len(DEFAULT_CONFIG['eventtypes']['pre_registered'])


def test_load_persistence_backend():
    brq = Baroque()
    brq._load_persistence_backend()
    klass = class_from_dotted_path(DEFAULT_CONFIG['events']['persistence_backend'])
    assert isinstance(brq._persistance_backend, klass)


def test_validate_event_schema():
    brq = Baroque()
    et = MetricEventType()
    event_valid = Event(et,
                      payload={'metric': 'temperature',
                               'value': 56.7793,
                               'timestamp': '2017-02-15T13:56:09Z'})
    event_invalid = Event(et, payload={'metric': 'temperature'})

    # Publish invalid event
    with pytest.raises(InvalidEventSchemaError):
        brq.publish(event_invalid)
        pytest.fail()

    # Publish valid event
    try:
        brq.publish(event_valid)
    except InvalidEventSchemaError:
        pytest.fail()


def test_on_topic_run():
    brq = Baroque()
    t1 = Topic('test-topic1', eventtypes=[MetricEventType(), GenericEventType()])
    assert len(brq.topics.topics) == 0
    brq.on_topic_run(t1, ReactorFactory.stdout())
    assert len(brq.topics.topics) == 1
    assert len(brq.topics.topics[t1]) == 1

    # one more reactor on the same topic
    brq.on_topic_run(t1, ReactorFactory.stdout())
    assert len(brq.topics.topics) == 1
    assert len(brq.topics.topics[t1]) == 2

    # let's register another topic
    t2 = Topic('test-topic2', eventtypes=[MetricEventType()])
    brq.on_topic_run(t2, ReactorFactory.stdout())
    assert len(brq.topics.topics) == 2
    assert len(brq.topics.topics[t1]) == 2
    assert len(brq.topics.topics[t2]) == 1


def test_publish_on_topic():
    brq = Baroque()
    t = brq.topics.new('test-topic1',
                       eventtypes=[MetricEventType(), GenericEventType()])

    evt = Event(MetricEventType())

    # trying to publish events to an unregistered topic
    with pytest.raises(UnregisteredTopicError):
        brq.publish_on_topic(evt, Topic('unregistered', []))
        pytest.fail()

    # using a box to keep state and make assertions
    box = Box()
    brq.on_topic_run(t, ReactorFactory.call_function(box, 'mark_called'))
    assert not box.called
    assert brq.events.count_all() == 0
    brq.publish_on_topic(evt, t)
    assert box.called
    assert brq.events.count_all() == 1
    assert evt.status == EventStatus.PUBLISHED


def test_print():
    print(Baroque())
