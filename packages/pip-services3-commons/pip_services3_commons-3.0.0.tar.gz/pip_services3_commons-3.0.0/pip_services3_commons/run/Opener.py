# -*- coding: utf-8 -*-
"""
    pip_services3_commons.run.Opener
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Opener component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IOpenable import IOpenable

class Opener:
    """
    Helper class that opens components.
    """
    @staticmethod
    def is_opened_one(component):
        """
        Checks if specified component is opened.

        To be checked components must implement [[IOpenable]] interface.
        If they don't the call to this method returns true.

        :param component: the component that is to be checked.

        :return: true if component is opened and false otherwise.
        """
        if isinstance(component, IOpenable):
            return component.is_opened()

        return True

    @staticmethod
    def is_opened(components):
        """
        Checks if all components are opened.

        To be checked components must implement [[IOpenable]] interface.
        If they don't the call to this method returns true.

        :param components: a list of components that are to be checked.

        :return: true if all components are opened and false if at least one component is closed.
        """
        if components == None:
            return True

        result = True
        for component in components:
            result = result and Opener.is_opened_one(component)

        return result

    @staticmethod
    def open_one(correlation_id, component):
        """
        Opens specific component.

        To be opened components must implement [[IOpenable]] interface.
        If they don't the call to this method has no effect.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param component: the component that is to be opened.
        """
        if isinstance(component, IOpenable):
            component.open(correlation_id)

    @staticmethod
    def open(correlation_id, components):
        """
        Opens multiple components.

        To be opened components must implement [[IOpenable]] interface.
        If they don't the call to this method has no effect.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param components: the list of components that are to be closed.
        """
        if components == None:
            return

        for component in components:
            Opener.open_one(correlation_id, component)
