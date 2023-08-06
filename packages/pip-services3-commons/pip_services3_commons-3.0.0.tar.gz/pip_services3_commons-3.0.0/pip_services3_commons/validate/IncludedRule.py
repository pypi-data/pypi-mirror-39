# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.IncludedRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Included rule implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IValidationRule import IValidationRule
from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from ..reflect.ObjectReader import ObjectReader

class IncludedRule(IValidationRule):
    """
    Validation rule to check that value is included into the list of constants.

    Example:
        schema = new Schema().with_rule(IncludedRule(1, 2, 3))

        schema.validate(2)      // Result: no errors
        schema.validate(10)     // Result: 10 must be one of 1, 2, 3
    """
    _values = None

    def __init__(self, *values):
        """
        Creates a new validation rule and sets its values.

        :param values: a list of constants that value must be included to
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

        if not found:
            results.append(
                ValidationResult(
                    path,
                    ValidationResultType.Error,
                    "VALUE_NOT_INCLUDED",
                    name + " must be one of " + str(self._values),
                    self._values,
                    value
                )
            )
