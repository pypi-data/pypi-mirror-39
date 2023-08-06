# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.NotRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Not rule implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IValidationRule import IValidationRule
from .ValidationResult import ValidationResult
from .ValidationResultType import ValidationResultType

class NotRule(IValidationRule):
    """
    Validation rule negate another rule.
    When embedded rule returns no errors, than this rule return an error.
    When embedded rule return errors, than the rule returns no errors.

    Example:
        schema = Schema().with_rule(NotRule(ValueComparisonRule("EQ", 1)))

        schema.validate(1)          // Result: error
        schema.validate(5)          // Result: no error
    """
    _rule = None

    def __init__(self, rule):
        """
        Creates a new validation rule and sets its values

        :param rule: a rule to be negated.
        """
        self._rule = rule
    
    def validate(self, path, schema, value, results):
        """
        Validates a given value against this rule.

        :param path: a dot notation path to the value.

        :param schema: a schema this rule is called from

        :param value: a value to be validated.

        :param results: a list with validation results to add new results.
        """
        if self._rule == None:
            return

        name = path if path != None else "value"
        local_results = []

        self._rule.validate(path, schema, value, local_results)

        if len(local_results) > 0:
            return

        results.append(ValidationResult(
            path,
            ValidationResultType.Error,
            'NOT_FAILED',
            'Negative check for ' + name + ' failed',
            None,
            None
        ))
