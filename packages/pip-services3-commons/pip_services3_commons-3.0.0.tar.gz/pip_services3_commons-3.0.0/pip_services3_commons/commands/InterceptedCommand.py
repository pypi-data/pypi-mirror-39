# -*- coding: utf-8 -*-
"""
    pip_services3_commons.commands.InterceptedCommand
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Intercepted command implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ICommand import ICommand

class InterceptedCommand(ICommand):
    """
    Implements a ICommand command wrapped by an interceptor.
    It allows to build command call chains. The interceptor can alter execution
    and delegate calls to a next command, which can be intercepted or concrete.

    Example:
        class CommandLogger(ICommandInterceptor):
            def get_name(self, command):
                return command.get_name()

            def execute():
                ...

            def validate():
                ...
    """

    _intercepter = None
    _next = None

    def __init__(self, intercepter, next):
        """
        Creates a new InterceptedCommand, which serves as a link in an execution chain.
        Contains information about the interceptor that is being used and the next command in the chain.
        
        :param intercepter: the intercepter reference.

        :param next: the next intercepter or command in the chain.
        """
        self._intercepter = intercepter
        self._next = next

    def get_name(self):
        """
        Gets the command name.

        :return: the command name
        """
        return self._intercepter.get_name(self._next)

    def execute(self, correlation_id, args):
        """
        Executes the next command in the execution chain using the given Parameters parameters (arguments).
        
        :param correlation_id: a unique correlation/transaction id

        :param args: command arguments
        
        :return: an execution result.
        
        :raises: ValidationError: when execution fails for whatever reason.
        """
        return self._intercepter.execute(self._next, correlation_id, args)

    def validate(self, args):
        """
        Validates the Parameters parameters (arguments)
        that are to be passed to the command that is next in the execution chain.
        
        :param args: command arguments
        
        :return: a list of validation results
        """
        return self._intercepter.validate(self._next, args)
    