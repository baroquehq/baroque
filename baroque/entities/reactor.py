from baroque.utils import timestamp as ts


class Reactor:
    """An action to be executed whenever some type of events are published,
    with an optional condition to be satisfied satisfied. If a condition is
    set, this is checked out and if the outcome is ``True`` then the action
    is executed. If no condition is set, then the action is always executed.

    Args:
        reaction (function): the action to be executed
        condition (function, optional): the boolean condition to be satisfied

    Raises:
        `AssertionError`: when the supplied reaction is `None` or is not a callable, or (when supplied) when the condition is not a callable

    """
    def __init__(self, reaction, condition=None):
        assert reaction is not None
        assert callable(reaction)
        self.reaction_function = reaction
        if condition is not None:
            assert callable(condition)
        self.condition_function = condition
        self.last_reaction_timestamp = None
        self.id_last_event_reacted = None
        self.reactions_count = 0

    def react(self, event):
        """Execute the action of this reactor.

        Note:
            the condition of this reactor is out of the scope of this method
            (please see method :obj:``react_conditionally()``)

        Args:
            reaction (function): the action to be executed
            condition (function, optional): the boolean condition to be satisfied

        """
        self.reaction_function(event)
        self.reactions_count += 1
        self.last_reaction_timestamp = ts.utc_now()
        self.id_last_event_reacted = event.id

    def only_if(self, condition):
        """Sets the boolean condition for this reactor.

        Args:
            condition (function): the boolean condition to be satisfied

        """
        assert callable(condition)
        self.condition_function = condition

    def _condition_met(self, event):
        """Checks if the condition is satisfied when fed with an event.

        Args:
            event (:obj:`baroque.entities.event.Event`): the event to be fed to
            the condition function

        Returns:
            ``True`` if no condition function is set or if the condition is
            satisfied, ``False`` otherwise

        """
        if self.condition_function is None:
            return True
        return self.condition_function(event)

    def react_conditionally(self, event):
        """First checks if the condition is satisfied, then based on the outcome
        executes the action.

        Args:
            event (:obj:`baroque.entities.event.Event`): the triggering event

        """
        if self._condition_met(event):
            self.react(event)

    def count_reactions(self):
        """Gives the number of times this reactor's action has been executed

        Returns:
            int

        """
        return self.reactions_count

    def last_reacted_on(self):
        """Gives the timestamp of the last time when the reactor's action has
        been executed

        Returns:
            str if reactor reacted at least once, ``None`` otherwise

        """
        if self.last_reaction_timestamp is None:
            return None
        return ts.stringify(self.last_reaction_timestamp)

    def last_event_reacted(self):
        """Gives the ID of the last event this reactor reacted on

        Returns:
            str

        """
        return self.id_last_event_reacted

    def __repr__(self):
        return '<{}.{} - reaction function: {}> - ' \
               'condition function: {} - ' \
               'last reaction on: {}'.format(
                    __name__,
                    self.__class__.__name__,
                    self.reaction_function,
                    self.condition_function or 'None',
                    self.last_reacted_on() or 'Never'
                )
