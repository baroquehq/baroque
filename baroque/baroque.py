from .constants import BAROQUE_VERSION
from .datastructures import registries, counters
from .utils import configreader, importer
from .entities.eventtype import EventType
from .entities.event import Event
from .exceptions.eventtypes import UnregisteredEventTypeError, \
    InvalidEventSchemaError
from .exceptions.topics import UnregisteredTopicError


class Baroque:
    """The Baroque event broker class.

    Note:
        When no configuration file is specified, the default configuration
        is loaded.

    Args:
        configfile (str, optional): Path to the configuration YML file.

    Raises:
        :obj:`baroque.exceptions.configuration.ConfigurationNotFoundError`: when the supplied filepath is not a regular file
        :obj:`baroque.exceptions.configuration.ConfigurationParseError`: when the supplied file cannot be parsed

    """

    def __init__(self, configfile=None):
        self.config = configreader.read_config_or_default(configfile)
        self.reactreg = registries.ReactorsRegistry()
        self.topicsreg = registries.TopicsRegistry()
        self.evtcounter = counters.EventCounter()
        self._load_preregistered_eventtypes()
        self._load_persistence_backend()

    @property
    def configuration(self):
        """:obj:`dict`: the configuration for this broker instance"""
        return self.config

    @property
    def version(self):
        """:obj:`tuple`: version tuple for this broker instance"""
        return BAROQUE_VERSION

    @property
    def reactors(self):
        """:obj:`baroque.datastructures.registries.ReactorRegistry`:
        registry of reactors subscribed to this broker instance"""
        return self.reactreg

    @property
    def eventtypes(self):
        """:obj:`baroque.datastructures.registries.EventTypesRegistry`:
        registry of event types registered on this broker instance"""
        return self.reactreg.get_event_types_registry()

    @property
    def events(self):
        """:obj:`baroque.datastructures.counters.EventCounter`:
        counter of events published on this broker instance so far"""
        return self.evtcounter

    @property
    def topics(self):
        """:obj:`baroque.datastructures.registries.TopicsRegistry`:
        registry of topics registered on this broker instance"""
        return self.topicsreg

    def reset(self):
        """Resets the reactors register and the published events counter of
        this broker instance.

        """
        self.reactreg = registries.ReactorsRegistry()
        self.evtcounter = counters.EventCounter()

    # -------- reactor-related methods --------
    def on(self, eventtype):
        """Registers an event type on the broker.

        Args:
            eventtype (:obj:`baroque.entities.eventtype.EventType`): the event type to be registered

        Returns:
            :obj:`baroque.datastructures.bags.ReactorsBag`

        """
        return self.reactreg.get_or_create_bag(eventtype)

    def on_any_event_run(self, reactor):
        """Subscribes a reactor on the broker to be run upon any event firing.

        Args:
            reactor (:obj:`baroque.entities.reactor.Reactor`): the reactor to be subscribed

        Returns:
            :obj:`baroque.datastructures.reactor.Reactor`

        """
        return self.reactreg.get_jolly_bag().run(reactor)

    # -------- event-related methods --------
    def publish(self, event):
        """Publishes an event on the broker.

        Note:
            This is a template-method

        Args:
            event (:obj:`baroque.entities.event.Event`): the event to be published

        """
        assert isinstance(event, Event)
        if self.config['events']['validate_schema']:
            self._validate_event_schema(event)
        self._count_event(event)
        self._execute_reactors(event)
        self._update_event_status(event)
        if self.config['events']['persist']:
            self._persist_event(event)

    # "private" methods
    def _count_event(self, event):
        """Increments the events counter of the broker

        Args:
            event (:obj:`baroque.entities.event.Event`): the event to be counted

        """
        self.evtcounter.increment_counting(event)

    def _execute_reactors(self, event):
        """Execute all reactors that subscribed to the event type of the input
        event.

        Args:
            event (:obj:`baroque.entities.event.Event`): the event
        Raises
            :obj:`baroque.exceptions.eventtypes.UnregisteredEventTypeError`: when the type of the event is not registered on the broker

        """
        propagate = self.config['reactors']['propagate_exceptions']
        ignore = self.config['eventtypes']['ignore_unregistered']
        if not ignore:
            if event.type not in self.eventtypes:
                raise UnregisteredEventTypeError(event.type)
        for r in self.reactreg.get_jolly_bag():
            try:
                r.react_conditionally(event)
            except:
                if propagate:
                    raise
        for r in self.reactreg.get_bag(event.type):
            try:
                r.react_conditionally(event)
            except:
                if propagate:
                    raise

    def _update_event_status(self, event):
        """Turns the event status to published.

        Args:
            event (:obj:`baroque.entities.event.Event`): the event whose status needs to be set to published.

        """
        event.set_published()

    def _persist_event(self, event):
        """Persists the event information to a datastore.

        Args:
            event (:obj:`baroque.entities.event.Event`): the event to be persisted

        """
        self._persistance_backend.create(event)

    def _load_preregistered_eventtypes(self):
        """Register predefined event types (as per configuration) on this
        broker instance"""
        for path in self.config['eventtypes']['pre_registered']:
            class_ = importer.class_from_dotted_path(path)
            eventtype = class_()
            self.eventtypes.register(eventtype)

    def _load_persistence_backend(self):
        """Loads on this broker instance the persistence backend defined in
        configuration"""
        path = self.config['events']['persistence_backend']
        if path is not None:
            class_ = importer.class_from_dotted_path(path)
            self._persistance_backend = class_()

    def _validate_event_schema(self, event):
        """Validate the JSON Schema of the input event.

        Args:
            event (:obj:`baroque.entities.event.Event`): the event whose JSON schema needs to be validated.
        Raises
            :obj:`baroque.exceptions.eventtypes.InvalidEventSchema`:
            when the type of the event is not registered on the broker

        """
        if not EventType.validate(event, event.type):
            raise InvalidEventSchemaError(event)

    # -------- event-related methods --------
    def publish_on_topic(self, event, topic):
        """Publishes an event on a specified topic registered on the broker.

        Note:
            This is a template-method

        Args:
            event (:obj:`baroque.entities.event.Event`): the event to be published on the topic
            topic (:obj:`baroque.entities.topic.Topic`): the topic on which the event must be published

        Raises
            :obj:`baroque.exceptions.topics.UnregisteredTopicError`:
            when trying to publish events on a topic that is not registered
            on the broker

        """
        if topic not in self.topics:
            raise UnregisteredTopicError(topic)
        self._count_event(event)
        self.topics.publish_on_topic(event, topic)
        self._update_event_status(event)
        if self.config['events']['persist']:
            self._persist_event(event)

    def on_topic_run(self, topic, reactor):
        """Attaches a reactor on a topic registered on the broker.

        Args:
            topic (:obj:`baroque.entities.topic.Topic`): the topic to which the reactor must be attached
            reactor (:obj:`baroque.entities.reactor.Reactor`): the reactor to be attached to the topic
        """
        if topic not in self.topics:
            if self.config['topics']['register_on_binding']:
                self.topics.register(topic)
            else:
                raise UnregisteredTopicError(topic)
        self.topics.on_topic_run(topic, reactor)

    # -------- aliases --------

    def fire(self, event):
        """Alias for `baroque.baroque.Baroque.publish()` method"""
        self.publish(event)

    def on_any_event_trigger(self, reactor):
        """Alias for `baroque.baroque.Baroque.on_any_event_run()` method"""
        return self.on_any_event_run(reactor)

    # -------- magic methods -------
    def __repr__(self):
        return '<{}.{}'.format(__name__, self.__class__.__name__)

