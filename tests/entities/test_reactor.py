import pytest
from baroque.entities.reactor import Reactor
from baroque.entities.event import Event
from baroque.defaults.eventtypes import GenericEventType


# reaction
def greet(event):
    print('hello')


# condition
def only_test_events(event):
    return 'test' in event.payload if event.payload is not None else False


def test_constructor_failures():
    with pytest.raises(TypeError):
        Reactor()
        pytest.fail()
    with pytest.raises(AssertionError):
        Reactor(None)
        pytest.fail()
    with pytest.raises(AssertionError):
        Reactor(123)
        pytest.fail()
    with pytest.raises(AssertionError):
        Reactor('test', condition=123)
        pytest.fail()


def test_constructor():
    r = Reactor(greet)
    assert r.reaction_function == greet
    assert r.condition_function is None
    assert r.last_reaction_timestamp is None
    assert r.id_last_event_reacted is None
    assert r.reactions_count == 0


def test_only_if():
    r = Reactor(greet)
    assert r.condition_function is None
    cond = lambda x: False
    r.only_if(cond)
    assert r.condition_function is not None
    with pytest.raises(AssertionError):
        r = Reactor(greet)
        r.only_if('not-a-function')
        pytest.fail()


def test_condition_met():
    r = Reactor(greet)
    evt = Event(GenericEventType(), payload=dict())
    # no condition set
    is_met = r._condition_met(evt)
    assert is_met
    # condition is not met
    r.only_if(only_test_events)
    is_met = r._condition_met(evt)
    assert not is_met
    # condition is met
    evt.payload['test'] = 'value'
    is_met = r._condition_met(evt)
    assert is_met


def test_react():
    r = Reactor(greet)
    evt = Event(GenericEventType())
    r.react(evt)
    assert r.count_reactions() == 1
    assert r.last_event_reacted() is not None
    assert r.last_reacted_on() is not None


def test_react_conditionally():
    r = Reactor(greet, condition=only_test_events)
    evt = Event(GenericEventType())
    # condition is not met
    r.react_conditionally(evt)
    assert r.count_reactions() == 0
    assert r.last_event_reacted() is None
    assert r.last_reacted_on() is None
    # condition is met
    evt.payload = {'test': 'value'}
    r.react_conditionally(evt)
    assert r.count_reactions() == 1
    assert r.last_event_reacted() is not None
    assert r.last_reacted_on() is not None


def test_print():
    print(Reactor(lambda x: 1))
