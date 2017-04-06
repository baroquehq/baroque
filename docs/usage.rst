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


Event Types
-----------

TBD


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
