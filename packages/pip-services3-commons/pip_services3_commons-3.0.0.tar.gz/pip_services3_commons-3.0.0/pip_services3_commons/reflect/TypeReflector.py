# -*- coding: utf-8 -*-
"""
    pip_services3_commons.reflect.TypeReflector
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Type reflector implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import importlib

from pip_services3_commons.convert import TypeConverter, TypeCode

from ..errors.NotFoundException import NotFoundException

class TypeReflector:
    """
    Helper class to perform object type introspection and object instantiation.

    This class has symmetric implementation across all languages supported
    by Pip.Services toolkit and used to support dynamic data processing.

    Because all languages have different casing and case sensitivity rules,
    this TypeReflector treats all type names as case insensitive.

    Example:
        descriptor = TypeDescriptor("MyObject", "mylibrary")
        Typeeflector.get_type_by_descriptor(descriptor)
        myObj = TypeReflector.create_instance_by_descriptor(descriptor)
        TypeDescriptor.is_primitive(myObject) 		// Result: false
        TypeDescriptor.is_primitive(123)				// Result: true
    """
    @staticmethod
    def get_type(name, library):
        """
        Gets object type by its name and library where it is defined.

        :param name: an object type name.

        :param library: a library where the type is defined

        :return: the object type or null is the type wasn't found.
        """
        if name == None:
            raise Exception("Class name cannot be null")
        if library == None:
            raise Exception("Module name cannot be null")

        try:
            module = importlib.import_module(library)
            return getattr(module, name)
        except:
           return None

    @staticmethod
    def get_type_by_descriptor(descriptor):
        """
        Gets object type by type descriptor.

        :param descriptor: a type descriptor that points to an object type

        :return: the object type or null is the type wasn't found.
        """
        if descriptor == None:
            raise Exception("Type descriptor cannot be null")

        return TypeReflector.get_type(descriptor.get_name(), descriptor.get_library())

    @staticmethod
    def create_instance(name, library, *args):
        """
        Creates an instance of an object type specified by its name and library where it is defined.

        :param name: an object type (factory function) to create.

        :param library: a library (module) where object type is defined.

        :param args: arguments for the object constructor.

        :return: the created object instance.
        """
        obj_type = TypeReflector.get_type(name, library)
        if obj_type == None:
            raise NotFoundException(
                None, "TYPE_NOT_FOUND", "Type " + name + "," + library + " was not found"
            ).with_details("type", name).with_details("library", library)
        
        return obj_type(*args)

    @staticmethod
    def create_instance_by_type(obj_type, *args):
        """
        Creates an instance of an object type.

        :param obj_type: an object type (factory function) to create.

        :param args: arguments for the object constructor.

        :return: the created object instance.
        """
        if obj_type == None:
            raise Exception("Class type cannot be null")

        return obj_type(*args)

    @staticmethod
    def create_instance_by_descriptor(descriptor, *args):
        """
        Creates an instance of an object type specified by type descriptor.

        :param descriptor: a type descriptor that points to an object type

        :param args: arguments for the object constructor.

        :return: the created object instance.
        """
        if descriptor == None:
            raise Exception("Type descriptor cannot be null")

        return TypeReflector.create_instance(descriptor.get_name(), descriptor.get_library(), args)

    @staticmethod
    def is_primitive(value):
        """
        Checks if value has primitive type.

        Primitive types are: numbers, strings, booleans, date and time.
        Complex (non-primitive types are): objects, maps and arrays

        :param value: a value to check

        :return: true if the value has primitive type and false if value type is complex.
        """
        typeCode = TypeConverter.to_type_code(value)
        return typeCode == TypeCode.String or typeCode == TypeCode.Enum or typeCode == TypeCode.Boolean \
               or typeCode == TypeCode.Integer or typeCode == TypeCode.Long \
               or typeCode == TypeCode.Float or typeCode == TypeCode.Double \
               or typeCode == TypeCode.DateTime or typeCode == TypeCode.Duration
