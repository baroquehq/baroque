class UnregisteredEventTypeError(Exception):
    """Raised when attempting to publish on the broker events of an
    unregistered type"""
    pass


class InvalidEventSchemaError(Exception):
    """Raised when the event validation against its eventtype JSON
    schema fails"""
    pass
