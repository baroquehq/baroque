import collections
from baroque.entities.reactor import Reactor
from baroque.entities.eventtype import EventType


class ReactorsBag:
    """A type-aware collection of reactors."""

    def __init__(self):
        self.reactors = list()

    def run(self, reactor):
        """Adds a reactor to this bag.

        Args:
            reactor (:obj:`baroque.entities.reactor.Reactor`): the reactor to be added

        Raises:
            `AssertionError`: when the supplied arg is not a :obj:`baroque.entities.reactor.Reactor` instance

        """
        assert isinstance(reactor, Reactor)
        if reactor not in self.reactors:
            self.reactors.append(reactor)
        return reactor

    def remove(self, reactor):
        """Removes a reactor from this bag.

        Args:
            reactor (:obj:`baroque.entities.reactor.Reactor`): the reactor to be removed

        """
        self.reactors.remove(reactor)

    def remove_all(self):
        """Removes all reactors from this bag."""
        self.reactors = list()

    def count(self):
        """Tells how many reactors are in this bag.

        Returns:
            int

        """
        return len(self)

    def trigger(self, reactor):
        """Alias for `baroque.datastructures.bags.ReactorBag.run` method

        Args:
            reactor (:obj:`baroque.entities.reactor.Reactor`): the reactor to be added

        Raises:
            `AssertionError`: when the supplied arg is not a :obj:`baroque.entities.reactor.Reactor` instance

        """
        return self.run(reactor)

    def __contains__(self, item):
        return item in self.reactors

    def __iter__(self):
        return (r for r in self.reactors)

    def __len__(self):
        return len(self.reactors)

    def __repr__(self):
        return str(self.reactors)


class EventTypesBag:
    """A type-aware collection of event types

    Args:
        eventtypes (collection, optional): collection of :obj:`baroque.entities.eventtypes.EventType` items.

    """
    def __init__(self, eventtypes=None):
        self.types = set()
        if eventtypes is not None:
            self.add(eventtypes)

    def add(self, eventtypes):
        """Adds a collection of eventtypes to this bag.

        Args:
            `list` of (:obj:`baroque.entities.eventtypes.EventType`): the event types to be added

        Raises:
            `AssertionError`: when the supplied arg is not a collection or its items are not :obj:`baroque.entities.eventtypes.EventType` instances or :obj:`baroque.entities.eventtypes.EventType` subclasses 

        """
        assert not isinstance(eventtypes, str)
        assert isinstance(eventtypes, collections.Iterable)
        assert all([isinstance(et, EventType) or type(et) == type
                    for et in eventtypes])
        self.types.update(set([type(et) for et in eventtypes]))

    def __len__(self):
        return len(self.types)

    def __iter__(self):
        return (et for et in self.types)

    def __contains__(self, item):
        return type(item) in self.types
