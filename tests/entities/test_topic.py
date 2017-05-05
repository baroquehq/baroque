import pytest
from baroque.entities.topic import Topic
from baroque.defaults.eventtypes import GenericEventType, DataOperationEventType


def test_constructor_failures():
    with pytest.raises(TypeError):
        Topic()
        pytest.fail()
    with pytest.raises(AssertionError):
        Topic(123, [])
        pytest.fail()
    with pytest.raises(AssertionError):
        Topic('test', None)
        pytest.fail()
    with pytest.raises(AssertionError):
        Topic('test', 'abc')
        pytest.fail()
    with pytest.raises(AssertionError):
        Topic('test', ['abc'])
        pytest.fail()
    with pytest.raises(AssertionError):
        Topic('test', [], tags='abc')
        pytest.fail()


def test_constructor():
    t = Topic('test', [], description='this is a test topic', owner='me')
    assert t.id is not None
    assert len(t.eventtypes) == 0
    assert t.owner is not None
    assert len(t.tags) == 0
    assert t.timestamp is not None
    ets = [GenericEventType(), DataOperationEventType()]
    t = Topic('test', ets,
              description='this is a test topic', owner='me',
              tags=['x', 'y'])
    assert len(t.eventtypes) == 2
    assert len(t.tags) == 2


def test_print():
    print(Topic('test', []))
