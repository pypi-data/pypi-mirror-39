# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.ObjectSchema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Object schema implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .Schema import Schema
from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from .PropertySchema import PropertySchema
from ..reflect.ObjectReader import ObjectReader

class ObjectSchema(Schema):
    """
    Schema to validate user defined objects.

    Example:
        schema = ObjectSchema(false)
                            .with_optional_property("id", TypeCode.String)
                            .with_required_property("name", TypeCode.String)

        schema.validate({ id: "1", name: "ABC" })       // Result: no errors
        schema.validate({ name: "ABC" })                // Result: no errors
        schema.validate({ id: 1, name: "ABC" })         // Result: id type mismatch
        schema.validate({ id: 1, _name: "ABC" })        // Result: name is missing, unexpected _name
        schema.validate("ABC")                          // Result: type mismatch
    """
    properties = None
    is_allow_undefined = None

    def __init__(self):
        """
        Creates a new validation schema and sets its values.
        """
        super(ObjectSchema, self).__init__()
        self.is_allow_undefined = False

    def allow_undefined(self, value):
        """
        Sets flag to allow undefined properties

        This method returns reference to this exception to implement Builder pattern
        to chain additional calls.

        :param value: true to allow undefined properties and false to disallow.

        :return: this validation schema.
        """
        self.is_allowUndefined = value
        return self

    def with_property(self, schema):
        """
        Adds a validation schema for an object property.

        This method returns reference to this exception to implement Builder pattern
        to chain additional calls.

        :param schema: a property validation schema to be added.

        :return: this validation schema.
        """
        self.properties = self.properties if self.properties != None else []
        self.properties.append(schema)
        return self

    def with_required_property(self, name, typ, *rules):
        """
        Adds a validation schema for a required object property.

        :param name: a property name.

        :param typ: (optional) a property schema or type.

        :param rules: (optional) a list of property validation rules.

        :return: the validation schema
        """
        self.properties = self.properties if self.properties != None else []
        schema = PropertySchema(name, typ)
        schema.rules = rules
        schema.make_required()
        return self.with_property(schema)

    def with_optional_property(self, name, typ, *rules):
        """
        Adds a validation schema for an optional object property.

        :param name: a property name.

        :param typ: (optional) a property schema or type.

        :param rules: (optional) a list of property validation rules.

        :return: the validation schema
        """
        self.properties = self.properties if self.properties != None else []
        schema = PropertySchema(name, typ)
        schema.rules = rules
        schema.make_optional()
        return self.with_property(schema)

    def _perform_validation(self, path, value, results):
        """
        Validates a given value against the schema and configured validation rules.

        :param path: a dot notation path to the value.

        :param value: a value to be validated.

        :param results: a list with validation results to add new results.
        """
        super(ObjectSchema, self)._perform_validation(path, value, results)

        if value == None:
            return

        name = path if path != None else "value"
        properties = ObjectReader.get_properties(value)

        # Process defined properties
        if self.properties != None:
            for property_schema in self.properties:
                processed_name = None

                for (key, value) in properties.items():
                    # Find properties case insensitive
                    if property_schema.name != None and key.lower() == property_schema.name.lower():
                        property_schema._perform_validation(path, value, results)
                        processed_name = key
                        break

                if processed_name == None:
                    property_schema._perform_validation(path, None, results)
                else:
                    del properties[processed_name]

        # Process unexpected properties
        for (key, value) in properties.items():
            property_path = key if path == None or len(path) == 0 else path + "." + key

            results.append(
                ValidationResult(
                    property_path,
                    ValidationResultType.Warning,
                    "UNEXPECTED_PROPERTY",
                    name + " contains unexpected property " + str(key),
                    None,
                    key
                )
            )
