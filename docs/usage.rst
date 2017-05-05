How to use Baroque
==================

Using Baroque is simple: you only need to declare what you want to happen
whenever events of a specific type occurs.
This concept can be further leveraged through topics, which basically are
a convenient way for you to make something happen whenever multiple types of
events occur: a topic is a "named manifest" of your subscription to the
occurring of those event types.

Let's dive a bit deeper into Baroque gears...


Reactors
--------
Reactors are objects that embed a Python function called "reaction": this function
is "that something you wanted to happen"!
You just have to provide that function, which can do literally anything you
want, eg:

  - change properties of one or more objects
  - invoke other functions
  - call an HTTP API
  - spawna new worker thread
  - put a message on a queue
  - send an e-mail, SMS or push notification
  - print something on the console
  - write a row on a database table

Sky is the limit...

The only constraint that Baroque gives to reaction functions is that they must
parametrically accept at least one positional argument: the triggering event.
Baroque will pass in the event object whenever it executes the reaction function

When does the execution of the reaction happen?
Whenever Baroque knows that an event of a certain type has been fired and that
event types must result into the execution of that reactor.

Specifying the binding between Reactors and Event Types is the core operation
when using Baroque, and it's up to you:


.. code:: python

    from baroque import Baroque, Reactor, MetricEventType

    brq = Baroque()

    # create a simple reactor from a reaction function
    def greet(event):
        print("Hello world")
    reactor = Reactor(greet)

    # Tell Baroque to run your reactor whenever any event of type
    # MetricEventType is published
    brq.on(MetricEventType).run(reactor)


What if you want to execute your reaction function *only if* some conditions
on the event are met?
Don't worry: along with a reaction, a Reactor can embed a "condition" function.
The condition is a standard Python function that you provide to the Reactor
and must comply to the following:

  - it gets one parameter: the Event object
  - it returns a boolean value (*True* if the condition is met or *False* if it
    is not)

If you don't specify any condition when you create a Reactor object, no checks
will be performed on the event that triggered the execution of the Reactor

Example:

.. code:: python

    from baroque import Reactor, Baroque, Event, GenericEventType

    # Reaction function
    def greet(event):
        print("Hello {}".format(event.payload.get("name", "world"))

    # Condition function
    def only_if_name_provided(event):
        return "name" in event.payload

    reactor = Reactor(greet, only_if_name_provided)
    brq = Baroque()
    brq.on_any_event_run(reactor)


    # The greeting is printed only if the triggering event contains a field
    # named "name" in its payload...
    brq.publish(Event(GenericEventType, payload={}))                # reaction is not run
    brq.publish(Event(GenericEventType, payload={"name": "bob"}))   # reaction is run


For your convenience, Baroque offers a few out-of-the-box reactors types,
available through a factory object:

.. code:: python

    from baroque import ReactorFactory

    reactor = ReactorFactory.stdout         # mirror-print of event object on terminal
    reactor = ReactorFactory.call_function  # invoke a function on an object instance
    reactor = ReactorFactory.json_webhook   # HTTP POSTs some JSON to a URL


Events
------
Events are the core concept in Baroque. An event is an object that describes
something that happened and that you want to notify to someone in order to allow
something to happen in reaction to that.

At its bare minimum, an event is just a box of metadata defined by you and
characterized by a specific event type: you can create and publish many different
events of the same type.

The event type can either a valid instance of a subclass of the `EventType` class
or the subclass.

For example, this is an event of type `GenericEventType`, which is a subtype of
`EventType`:


.. code:: python

    from baroque import Event, GenericEventType
    event1 = Event(GenericEventType)
    event2 = Event(GenericEventType())


An event has the following fields:

  * a unique UUID
  * an optional payload (`dict`) containing user-defined metadata
  * an optional description
  * an optional `set` of tags
  * a publication status (`PUBLISHED` vs `UNPUBLISHED`)
  * a creation timestamp
  * an optional owner


In code:

.. code:: python

    event = Event(TweetEvent,
                  payload=dict(tweet_id=12345678,
                               tweet_text="howdy this is a tweet"),
                  description='My first tweet',
                  owner='csparpa')
    event.json()
    event.md5()
    event.id
    event.owner
    event.type
    event.status
    event.description
    event.timestamp   # set to current timestamp with: event.touch()
    event.payload
    event.tags
    event.tags.update(‘twitter’, ‘tweet’)


Any event can be dumped to JSON or can provide its own MD5 hash:

.. code:: python

    event.md5()
    event.json()


Event Types
-----------

As stated before, each event must be identified by one event type. Event types
are the way Baroque uses to:

  - *convey events contents* in terms of data and structure, and *validate* them:
    this means that datastructures (eg. payload, sections of payload, whole
    event structure, etc.) carried by events of specific types can be validated
    so that events that claim to be of those types but do not carry well-formed
    data can be spot and handled with. Validation is enabled via JSON Schema.
  - *convey events hierarchy*: you can create event types hierarchies


You can either define custom event types or use the ones that Baroque offers
for your convenience, which you can find in module `baroque.defaults.eventtypes`

Let's start with the latter ones.

You might have no need to create any events hierarchy nor to specify what data
your events carry: in this case, it's just OK to use a `GenericEventType`, which
is a kind of "wildcard" event type that applies no schema validation on events
and is not included in any event types hierarchy

.. code:: python

    from baroque import Event, GenericEventType
    event = Event(GenericEventType)

The off-the-shelf event types include:

  * `StateTransitionEventType` - models events fired on state machine transitions
  * `DataOperationEventType` - models events fired on manipulation of data entities
  * `MetricEventType` - models events fired on phenomena sampling or time-series variations

These event types apply schema validation to events: please refer to the code
documentation to check out the expected format for data carried by these events.

In case you need to define your own event types, just subclass the base class
`baroque.entities.eventtype.EventType` and provide the JSON schema you want
events of your custom type to be validated against.

In example, let us imagine that we want to define events of type "BabyBornEventType"
that must contain in their payload at least two information: the name of the
baby and the baby's birth date:

.. code:: python

    from baroque import EventType

    class BabyBornEventType(EventType):
        def __init__(self, owner=None):
            EventType.__init__(
                self,
                '''{
                  "$schema": "http://json-schema.org/draft-04/schema#",
                  "type": "object",
                  "properties": {
                    "payload": {
                      "type": "object",
                      "properties": {
                        "baby_name": {
                          "type": ["string"]
                        },
                        "birth_date": {
                          "type": ["string"]
                        }
                      },
                      "required": [
                        "baby_name",
                        "birth_date"
                      ]
                    }
                  },
                  "required": [
                    "payload"
                  ]
                }''',
                description='A new baby is born',
                owner=owner)

Then if we instantiate events of type `BabyBornEventType`, they must conform
to the JSON schema that we specified on the type:

.. code:: python

    from baroque import Event

    # this event is valid
    valid_event = Event(BabyBornEventType,
                        payload=dict(baby_name='Bob',
                                     birth_date='2017-04-19'))

    # this event is not valid, as it does not carry the required data
    invalid_event = Event(BabyBornEventType,
                          payload=dict(foo='bar'))

Invalid events can result in exceptions raised when trying to publish them:
this depends on the library configuration (please see the relevant documentation
section). By default, Baroque validates all events schema.


Please refer to JSON Schema specification_ for details about expressing events
contents.


.. _specification: http://json-schema.org


Topics
------

Topics are channels for notifying multiple event consumers at once that events
of specific types have been published; they're a way to decouple producers
of events from their consumers.

When you crete a topic you need to specify what event types it is bound to
(passing in an iterable of either `EventType` instances or subclasses); a topic
can be bound to one or more event types. Topic must have a name and can optionally have an owner,
a description and a set of tags (strings) you can use later to search for the topic.
Each topic also gets an unique ID:

.. code:: python

    from baroque import Topic
    family_event_types = [ClaudioRelativesEventType(), ClaudioEventType()]
    topic = Topic('my-family-events',
                  family_event_types,
                  description='all events about me and my family will be published here',
                  owner='me',
                  tags=['claudio', 'events'])


To make a topic useful, you must register it to the Baroque broker instance:

.. code:: python

    from baroque import Baroque
    brq = Baroque()
    brq.topics.register(topic)



A useful shortcut for creating topics *and* registering them on the broker is
the following:

.. code:: python

    from baroque import Baroque
    brq = Baroque()
    family_event_types = [ClaudioRelativesEventType(), ClaudioEventType()]
    topic = brq.topics.new('my-family-events',
                           family_event_types,
                           description='all events about me and my family will be published here',
                           owner='me',
                           tags=['claudio', 'events'])


Event consumers *subscribe* to the topic by passing to the broker instance
both a reference to that topic and the reactor object they want to be executed
whenever *any* events of the types bound to the topic will be published on the
broker:

.. code:: python

    from baroque import Baroque, ReactorFactory
    brq = Baroque()
    reactor = ReactorFactory.stdout
    brq.on_topic_run(topic, reactor)


If the topic is not registered on the broker instance yet, this will be automatically
registered. Baroque can be configured to raise an `UnregisteredTopicError` instead.

Subscribers can leverage Baroque topics search features to look for interesting
topics:

.. code:: python

    from baroque import Baroque
    brq = Baroque()
    brq.topics.of('somebody')       # finds all topics owned by someone
    brq.with_id('d3d5beb8')         # finds the topic with the specified ID
    brq.with_name('my-topic')       # finds the topic with the specified name
    brq.with_tags(['tag1', 'tag2']) # finds all topics marked with the specified tags


Event producers that want their events to be published on a topic must do
it via the broker; this will trigger execution of all reactors that were bound
to the topic:

.. code:: python

    from baroque import Baroque, Event
    brq = Baroque()

    claudio_event = Event(ClaudioEventType())
    brq.publish_on_topic(claudio_event, claudio_event)

    cousin_event = Event(ClaudioRelativesEventType())
    brq.publish_on_topic(cousin_event, claudio_event)


The Baroque broker
------------------
TBD