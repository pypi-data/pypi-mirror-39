# -*- coding: utf-8 -*-
"""
    pip_services3_commons.run.INotifiable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for notifiable components with parameters
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class INotifiable:
    """
    Interface for components that can be asynchronously notified.
    The notification may include optional argument that describe the occured event
    """

    def notify(self, correlation_id, args):
        """
        Notifies the component about occured event.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param args: notification arguments.
        """
        raise NotImplementedError('Method from interface definition')
