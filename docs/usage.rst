How to use Baroque
==================

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
