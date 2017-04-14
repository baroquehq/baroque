from baroque import Event, Reactor
from .eventtypes import PeerJoinedEventType, PeerLeftEventType, \
    MessageEventType


class Peer:
    def __init__(self, name, event_broker, events_topic):
        self.name = name
        self.broker = event_broker
        self.topic = events_topic
        self.listen()
        
    def listen(self):
        def decorate_line(line):
            return "[{}@host]$ {}".format(self.name, line)
        
        def display_on_console(event):
            line = ''
            if isinstance(event.type, PeerJoinedEventType):
                line = '{} joined the room on {}'.format(
                                    event.payload['peer'],
                                    event.timestamp)
            if isinstance(event.type, PeerLeftEventType):
                line = '{} left the room on {}'.format(
                                    event.payload['peer'],
                                    event.timestamp)
            if isinstance(event.type, MessageEventType):
                line = 'Message received from {} on {}: {}'.format(
                                    event.payload['sender'],
                                    event.timestamp,
                                    event.payload['text'])
            if line:
                print(decorate_line(line))

        # only display messages whose owner is not self
        self.broker.on_topic_run(self.topic,
                                 Reactor(display_on_console,
                                         lambda evt: evt.owner != self.name))
    
    def send_message(self, message_text):
        evt = Event(MessageEventType,
                    payload=dict(sender=self.name,
                                 text=message_text),
                    owner=self.name)
        self.broker.publish_on_topic(evt, self.topic)
