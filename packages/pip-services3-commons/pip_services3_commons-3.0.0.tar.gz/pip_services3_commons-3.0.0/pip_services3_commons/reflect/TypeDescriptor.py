# -*- coding: utf-8 -*-
"""
    pip_services3_commons.reflect.TypeDescriptor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Type descriptor implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..errors.ConfigException import ConfigException

class TypeDescriptor:
    """
    Descriptor that points to specific object type by it's name
    and optional library (or module) where this type is defined.

    This class has symmetric implementation across all languages supported
    by Pip.Services toolkit and used to support dynamic data processing.
    """
    _name = None
    _library = None
        
    def __init__(self, name, library):
        """
        Creates a new instance of the type descriptor and sets its values.

        :param name: a name of the object type.

        :param library: a library or module where this object type is implemented.
        """
        self._name = name
        self._library = library

    def get_name(self):
        """
        Get the name of the object type.

        :return: the name of the object type.
        """
        return self._name

    def get_library(self):
        """
        Gets the name of the library or module where the object type is defined.

        :return: the name of the library or module.
        """
        return self._library

    def __eq__(self, other):
        """
        Compares this descriptor to a value.
        If the value is also a TypeDescriptor it compares their name and library fields.
        Otherwise this method returns false.

        :param other: a value to compare.

        :return: true if value is identical TypeDescriptor and false otherwise.
        """
        if isinstance(other, TypeDescriptor):
            if self._name == None or other._name == None:
                return False
            if self._name != other._name:
                return False
            if self._library == None or other._library == None or self._library == other._library: 
                return True
        
        return False

    def __str__(self):
        """
        Gets a string representation of the object. The result has format name[,library]

        :return: a string representation of the object.
        """
        result = self._name
        if self._library != None:
            result += ','+ self._library
        return result

    @staticmethod
    def from_string(value):
        """
        Parses a string to get descriptor fields and returns them as a Descriptor.
        The string must have format name[,library]

        :param value: a string to parse.

        :return: a newly created Descriptor.
        """
        if value == None or len(value) == 0:
            return None
                
        tokens = value.split(",")
        if len(tokens) == 1:
            return TypeDescriptor(tokens[0].strip(), None)
        elif len(tokens) == 2:
            return TypeDescriptor(tokens[0].strip(), tokens[1].strip())
        else:
            raise ConfigException(
                None, "BAD_DESCRIPTOR", "Type descriptor " + value + " is in wrong format"
            ).with_details("descriptor", value)

