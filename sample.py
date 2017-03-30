from baroque import Baroque, Event, Reactor, GenericEventType, ReactorFactory

# instantiate the library
brq = Baroque()

# EventTypes mark categories of events
eventtype = GenericEventType()

# Events are simple objects with properties
event = Event(eventtype)

# Reactors are stateless functions
# instantiate a predefined reactor that mirrors the triggering event on stdout
reactor = ReactorFactory.stdout()

# attach the reactor to any incoming event of type "eventtype"
brq.on(eventtype).run(reactor)    # same as: brq.on("foobar").trigger(reactor)

# now fire the event
brq.publish(event)    # same as: brq.fire(event)

# view all tracked event types
print(brq.eventtypes)
print(brq.eventtypes.count())

# remove a reactor for a given event type
brq.reactors.to(eventtype).remove(reactor)

# ... or all reactors for it
brq.reactors.to(eventtype).remove_all()

# ... or remove reactors for any kind of event type
brq.reactors.remove_all()


# try again but with your custom reactors
def randomize(event):
  from random import randint
  print(randint(1, 10))

my_reactor = Reactor(randomize)

# run a reactor upon any incoming event
brq.on_any_event_run(my_reactor)
event = Event(eventtype)
brq.publish(event)

# view all attached reactors, or all reactors for a specific event type
print(brq.reactors)
print(brq.reactors.to(eventtype))
print(brq.reactors.to(eventtype).count())
print(brq.reactors.to_any_event())
print(brq.reactors.to_any_event().count())

brq.reactors.to_any_event().remove_all()
brq.reactors.remove_all()

# reactors can run only if specific conditions are met
def condition(event):
  return 'test' in event.payload
r = Reactor(randomize)
brq.on_any_event_trigger(r).only_if(condition)  # same as: brq.on_any_event_trigger(Reactor(randomize, condition))
event_with = Event(eventtype, payload=dict(test=1))
event_without = Event(eventtype, payload=dict(label='text'))
brq.publish(event_without)
brq.publish(event_with)
print('reactor reated {} times'.format(r.count_reactions()))
print(r.last_reacted_on())
print(r.last_event_reacted())