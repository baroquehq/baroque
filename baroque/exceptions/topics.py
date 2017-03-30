class UnregisteredTopicError(Exception):
    """Raised when attempting to publish events on a topic that is not registered
    on the broker"""
    pass
