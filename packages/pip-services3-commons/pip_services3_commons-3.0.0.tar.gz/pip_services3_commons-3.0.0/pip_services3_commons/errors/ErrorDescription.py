# -*- coding: utf-8 -*-
"""
    pip_services3_commons.errors.ErrorDescription
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Error description implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ErrorDescription(object):
    """
    Serializeable error description. It is use to pass information about errors
    between microservices implemented in different languages. On the receiving side
    [[ErrorDescription]] is used to recreate exception object close to its original type
    without missing additional details.
    """
    category = None
    status = None
    code = None
    message = None
    details = None
    correlation_id = None
    cause = None
    stack_trace = None

    def __init__(self):
        pass

    def to_json(self):
        return {
            'category': self.category,
            'status': self.status,
            'code': self.code,
            'message': self.message,
            'details': self.details,
            'correlation_id': self.correlation_id,
            'cause': self.cause,
            'stack_trace': self.stack_trace
        }

    @staticmethod
    def from_json(json):
        if not isinstance(json, dict):
            return json

        error = ErrorDescription()
        error.category = json['category']
        error.status = json['status']
        error.code = json['code']
        error.message = json['message']
        error.details = json['details']
        error.correlation_id = json['correlation_id']
        error.cause = json['cause']
        error.stack_trace = json['stack_trace']
        return error
