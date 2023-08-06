# -*- coding: utf-8 -*-
"""
    pip_services3_commons.commands.ICommandable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for commandable components
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ICommandable:
    """
    An interface for commandable objects, which are part of the command design pattern.
    The commandable object exposes its functonality as commands and events groupped
    into a CommandSet.

    This interface is typically implemented by controllers and is used to auto generate
    external interfaces.

    Example:
        class MyDataController(ICommandable, IMyDataController):
            _commandSet = None

            def get_command_set(self):
                if self._commandSet == None:
                    _commandSet = MyDataCommandSet(self)
                return self._commandSet
    """

    def get_command_set(self):
        """
        Gets a command set with all supported commands and events.

        :return: a command set with commands and events.
        """
        raise NotImplementedError('Method from interface definition')
