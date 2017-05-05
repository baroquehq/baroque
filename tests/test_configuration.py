import pytest
from baroque import Baroque, EventType
from baroque.defaults.config import DEFAULT_CONFIG as cfg
from baroque.exceptions.eventtypes import UnregisteredEventTypeError, \
    InvalidEventSchemaError
from baroque.exceptions.topics import UnregisteredTopicError
from baroque.entities.reactor import Reactor
from baroque.entities.event import Event
from baroque.entities.topic import Topic
from baroque.defaults.eventtypes import GenericEventType, MetricEventType
from baroque.defaults.reactors import ReactorFactory
from baroque.persistence.backend import PersistenceBackend


class FakeEventType(EventType):
    def __init__(self, owner=None):
        EventType.__init__(self,
                           '{}',
                           description='fake',
                           owner=owner)


class FakePersistenceBackend(PersistenceBackend):
    def __init__(self):
        self._events = list()

    def create(self, event):
        self._events.append(event)

    def __len__(self):
        return len(self._events)


def test_exception_bubbling():
    # do propagate
    cfg['reactors']['propagate_exceptions'] = True
    brq = Baroque()
    brq.config = cfg

    def reaction_raising_error(evt):
        raise FileNotFoundError()

    r = Reactor(reaction_raising_error)
    brq.on(GenericEventType()).run(r)
    with pytest.raises(FileNotFoundError):
        brq.publish(Event(GenericEventType()))
        pytest.fail()

    # do not propagate
    cfg['reactors']['propagate_exceptions'] = False
    brq = Baroque()
    brq.config = cfg

    brq.on(GenericEventType()).run(r)
    try:
        brq.publish(Event(GenericEventType()))
    except FileNotFoundError:
        pytest.fail()


def test_ignore_unregistered_eventtypes():
    # do ignore
    cfg['eventtypes']['ignore_unregistered'] = True
    brq = Baroque()
    brq.config = cfg
    try:
        brq.publish(Event(GenericEventType()))
    except UnregisteredEventTypeError:
        pytest.fail()

    # do not ignore
    cfg['eventtypes']['ignore_unregistered'] = False
    brq = Baroque()
    brq.config = cfg
    with pytest.raises(UnregisteredEventTypeError):
        brq.publish(Event(FakeEventType()))
        pytest.fail()


def test_preregistered_eventtypes():
    fake = 'tests.test_configuration.FakeEventType'
    cfg['eventtypes']['pre_registered'] = [fake]
    brq = Baroque()
    assert FakeEventType() in brq.eventtypes


def test_validate_schema():
    cfg['eventtypes']['pre_registered'] = ['baroque.defaults.eventtypes.MetricEventType']
    brq = Baroque()
    brq.config = cfg
    et = MetricEventType()
    event = Event(et, payload=dict(a=1, b=2))

    # do not validate
    cfg['events']['validate_schema'] = False
    brq.config = cfg
    try:
        brq.publish(event)
    except InvalidEventSchemaError:
        pytest.fail()

    # do validate
    cfg['events']['validate_schema'] = True
    with pytest.raises(InvalidEventSchemaError):
        brq.publish(event)


def test_register_on_binding():
    # do register topics upon reactor binding
    cfg['topics']['register_on_binding'] = True
    brq = Baroque()
    brq.config = cfg
    t = Topic('test-topic', [])
    assert len(brq.topics) == 0
    brq.on_topic_run(t, ReactorFactory.stdout())
    assert len(brq.topics) == 1

    # do not register topics upon reactor binding: throw an exception
    cfg['topics']['register_on_binding'] = False
    brq = Baroque()
    brq.config = cfg
    with pytest.raises(UnregisteredTopicError):
        brq.on_topic_run(t, ReactorFactory.stdout())


def test_persist():
    # persist events
    brq = Baroque()
    cfg['eventtypes']['ignore_unregistered'] = True
    cfg['eventtypes']['pre_registered'] = ['baroque.defaults.eventtypes.GenericEventType']
    cfg['topics']['register_on_binding'] = True
    cfg['events']['persist'] = True
    brq.config = cfg
    evt1 = Event(GenericEventType())
    assert len(brq._persistance_backend) == 0
    brq.publish(evt1)
    assert len(brq._persistance_backend) == 1
    assert evt1 in brq._persistance_backend

    evt2 = Event(GenericEventType())
    t = brq.topics.new('test-topic',
                       eventtypes=[MetricEventType(), GenericEventType()])
    assert len(brq._persistance_backend) == 1
    brq.publish_on_topic(evt2, t)
    assert len(brq._persistance_backend) == 2
    assert evt2 in brq._persistance_backend

    # do not persist events
    brq = Baroque()
    cfg['events']['persist'] = False
    brq.config = cfg
    evt3 = Event(GenericEventType())
    assert len(brq._persistance_backend) == 0
    brq.publish(evt3)
    assert len(brq._persistance_backend) == 0

    evt4 = Event(GenericEventType())
    t = brq.topics.new('test-topic',
                       eventtypes=[MetricEventType(), GenericEventType()])
    assert len(brq._persistance_backend) == 0
    brq.publish_on_topic(evt4, t)
    assert len(brq._persistance_backend) == 0


def test_persistence_backend():
    brq = Baroque()

    # test we're actually using the claimed persistence backend
    cfg['events']['persist'] = True
    cfg['events']['persistence_backend'] = 'tests.test_configuration.FakePersistenceBackend'
    brq.config = cfg

    pb = brq._persistance_backend
    assert len(pb) == 0
    evt = Event(GenericEventType())
    brq.publish(evt)
    assert len(pb) == 1
    assert evt in pb
