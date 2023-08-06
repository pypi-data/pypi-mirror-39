# -*- coding: utf-8 -*-
"""
    pip_services3_commons.errors.ApplicationException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Application exception type
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import traceback

from .ErrorCategory import ErrorCategory

class ApplicationException(Exception):
    """
    Defines a base class to defive various application exceptions.

    Most languages have own definition of base exception (error) types.
    However, this class is implemented symmetrically in all languages
    supported by PipServices toolkit. It allows to create portable implementations
    and support proper error propagation in microservices calls.

    Error propagation means that when microservice implemented in one language
    calls microservice(s) implemented in a different language(s), errors are returned
    throught the entire call chain and restored in their original (or close) type.

    Since number of potential exception types is endless, PipServices toolkit
    supports only 12 standard categories of exceptions defined in [[ErrorCategory]].
    This [[ApplicationException]] class acts as a basis for all other 12 standard exception types.

    Most exceptions have just free-form message that describes occured error.
    That may not be sufficient to create meaninful error descriptions.
    The [[ApplicationException]] class proposes an extended error definition that has more standard fields:
    - message: is a human-readable error description
    - category: one of 12 standard error categories of errors
    - status: numeric HTTP status code for REST invocations
    - code: a unique error code, usually defined as "MY_ERROR_CODE"
    - correlation_id: a unique transaction id to trace execution through a call chain
    - details: map with error parameters that can help to recreate meaningful error description in other languages
    - stack_trace: a stack trace
    - cause: original error that is wrapped by this exception

    ApplicationException class is not serializable. To pass errors through the wire
    it is converted into [[ErrorDescription]] object and restored on receiving end into identical exception type.
    """

    message = None
    category = ErrorCategory.Unknown
    status = 500
    code = 'UNKNOWN'
    details = None
    correlation_id = None
    stack_trace = None
    cause = None
    
    def __init__(self, category = ErrorCategory.Unknown, correlation_id = None, code = 'UNKNOWN', message = 'Unknown error'):
        """
        Creates a new instance of application exception and assigns its values.

        :param category: (optional) a standard error category. Default: Unknown

        :param correlation_id: (optional) a unique transaction id to trace execution through call chain.

        :param code: (optional) a unique error code. Default: "UNKNOWN"

        :param message: (optional) a human-readable description of the error.
        """
        super(ApplicationException, self).__init__(message)
        
        self.message = message
        self.correlation_id = correlation_id;
        self.code = code
        self.category = category
        self.name = code
        self.stack_trace = traceback.format_exc()
        
    def __str__(self):
        return str(self.message) if self.message != None else 'Unknown error'

    def to_json(self):
        return { 
            'category': self.category,
            'code': self.code,
            'status': self.status,
            'details': self.details,
            'correlation_id': self.correlation_id,
            'message': self.message,
            'cause': str(self.cause),
            'stack_stace': self.stack
        }
        
    def get_cause_string(self):
        """
        Gets original error wrapped by this exception as a string message.

        :return: an original error message.
        """
        return str(self.cause)

    def set_cause_string(self, value):
        """
        Sets original error wrapped by this exception as a string message.

        :param value: an original error message.
        """
        self.cause = value

    def get_stack_trace_string(self):
        """
        Gets a stack trace where this exception occured.

        :return: a stack trace as a string.
        """
        if (self.stack_trace != None):
            return self.stack_trace
        # elif (hasattr(self, 'tb_frame')):
        #     return traceback.format_tb(self)
        else:
            return None

    def set_stack_trace_string(self, value):
        """
        Sets a stack trace where this exception occured.

        :param value: a stack trace as a string
        """
        self.stack_trace = value

    def with_code(self, code):
        """
        Sets a unique error code.
        This method returns reference to this exception to implement Builder pattern to chain additional calls.

        :param code: a unique error code

        :return: this exception object
        """
        self.code = code if code != None else 'UNKNOWN'
        self.name = code
        return self
        
    def with_status(self, status):
        """
        Sets a HTTP status code which shall be returned by REST calls.
        This method returns reference to this exception to implement Builder pattern to chain additional calls.

        :param status: an HTTP error code.

        :return: this exception object
        """
        self.status = status if status != None else 500
        return self
        
    def with_details(self, key, value):
        """
        Sets a parameter for additional error details.
        This details can be used to restore error description in other languages.

        This method returns reference to this exception to implement Builder pattern to chain additional calls.

        :param key: a details parameter name

        :param value: a details parameter name

        :return: this exception object
        """
        self.details = self.details if self.details != None else {}
        self.details[key] = value
        return self
        
    def with_cause(self, cause):
        """
        Sets a original error wrapped by this exception

        This method returns reference to this exception to implement Builder pattern to chain additional calls.

        :param cause: original error object

        :return: this exception object
        """
        self.cause = cause
        return self
        
    def with_correlation_id(self, correlation_id):
        """
        Sets a correlation id which can be used to trace this error through a call chain.

        This method returns reference to this exception to implement Builder pattern to chain additional calls.

        :param correlation_id: a unique transaction id to trace error through call chain

        :return: this exception object
        """
        self.correlation_id = correlation_id
        return self
                
    def wrap(self, cause):
        """
        Wraps another exception into an application exception object.

        If original exception is of ApplicationException type it is returned without changes.
        Otherwise a new ApplicationException is created and original error is set as its cause.

        :param cause: an original error object

        :return: an original or newly created ApplicationException
        """
        if isinstance(cause, ApplicationException):
            return cause
            
        self.with_cause(cause)
        return self

    @staticmethod
    def wrap_exception(exception, cause):
        """
        Wraps another exception into specified application exception object.

        If original exception is of ApplicationException type it is returned without changes.
        Otherwise the original error is set as a cause to specified ApplicationException object.

        :param exception: an ApplicationException object to wrap the cause

        :param cause: an original error object

        :return: an original or newly created ApplicationException
        """
        if isinstance(cause, ApplicationException):
            return cause
        
        exception.with_cause(cause)
        return exception
            
    # @staticmethod
    # def from_value(value):
    #     value = value if isinstance(value, dict) else dict(value)
    #
    #     error = MicroserviceError(
    #         value['category'] if 'category' in value else None,
    #         value['correlation_id'] if 'correlation_id' in value else None,
    #         value['code'] if 'code' in value else None,
    #         value['message'] if 'message' in value else None
    #     ).with_status(value['status'])
    #
    #     if 'cause' in value:
    #         error.with_cause(value['cause'])
    #     if 'details' in value:
    #         error.with_details(value['details'])
    #     if 'stack_trace' in value:
    #         error.with_stack(value['stack_trace'])
    #
    #     return error