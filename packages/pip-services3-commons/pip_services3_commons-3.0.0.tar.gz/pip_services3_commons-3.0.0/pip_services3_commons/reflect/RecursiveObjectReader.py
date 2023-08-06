# -*- coding: utf-8 -*-
"""
    pip_services3_commons.reflect.RecursiveObjectReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Recursive object reader implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..convert.TypeCode import TypeCode
from ..convert.TypeConverter import TypeConverter
from .ObjectReader import ObjectReader

class RecursiveObjectReader:
    """
    Helper class to perform property introspection and dynamic reading.

    It is similar to [[ObjectReader]] but reads properties recursively
    through the entire object graph. Nested property names are defined
    using dot notation as "object.subobject.property"
    """
    @staticmethod
    def _perform_has_property(obj, names, name_index):
        if name_index < len(names) - 1:
            value  = ObjectReader.get_property(obj, names[name_index])
            if value != None:
                return RecursiveObjectReader._perform_has_property(value, names, name_index + 1)
            else:
                return False
        else:
            return ObjectReader.has_property(obj, names[name_index])


    @staticmethod
    def has_property(obj, name):
        """
        Checks recursively if object or its subobjects has a property with specified name.

        The object can be a user defined object, map or array.
        The property name correspondently must be object property, map key or array index.

        :param obj: an object to introspect.

        :param name: a name of the property to check.

        :return: true if the object has the property and false if it doesn't.
        """
        if obj == None or name == None:
            return False

        names = name.split(".")
        if names == None or len(names) == 0: 
            return False

        return RecursiveObjectReader._perform_has_property(obj, names, 0)

    
    @staticmethod
    def _perform_get_property(obj, names, name_index):
        if name_index < len(names) - 1:
            value = ObjectReader.get_property(obj, names[name_index])
            if value != None:
                return RecursiveObjectReader._perform_get_property(value, names, name_index + 1)
            else:
                return None
        else:
            return ObjectReader.get_property(obj, names[name_index])


    @staticmethod
    def get_property(obj, name):
        """
        Recursively gets value of object or its subobjects property specified by its name.

        The object can be a user defined object, map or array.
        The property name correspondently must be object property, map key or array index.

        :param obj: an object to read property from.

        :param name: a name of the property to get.

        :return: the property value or null if property doesn't exist or introspection failed.
        """
        if obj == None or name == None:
            return None

        names = name.split(".")
        if names == None or len(names) == 0:
            return None

        return RecursiveObjectReader._perform_get_property(obj, names, 0)


    @staticmethod
    def _is_simple_value(value):
        code = TypeConverter.to_type_code(value)
        return code != TypeCode.Array and code != TypeCode.Map and code != TypeCode.Object


    @staticmethod
    def _perform_get_property_names(obj, path, result, cycle_detect):
        map = ObjectReader.get_properties(obj)
        
        if len(map) != 0 and len(cycle_detect) < 100:
            cycle_detect.append(obj)
            try:
                for (key, value) in map.items():
                    # Prevent cycles 
                    if value in cycle_detect:
                        continue

                    key = path + "." + key if path != None else key
                    
                    # Add simple values directly
                    if RecursiveObjectReader._is_simple_value(value):
                        result.append(key)
                    # Recursively go to elements
                    else:
                        RecursiveObjectReader._perform_get_property_names(value, key, result, cycle_detect)
            finally:
                cycle_detect.remove(obj)
        else:
            if path != None:
                result.append(path)


    @staticmethod
    def get_property_names(obj):
        """
        Recursively gets names of all properties implemented in specified object and its subobjects.

        The object can be a user defined object, map or array.
        Returned property name correspondently are object properties, map keys or array indexes.

        :param obj: an object to introspect.

        :return: a list with property names.
        """
        property_names = []
        
        if obj != None:
            cycle_detect = []
            RecursiveObjectReader._perform_get_property_names(obj, None, property_names, cycle_detect)

        return property_names

    @staticmethod
    def _perform_get_properties(obj, path, result, cycle_detect):
        map = ObjectReader.get_properties(obj)
        
        if len(map) != 0 and len(cycle_detect) < 100:
            cycle_detect.append(obj)
            try:
                for (key, value) in map.items():
                    # Prevent cycles 
                    if value in cycle_detect:
                        continue

                    key = path + "." + key if path != None else key
                    
                    # Add simple values directly
                    if RecursiveObjectReader._is_simple_value(value):
                        result[key] = value
                    # Recursively go to elements
                    else:
                        RecursiveObjectReader._perform_get_properties(value, key, result, cycle_detect)
            finally:
                cycle_detect.remove(obj)
        else:
            if path != None:
                result[path] = obj


    @staticmethod
    def get_properties(obj):
        """
        Get values of all properties in specified object and its subobjects and returns them as a map.

        The object can be a user defined object, map or array.
        Returned properties correspondently are object properties, map key-pairs or array elements with their indexes.

        :param obj: an object to get properties from.

        :return: a map, containing the names of the object's properties and their values.
        """
        properties = {}
        
        if obj != None:
            cycle_detect = []
            RecursiveObjectReader._perform_get_properties(obj, None, properties, cycle_detect)

        return properties
