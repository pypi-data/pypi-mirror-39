# -*- coding: utf-8 -*-
"""
    pip_services_runtime.refer.Descriptor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Component descriptor implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..errors.ConfigException import ConfigException

class Descriptor(object):
    """
    Locator type that most often used in PipServices toolkit.
    It locates components using several fields:
        - Group: a package or just named group of components like "pip-services"
        - Type: logical component type that defines it's contract like "persistence"
        - Kind: physical implementation type like "mongodb"
        - Name: unique component name like "default"
        - Version: version of the component contract like "1.0"

    The locator matching can be done by all or only few selected fields.
    The fields that shall be excluded from the matching must be set to <code>"*"</code> or <code>null</code>.
    That approach allows to implement many interesting scenarios. For instance:
        - Locate all loggers (match by type and version)
        - Locate persistence components for a microservice (match by group and type)
        - Locate specific component by its name (match by name)

    Example:
        locator1 = Descriptor("mygroup", "connector", "aws", "default", "1.0")
        locator2 = Descriptor.from_string("mygroup:connector:*:*:1.0")

        locator1.match(locator2);		// Result: true
        locator1.eq(locator2);		// Result: true
        locator1.exact_match(locator2);	// Result: false
    """

    _group = None
    _type = None
    _kind = None
    _name = None
    _version = None
    
    def __init__(self, group, type, kind, name, version):
        """
        Creates a new instance of the descriptor.

        :param group: a logical component group

        :param type: a logical component type or contract

        :param kind: a component implementation type

        :param name: a unique component name

        :param version: a component implementation version
        """
        group = None if "*" == group else group 
        type = None if "*" == type else type
        kind = None if "*" == kind else kind
        name  = None if "*" == name else name
        version = None if "*" == version else version
        
        self._group = group
        self._type = type
        self._kind = kind
        self._name = name
        self._version = version

    def get_group(self): 
        """
         Gets the component's logical group.

        :return: the component's logical group
        """
        return self._group 

    def get_type(self):
        """
        Gets the component's logical type.

        :return: the component's logical type.
        """
        return self._type

    def get_kind(self):
        """
        Gets the component's implementation type.

        :return: the component's implementation type.
        """
        return self._kind

    def get_name(self):
        """
        Gets the unique component's name.

        :return: the unique component's name.
        """
        return self._name 

    def get_version(self):
        """
        Gets the component's implementation version.

        :return: the component's implementation version.
        """
        return self._version 

    def _match_field(self, field1, field2):
        return field1 == None \
            or field2 == None \
            or field1 == field2

    def match(self, descriptor):
        """
        Partially matches this descriptor to another descriptor.
        Fields that contain "*" or null are excluded from the match.

        :param descriptor: the descriptor to match this one against.

        :return: true if descriptors match and false otherwise
        """
        return self._match_field(self._group, descriptor.get_group()) \
            and self._match_field(self._type, descriptor.get_type()) \
            and self._match_field(self._kind, descriptor.get_kind()) \
            and self._match_field(self._name, descriptor.get_name()) \
            and self._match_field(self._version, descriptor.get_version())

    def _exact_match_field(self, field1, field2):
        if field1 == None and field2 == None:
            return True
        if field1 == None or field2 == None:
            return False
        return field1 == field2

    def exact_match(self, descriptor):
        """
        Matches this descriptor to another descriptor by all fields. No exceptions are made.

        :param descriptor: the descriptor to match this one against.

        :return: true if descriptors match and false otherwise.
        """
        return self._exact_match_field(self._group, descriptor.get_group()) \
            and self._exact_match_field(self._type, descriptor.get_type()) \
            and self._exact_match_field(self._kind, descriptor.get_kind()) \
            and self._exact_match_field(self._name, descriptor.get_name()) \
            and self._exact_match_field(self._version, descriptor.get_version())

    def is_complete(self):
        """
        Checks whether all descriptor fields are set.
        If descriptor has at least one "*" or null field it is considered "incomplete"

        :return: true if all descriptor fields are defined and false otherwise.
        """
        return self._group != None and self._type != None \
            and self._kind != None and self._name != None and self._version != None

    def __eq__(self, other):
        """
        Compares this descriptor to a value.
        If value is a Descriptor it tries to match them, otherwise the method returns false.

        :param other: the value to match against this descriptor.

        :return: true if the value is matching descriptor and false otherwise.
        """
        if isinstance(other, Descriptor):
            return self.match(other)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        """
        Gets a string representation of the object.
        The result is a colon-separated list of descriptor fields as "mygroup:connector:aws:default:1.0"

        :return: a string representation of the object.
        """
        result = ''
        result += self._group if self._group != None else '*'
        result += ':'
        result += self._type if self._type != None else '*'
        result += ':'
        result += self._kind if self._kind != None else '*'
        result += ':'
        result += self._name if self._name != None else '*'
        result += ':'
        result += self._version if self._version != None else '*'
        return result
    
    @staticmethod
    def from_string(value):
        """
        Parses colon-separated list of descriptor fields and returns them as a Descriptor.

        :param value: colon-separated descriptor fields to initialize Descriptor.

        :return: a newly created Descriptor.
        """
        if value == None or len(value) == 0:
            return None
                
        tokens = value.split(":")
        if len(tokens) != 5:
            raise ConfigException(
                None, "BAD_DESCRIPTOR", "Descriptor " + str(value) + " is in wrong format"
            ).with_details("descriptor", value)
            
        return Descriptor(tokens[0].strip(), tokens[1].strip(), tokens[2].strip(), tokens[3].strip(), tokens[4].strip())

