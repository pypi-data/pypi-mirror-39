# -*- coding: utf-8 -*-
"""
    pip_services3_commons.convert.JsonConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Json conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import json

from .RecursiveMapConverter import RecursiveMapConverter

class JsonConverter():
    """
    Converts arbitrary values from and to JSON (JavaScript Object Notation) strings.

    Example:
        value1 = JsonConverter.from_json("{\"key\":123}") // Result: { key: 123 }
        value2 = JsonConverter.to_map({ key: 123}) // Result: "{\"key\":123}"
    """
    @staticmethod
    def from_json(value):
        """
        Converts JSON string into a value.

        :param value: the JSON string to convert.

        :return: converted object value or null when value is None.
        """
        if value == None:
            return None

        value = json.loads(value)

    @staticmethod
    def to_json(value):
        """
        Converts value into JSON string.

        :param value: the value to convert.

        :return: JSON string or null when value is None.
        """
        if value == None:
            return None

        return json.dumps(value)

    @staticmethod
    def to_nullable_map(value):
        """
        Converts JSON string into map object or returns null when conversion is not possible.

        :param value: the JSON string to convert.

        :return: Map object value or null when conversion is not supported.
        """
        if value == None:
            return None

        # Parse JSON
        try:
            value = json.loads(value)
            return RecursiveMapConverter.to_nullable_map(value)
        except:
            return None

    @staticmethod
    def to_map(value):
        """
        Converts JSON string into map object or returns empty map when conversion is not possible.

        :param value: the JSON string to convert.

        :return: Map object value or empty object when conversion is not supported.
        """
        result = JsonConverter.to_nullable_map(value)
        return result if result != None else {}

    @staticmethod
    def to_map_with_default(value, default_value):
        """
        Converts JSON string into map object or returns default value when conversion is not possible.

        :param value: the JSON string to convert.

        :param default_value: the default value.

        :return: Map object value or default when conversion is not supported.
        """
        result = JsonConverter.to_nullable_map(value)
        return result if result != None else default_value
