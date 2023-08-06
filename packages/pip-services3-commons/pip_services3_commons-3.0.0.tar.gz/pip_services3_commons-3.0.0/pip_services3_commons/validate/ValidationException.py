# -*- coding: utf-8 -*-
"""
    pip_services_common.validate.ValidationException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Validation exception type
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from ..errors.BadRequestException import BadRequestException

class ValidationException(BadRequestException):
    """
    Errors in schema validation.

    Validation errors are usually generated based in [[ValidationResult]].
    If using strict mode, warnings will also raise validation exceptions.
    """
    def __init__(self, correlation_id, results):
        """
        Creates a new instance of validation exception and assigns its values.

        :param correlation_id: (optional) a unique transaction id to trace execution through call chain.

        :param results: (optional) a list of validation results
        """
        message = ValidationException.compose_message(results)
        super(BadRequestException, self).__init__(correlation_id, 'INVALID_DATA', message)

    @staticmethod
    def compose_message(results):
        """
        Composes human readable error message based on validation results.

        :param results: a list of validation results.

        :return: a composed error message.
        """
        message = ''
        message += 'Validation failed'

        if results != None and len(results) > 0:
            first = True
            for result in results:
                if result.type != ValidationResultType.Information:
                    if not first: 
                        message += ': '
                    else:
                        message += ', '
                    message += result.message
                    first = False

        return message

    @staticmethod
    def throw_exception_if_needed(correlation_id, results, strict):
        """
        Throws ValidationException based on errors in validation results.
        If validation results have no errors, than no exception is thrown.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param results: list of validation results that may contain errors

        :param strict: true to treat warnings as errors.
        """
        has_errors = False
        for result in results:
            if result.type == ValidationResultType.Error:
                has_errors = True
            if strict and result.type == ValidationResultType.Warning:
                has_errors = True

        if has_errors:
            raise ValidationException(correlation_id, results)
