# -*- coding: utf-8 -*-
"""
    pip_services3_commons.refer.DependencyResolver
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Dependency resolver component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IReferenceable import IReferenceable
from ..config.IReconfigurable import IReconfigurable
from ..convert.StringConverter import StringConverter
from ..refer.Descriptor import Descriptor
from ..refer.ReferenceException import ReferenceException

class DependencyResolver(IReconfigurable, IReferenceable):
    """
    Helper class for resolving component dependencies.
    The resolver is configured to resolve named dependencies by specific locator.
    During deployment the dependency locator can be changed.

    This mechanism can be used to clarify specific dependency among several alternatives.
    Typically components are configured to retrieve the first dependency that matches
    logical group, type and version. But if container contains more than one instance
    and resolution has to be specific about those instances, they can be given a unique
    name and dependency resolvers can be reconfigured to retrieve dependencies by their name.

    Configuration parameters

    dependencies:
        - [dependency name 1]: Dependency 1 locator (descriptor)
        - ...
        - [dependency name N]: Dependency N locator (descriptor)

    References:
        - References must match configured dependencies.

    Example:
        class MyComponent(IConfigurable, IReferenceable):
            _dependencyResolver = None
            _persistence = None

            def __init__(self):
                self._dependencyResolver.put("persistence", new Descriptor("mygroup", "persistence", "*", "*", "1.0"))

            def configure(self, config):
                self._dependencyResolver.configure(config)

            def set_references(self, references):
                self._dependencyResolver.setReferences(references)
                self._persistence = self._dependencyResolver.get_one_required("persistence")

            component = MyComponent()
            component.configure(ConfigParams.from_tuples(
            "dependencies.persistence", "mygroup:persistence:*:persistence2:1.0"))

            component.setReferences(References.from_tuples(Descriptor("mygroup","persistence","*","persistence1","1.0"),
            MyPersistence(),
            Descriptor("mygroup","persistence","*","persistence2","1.0"), MyPersistence()
            // This dependency shall be set))
    """
    _dependencies = None
    _references = None

    def __init__(self, config = None, references = None):
        """
        Creates a new instance of the dependency resolver.

        :param config: (optional) default configuration where key is dependency name and value is locator (descriptor)

        :param references: (optional) default component references
        """
        self._dependencies = {}
        if config != None:
            self.configure(config)
        if references != None:
            self.set_references(references)

    def configure(self, config):
        """
        Configures the component with specified parameters.

        :param config: configuration parameters to set.
        """
        dependencies = config.get_section("dependencies")
        names = dependencies.get_key_names()
        for name in names:
            locator = dependencies.get(name)
            if locator == None:
                continue
            
            try:
                descriptor = Descriptor.from_string(locator)
                if descriptor != None:
                    self._dependencies[name] = descriptor
                else:
                    self._dependencies[name] = locator
            except Exception as ex:
                self._dependencies[name] = locator


    def set_references(self, references):
        """
        Sets the component references. References must match configured dependencies.

        :param references: references to set.
        """
        self._references = references


    def put(self, name, locator):
        """
        Adds a new dependency into this resolver.

        :param name: the dependency's name.

        :param locator: the locator to find the dependency by.
        """
        self._dependencies[name] = locator


    def _locate(self, name):
        """
        Gets a dependency locator by its name.

        :param name: the name of the dependency to locate.
        :return: the dependency locator or null if locator was not configured.
        """
        if name == None:
            raise Exception("Dependency name cannot be null")
        if self._references == None:
            raise Exception("References shall be set")
        
        return self._dependencies.get(name)


    def get_optional(self, name):
        """
        Gets all optional dependencies by their name.

        :param name: the dependency name to locate.

        :return: a list with found dependencies or empty list of no dependencies was found.
        """
        locator = self._locate(name)
        return self._references.get_optional(locator) if locator != None else None


    def get_required(self, name):
        """
        Gets all required dependencies by their name.
        At least one dependency must be present. If no dependencies was found it throws a [[ReferenceException]]

        :param name: the dependency name to locate.

        :return: a list with found dependencies.
        """
        locator = self._locate(name)
        if locator == None:
            raise ReferenceException(None, name)
        
        return self._references.get_required(locator)


    def get_one_optional(self, name):
        """
        Gets one optional dependency by its name.

        :param name: the dependency name to locate.

        :return: a dependency reference or null of the dependency was not found
        """
        locator = self._locate(name)
        return self._references.get_one_optional(locator) if locator != None else None


    def get_one_required(self, name):
        """
        Gets one required dependency by its name.
        At least one dependency must present. If the dependency was found it throws a [[ReferenceException]]

        :param name: the dependency name to locate.

        :return: a dependency reference
        """
        locator = self._locate(name)
        if locator == None:
            raise ReferenceException(None, name)
        
        return self._references.get_one_required(locator)


    def find(self, name, required):
        """
        Finds all matching dependencies by their name.

        :param name: the dependency name to locate.

        :param required: true to raise an exception when no dependencies are found.

        :return: a list of found dependencies
        """
        if name == None:
            raise Exception("Name cannot be null")
        
        locator = self._locate(name)
        if locator == None:
            if required:
                raise ReferenceException(None, name)
            return None
        
        return self._references.find(locator, required)


    @staticmethod
    def from_tuples(*tuples):
        """
        Creates a new DependencyResolver from a list of key-value pairs called tuples
        where key is dependency name and value the depedency locator (descriptor).

        :param tuples: a list of values where odd elements are dependency name
        and the following even elements are dependency locator (descriptor)

        :return: a newly created DependencyResolver.
        """
        result = DependencyResolver()
        if tuples == None or len(tuples) == 0:
            return result
        
        index = 0
        while index < len(tuples):
            if index + 1 >= len(tuples):
                break

            name = StringConverter.to_string(tuples[index])
            locator = tuples[index + 1]

            result.put(name, locator)
            index = index + 2
        
        return result
