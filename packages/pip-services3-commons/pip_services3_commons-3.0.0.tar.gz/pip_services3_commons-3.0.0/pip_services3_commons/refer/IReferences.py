# -*- coding: utf-8 -*-
"""
    pip_services3_commons.refer.IReferences
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for references components.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IReferences:
    """
    Interface for a map that holds component references and passes them to components
    to establish dependencies with each other.

    Together with [[IReferenceable]] and [[IUnreferenceable]] interfaces it implements
    a Locator pattern that is used by PipServices toolkit for Inversion of Control
    to assign external dependencies to components.

    The IReferences object is a simple map, where keys are locators
    and values are component references. It allows to add, remove and find components
    by their locators. Locators can be any values like integers, strings or component types.
    But most often PipServices toolkit uses [[Descriptor]] as locators that match
    by 5 fields: group, type, kind, name and version.

    Example:
        class MyController(IReferences):
            _persistence = None

            def set_references(self, references):
                self._persistence = references.getOneRequired(Descriptor("mygroup", "persistence", "*", "*", "1.0"))

        persistence = MyMongoDbPersistence()

        references = References.from_tuples(
        Descriptor("mygroup", "persistence", "mongodb", "default", "1.0"), persistence,
        Descriptor("mygroup", "controller", "default", "default", "1.0"), controller)

        controller.set_references(references)
    """

    def put(self, locator = None, reference = None):
        """
        Puts a new reference into this reference map.

        :param locator: a component reference to be added.

        :param reference: a locator to find the reference by.
        """
        raise NotImplementedError('Method from interface definition')

    def remove(self, locator):
        """
        Removes a previously added reference that matches specified locator.
        If many references match the locator, it removes only the first one.
        When all references shall be removed, use [[removeAll]] method instead.

        :param locator: a locator to remove reference

        :return: the removed component reference.
        """
        raise NotImplementedError('Method from interface definition')

    def get_all_locators(self):
        """
        Gets locators for all registered component references in this reference map.

        :return: a list with component locators.
        """
        raise NotImplementedError('Method from interface definition')

    def get_all(self):
        """
        Gets all component references registered in this reference map.

        :return: a list with component references.
        """
        raise NotImplementedError('Method from interface definition')

    def get_optional(self, locator):
        """
        Gets all component references that match specified locator.

        :param locator: the locator to find references by.

        :return: a list with matching component references or empty list if nothing was found.
        """
        raise NotImplementedError('Method from interface definition')

    def get_required(self, locator):
        """
        Gets all component references that match specified locator.
        At least one component reference must be present. If it doesn't the method throws an error.

        :param locator: the locator to find references by.

        :return: a list with matching component references.

        :raises: a [[ReferenceException]] when no references found.
        """
        raise NotImplementedError('Method from interface definition')

    def get_one_optional(self, locator):
        """
        Gets an optional component reference that matches specified locator.

        :param locator: the locator to find references by.

        :return: a matching component reference or null if nothing was found.
        """
        raise NotImplementedError('Method from interface definition')

    def get_one_required(self, locator):
        """
        Gets a required component reference that matches specified locator.

        :param locator: the locator to find a reference by.

        :return: a matching component reference.

        :raises: a [[ReferenceException]] when no references found.
        """
        raise NotImplementedError('Method from interface definition')

    def get_one_before(self, reference, locator):
        raise NotImplementedError('Method from interface definition')

    def find(self, locator, required):
        """
        Gets all component references that match specified locator.

        :param locator: the locator to find a reference by.

        :param required: forces to raise an exception if no reference is found.

        :return: a list with matching component references.

        :raises: a [[ReferenceException]] when required is set to true but no references found.
        """
        raise NotImplementedError('Method from interface definition')
