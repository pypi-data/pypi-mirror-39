# -*- coding: utf-8 -*-
"""
    pip_services3_commons.commands.Command
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Command implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ICommand import ICommand
from ..errors.InvocationException import InvocationException

class Command(ICommand):
    """
    Concrete implementation of ICommand interface.
    Command allows to call a method or function using Command pattern.

    Example:
        def handler(*args):
            param1 = args.getAsFloat("param1")
            param2 = args.getAsFloat("param2")
            return param1 + param2

        command = Command("add", None, handler)

        result = command.execute("123",  Parameters.fromTuples("param1", 2, "param2", 2))

        print result.__str__()

    See ICommand, CommandSet
    """

    _name = None
    _schema = None
    _function = None

    def __init__(self, name, schema, function):
        """
        Creates a new command object and assigns it's parameters.

        :param name: the name of the command

        :param schema: a validation schema for command arguments

        :param function: an execution function to be wrapped into this command.
        """
        if name == None:
            raise TypeError("Command name is not set")
        if function == None:
            raise TypeError("Command function is not set")
        
        self._name = name
        self._schema = schema
        self._function = function

    def get_name(self):
        """
        Gets the command name.

        :return: the command name
        """
        return self._name

    def execute(self, correlation_id, args):
        """
        Executes the command. Before execution is validates Parameters args using the
        defined schema. The command execution intercepts ApplicationException raised
        by the called function and throws them.
        
        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param args: the parameters (arguments) to pass to this command for execution.
        
        :return: an execution result.
        
        :raises: ApplicationException: when execution fails for whatever reason.
        """
        # Validate arguments
        if self._schema != None:
            self._schema.validate_and_throw_exception(correlation_id, args)
        
        # Call the function
        try:
            return self._function(correlation_id, args)
        # Intercept unhandled errors
        except Exception as ex:
            raise InvocationException(
                correlation_id,
                "EXEC_FAILED",
                "Execution " + self._name + " failed: " + str(ex)
            ).with_details("command", self._name).wrap(ex)


    def validate(self, args):
        """
        Performs validation of the command arguments.
        
        :param args: the parameters (arguments) to validate using this command's schema.
        
        :return: an array of ValidationResults or an empty array (if no schema is set).
        """
        # When schema is not defined, then skip validation
        if self._schema != None: 
            return self._schema.validate(args)
        
        # ToDo: Complete implementation
        return []