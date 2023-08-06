# -*- coding: utf-8 -*-
"""
    pip_services3_commons.run.Closer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Closer component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IClosable import IClosable

class Closer:
    """
    Helper class that closes previously opened components.
    """

    @staticmethod
    def close_one(correlation_id, component):
        """
        Closes specific component.

        To be closed components must implement [[ICloseable]] interface.
        If they don't the call to this method has no effect.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param component: the component that is to be closed.
        """
        if isinstance(component, IClosable):
            component.close(correlation_id)

    @staticmethod
    def close(correlation_id, components):
        """
        Closes multiple components.

        To be closed components must implement [[ICloseable]] interface.
        If they don't the call to this method has no effect.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param components: the list of components that are to be closed.
        """
        if components == None:
            return

        for component in components:
            Closer.close_one(correlation_id, component)
