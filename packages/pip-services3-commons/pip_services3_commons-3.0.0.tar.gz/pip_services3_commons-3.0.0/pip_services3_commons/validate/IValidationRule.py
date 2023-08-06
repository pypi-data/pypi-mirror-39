# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.IValidationRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for schema validation rules.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IValidationRule(object):
    """
    Interface for validation rules.
    Validation rule can validate one or multiple values
    against complex rules like: value is in range, one property is less than another property,
    enforce enumerated values and more.

    This interface allows to implement custom rules.
    """
    def validate(self, path, schema, value, results):
        """
        Validates a given value against this rule.

        :param path: a dot notation path to the value.

        :param schema: a schema this rule is called from

        :param value: a value to be validated.

        :param results: a list with validation results to add new results.
        """
        raise NotImplementedError('Method from interface definition')