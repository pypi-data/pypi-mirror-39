# -*- coding: utf-8 -*-
"""
    pip_services3_commons.reflect.PropertyReflector
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Property reflector implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class PropertyReflector:
    """
    Helper class to perform property introspection and dynamic reading and writing.

    This class has symmetric implementation across all languages supported
    by Pip.Services toolkit and used to support dynamic data processing.

    Because all languages have different casing and case sensitivity rules,
    this PropertyReflector treats all property names as case insensitive.

    Example:
        myObj = MyObject()

        properties = PropertyReflector.get_property_names()
        PropertyReflector.has_property(myObj, "myProperty")

        value = PropertyReflector.get_property(myObj, "myProperty")
        PropertyReflector.set_property(myObj, "myProperty", 123)
    """
    @staticmethod
    def _is_property(property, name):
        if callable(property):
            return False

        if name.startswith("_"):
            return False

        return True 


    @staticmethod
    def has_property(obj, name):
        """
        Checks if object has a property with specified name.

        :param obj: an object to introspect.

        :param name: a name of the property to check.

        :return: true if the object has the property and false if it doesn't.
        """
        if obj == None:
            raise Exception("Object cannot be null")
        if name == None:
            raise Exception("Property name cannot be null")

        name = name.lower()

        for property_name in dir(obj): 
            if property_name.lower() != name:
                continue

            property = getattr(obj, property_name)

            if PropertyReflector._is_property(property, property_name):
                return True
        
        return False


    @staticmethod
    def get_property(obj, name):
        """
        Gets value of object property specified by its name.

        :param obj: an object to read property from.

        :param name: a name of the property to get.

        :return: the property value or null if property doesn't exist or introspection failed.
        """
        if obj == None:
            raise Exception("Object cannot be null")
        if name == None:
            raise Exception("Property name cannot be null")
        
        name = name.lower()
        
        try:
            for property_name in dir(obj): 
                if property_name.lower() != name:
                    continue

                property = getattr(obj, property_name)

                if PropertyReflector._is_property(property, property_name):
                    return property
        except:
            pass
        
        return None


    @staticmethod
    def get_property_names(obj):
        """
        Gets names of all properties implemented in specified object.

        :param obj: an objec to introspect.

        :return: a list with property names.
        """
        property_names = []
        
        for property_name in dir(obj):

            property = getattr(obj, property_name)

            if PropertyReflector._is_property(property, property_name):
                property_names.append(property_name)

        return property_names


    @staticmethod
    def get_properties(obj):
        """
        Get values of all properties in specified object and returns them as a map.

        :param obj: an object to get properties from.

        :return: a map, containing the names of the object's properties and their values.
        """
        properties = {}
        
        for property_name in dir(obj):

            property = getattr(obj, property_name)

            if PropertyReflector._is_property(property, property_name):
                properties[property_name] = property

        return properties


    @staticmethod
    def set_property(obj, name, value):
        """
        Sets value of object property specified by its name.

        If the property does not exist or introspection fails
        this method doesn't do anything and doesn't any throw errors.

        :param obj: an object to write property to.

        :param name: a name of the property to set.

        :param value: a new value for the property to set.
        """
        if obj == None:
            raise Exception("Object cannot be null")
        if name == None:
            raise Exception("Property name cannot be null")
        
        name = name.lower()
        
        try:
            for property_name in dir(obj): 
                if property_name.lower() != name:
                    continue

                property = getattr(obj, property_name)

                if PropertyReflector._is_property(property, property_name):
                    setattr(obj, property_name, value)
        except:
            pass


    @staticmethod
    def set_properties(obj, values):
        """
        Sets values of some (all) object properties.

        If some properties do not exist or introspection fails
        they are just silently skipped and no errors thrown.

        :param obj: an object to write properties to.

        :param values: a map, containing property names and their values.
        """
        if values == None or len(values) == 0:
            return

        for (name, value) in values:
            PropertyReflector.set_property(obj, name, value)

