from baroque import EventType


class MessageEventType(EventType):
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
                    "sender": {
                      "type": ["string", "number"]
                    }
                    "text": {
                      "type": ["string", "number"]
                    }
                  },
                  "required": [
                    "sender"
                    "text"
                  ]
                }
              },
              "required": [
                "payload"
              ]
            }''',
            description='Chatroom message events',
            owner=owner)


class PeerJoinedEventType(EventType):
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
                    "peer": {
                      "type": ["string", "number"]
                    }
                  },
                  "required": [
                    "peer"
                  ]
                }
              },
              "required": [
                "payload"
              ]
            }''',
            description='Peer joining chatroom events',
            owner=owner)


class PeerLeftEventType(EventType):
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
                    "peer": {
                      "type": ["string", "number"]
                    }
                  },
                  "required": [
                    "peer"
                  ]
                }
              },
              "required": [
                "payload"
              ]
            }''',
            description='Peer leaving chatroom events',
            owner=owner)
