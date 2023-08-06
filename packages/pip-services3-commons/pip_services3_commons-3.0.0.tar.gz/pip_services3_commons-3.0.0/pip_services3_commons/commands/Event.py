# -*- coding: utf-8 -*-
"""
    pip_services3_commons.commands.Event
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Event implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IEvent import IEvent
from ..errors.InvocationException import InvocationException

class Event(IEvent):
    """
    Concrete implementation of IEvent interface.
    It allows to send asynchronous notifications to multiple subscribed listeners.

    Example:
        event = Event("my_event")

        event.addListener(myListener)

        event.notify("123", Parameters.fromTuples("param1", "ABC", "param2", 123)

    See IEvent, IEventListener
    """

    _name = None
    _listeners = None

    def __init__(self, name):
        """
        Creates a new event and assigns its name.

        :param name: name of the event

        :raises: Exception: when Event name is not set.
        """
        if name == None:
            raise Exception("Event name is not set")

        self._name = name
        self_listeners = []

    def get_name(self):
        """
        Gets the event name.

        :return: the event name
        """
        return self._name

    def get_listeners(self):
        """
        Gets all listeners registred in this event.

        :return: a list with listeners
        """
        return list(self._listeners)

    def add_listener(self, listener):
        """
        Adds a listener to receive notifications when this event is fired.

        :param listener: a listener reference to added
        """
        self._listeners.append(listener)

    def remove_listener(self, listener):
        """
        Removes a listener, so that it no longer receives notifications for this event.

        :param listener: a listener reference to removed
        """
        self._listeners.remove(listener)
    
    def notify(self, correlation_id, args):
        """
        Fires this event and notifies all registred listeners.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param args: the parameters to raise this event with.
        """
        for listener in self._listeners:
            try:
                listener.on_event(correlation_id, self, args)
            except Exception as ex:
                raise InvocationException(
                    correlation_id,
                    "EXEC_FAILED",
                    "Raising event " + self._name + " failed: " + str(ex)
                ).with_details("event", self._name).wrap(ex)
