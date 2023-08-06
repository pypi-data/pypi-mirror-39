# -*- coding: utf-8 -*-
"""
    pip_services3_commons.refer.Reference
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Reference component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class Reference(object):
    """
    Contains a reference to a component and locator to find it.
    It is used by [[References]] to store registered component references.
    """

    _locator = None
    _component = None


    def __init__(self, locator, component):
        """
        Create a new instance of the reference object and assigns its values.

        :param locator: a locator to find the reference.

        :param component: a reference to component.
        """
        if component == None:
            raise Exception("Component cannot be null")
        
        self._locator = locator
        self._component = component


    def match(self, locator):
        """
        Matches locator to this reference locator. Descriptors are matched using equal method.
        All other locator types are matched using direct comparison.

        :param locator: the locator to match.

        :return: true if locators are matching and false it they don't.
        """
        # Locate by direct reference matching
        if self._component == locator:
            return True
        # Locate by direct locator matching
        elif self._locator != None:
            return self._locator == locator
        else:
            return False


    def get_component(self):
        """
        Gets the stored component reference.

        :return: the component's references.
        """
        return self._component


    def get_locator(self):
        """
        Gets the stored component locator.

        :return: the component's locator.
        """
        return self._locator
