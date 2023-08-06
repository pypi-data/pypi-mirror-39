# -*- coding: utf-8 -*-
"""
    pip_services3_commons.errors.ErrorDescriptionFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Error description factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import traceback

from .ErrorDescription import ErrorDescription
from .ErrorCategory import ErrorCategory
from .ApplicationException import ApplicationException

class ErrorDescriptionFactory(object):
    """
    Factory to create serializeable [[ErrorDescription]] from [[ApplicationException]]
    or from arbitrary errors.

    The ErrorDescriptions are used to pass errors through the wire between microservices
    implemented in different languages. They allow to restore exceptions on the receiving side
    close to the original type and preserve additional information.
    """
    @staticmethod
    def create(ex):
        """
        Creates a serializable ErrorDescription from error object.

        :param ex: an error object

        :return: a serializeable ErrorDescription object that describes the error.
        """
        description = ErrorDescription()

        if isinstance(ex, ApplicationException):
            description.category = ex.category
            description.status = ex.status
            description.code = ex.code
            description.message = ex.message
            description.details = ex.details
            description.correlation_id = ex.correlation_id
            description.cause = ex.get_cause_string()
            description.stack_trace = ex.get_stack_trace_string()
        elif isinstance(ex, Exception):
            description.category = ErrorCategory.Unknown
            description.status = 500
            description.code = 'UNKNOWN'
            description.message = ex.message
            #description.cause = ex.xxx
            if hasattr(ex, 'tb_trace'):
                description.stack_trace = traceback.format_tb(ex)
        else:
            description.category = ErrorCategory.Unknown
            description.status = 500
            description.code = 'UNKNOWN'
            description.message = str(ex)

        return description
