class PersistenceBackend:

    def create(self, event):
        """Persists an event.

        Args:
            event (:obj:`baroque.entities.event.Event`): the event to be persisted

        """
        pass

    def read(self, event_id):
        """Loads an event.

        Args:
            event_id (str): the identifier of the event to be loaded

        Returns:
            :obj:`baroque.entities.event.Event`

        """
        pass

    def update(self, event):
        """Updates the event.

        Args:
            event (:obj:`baroque.entities.event.Event`): the event to be updated

        """
        pass

    def delete(self, event_id):
        """Deletes an event.

        Args:
            event_id (str): the identifier of the event to be deleted

        """
        pass
