import uuid
import hashlib
from json import dumps
from .eventtype import EventType
from baroque.utils import timestamp as ts


class EventStatus:
    """
    Represents the binary state of events publication: ``published`` or
    ``unpublished``"""
    UNPUBLISHED = 'unpublished'
    PUBLISHED = 'published'


class Event:
    """An event that can be published.

    Args:
        eventtype (:obj:`baroque.entities.eventtype.EventType` instance or `type` object): the type of the event
        payload (dict, optional): the content of this event
        description (str, optional): the description of this event
        owner (str, optional): the owner of this event

    """
    def __init__(self, eventtype, payload=None, description=None, owner=None):
        assert eventtype is not None
        if type(eventtype) == type:
            eventtype = eventtype()
        assert isinstance(eventtype, EventType)
        if payload is not None:
            assert isinstance(payload, dict)
        self.id = str(uuid.uuid4())
        self.type = eventtype
        self.owner = owner
        self.status = EventStatus.UNPUBLISHED
        self.description = description
        self.payload = payload
        self.tags = set()
        self.timestamp = None
        self.touch()

    def set_published(self):
        """Sets the status of this event to published."""
        self.status = EventStatus.PUBLISHED

    def set_unpublished(self):
        """Sets the status of this event to unpublished."""
        self.status = EventStatus.UNPUBLISHED

    def touch(self):
        """Sets the current time as timestamp of this event"""
        self.timestamp = ts.utc_now()

    def json(self):
        """Dumps this object to a JSON string.

        Returns:
            str

        """
        data = dict(id=self.id, type=self.type.json(),
                    owner=self.owner, status=self.status,
                    description=self.description, payload=self.payload,
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
        return '<{}.{} - type: {} - id: {}>'.format(
            __name__,
            self.__class__.__name__,
            self.type.__class__.__name__,
            self.id
        )

