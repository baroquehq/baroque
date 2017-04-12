import uuid
import collections
from baroque import Baroque, Event, DataOperationEventType, Reactor
from baroque.utils.timestamp import stringify, utc_now

'''
We want to track on a journal datastructure each and every non-idempotent
change that an observed datasource undergoes. So that - i.e. - we enable things
such as change data capture, events sourcing, etc..
'''


class DataSource:

    """
    The datasource could be i.e. a 
    database table: every time a row is created, updated or deleted a corresponding
    event is fired and we want that to be tracked.
    """

    def __init__(self, name, event_broker, event_topic):
        self.name = name
        self.rows = dict()
        self.broker = event_broker
        self.topic = event_topic

    def add(self, *args):
        pk = str(uuid.uuid4())
        self.rows[pk] = args
        event = Event(DataOperationEventType,
                      payload={'datum': {
                                    'table': self.name,
                                    'data_type': 'row',
                                    'pk': pk
                                },
                               'operation': 'creation',
                               'meta': {}})
        self.broker.publish_on_topic(event, self.topic)
        return pk

    def update(self, pk, *args):
        self.rows[pk] = args
        event = Event(DataOperationEventType,
                      payload={'datum': {
                                    'table': self.name,
                                    'data_type': 'row',
                                    'pk': pk
                                },
                               'operation': 'update',
                               'meta': {}})
        self.broker.publish_on_topic(event, self.topic)

    def delete(self, pk):
        del self.rows[pk]
        event = Event(DataOperationEventType,
                      payload={'datum': {
                                    'table': self.name,
                                    'data_type': 'row',
                                    'pk': pk
                                },
                               'operation': 'deletion',
                               'meta': {}})
        self.broker.publish_on_topic(event, self.topic)


class Journal:

    """
    Our journal will listen to a specific topic
    """

    def __init__(self, event_broker, observed_topic):
        self.topic = observed_topic
        self.messages = collections.OrderedDict()

        def append(evt):
            self.messages[evt.timestamp] = {
                'pk': evt.payload['datum']['pk'],
                'operation': evt.payload['operation']}
        event_broker.on_topic_run(topic, Reactor(append))

    def print_history(self):
        for ts, message in self.messages.items():
            print('{} : {} of row with pk={}'.format(
                ts, message['operation'],
                message['pk']))


brq = Baroque()
topic = brq.topics.new('datasource_changes',
                       eventtypes=[DataOperationEventType()],
                       description='changes in a datasource',
                       owner='me')
journal = Journal(brq, topic)

# let's make new friends!
friends = DataSource('friends', brq, topic)
pk_louis = friends.add('Louis', 'Armstrong', 'US')
pk_mick = friends.add('Mick', 'Jagger', 'GB')
pk_luciano = friends.add('Luciano', 'Pavarotti', 'FR')
friends.update(pk_luciano, 'Luciano', 'Pavarotti', 'IT')
friends.delete(pk_mick)

# and now let's review the history of changes to the datasource
journal.print_history()

