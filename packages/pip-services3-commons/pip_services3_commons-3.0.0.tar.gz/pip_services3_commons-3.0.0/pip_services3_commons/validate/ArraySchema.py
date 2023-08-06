# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.ArraySchema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Array schema implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .Schema import Schema
from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from ..reflect.ObjectReader import ObjectReader

class ArraySchema(Schema):
    """
    Schema to validate arrays.

    Example:
        schema = ArraySchema(TypeCode.String)

        schema.validate(["A", "B", "C"])    // Result: no errors
        schema.validate([1, 2, 3])          // Result: element type mismatch
        schema.validate("A")                // Result: type mismatch
    """
    value_type = None

    def __init__(self, value_type):
        """
        Creates a new instance of validation schema and sets its values.

        :param value_type: a type of array elements. None means that elements may have any type.
        """
        super(ArraySchema, self).__init__()
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

        super(ArraySchema, self)._perform_validation(path, value, results)

        if value == None:
            return

        if isinstance(value, list) or isinstance(value, set) or isinstance(value, tuple):
            index = 0
            for element in value:
                element_path = str(index) if path == None or len(path) == 0 else path + "." + str(index)
                self._perform_type_validation(element_path, self.value_type, element, results)
                index += 1
        else:
            results.append(
                ValidationResult(
                    path,
                    ValidationResultType.Error,
                    "VALUE_ISNOT_ARRAY",
                    name + " type must be List or Array",
                    "List",
                    type(value)
                )
            )
