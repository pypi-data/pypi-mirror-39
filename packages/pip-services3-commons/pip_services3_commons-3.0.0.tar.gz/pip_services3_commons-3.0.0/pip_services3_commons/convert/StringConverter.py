# -*- coding: utf-8 -*-
"""
    pip_services3_commons.convert.StringConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    String conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import datetime

class StringConverter():
    """
    Converts arbitrary values into strings using extended conversion rules:
    - Numbers: are converted with '.' as decimal point
    - DateTime: using ISO format
    - Boolean: "true" for true and "false" for false
    - Arrays: as comma-separated list
    - Other objects: using <code>toString()</code> method

    Example:
        value1 = StringConverter.to_string(123.456) // Result: "123.456"
        value2 = StringConverter.to_string(true) // Result: "true"
        value3 = StringConverter.to_string(datetime.datetime(2018,0,1)) // Result: "2018-01-01T00:00:00.00"
        value4 = StringConverter.to_string([1,2,3]) // Result: "1,2,3"
    """
    @staticmethod
    def to_nullable_string(value):
        """
        Converts value into string or returns None when value is None.

        :param value: the value to convert.

        :return: string value or None when value is None.
        """
        if value == None:
            return None
        if type(value) == datetime.date:
            return value.isoformat()
        if type(value) == datetime.datetime:
            if value.tzinfo == None:
                return value.isoformat() + "Z"
            else:
                return value.isoformat()

        if type(value) == list:
            builder = ''
            for element in value:
                if len(builder) > 0:
                    builder = builder + ","
                builder = builder + element
            return builder.__str__()
        return str(value)

    @staticmethod
    def to_string(value):
        """
        Converts value into string or returns "" when value is None.

        :param value: the value to convert.

        :return: string value or "" when value is None.
        """
        return StringConverter.to_string_with_default(value, None)

    @staticmethod
    def to_string_with_default(value, default_value):
        """
        Converts value into string or returns default when value is None.

        :param value: the value to convert.

        :param default_value: the default value.

        :return: string value or default when value is null.
        """
        result = StringConverter.to_nullable_string(value)
        return result if result != None else default_value
