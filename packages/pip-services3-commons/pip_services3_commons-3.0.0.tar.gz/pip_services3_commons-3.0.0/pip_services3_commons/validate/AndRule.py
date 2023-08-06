# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.AndRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    And rule implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IValidationRule import IValidationRule

class AndRule(IValidationRule):
    """
    Validation rule to combine rules with AND logical operation.
    When all rules returns no errors, than this rule also returns no errors.
    When one of the rules return errors, than the rules returns all errors.

    Example:
        schema = Schema().with_rule(AndRule(ValueComparisonRule("GTE", 1), ValueComparisonRule("LTE", 10)))

        schema.validate(0)          // Result: 0 must be greater or equal to 1
        schema.validate(5)          // Result: no error
        schema.validate(20)         // Result: 20 must be letter or equal 10
    """
    _rules = None

    def __init__(self, *rules):
        """
        Creates a new validation rule and sets its values.

        :param rules: a list of rules to join with AND operator
        """
        self._rules = rules
    
    def validate(self, path, schema, value, results):
        """
        Validates a given value against this rule.

        :param path: a dot notation path to the value.

        :param schema: a schema this rule is called from

        :param value: a value to be validated.

        :param results: a list with validation results to add new results.
        """
        if self._rules == None:
            return

        for rule in self._rules:
            rule.validate(path, schema, value, results)
