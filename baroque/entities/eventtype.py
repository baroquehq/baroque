import hashlib
from json import dumps, loads
from jsonschema import ValidationError
from jsonschema import validate as check


class EventType:
    """The type of an event, describing its semantics and content.

    Args:
        jsonschema (str): the JSON schema string describing the content of the
         events having this type
        description (str, optional): the description of this event type
        owner (str, optional): the owner of this event type

    """

    def __init__(self, jsonschema, description=None, owner=None):
        assert jsonschema is not None
        assert isinstance(jsonschema, str)
        self.jsonschema = jsonschema
        self.owner = owner
        self.description = description
        self.tags = set()

    @staticmethod
    def validate(evt, evttype):
        """Validates the content of an event against the JSON schema of its type.

        Args:
            evt (:obj:`baroque.entities.event.Event`): the event to be validated
            evttype (:obj:`baroque.entities.eventtype.EventType`): the type of
            the event that needs to be validated

        Returns:
            ``True`` if validation is OK, ``False`` otherwise

        """
        try:
            assert evt.type == evttype
            check(loads(evt.json()), loads(evttype.jsonschema))
            return True
        except (AssertionError, ValidationError):
            return False

    def json(self):
        """Dumps this object to a JSON string.

        Returns:
            str

        """
        data = dict(jsonschema=self.jsonschema, owner=self.owner,
                    description=self.description, tags=list(self.tags))
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
        return '<{}.{} - description: {}>'.format(
            __name__,
            self.__class__.__name__,
            self.description or 'None'
        )
