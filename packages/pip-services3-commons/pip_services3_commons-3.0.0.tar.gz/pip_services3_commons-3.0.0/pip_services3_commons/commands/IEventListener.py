# -*- coding: utf-8 -*-
"""
    pip_services3_commons.commands.IEventListener
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for event listeners.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IEvent import IEvent

class IEventListener(object):
    """
    An interface for listener objects that receive notifications on fired events.

    Example:
        class MyListener(IEventListener):
            def on_event(self, correlation_id, event, value):
                print "Fired event " + event.get_name()
    """

    def on_event(self, correlation_id, event, value):
        """
        A method called when events this listener is subscrubed to are fired.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param event: event reference

        :param value: event arguments
        """
        raise NotImplementedError('Method from interface definition')
