# Baroque

![Baroque](https://raw.githubusercontent.com/csparpa/baroque/master/baroque.png)

## Events made easy
Baroque is an event brokering framework with a honey-sweet interface.

It features an out-of-the-box efficient implementation of the publish-subscriber 
pattern enabled by high-level abstractions, allowing quick development of 
event-driven applications.

The main focus of Baroque is provide a human-friendly interface to event
brokering operations, in terms of API and configuration.


### Features in a nutshell
  - Create **Events** as lightweight JSON containers of custom metadata, each 
    with a named type and suitable of JSON schema validation
  - **publish** events of any type and **subscribe** execution of stateless 
    callback functions (aka: **reactors**) upon events firing
  - reactors can be conditionally executed (you say when the magic happens). You
    can either provide your custom reactors or leverage Baroque's built-in ones
  - validate
  - create event distribution **topics** from specified pools of event types 
    and easily publish events on them, triggering execution of subscribers'
    reactors
  - optionally track events in-memory or save them to persistent datastores 

Baroque is...
  - designed for humans (nerds and non-nerds!)
  - plug and play into your own code
  - easily configurable: go with reasonable defaults or edit a simple 
    YML config file
  - extensible through a set of extension code hooks
  - heavily tested


##  Installation

Install with `pip` for your ease:

```shell
$ pip install baroque
```

Baroque runs on Python 3.5+


## Usage examples
```python
from baroque import Baroque, Reactor, EventFactory

# Pub-sub is easy with Baroque!

# 1. Instantiate the event broker:
brq = Baroque()

# 2. Create reactors, which basically are functions. This one - in example -
# prints the input event's content to the console as JSON
reactor = Reactor(lambda event: print(event.json()))

# 3. Now tell the broker that we want to run our reactor upon events of any type:
brq.on_any_event_run(reactor)


# 4. Good! Now let's publish an event on the broker:
event = EventFactory.new(payload=dict(key1='value1', key2='value2'), owner='me')
brq.publish(event)

# ... and our terminal should display something like this:
'''
{
    "timestamp": "2017-03-28T23:20:57Z",
	"owner": "me",
	"links": [],
	"tags": [],
	"payload": 
	  {"key2": "value2",
	  "key1": "value1"},
	"status": "unpublished",
    ...
}
'''
```

See more examples in the `samples` folder


## Documentation
The library API documentation is available on Read the Docs

## License
MIT license

