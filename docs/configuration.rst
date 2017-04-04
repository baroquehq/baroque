Configuring Baroque
===================

Baroque behaviour can be easily configured

Default configuration
---------------------
The default configuration is stored in module:

.. code:: python

    baroque.defaults.config

as a Python dictionary and is loaded upon broker instantiation if no custom
configuration file is provided as argument.

An actual YML version of the default version is stored in the root path of
Baroque's installation (file: _baroque.yml_)

Custom configuration
--------------------

Custom configurations can be provided as YML files, and can be loaded upon
broker instantiation as follows:

.. code:: python

    from baroque import Baroque
    brq = Baroque(configfile='path/to/file.yml')

Baroque validates the YML syntax, but performs no validation on the provided
configuration switches (whether they make sense or not): the check is done in
a lazy way - in other when the switches are actually used.

Configuration switches
----------------------
Switches are grouped according to Baroque's data entities they impact:

  - **Event Types**
      * *ignore_unregistered*: shall Baroque ignore upon events publication all the
        events with a type that is not registered? If not, then raise an exception [boolean]
      * *pre_registered*: this is the list of _EventType_ subclasses that are pre-registered
        on the broker right from the start, so that it is possible to publish on the broker events
        of those types without further hassle [list of str, each one being a dotted Python class path]
  - **Events**
      * *validate_schema*: shall Baroque validate event type schema upon all events upon publishing?
        If not, raise an exception [boolean]
      * *persist*: Shall Baroque persist all published events on the provided persistence provider? [boolean]
      * *persistence_provider*: this is the class implementing events persistence. Must be
        a subtype of *baroque.backend.PersistenceBackend* asbtract class [str, dotted Python class path]
  - **Reactors**
      * *propagate_exceptions*: shall Baroque bubble up exceptions raised by any reactor
        whenever they occur? If not, catch them silently [boolean]
  - **Topics**
      * *register_on_binding*: shall Baroque register a previously unregistered topic whenever
        a reactor is bound to it? If not, raise an exception [boolean]



Example of YML config file contents
-----------------------------------
This is an example of a possible YML file contents:

.. code::

    eventtypes:
      ignore_unregistered: false
      pre_registered:
    baroque.entities.eventtype.GenericEventType
    baroque.entities.eventtype.StateTransitionEventType
    baroque.entities.eventtype.DataOperationEventType
    baroque.entities.eventtype.MetricEventType
    events:
      validate_schema: true
      persist: false
      persistence_provider: baroque.persistence.inmemory.DictBackend
    reactors:
      propagate_exceptions: true
    topics:
      register_on_binding: true