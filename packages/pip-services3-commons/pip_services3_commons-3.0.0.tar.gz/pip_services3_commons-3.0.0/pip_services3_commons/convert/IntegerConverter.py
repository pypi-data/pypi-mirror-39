# -*- coding: utf-8 -*-
"""
    pip_services3_commons.convert.IntegerConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Integer conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IntegerConverter():
    """
    Converts arbitrary values into integers using extended conversion rules:
    - Strings are converted to floats, then to integers
    - DateTime: total number of milliseconds since unix epoсh
    - Boolean: 1 for true and 0 for false

    Example:
        value1 = IntegerConverter.to_nullable_integer("ABC") // Result: None
        value2 = IntegerConverter.to_nullable_integer("123.456") // Result: 123
        value3 = IntegerConverter.to_nullable_integer(true) // Result: 1
        value4 = IntegerConverter.to_nullable_integer(datetime.datetime.now()) // Result: current milliseconds
    """
    @staticmethod
    def to_nullable_integer(value):
        """
        Converts value into integer or returns null when conversion is not possible.

        :param value: the value to convert.

        :return: integer value or null when conversion is not supported.
        """
        # Shortcuts
        if value == None:
            return None

        try:
            value = float(value)
            return int(value)
        except:
            return None

    @staticmethod
    def to_integer(value):
        """
        Converts value into integer or returns 0 when conversion is not possible.

        :param value: the value to convert.

        :return: integer value or 0 when conversion is not supported.
        """
        return IntegerConverter.to_integer_with_default(value, 0)

    @staticmethod
    def to_integer_with_default(value, default_value):
        """
        Converts value into integer or returns default value when conversion is not possible.

        :param value: the value to convert.

        :param default_value: the default value.

        :return: integer value or default when conversion is not supported.
        """
        result = IntegerConverter.to_nullable_integer(value)
        return result if result != None else default_value
