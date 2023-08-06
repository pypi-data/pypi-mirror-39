# -*- coding: utf-8 -*-
"""
    pip_services_common.errors.InvalidStateException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    InvalidState exception type
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory
from .ApplicationException import ApplicationException

class InvalidStateException(ApplicationException):
    """
    Errors related to calling operations, which require the component to be in a specific state.

    For instance, business calls when component is not ready
    """

    def __init__(self, correlation_id = None, code = None, message = None):
        """
        Creates an error instance and assigns its values.

        :param correlation_id: (optional) a unique transaction id to trace execution through call chain.

        :param code: (optional) a unique error code. Default: "UNKNOWN"

        :param message: (optional) a human-readable description of the error.
        """
        super(InvalidStateException, self).__init__(ErrorCategory.InvalidState, correlation_id, code, message)
        self.status = 500
