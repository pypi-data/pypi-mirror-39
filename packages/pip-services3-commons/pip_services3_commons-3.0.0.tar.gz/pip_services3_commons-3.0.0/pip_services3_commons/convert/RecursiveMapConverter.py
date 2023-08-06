# -*- coding: utf-8 -*-
"""
    pip_services3_commons.convert.RecursiveMapConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Recursive map conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class RecursiveMapConverter():
    """
    Converts arbitrary values into map objects using extended conversion rules.
    This class is similar to [[MapConverter]], but is recursively converts all values stored in objects and arrays.

    Example:
        value1 = RecursiveMapConverted.to_nullable_map("ABC") // Result: None
        value2 = RecursiveMapConverted.to_nullable_map({ key: 123 }) // Result: { key: 123 }
        value3 = RecursiveMapConverted.to_nullable_map([1,[2,3]) // Result: { "0": 1, { "0": 2, "1": 3 } }
    """
    @staticmethod
    def _value_to_map(value, classkey = None):
        if isinstance(value, dict):
            data = {}
            for (k, v) in value.items():
                data[k] = RecursiveMapConverter._value_to_map(v, classkey)
            return data
        elif hasattr(value, "_ast"):
            return RecursiveMapConverter._value_to_map(value._ast())
        elif hasattr(value, "__iter__"):
            return [RecursiveMapConverter._value_to_map(v, classkey) for v in value]
        elif hasattr(value, "__dict__"):
            data = {} 
            for k in dir(value):
                v = getattr(value, k)
                if not callable(v) and not k.startswith('_'):
                    data[k] = RecursiveMapConverter._value_to_map(v, classkey)
            if classkey is not None and hasattr(value, "__class__"):
                data[classkey] = value.__class__.__name__
            return data
        else:
            return value

    @staticmethod
    def to_nullable_map(value):
        """
        Converts value into map object or returns null when conversion is not possible.

        :param value: the value to convert.

        :return: map object or null when conversion is not supported.
        """
        if value == None:
            return None

        return RecursiveMapConverter._value_to_map(value)

    @staticmethod
    def to_map(value):
        """
        Converts value into map object or returns empty map when conversion is not possible

        :param value: the value to convert.

        :return: map object or empty map when conversion is not supported.
        """
        result = RecursiveMapConverter.to_nullable_map(value)
        return result if result != None else {}

    @staticmethod
    def to_map_with_default(value, default_value):
        """
        Converts value into map object or returns default when conversion is not possible

        :param value: the value to convert.

        :param default_value: the default value.

        :return: map object or emptu map when conversion is not supported.
        """
        result = RecursiveMapConverter.to_nullable_map(value)
        return result if result != None else default_value
