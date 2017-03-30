from baroque.entities.event import Event
from .eventtypes import GenericEventType


class EventFactory:
    """A factory class that exposes methods to quickly create useful
    :obj:`baroque.entities.event.Event` instances"""

    @classmethod
    def new(cls, **kwargs):
        """Factory method returning a generic type event.
    
        Args:
            **kwargs: positional arguments for `Event` instantiation
    
        Returns:
            :obj:`baroque.entities.event.Event`
    
        """
        return Event(GenericEventType(), **kwargs)
