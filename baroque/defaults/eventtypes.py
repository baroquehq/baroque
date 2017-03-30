from baroque.entities.eventtype import EventType


class GenericEventType(EventType):
    """Describes generic events with a free-form content.

    Args:
        owner (str, optional): ID of the owner of this event type.

    """
    def __init__(self, owner=None):
        EventType.__init__(self,
                           '''{
                             "$schema": "http://json-schema.org/draft-04/schema#"
                           }''',
                           description='Generic event',
                           owner=owner)


class StateTransitionEventType(EventType):
    """Describes events cast when something changes its state.
    Suitable i.e. to track state machines changes.
    Old and new states are conveyed in the event payload, as well as
    the cause of the state transition.

    Args:
        owner (str, optional): ID of the owner of this event type.

    """
    def __init__(self, owner=None):
        EventType.__init__(
            self,
            '''{
              "$schema": "http://json-schema.org/draft-04/schema#",
              "type": "object",
              "properties": {
                "payload": {
                  "type": "object",
                  "properties": {
                    "from_status": {
                      "type": ["string", "number"]
                    },
                    "to_status": {
                      "type": ["string", "number"]
                    },
                    "trigger": {
                      "type": ["string", "number"]
                    },
                    "meta": {
                      "type": ["object"],
                      "properties": {}
                    }
                  },
                  "required": [
                    "from_status",
                    "to_status",
                    "trigger"
                  ]
                }
              },
              "required": [
                "payload"
              ]
            }''',
            description='State transition events',
            owner=owner)


class DataOperationEventType(EventType):
    """Describes events cast when some kind of operation is done on a
    piece of data.
    Suitable i.e. to track CRUD operations on DB tables or whole datastores.
    Details about the impacted data entity and the operation are
    conveyed in the event payload.

    Args:
        owner (str, optional): ID of the owner of this event type.

    """
    def __init__(self, owner=None):
        EventType.__init__(
            self,
            '''
            {
              "$schema": "http://json-schema.org/draft-04/schema#",
              "type": "object",
              "properties": {
                "payload": {
                  "type": "object",
                  "properties": {
                    "datum": {
                      "type": "object",
                      "properties": {}
                    },
                    "operation": {
                      "type": "string"
                    },
                    "timestamp": {
                      "type": ["number", "string"]
                    },
                    "meta": {
                      "type": "object",
                      "properties": {}
                    }
                  },
                  "required": [
                    "datum",
                    "operation",
                    "timestamp"
                  ]
                }
              },
              "required": [
                "payload"
              ]
            }
            ''',
            description='Data operation events',
            owner=owner)


class MetricEventType(EventType):
    """Describes events carrying metric data.
    Suitable i.e. to track values about measured physical quantities.
    The metric name and value are conveyed in the event payload.

    Args:
        owner (str, optional): ID of the owner of this event type.

    """
    def __init__(self, owner=None):
        EventType.__init__(
            self,
            '''
            {
              "$schema": "http://json-schema.org/draft-04/schema#",
              "type": "object",
              "properties": {
                "payload": {
                  "type": "object",
                  "properties": {
                    "metric": {
                      "type": ["string", "number"]
                    },
                    "value": {
                      "type": ["string", "number"]
                    },
                    "timestamp": {
                      "type": ["string", "number"]
                    },
                    "meta": {
                      "type": "object",
                      "properties": {}
                    }
                  },
                  "required": [
                    "metric",
                    "value",
                    "timestamp"
                  ]
                }
              },
              "required": [
                "payload"
              ]
            }
            ''',
            description='Metric events',
            owner=owner)
