# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.ValueComparisonRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Value comparison rule implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IValidationRule import IValidationRule
from .ObjectComparator import ObjectComparator
from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult

class ValueComparisonRule(IValidationRule):
    """
    Validation rule that compares value to a constant.

    Example:
        schema = Schema().with_rule(ValueComparisonRule("EQ", 1))

        schema.validate(1)          // Result: no errors
        schema.validate(2)          // Result: 2 is not equal to 1
    """
    _operation = None
    _value = None

    def __init__(self, operation, value):
        """
        Creates a new validation rule and sets its values.

        :param operation: a comparison operation: "==" ("=", "EQ"), "!= " ("<>", "NE");
                                                  "<"/">" ("LT"/"GT"), "<="/">=" ("LE"/"GE"); "LIKE".

        :param value: a constant value to compare to
        """
        self._operation = operation
        self._value = value

    def validate(self, path, schema, value, results):
        """
        Validates a given value against this rule.

        :param path: a dot notation path to the value.

        :param schema: a schema this rule is called from

        :param value: a value to be validated.

        :param results: a list with validation results to add new results.
        """
        name = path if path != None else "value"

        if not ObjectComparator.compare(value, self._operation, self._value):
            results.append(
                ValidationResult(
                    path,
                    ValidationResultType.Error,
                    "BAD_VALUE",
                    name + " must " + str(self._operation) + " " + str(self._value) + " but found " + str(value),
                    str(self._operation) + " " + str(self._value),
                    value
                )
            )

