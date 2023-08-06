# -*- coding: utf-8 -*-
"""
    pip_services3_commons.commands.ICommandIntercepter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for command intercepters.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ICommandIntercepter(object):
    """
    An interface for stackable command intercepters, which can extend
    and modify the command call chain.

    This mechanism can be used for authentication, logging, and other functions.
    """

    def get_name(self, command):
        """
        Gets the name of the wrapped command.

        The interceptor can use this method to override the command name.
        Otherwise it shall just delegate the call to the wrapped command.

        :param command: the next command in the call chain.

        :return: the name of the wrapped command.
        """
        raise NotImplementedError('Method from interface definition')

    def execute(self, correlation_id, command, args):
        """
        Executes the wrapped command with specified arguments.

        The interceptor can use this method to intercept and alter the command execution.
        Otherwise it shall just delete the call to the wrapped command.
        
        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param command: the next command in the call chain that is to be executed.

        :param args: the parameters (arguments) to pass to the command for execution.
        
        :return: an execution result.
        
        :raises: ApplicationException when execution fails for whatever reason.
        """
        raise NotImplementedError('Method from interface definition')

    def validate(command, args):
        """
        Validates arguments of the wrapped command before its execution.

        The interceptor can use this method to intercept and alter validation of the command arguments.
        Otherwise it shall just delegate the call to the wrapped command.
        
        :param command: intercepted ICommand

        :param args: command arguments
        
        :return: a list of validation results.
        """
        raise NotImplementedError('Method from interface definition')
    