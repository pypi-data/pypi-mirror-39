# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.PropertySchema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Validation schema for object properties
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .Schema import Schema

class PropertySchema(Schema):
    """
    Schema to validate object properties

    Example:
        schema = ObjectSchema().with_property(PropertySchema("id", TypeCode.String))

        schema.validate({ id: "1", name: "ABC" })       // Result: no errors
        schema.validate({ name: "ABC" })                // Result: no errors
        schema.validate({ id: 1, name: "ABC" })         // Result: id type mismatch
    """
    name = None
    value_type = None 

    def __init__(self, name = None, value_type = None):
        """
        Creates a new validation schema and sets its values.

        :param name: (optional) a property name

        :param value_type: (optional) a property type
        """
        super(PropertySchema, self).__init__()
        self.name = name
        self.value_type = value_type

    def _perform_validation(self, path, value, results):
        """
        Validates a given value against the schema and configured validation rules.

        :param path: a dot notation path to the value.

        :param value: a value to be validated.

        :param results: a list with validation results to add new results.
        """
        path = self.name if path == None or len(path) == 0 else path + "." + self.name

        super(PropertySchema, self)._perform_validation(path, value, results)
        self._perform_type_validation(path, self.value_type, value, results)
