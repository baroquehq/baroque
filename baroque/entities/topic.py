import uuid
import hashlib
import collections
from json import dumps
from baroque.datastructures.bags import EventTypesBag
from baroque.utils import timestamp as ts


class Topic:
    """A distribution channel where events of specific types can be published
    and can be seen by subscribers of the topic. Topic subscribers will attach
    a reactor to the topic, which will be fired whenever any event of the types
    that are supported by the topic is published on the topic itself.

    Args:
        name (str): the name of this topic
        eventtypes (collection): the :obj:`baroque.entities.eventtype.EventType` objects that characterize this topic
        description (str, optional): a description of this topic
        owner (str, optional): the owner of this topic
        tags (set, optional): the `set` of tags that describe this topic

    Raises:
        `AssertionError`: name or tags are `None` or have a wrong type

    """

    def __init__(self, name, eventtypes, description=None, owner=None,
                 tags=None):
        assert name is not None
        assert isinstance(name, str)
        self.name = name
        assert eventtypes is not None
        if len(eventtypes) != 0:
            self.types = EventTypesBag(eventtypes)
        else:
            self.types = EventTypesBag()
        self.description = description
        self.owner = owner
        if tags is not None:
            assert not isinstance(tags, str)
            assert isinstance(tags, collections.Iterable)
            self.tags = set(tags)
        else:
            self.tags = set()
        self.id = str(uuid.uuid4())
        self.timestamp = None
        self.touch()

    @property
    def eventtypes(self):
        """:obj:`baroque.datastructures.bags.EventTypesBag`: bag containing the
         event types of this topic"""
        return self.types

    def touch(self):
        """Sets the current time as timestamp of this topic"""
        self.timestamp = ts.utc_now()

    def json(self):
        """Dumps this object to a JSON string.

        Returns:
            str

        """
        data = dict(id=self.id, owner=self.owner, description=self.description,
                    eventtypes=[str(et) for et in self.types],
                    tags=list(self.tags), timestamp=ts.stringify(self.timestamp))
        return dumps(data)

    def md5(self):
        """Returns the MD5 hash of this object.

        Returns:
            str

        """
        m = hashlib.md5()
        m.update(self.json().encode('utf-8'))
        return m.hexdigest()

    def __repr__(self):
        return '<{}.{} - name: {} - owner: {} - eventtypes: {}>'.format(
            __name__,
            self.__class__.__name__,
            self.name,
            self.owner or 'None',
            ', '.join([str(et) for et in self.types]) or 'None'
        )
