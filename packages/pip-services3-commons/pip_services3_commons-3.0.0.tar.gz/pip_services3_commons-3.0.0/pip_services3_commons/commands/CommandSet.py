# -*- coding: utf-8 -*-
"""
    pip_services3_commons.commands.CommandSet
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Command set implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..errors.BadRequestException import BadRequestException
from ..validate.ValidationException import ValidationException
from ..validate.ValidationResult import ValidationResult
from ..validate.ValidationResultType import ValidationResultType
from ..data.IdGenerator import IdGenerator
from  .InterceptedCommand import InterceptedCommand

class CommandSet(object):
    """
    Contains a set of commands and events supported by a ICommandable commandable object.
    The CommandSet supports command interceptors to extend and the command call chain.

    CommandSets can be used as alternative commandable interface to a business object.
    It can be used to auto generate multiple external services for the business object
    without writing much code.

    Example:
        class MyDataCommandSet(CommandSet):
            _controller = None

            def __init__(self, controller):
                super(MyDataCommandSet, self).__init__()

                self._controller = controller

                self.add_command(self._make_get_my_data_command())

            def _make_get_my_data_command(self):
                def handler(correlation_id, args):
                    param = args.get_as_string('param')
                    return self._controller.get_my_data(correlation_id, param)

                return Command(
                    "get_mydata",
                    None,
                    handler
                )

    See Command, Event, ICommandable
    """

    _commands = None
    _commands_by_name = None
    _events = None
    _events_by_name = None
    _intercepters = None

    def __init__(self):
        """
        Creates an empty CommandSet object.
        """
        self._commands = []
        self._commands_by_name = {}
        self._events = []
        self._events_by_name = {}
        self._intercepters = []

    def get_commands(self):
        """
        Gets all commands registered in this command set.

        :return: ICommand list with all commands supported by component.
        """
        return self._commands

    def get_events(self):
        """
        Gets all events registered in this command set.

        :return: ICommand list with all events supported by component.
        """
        return self._events

    def find_command(self, command):
        """
        Searches for a command by its name.
        
        :param command: the name of the command to search for.

        :return: the command, whose name matches the provided name.
        """
        if command in self._commands_by_name:
            return self._commands_by_name[command]
        else:
            return None

    def find_event(self, event):
        """
        Searches for an event by its name in this command set.
        
        :param event: the name of the event to search for.

        :return: the event, whose name matches the provided name.
        """
        if event in self._events_by_name:
            return self._events_by_name[event]
        else:
            return None

    def _build_command_chain(self, command):
        """
        Builds execution chain including all intercepters and the specified command.

        :param command: the command to build a chain.
        """
        next = command
        for intercepter in reversed(self._intercepters):
            next = InterceptedCommand(intercepter, next)
        self._commands_by_name[next.get_name()] = next

    def _rebuild_all_command_chains(self):
        """
        Rebuilds execution chain for all registered commands.
        This method is typically called when intercepters are changed.
        Because of that it is more efficient to register intercepters
        before registering commands (typically it will be done in abstract classes).
        However, that performance penalty will be only once during creation time.
        """
        self._commands_by_name = {}
        for command in self._commands:
            self._build_command_chain(command)

    def add_command(self, command):
        """
        Adds a ICommand command to this command set.
        
        :param command: a command instance to be added
        """
        self._commands.append(command)
        self._build_command_chain(command)

    def add_commands(self, commands):
        """
        Adds multiple ICommand commands to this command set.
        
        :param commands: the array of commands to add.
        """
        for command in commands:
            self.add_command(command)

    def add_event(self, event):
        """
        Adds an IEvent event to this command set.
        
        :param event: an event instance to be added
        """
        self._events.append(event)
        self._events_by_name[event.get_name] = event

    def add_events(self, events):
        """
        Adds multiple [[IEvent events]] to this command set.
        
        :param events: the array of events to add.
        """
        for event in events:
            self.add_event(event)

    def add_command_set(self, command_set):
        """
        Adds all of the commands and events from specified CommandSet command set
        into this one.
        
        :param command_set: a commands set to add commands from
        """
        for command in command_set.get_commands():
            self.add_command(command)

        for event in command_set.get_events():
            self.add_event(event)

    def add_intercepter(self, intercepter):
        """
        Adds a ICommandInterceptor command interceptor to this command set.
        
        :param intercepter: an intercepter instance to be added.
        """
        self._intercepters.append(intercepter)
        self._rebuild_all_command_chains()

    def execute(self, correlation_id, command, args):
        """
        Executes a ICommand command specificed by its name.
        
        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param command: the name of that command that is to be executed.

        :param args: the parameters (arguments) to pass to the command for execution.
        
        :return: the execution result.
        
        :raises: ValidationException: when execution fails for any reason.
        """
        # Get command and throw error if it doesn't exist
        cref = self.find_command(command)
        if cref == None:
            raise BadRequestException(
                correlation_id,
                "CMD_NOT_FOUND",
                "Requested command does not exist"
            ).with_details("command", command)

        # Generate correlationId if it doesn't exist
        # Use short ids for now
        if correlation_id == None:
           correlation_id = IdGenerator.next_short()
        
        # Validate command arguments before execution and throw the 1st found error
        results = cref.validate(args)
        ValidationException.throw_exception_if_needed(correlation_id, results, False)
                
        # Execute the command.
        return cref.execute(correlation_id, args)

    def validate(self, command, args):
        """
        Validates Parameters args for command specified by its name using defined schema.
        If validation schema is not defined than the methods returns no errors.
        It returns validation error if the command is not found.
        
        :param command: the name of the command for which the 'args' must be validated.

        :param args: the parameters (arguments) to validate.
        
        :return: an array of ValidationResults. If no command is found by the given
                 name, then the returned array of ValidationResults will contain a
                 single entry, whose type will be ValidationResultType.Error.
        """
        cref = self.find_command(command)
        if cref == None:
            results = []
            results.append( \
                ValidationResult(
                    None, ValidationResultType.Error,
                    "CMD_NOT_FOUND", 
                    "Requested command does not exist"
                )
            )
            return results

        return cref.validate(args)
    
    def add_listener(self, listener):
        """
        Adds a IEventListener listener to receive notifications on fired events.

        :param listener: a listener to be added
        """
        for event in self._events:
            event.add_listener(listener)

    def remove_listener(self, listener):
        """
        Removes previosly added IEventListener listener.

        :param listener: a listener to be removed
        """
        for event in self._events:
            event.remove_listener(listener)

    def notify(self, correlation_id, event, value):
        """
        Fires event specified by its name and notifies all registered
        IEventListener listeners

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param event: the name of the event that is to be fired.

        :param value: the event arguments (parameters).
        """
        e = self.find_event(event)
        if e != None:
            e.notify(correlation_id, value)
