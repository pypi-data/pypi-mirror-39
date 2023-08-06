# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.PropertiesComparisonRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Properties comparison rule implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IValidationRule import IValidationRule
from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from .ObjectComparator import ObjectComparator
from ..reflect.ObjectReader import ObjectReader

class PropertiesComparisonRule(IValidationRule):
    """
    Validation rule that compares two object properties.

    Example:
        schema = ObjectSchema().with_rule(PropertyComparisonRule("field1", "NE", "field2"))

        schema.validate({ field1: 1, field2: 2 })       // Result: no errors
        schema.validate({ field1: 1, field2: 1 })       // Result: field1 shall not be equal to field2
        schema.validate({})                             // Result: no errors
    """
    _property1 = None
    _property2 = None
    _operation = None

    def __init__(self, property1, operation, property2):
        """
        Creates a new validation rule and sets its arguments.

        :param property1: a name of the first property to compare.

        :param operation: a comparison operation: "==" ("=", "EQ"), "!= " ("<>", "NE");
                                                  "<"/">" ("LT"/"GT"), "<="/">=" ("LE"/"GE"); "LIKE".

        :param property2: a name of the second property to compare.
        """
        self._property1 = property1
        self._operation = operation
        self._property2 = property2

    def validate(self, path, schema, value, results):
        """
        Validates a given value against this rule.

        :param path: a dot notation path to the value.

        :param schema: a schema this rule is called from

        :param value: a value to be validated.

        :param results: a list with validation results to add new results.
        """
        name = path if path != None else "value"
        value1 = ObjectReader.get_property(value, self._property1)
        value2 = ObjectReader.get_property(value, self._property2)

        if not ObjectComparator.compare(value1, self._operation, value2):
            results.append(
                ValidationResult(
                    path,
                    ValidationResultType.Error,
                    "PROPERTIES_NOT_MATCH",
                    name + " must have " + str(self._property1) + " " + str(self._operation) + " " + str(self._property2),
                    value2,
                    value1
                )
            )
