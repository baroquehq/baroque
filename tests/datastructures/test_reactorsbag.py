import pytest
from baroque.entities.reactor import Reactor
from baroque.datastructures.bags import ReactorsBag
from baroque.defaults.reactors import ReactorFactory


def test_run():
    r = ReactorFactory.stdout()
    bag = ReactorsBag()
    result = bag.run(r)
    assert result == r
    assert len(bag.reactors) == 1
    assert bag.reactors[0] == r
    with pytest.raises(AssertionError):
        bag.run('not-a-reactor')
        pytest.fail()


def test_count():
    r1 = ReactorFactory.stdout()
    r2 = ReactorFactory.stdout()
    r3 = ReactorFactory.stdout()
    bag = ReactorsBag()
    bag.run(r1)
    bag.run(r2)
    bag.run(r3)
    assert bag.count() == 3


def test_remove():
    r1 = ReactorFactory.stdout()
    r2 = ReactorFactory.stdout()
    r3 = ReactorFactory.stdout()
    bag = ReactorsBag()
    bag.run(r1)
    bag.run(r2)
    bag.run(r3)
    assert bag.count() == 3
    bag.remove(r2)
    assert bag.count() == 2
    assert r1 in bag.reactors
    assert r3 in bag.reactors


def test_remove_all():
    r1 = ReactorFactory.stdout()
    r2 = ReactorFactory.stdout()
    r3 = ReactorFactory.stdout()
    bag = ReactorsBag()
    bag.run(r1)
    bag.run(r2)
    bag.run(r3)
    assert bag.count() == 3
    bag.remove_all()
    assert bag.count() == 0


def test_magic_iter():
    r1 = ReactorFactory.stdout()
    r2 = ReactorFactory.stdout()
    r3 = ReactorFactory.stdout()
    bag = ReactorsBag()
    bag.run(r1)
    bag.run(r2)
    bag.run(r3)
    for item in bag:
        assert isinstance(item, Reactor)


def test_magic_len():
    r1 = ReactorFactory.stdout()
    r2 = ReactorFactory.stdout()
    r3 = ReactorFactory.stdout()
    bag = ReactorsBag()
    bag.run(r1)
    bag.run(r2)
    bag.run(r3)
    assert len(bag) == 3


def test_magic_contains():
    r1 = ReactorFactory.stdout()
    r2 = ReactorFactory.stdout()
    r3 = ReactorFactory.stdout()
    bag = ReactorsBag()
    bag.run(r1)
    bag.run(r3)
    assert r1 in bag
    assert r2 not in bag
    assert r3 in bag


def test_print():
    print(ReactorsBag())
