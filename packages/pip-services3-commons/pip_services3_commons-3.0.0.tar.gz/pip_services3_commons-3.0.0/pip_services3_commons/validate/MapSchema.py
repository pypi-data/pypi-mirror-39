# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.MapSchema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Map schema implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .Schema import Schema
from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from ..reflect.ObjectReader import ObjectReader

class MapSchema(Schema):
    """
    Schema to validate maps.

    Example:
        schema = MapSchema(TypeCode.String, TypeCode.Integer)
        schema.validate({ "key1": "A", "key2": "B" })       // Result: no errors
        schema.validate({ "key1": 1, "key2": 2 })           // Result: element type mismatch
        schema.validate([ 1, 2, 3 ])                        // Result: type mismatch
    """
    key_type = None
    value_type = None

    def __init__(self, key_type = None, value_type = None):
        """
        Creates a new instance of validation schema and sets its values.

        :param key_type: a type of map keys. Null means that keys may have any type.

        :param value_type: a type of map values. Null means that values may have any type.
        """
        super(MapSchema, self).__init__()
        self.key_type = key_type
        self.value_type = value_type

    def _perform_validation(self, path, value, results):
        """
        Validates a given value against the schema and configured validation rules.

        :param path: a dot notation path to the value.

        :param value: a value to be validated.

        :param results: a list with validation results to add new results.
        """
        name = path if path != None else "value"
        value = ObjectReader.get_value(value)

        super(MapSchema, self)._perform_validation(path, value, results)

        if value == None:
            return

        if isinstance(value, dict):
            for (key, value) in value.items():
                element_path = key if path == None or len(path) == 0 else path + "." + key

                self._perform_type_validation(element_path, self.key_type, key, results)
                self._perform_type_validation(element_path, self.value_type, value, results)
        else:
            results.append(
                ValidationResult(
                    path,
                    ValidationResultType.Error,
                    "VALUE_ISNOT_MAP",
                    name + " type is expected to be Map",
                    "Map",
                    type(value)
                )
            )
