"""Scenario: we want to be notified on terminal whenever someone is
available to sell pills... That's easy with Baroque!"""

from baroque import Baroque, ReactorFactory, Event, GenericEventType

# 1. Instantiate the event broker
brq = Baroque()

# 2. Create a reactor that prints events on the terminal. Such a reactor is
# already built-in
reactor = ReactorFactory.stdout()

# 3. Now create an instantiable event type describing the availability
# of pills. That will simply lead to generic free-form payload events, so
# subclassing the default 'GenericEventType' will suffice


class PillsAvailable(GenericEventType):
    pass


# 4. Good, tell the broker that it needs to run the reactor every time that
# an event of type 'PillsAvailable' is published
brq.on(PillsAvailable).run(reactor)


# 5. We're set to go. Now let's create a PillsAvailable event and fire it
# on the broker
evt_payload = {
    'sender': 'somebody@somedomain.com',
    'subject': 'Pills',
    'reception time': '2017-03-29T08:19:00Z',
    'body': 'Hey! Want to buy some very good pills for $10?',
    'attachments': None,
}
evt = Event(eventtype=PillsAvailable,
            payload=evt_payload,
            description='Pills at $10',
            owner='the pusher')
brq.publish(evt)

# 6. Your console says that pills are purchasable... hurry up!
