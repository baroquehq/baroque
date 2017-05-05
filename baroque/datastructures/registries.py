import collections
from . import bags
from baroque.entities.event import Event
from baroque.entities.eventtype import EventType
from baroque.entities.reactor import Reactor
from baroque.entities.topic import Topic


class EventTypesRegistry:
    """Interface adapter to an event bag."""
    def __init__(self):
        self.registered_types = set()

    def register(self, eventtype):
        """Adds an event type to this registry.

        Args:
            eventtype (:obj:`baroque.entities.eventtypes.EventType` instance or `type` object): the event type to be added

        Raises:
            `AssertionError`: when argument is not an :obj:`baroque.entities.eventtypes.EventType` instance or a `type` object

        """
        if type(eventtype) == type:
            eventtype = eventtype()
        assert isinstance(eventtype, EventType)
        self.registered_types.add(type(eventtype))

    def count(self):
        """Tells how many event types are registered on this registry

        Returns:
            int

        """
        return len(self.registered_types)

    def remove(self, eventtype):
        """Removes an event type from this registry

        Args:
            eventtype (:obj:`baroque.entities.eventtypes.EventType` instance or `type` object): the event type to be removed

        Raises:
            `AssertionError`: when argument is not an :obj:`baroque.entities.eventtypes.EventType` instance or a `type` object

        """
        if type(eventtype) == type:
            eventtype = eventtype()
        assert isinstance(eventtype, EventType)
        self.registered_types.discard(type(eventtype))

    def remove_all(self):
        """Removes all event types from this registry."""
        self.registered_types = set()

    # --- magic methods ---

    def __contains__(self, eventtype):
        return type(eventtype) in self.registered_types

    def __len__(self):
        return len(self.registered_types)

    def __repr__(self):
        return '<{}.{} - event types: {}>'.format(
            __name__,
            self.__class__.__name__,
            ', '.join([t.__name__ for t in self.registered_types]) or 'None')


class ReactorsRegistry:
    """A tracker for reaactors. Each reactor is intended to be executed when
    a certain type of events is fired: the reactors-eventtypes relationship is
    stored internally using a dict of bag datastructures.
    
    Some reactors must be executed upon any event firing: these are stored 
    internally into a "jolly bag".
       
    """
    def __init__(self):
        self.registered_types = dict()
        self.jolly_bag = bags.ReactorsBag()
        self.evttypreg = EventTypesRegistry()

    def get_event_types_registry(self):
        """Gives the encapsulated event type registry

        Returns:
            :obj:`baroque.registries.EventTypeRegistry`

        """
        return self.evttypreg

    def get_or_create_bag(self, eventtype):
        """Gives the reactors bag associated to the specified event type, or
        creates one in case it does not exist yet.

        Args:
            eventtype (:obj:`baroque.entities.eventtype.EventType` instance or `type` object): the associated event type

        Returns:
            :obj:`baroque.datastructures.bags.ReactorsBag`
            
        Raises:
            `AssertionError`: when the supplied event type is not a :obj:`baroque.entities.eventtype.EventType` instance or a `type` object

        """
        if type(eventtype) == type:
            eventtype = eventtype()
        assert isinstance(eventtype, EventType)
        t = type(eventtype)
        if t not in self.registered_types:
            self.registered_types[t] = bags.ReactorsBag()
        self.evttypreg.register(eventtype)
        return self.registered_types[t]

    def get_bag(self, eventtype):
        """Gives the reactors bag associated to the specified event type.

        Args:
            eventtype (:obj:`baroque.entities.eventtype.EventType`): the associated event type

        Returns:
            :obj:`baroque.datastructures.bags.ReactorsBag`
            
        Raises:
            `AssertionError`: when the supplied event type is not a :obj:`baroque.entities.eventtype.EventType` instance or a `type` object

        """
        if type(eventtype) == type:
            eventtype = eventtype()
        t = type(eventtype)
        if t in self.registered_types:
            return self.registered_types[t]
        return bags.ReactorsBag()

    def get_jolly_bag(self):
        """Gives the encapsulated bag that contains reactors to be executed
        upon any event firing.

        Returns:
            :obj:`baroque.registries.EventTypeRegistry`

        """
        return self.jolly_bag

    def to(self, eventtype):
        """Gives the encapsulated bag that contains reactors to be executed
        upon the firing of events of the supplied type.

        Args:
            eventtype (:obj:`baroque.entities.eventtype.EventType`): the associated event type

        Returns:
            :obj:`baroque.datastructures.bags.ReactorsBag`

        """
        return self.get_bag(eventtype)

    def to_any_event(self):
        """Gives the encapsulated jolly bag, containing reactors to be executed
        upon the firing of any event.

        Returns:
            :obj:`baroque.datastructures.bags.ReactorsBag`

        """
        return self.get_jolly_bag()

    def remove_all(self):
        """Clears the contents of all the encapsulated reactor bags."""
        self.registered_types = dict()
        self.jolly_bag = bags.ReactorsBag()

    # --- magic methods ---

    def __repr__(self):
        return '<{}.{} - event types reactors: {} - jolly reactors: {}>'.format(
            __name__,
            self.__class__.__name__,
            ','.join(["'{}': {}".format(k, v) for k, v in self.registered_types.items()]) or 'None',
            ','.join(map(str, self.jolly_bag)))


class TopicsRegistry:
    """A tracker for reactors to be executed upong event firing of events on
    specified topics: the reactors-topics relationship is stored internally 
    using a dict"""
    def __init__(self):
        self.topics = dict()

    def register(self, topic):
        """Adds a topic to the registry.
    
        Args:
            topic (:obj:`baroque.entities.topic.Topic`): the topic to be added
    
        """
        assert topic is not None
        assert isinstance(topic, Topic)
        if topic not in self.topics:
            self.topics[topic] = list()

    def new(self, name, eventtypes, **kwargs):
        """Creates a new topic, adds it to the registry and returns it.
    
        Args:
            name (str): name of the new topic
        eventtypes (collection): the :obj:`baroque.entities.eventtype.EventType` objects that characterize the new topic
            **kwargs: positional arguments for `Topic` instantiation
    
        Returns:
            :obj:`baroque.entities.topic.Topic`
    
        """
        topic = Topic(name, eventtypes, **kwargs)
        self.register(topic)
        return topic

    def count(self):
        """Tells how many topics are registered.
    
        Returns:
            int
    
        """
        return len(self.topics)

    def remove(self, topic):
        """Removes a topic from the registry.
    
        Args:
            topic (:obj:`baroque.entities.topic.Topic`): the topic to be removed
    
        """
        self.topics.pop(topic)

    def remove_all(self):
        """Clears all the topics from the registry."""
        self.topics.clear()

    def of(self, owner):
        """Returns the topics belonging to the supplied owner
    
        Args:
            owner (str): the topics owner
    
        Returns:
            `list` of :obj:`baroque.entities.topic.Topic` items
    
        """
        assert owner is not None
        return [t for t in self.topics if t.owner == owner]

    def with_id(self, id):
        """Returns the topic with the specified identifier
    
        Args:
            id (str): the topic id
    
        Returns:
            :obj:`baroque.entities.topic.Topic`
    
        """
        assert id is not None
        for t in self.topics:
            if t.id == id:
                return t
        return None

    def with_name(self, name):
        """Returns the topic with the specified name (exact string matching)
    
        Args:
            name (str): the topic name
    
        Returns:
            :obj:`baroque.entities.topic.Topic`
    
        """
        assert name is not None
        for t in self.topics:
            if t.name == name:
                return t
        return None

    def with_tags(self, tags):
        """Returns the topics marked by the specified tags.
    
        Args:
            tags (`set` of str items): the tag set
    
        Returns:
            `list` of :obj:`baroque.entities.topic.Topic` items
    
        Raises:
            `AssertionError`: when the supplied tag set is not an iterable
    
        """
        assert tags is not None
        assert not isinstance(tags, str)
        assert isinstance(tags, collections.Iterable)
        result = list()
        if len(tags) == 0:
            return result
        tags = set(tags)
        for topic in self.topics:
            if tags.issubset(topic.tags):
                result.append(topic)
        return result

    def on_topic_run(self, topic, reactor):
        """Binds the specified reactor to event firing on the specified topic.
    
        Args:
            topic (`:obj:`baroque.entities.topic.Topic`): the topic
            reactor (:obj:`baroque.entities.reactor.Reactor`): the reactor
    
        Raises:
            `AssertionError`: when any of the supplied args is of wrong type
    
        """
        assert isinstance(topic, Topic)
        assert isinstance(reactor, Reactor)
        if topic in self.topics:
            self.topics[topic].append(reactor)

    def publish_on_topic(self, event, topic):
        """Publishes an event on a tracked topic, executing all the reactors
         bound to that topic.
    
        Args:
            event (`:obj:`baroque.entities.event.Event`): the event to be published
            topic (`:obj:`baroque.entities.topic.Topic`): the target topic
    
        Raises:
            `AssertionError`: when any of the supplied args is of wrong type
    
        """
        assert isinstance(event, Event)
        assert isinstance(topic, Topic)

        # check if the eventtype of the event is registered on the topic
        if event.type not in topic.eventtypes:
            return

        # run all reactors associated to the topic
        for reactor in self.topics[topic]:
            reactor.react_conditionally(event)

    # --- magic methods ---

    def __len__(self):
        return len(self.topics)

    def __contains__(self, topic):
        return topic in self.topics

    def __iter__(self):
        return (t for t in self.topics)
