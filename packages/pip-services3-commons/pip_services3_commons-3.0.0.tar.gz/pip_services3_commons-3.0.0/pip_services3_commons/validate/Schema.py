# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.Schema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Validation schema for complex objects.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from .ValidationException import ValidationException
from ..reflect.ObjectReader import ObjectReader
from ..reflect.TypeMatcher import TypeMatcher
from ..convert.TypeConverter import TypeConverter

class Schema(object):
    """
    Basic schema that validates values against a set of validation rules.

    This schema is used as a basis for specific schemas to validate
    objects, project properties, arrays and maps.
    """
    required = None
    rules = None

    def __init__(self, required = False, rules = None):
        """
        Creates a new instance of validation schema and sets its values.

        :param required: (optional) true to always require non-null values.

        :param rules: (optional) a list with validation rules.
        """
        self.required = required
        self.rules = rules if rules != None else []

    def make_required(self):
        """
        Makes validated values always required (non-null).
        For null values the schema will raise errors.

        This method returns reference to this exception to implement Builder pattern
        to chain additional calls.

        :return: this validation schema
        """
        self.required = True
        return self

    def make_optional(self):
        """
        Makes validated values optional.
        Validation for null values will be skipped.

        This method returns reference to this exception to implement Builder pattern
        to chain additional calls.

        :return: this validation schema
        """
        self.required = False
        return self

    def with_rule(self, rule):
        """
        Adds validation rule to this schema.

        This method returns reference to this exception to implement Builder pattern
        to chain additional calls.

        :param rule: a validation rule to be added.

        :return: this validation schema.
        """
        self.rules = self.rules if self.rules != None else []
        self.rules.append(rule)
        return self

    def _perform_validation(self, path, value, results):
        """
        Validates a given value against the schema and configured validation rules.

        :param path: a dot notation path to the value.

        :param value: a value to be validated.

        :param results: a list with validation results to add new results.
        """
        name = path if path != None else "value"

        if value == None:
            # Check for required values
            if self.required:
                results.append(
                    ValidationResult(
                        path,
                        ValidationResultType.Error,
                        "VALUE_IS_NULL",
                        name + " cannot be null",
                        "NOT NULL",
                        None
                    )
                )
        else:
            value = ObjectReader.get_value(value)

            # Check validation rules
            if self.rules != None:
                for rule in self.rules:
                    rule.validate(path, self, value, results)

    def _type_to_string(self, typ):
        if typ == None:
            return "unknown"
        return TypeConverter.to_string(typ)

    def _perform_type_validation(self, path, typ, value, results):
        """
        Validates a given value to match specified type.
        The type can be defined as a Schema, type, a type name or [[TypeCode]].
        When type is a Schema, it executes validation recursively against that Schema.

        :param path: a dot notation path to the value.

        :param typ: a type to match the value type

        :param value: a value to be validated.

        :param results: a list with validation results to add new results.
        """
        # If type it not defined then skip
        if typ == None:
            return

        # Perform validation against schema
        if isinstance(typ, Schema):
            schema = typ
            schema._perform_validation(path, value, results)
            return

        # If value is null then skip
        value = ObjectReader.get_value(value)
        if value == None:
            return

        name = path if path != None else "value"
        value_type = type(value)

        # Match types
        if TypeMatcher.match_type(typ, value_type):
            return
        
        # Generate type mismatch error
        results.append(
            ValidationResult(
                path,
                ValidationResultType.Error,
                "TYPE_MISMATCH",
                name + " type must be " + self._type_to_string(typ) + " but found " + self._type_to_string(value_type),
                typ,
                value_type
            )
        )

    def validate(self, value):
        """
        Validates the given value and results validation results.

        :param value: a value to be validated.

        :return: a list with validation results.
        """
        results = []
        self._perform_validation("", value, results)
        return results

    def validate_and_throw_exception(self, correlation_id, value, strict = False):
        """
        Validates the given value and throws a [[ValidationException]] if errors were found.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param value: a value to be validated.

        :param strict: true to treat warnings as errors.
        """
        results = self.validate(value)
        ValidationException.throw_exception_if_needed(correlation_id, results, strict)
