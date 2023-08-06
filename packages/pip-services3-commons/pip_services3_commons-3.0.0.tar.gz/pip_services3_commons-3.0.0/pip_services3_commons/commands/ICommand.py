# -*- coding: utf-8 -*-
"""
    pip_services3_commons.commands.ICommand
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for commands.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..run.IExecutable import IExecutable

class ICommand(IExecutable):
    """
    An interface for Commands, which are part of the Command design pattern.
    Each command wraps a method or function and allows to call them in uniform and safe manner.
    """

    def get_name(self):
        """
        Gets the command name.

        :return: the command name
        """
        raise NotImplementedError('Method from interface definition')

    def validate(self, args):
        """
        Validates command arguments before execution using defined schema.
        
        :param args: the parameters (arguments) to validate.

        :return: a list of validation results
        """
        raise NotImplementedError('Method from interface definition')
    