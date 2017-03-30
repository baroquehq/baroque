from baroque.defaults import eventtypes
from baroque import Event, EventType


def test_generic_eventtype():
    et = eventtypes.GenericEventType()
    event = Event(et, payload=dict(test='value'))
    assert EventType.validate(event, et)

    # test printing
    print(et)


def test_state_transition_eventtype():
    # validation failure
    et = eventtypes.StateTransitionEventType()
    event = Event(et)
    assert not EventType.validate(event, et)

    # validation OK
    event = Event(et,
                  payload={'from_status': 'A',
                           'to_status': 'B',
                           'trigger': 'system_failure',
                           'meta': {
                               'key1': 'val1',
                               'key2': 'val2'
                           }})
    assert EventType.validate(event, et)

    # test printing
    print(et)


def test_data_operation_eventtype():
    # validation failure
    et = eventtypes.DataOperationEventType()
    event = Event(et)
    assert not EventType.validate(event, et)

    # validation OK
    event = Event(et,
                  payload={'datum': {
                                'file': '/home/test.txt',
                                'char_position': 45
                            },
                           'operation': 'modify',
                           'timestamp': '2017-02-15T13:56:09Z',
                           'meta': {
                               'old_char': 'F',
                               'new_char': 'N'
                           }})
    assert EventType.validate(event, et)

    # test printing
    print(et)


def test_metric_eventtype():
    # validation failure
    et = eventtypes.MetricEventType()
    event = Event(et)
    assert not EventType.validate(event, et)

    # validation OK
    event = Event(et,
                  payload={'metric': 'temperature',
                           'value': 56.7793,
                           'timestamp': '2017-02-15T13:56:09Z'})
    assert EventType.validate(event, et)

    # test printing
    print(et)
