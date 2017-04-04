from baroque import Baroque, Event, DataOperationEventType, Reactor
from baroque.utils.timestamp import stringify, utc_now

'''
We want to keep in sync the value of a property of a target object instance (we will
call it: target instance) with the values of a property of an observed instance,
as the latter change. This is a one-way syncing.
The syncing mechanism is as follows:
  - The update on the observed instance is notified using Baroque's out-of-the-box
    `DataOperationEventType` event type (but one can also develop its own `EventType`
    subclass and use it!)
  - every time the observed property changes, an event is published on the broker
  - the publication triggers the execution of a reactor, which is the update of
    the target object instance's property
'''

brq = Baroque()


class Observed:

    field = None

    def __init__(self, val):
        self.field = val

    def __setattr__(self, key, value):
        event = Event(DataOperationEventType,
                      payload={'datum': {
                                    'class': 'Observed',
                                    'property': 'field'
                                },
                               'operation': 'modify',
                               'timestamp': stringify(utc_now()),
                               'meta': {
                                   'old_value': self.field,
                                   'new_value': value
                               }})
        super().__setattr__(key, value)
        brq.publish(event)


class Synced:
    def __init__(self):
        self.old_value = None
        self.new_value = None

# Instantiate objects
observed = Observed('aaa')
synced = Synced()

# Create and bind the reactor

def assign(event):
    synced.old_value = event.payload['meta']['old_value']
    synced.new_value = event.payload['meta']['new_value']

reactor = Reactor(assign)
brq.on(DataOperationEventType).run(reactor)

# Change the observed instance
observed.field = 'zzz'

print('The observed property changed from {} to {}'.format(
    synced.old_value, synced.new_value))

observed.field = 123

print('The observed property changed from {} to {}'.format(
    synced.old_value, synced.new_value))
