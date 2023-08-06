# -*- coding: utf-8 -*-
"""
    pip_services3_commons.data.AnyValue
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    AnyValue implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services3_commons.data import AnyValueArray, AnyValueMap

from ..convert.TypeConverter import TypeConverter
from ..convert.StringConverter import StringConverter
from ..convert.BooleanConverter import BooleanConverter
from ..convert.IntegerConverter import IntegerConverter
from ..convert.LongConverter import LongConverter
from ..convert.FloatConverter import FloatConverter
from ..convert.DateTimeConverter import DateTimeConverter
from ..convert.ArrayConverter import ArrayConverter
from ..convert.MapConverter import MapConverter


class AnyValue():
    """
    Cross-language implementation of dynamic object what can hold value of any type.
    The stored value can be converted to different types using variety of accessor methods.

    Example::
        value1 = AnyValue("123.456");

        value1.get_as_integer()   // Result: 123
        value1.get_as_string()    // Result: "123.456"
        value1.get_as_float()     // Result: 123.456
    """
    value = None

    def __init__(self, value = None):
        """
        Creates a new instance of the object and assigns its value.

        :param value: (optional) value to initialize this object.
        """
        if isinstance(value, AnyValue):
            self.value = value.value
        else:
            self.value = value

    def get_type_code(self):
        """
        Gets type code for the value stored in this object.

        :return: type code of the object value.
        """
        return TypeConverter.to_type_code(self.value)

    def get_as_object(self):
        """
        Gets the value stored in this object without any conversions

        :return: the object value.
        """
        return self.value

    def set_as_object(self, value):
        """
        Sets a new value for this object

        :param value: the new object value.
        """
        self.value = value
    
    def get_as_nullable_string(self):
        """
        Converts object value into a string or returns null if conversion is not possible.

        :return: string value or None if conversion is not supported.
        """
        return StringConverter.to_nullable_string(self.value)

    def get_as_string(self):
        """
        Converts object value into a string or returns "" if conversion is not possible.

        :return: string value or "" if conversion is not supported.
        """
        return StringConverter.to_string(self.value)

    def get_as_string_with_default(self, default_value):
        """
        Converts object value into a string or returns default value if conversion is not possible.

        :param default_value: the default value.

        :return: string value or default if conversion is not supported.
        """
        return StringConverter.to_string_with_default(self.value, default_value)

    def get_as_nullable_boolean(self):
        """
        Converts object value into a boolean or returns null if conversion is not possible.

        :return: boolean value or null if conversion is not supported.
        """
        return BooleanConverter.to_nullable_boolean(self.value)

    def get_as_boolean(self):
        """
        Converts object value into a boolean or returns false if conversion is not possible.

        :return: string value or false if conversion is not supported.
        """
        return BooleanConverter.to_boolean(self.value)

    def get_as_boolean_with_default(self, default_value):
        """
        Converts object value into a boolean or returns default value if conversion is not possible.

        :param default_value: the default value.

        :return: boolean value or default if conversion is not supported.
        """
        return BooleanConverter.to_boolean_with_default(self.value, default_value)

    def get_as_nullable_integer(self):
        """
        Converts object value into an integer or returns None if conversion is not possible.

        :return: integer value or None if conversion is not supported.
        """
        return IntegerConverter.to_nullable_integer(self.value)

    def get_as_integer(self):
        """
        Converts object value into an integer or returns 0 if conversion is not possible.

        :return: integer value or 0 if conversion is not supported.
        """
        return IntegerConverter.to_integer(self.value)

    def get_as_integer_with_default(self, default_value):
        """
        Converts object value into a integer or returns default value if conversion is not possible.

        :param default_value: the default value.

        :return: integer value or default if conversion is not supported.
        """
        return IntegerConverter.to_integer_with_default(self.value, default_value)

    def get_as_nullable_long(self):
        return LongConverter.to_nullable_long(self.value)

    def get_as_long(self):
        return LongConverter.to_long(self.value)

    def get_as_long_with_default(self, default_value):
        return LongConverter.to_long_with_default(self.value, default_value)

    def get_as_nullable_float(self):
        """
        Converts object value into a float or returns None if conversion is not possible.

        :return: float value or None if conversion is not supported.
        """
        return FloatConverter.to_nullable_float(self.value)

    def get_as_float(self):
        """
        Converts object value into a float or returns 0 if conversion is not possible.

        :return: float value or 0 if conversion is not supported.
        """
        return FloatConverter.to_float(self.value)

    def get_as_float_with_default(self, default_value):
        """
        Converts object value into a float or returns default value if conversion is not possible.

        :param default_value: the default value.

        :return: float value or default if conversion is not supported.
        """
        return FloatConverter.to_float_with_default(self.value, default_value)

    def get_as_nullable_datetime(self):
        """
        Converts object value into a Date or returns None if conversion is not possible.

        :return: Date value or None if conversion is not supported.
        """
        return DateTimeConverter.to_nullable_datetime(self.value)

    def get_as_datetime(self):
        """
        Converts object value into a Date or returns current date if conversion is not possible.

        :return: Date value or current date if conversion is not supported.
        """
        return DateTimeConverter.to_datetime(self.value)

    def get_as_datetime_with_default(self, default_value):
        """
        Converts object value into a Date or returns default value if conversion is not possible.

        :param default_value: the default value.

        :return: Date value or default if conversion is not supported.
        """
        return DateTimeConverter.to_datetime_with_default(self.value, default_value)

    def get_as_nullable_type(self, value_type):
        """
        Converts object value into a value defined by specied typecode. If conversion is not possible it returns None.

        :param value_type: the TypeCode that defined the type of the result

        :return: value defined by the typecode or null if conversion is not supported.
        """
        return TypeConverter.to_nullable_type(value_type, self.value)

    def get_as_type(self, value_type):
        """
        Converts object value into a value defined by specied typecode.
        If conversion is not possible it returns default value for the specified type.

        :param value_type: the TypeCode that defined the type of the result

        :return: value defined by the typecode or type default value if conversion is not supported.
        """
        return TypeConverter.to_type(value_type, self.value)

    def get_as_type_with_default(self, value_type, default_value):
        """
        Converts object value into a value defined by specied typecode.
        If conversion is not possible it returns default value.

        :param value_type: the TypeCode that defined the type of the result

        :param default_value: the default value

        :return: value defined by the typecode or type default value if conversion is not supported.
        """
        return TypeConverter.to_type_with_default(value_type, self.value, default_value)

    def get_as_array(self):
        """
        Converts object value into an AnyArray or returns empty AnyArray if conversion is not possible.

        :return: AnyArray value or empty AnyArray if conversion is not supported.
        """
        return AnyValueArray.from_value(self.value)

    def get_as_map(self):
        """
        Converts object value into AnyMap or returns empty AnyMap if conversion is not possible.

        :return: AnyMap value or empty AnyMap if conversion is not supported.
        """
        return AnyValueMap.from_value(self.value)


    def __eq__(self, other):
        """
        Compares this object value to specified specified value.
        When direct comparison gives negative results it tries to compare values as strings.

        :param other: the value to be compared with.

        :return: true when objects are equal and false otherwise.
        """
        if other == None and self.value == None:
            return True
        if other == None or self.value == None:
            return False

        if isinstance(other, AnyValue):
            other = other._value

        if other == self.value:
            return True
        
        str_value1 = StringConverter.to_string(self.value)
        str_value2 = StringConverter.to_string(other)

        if str_value1 == None or str_value2 == None:
            return False

        return str_value1 == str_value2


    def __ne__(self, other):
        return not self.__eq__(other)


    def equals_as(self, value_type, other):
        """
        Compares this object value to specified specified value.
        When direct comparison gives negative results it converts
        values to type specified by type code and compare them again.

        :param value_type: the Typecode type that defined the type of the result

        :param other: the value to be compared with.

        :return: true when objects are equal and false otherwise.
        """
        if other == None and self.value == None:
            return True
        if other == None or self.value == None:
            return False

        if isinstance(other, AnyValue):
            other = other._value

        if other == self.value:
            return True
        
        value1 = TypeConverter.to_type(value_type, self.value)
        value2 = TypeConverter.to_type(value_type, other)

        if value1 == None or value2 == None:
            return False

        return value1 == value2

    def __str__(self):
        """
        Gets a string representation of the object.

        :return: a string representation of the object.
        """
        return StringConverter.to_string(self.value)