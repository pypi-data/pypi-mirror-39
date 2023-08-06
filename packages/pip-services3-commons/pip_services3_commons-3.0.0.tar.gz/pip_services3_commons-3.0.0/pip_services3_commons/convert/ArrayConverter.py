# -*- coding: utf-8 -*-
"""
    pip_services3_commons.convert.ArrayConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Array conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ArrayConverter():
    """
    Converts arbitrary values into array objects.
    Example:
        [code]
        value1 = ArrayConverter.to_array([1, 2])		 // Result: [1, 2]
        value2 = ArrayConverter.to_array(1)			  // Result: [1]
        value2 = ArrayConverter.list_to_array("1,2,3")	// Result: ["1", "2", "3"]
        [/code]
    """
    @staticmethod
    def to_nullable_array(value):
        """
        Converts value into array object.
        Single values are converted into arrays with a single element.

        :param value: the value to convert.

        :return: array object or None when value is None.
        """
        # Shortcuts
        if value == None:
            return None
        if type(value) == list:
            return value 

        if type(value) in [tuple, set]:
            return list(value)
            
        return [value]

    @staticmethod
    def to_array(value):
        """
        Converts value into array object with empty array as default.
        Single values are converted into arrays with single element.

        :param value: the value to convert.

        :return: array object or empty array when value is None.
        """
        return ArrayConverter.to_array_with_default(value, [])

    @staticmethod
    def to_array_with_default(value, default_value):
        """
        Converts value into array object with specified default.
        Single values are converted into arrays with single element.

        :param value: the value to convert.

        :param default_value: default array object.

        :return: array object or default array when value is None.
        """
        result = ArrayConverter.to_nullable_array(value)
        return result if result != None else default_value

    @staticmethod
    def list_to_array(value):
        """
        Converts value into array object with empty array as default.
        Strings with comma-delimited values are split into array of strings.

        :param value: the list to convert.

        :return: array object or empty array when value is None
        """
        if value == None:
            return []
        elif type(value) in [list, tuple, set]:
            return list(value)
        elif type(value) in [str]:
            return value.split(',')
        else:
            return [value]
