"""Default Baroque configuration"""

DEFAULT_CONFIG = {
    'eventtypes': {
        'ignore_unregistered': True,
        'pre_registered': [
            'baroque.defaults.eventtypes.GenericEventType',
            'baroque.defaults.eventtypes.StateTransitionEventType',
            'baroque.defaults.eventtypes.DataOperationEventType',
            'baroque.defaults.eventtypes.MetricEventType'
        ]
    },
    'events': {
        'validate_schema': True,
        'persist': False,
        'persistence_backend': 'baroque.persistence.inmemory.DictBackend'
    },
    'reactors': {
        'propagate_exceptions': True
    },
    'topics': {
        'register_on_binding': True
    }
}
