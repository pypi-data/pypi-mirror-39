# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.ExcludedRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Excluded rule implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IValidationRule import IValidationRule
from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from ..reflect.ObjectReader import ObjectReader

class ExcludedRule(IValidationRule):
    """
    Validation rule to check that value is excluded from the list of constants.

    Example:
        schema = Schema().with_rule(ExcludedRule(1, 2, 3))

        schema.validate(2)      // Result: 2 must not be one of 1, 2, 3
        schema.validate(10)     // Result: no errors
    """
    _values = None

    def __init__(self, *values):
        """
        Creates a new validation rule and sets its values.

        :param values: a list of constants that value must be excluded from
        """
        self._values = values

    def validate(self, path, schema, value, results):
        """
        Validates a given value against this rule.

        :param path: a dot notation path to the value.

        :param schema: a schema this rule is called from

        :param value: a value to be validated.

        :param results: a list with validation results to add new results.
        """
        name = path if path != None else "value"
        found = False

        for this_value in self._values:
            if this_value != None and this_value == value:
                found = True
                break

        if found:
            results.append(
                ValidationResult(
                    path,
                    ValidationResultType.Error,
                    "VALUE_INCLUDED",
                    name + " must not be one of " + str(self._values),
                    self._values,
                    value
                )
            )
