# -*- coding: utf-8 -*-
"""
    pip_services3_commons.data.AnyValueArray
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    AnyValueArray implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services3_commons.data import AnyValue, AnyValueMap

from ..convert.TypeConverter import TypeConverter
from ..convert.StringConverter import StringConverter
from ..convert.BooleanConverter import BooleanConverter
from ..convert.IntegerConverter import IntegerConverter
from ..convert.LongConverter import LongConverter
from ..convert.FloatConverter import FloatConverter
from ..convert.DateTimeConverter import DateTimeConverter
from ..convert.ArrayConverter import ArrayConverter
from ..convert.MapConverter import MapConverter


class AnyValueArray(list):
    """
    Cross-language implementation of dynamic object array what can hold values of any type.
    The stored values can be converted to different types using variety of accessor methods.

    Example:
        value1 = AnyValueArray([1, "123.456", "2018-01-01"])
        value1.get_as_boolean(0)   // Result: true
        value1.get_as_integer(1)   // Result: 123
        value1.get_as_float(1)     // Result: 123.456
        value1.get_as_datetime(2)  // Result: datetime.datetime(2018,0,1)
    """
    def __init__(self, values = None):
        """
        Creates a new instance of the array and assigns its value.

        :param values: (optional) values to initialize this array.
        """
        super(AnyValueArray, self).__init__()
        if values != None and len(values) > 0:
            for value in values:
                self.append(value)

    def clear(self):
        """
        Clears this array by removing all its elements.
        """
        del self[:]

    def get_as_object(self, index = None):
        """
        Gets the value stored in array element without any conversions.
        When element index is not defined it returns the entire array value.

        :param index: (optional) an index of the element to get

        :return: the element value or value of the array when index is not defined.
        """
        if index == None:
            return self.get_as_array(index)
        else:
            return self[index]

    def set_as_object(self, index = None, value= None):
        """
        Sets a new value to array element specified by its index.
        When the index is not defined, it resets the entire array value.
        This method has double purpose because method overrides are not supported in JavaScript.

        :param index: (optional) an index of the element to set

        :param value: a new element or array value.
        """
        if index == None and value != None:
            self.set_as_array(value)
        else:
            self[index] = value

    def get_as_array(self, index):
        """
        Converts array element into an AnyValueArray or returns empty AnyValueArray if conversion is not possible.

        :param index: an index of element to get.

        :return: AnyValueArray value of the element or empty AnyValueArray if conversion is not supported.
        """
        if index == None:
            array = []
            for value in self:
                array.append(value)
            return array
        else:
            value = self[index]
            return AnyValueArray.from_value(value)

    def set_as_array(self, values):
        """
        Sets a new values to array element

        :param values: values to set
        """
        del self[:]
        for value in values:
            self.append(value)

    def get_as_nullable_string(self, index):
        """
        Converts array element into a string or returns None if conversion is not possible.

        :param index: an index of element to get.

        :return: string value of the element or None if conversion is not supported.
        """
        value = self[index]
        return StringConverter.to_nullable_string(value)

    def get_as_string(self, index):
        """
        Converts array element into a string or returns "" if conversion is not possible.

        :param index: an index of element to get.

        :return: string value ot the element or "" if conversion is not supported.
        """
        value = self[index]
        return StringConverter.to_string(value)

    def get_as_string_with_default(self, index, default_value):
        """
        Converts array element into a string or returns default value if conversion is not possible.

        :param index: an index of element to get.

        :param default_value: the default value

        :return: string value ot the element or default value if conversion is not supported.
        """
        value = self[index]
        return StringConverter.to_string_with_default(value, default_value)

    def get_as_nullable_boolean(self, index):
        """
        Converts array element into a boolean or returns None if conversion is not possible

        :param index: an index of element to get.

        :return: boolean value of the element or None if conversion is not supported.
        """
        value = self[index]
        return BooleanConverter.to_nullable_boolean(value)

    def get_as_boolean(self, index):
        """
        Converts array element into a boolean or returns false if conversion is not possible.

        :param index: an index of element to get.

        :return: boolean value ot the element or false if conversion is not supported.
        """
        value = self[index]
        return BooleanConverter.to_boolean(value)

    def get_as_boolean_with_default(self, index, default_value):
        """
        Converts array element into a boolean or returns default value if conversion is not possible.

        :param index: an index of element to get.

        :param default_value: the default value

        :return: boolean value ot the element or default value if conversion is not supported.
        """
        value = self[index]
        return BooleanConverter.to_boolean_with_default(value, default_value)

    def get_as_nullable_integer(self, index):
        """
        Converts array element into an integer or returns None if conversion is not possible.

        :param index: an index of element to get.

        :return: integer value of the element or None if conversion is not supported.
        """
        value = self[index]
        return IntegerConverter.to_nullable_integer(value)

    def get_as_integer(self, index):
        """
        Converts array element into an integer or returns 0 if conversion is not possible.

        :param index: an index of element to get.

        :return: integer value ot the element or 0 if conversion is not supported.
        """
        value = self[index]
        return IntegerConverter.to_integer(value)

    def get_as_integer_with_default(self, index, default_value):
        """
        Converts array element into an integer or returns default value if conversion is not possible.

        :param index: an index of element to get.

        :param default_value: the default value

        :return: integer value ot the element or default value if conversion is not supported.
        """
        value = self[index]
        return IntegerConverter.to_integer_with_default(value, default_value)

    def get_as_nullable_long(self, index):
        value = self[index]
        return LongConverter.to_nullable_long(value)

    def get_as_long(self, index):
        value = self[index]
        return LongConverter.to_long(value)

    def get_as_long_with_default(self, index, default_value):
        value = self[index]
        return LongConverter.to_long_with_default(value, default_value)

    def get_as_nullable_float(self, index):
        """
        Converts array element into a float or returns None if conversion is not possible.

        :param index: an index of element to get.

        :return: float value of the element or None if conversion is not supported.
        """
        value = self[index]
        return FloatConverter.to_nullable_float(value)

    def get_as_float(self, index):
        """
        Converts array element into a float or returns 0 if conversion is not possible.

        :param index: an index of element to get.

        :return: float value ot the element or 0 if conversion is not supported.
        """
        value = self[index]
        return FloatConverter.to_float(value)

    def get_as_float_with_default(self, index, default_value):
        """
        Converts array element into a float or returns default value if conversion is not possible.

        :param index: an index of element to get.

        :param default_value: the default value

        :return: float value ot the element or default value if conversion is not supported.
        """
        value = self[index]
        return FloatConverter.to_float_with_default(value, default_value)

    def get_as_nullable_datetime(self, index):
        """
        Converts array element into a Date or returns None if conversion is not possible.

        :param index: an index of element to get.

        :return: Date value of the element or None if conversion is not supported.
        """
        value = self[index]
        return DateTimeConverter.to_nullable_datetime(value)

    def get_as_datetime(self, index):
        """
        Converts array element into a Date or returns the current date if conversion is not possible.

        :param index: an index of element to get.

        :return: Date value ot the element or the current date if conversion is not supported.
        """
        value = self[index]
        return DateTimeConverter.to_datetime(value)

    def get_as_datetime_with_default(self, index, default_value):
        """
        Converts array element into a Date or returns default value if conversion is not possible.

        :param index: an index of element to get.

        :param default_value: the default value

        :return: Date value ot the element or default value if conversion is not supported.
        """
        value = self[index]
        return DateTimeConverter.to_datetime_with_default(value, default_value)

    def get_as_nullable_type(self, index, value_type):
        """
        Converts array element into a value defined by specied typecode.
        If conversion is not possible it returns None.

        :param index: an index of element to get.

        :param value_type: the TypeCode that defined the type of the result

        :return: element value defined by the typecode or None if conversion is not supported.
        """
        value = self[index]
        return TypeConverter.to_nullable_type(value_type, value)

    def get_as_type(self, index, value_type):
        """
        Converts array element into a value defined by specied typecode.
        If conversion is not possible it returns default value for the specified type.

        :param index: an index of element to get.

        :param value_type: the TypeCode that defined the type of the result

        :return: element value defined by the typecode or default if conversion is not supported.
        """
        value = self[index]
        return TypeConverter.to_type(value_type, value)

    def get_as_type_with_default(self, index, value_type, default_value):
        """
        Converts array element into a value defined by specied typecode.
        If conversion is not possible it returns default value.

        :param index: an index of element to get.

        :param value_type: the TypeCode that defined the type of the result

        :param default_value: the default value

        :return: element value defined by the typecode or default value if conversion is not supported.
        """
        value = self[index]
        return TypeConverter.to_type_with_default(value_type, value, default_value)

    # def get_as_array(self, index):
    #     value = self[index]
    #     return AnyValueArray.from_value(value)

    def get_as_value(self, index):
        """
        Converts array element into an AnyValue or returns an empty AnyValue if conversion is not possible.

        :param index: an index of element to get.

        :return: AnyValue value of the element or empty AnyValue if conversion is not supported.
        """
        value = self[index]
        return AnyValue(value)

    def get_as_map(self, index):
        """
        Converts array element into an AnyValueMap or returns empty AnyValueMap if conversion is not possible.

        :param index: an index of element to get.

        :return: AnyValueMap value of the element or empty AnyValueMap if conversion is not supported.
        """
        value = self[index]
        return AnyValueMap.from_value(value)


    def contains(self, value):
        """
        Checks if this array contains a value.
        The check uses direct comparison between elements and the specified value.

        :param value: a value to be checked

        :return: true if this array contains the value or false otherwise.
        """
        str_value = StringConverter.to_nullable_string(value)

        for element in self:
            str_element = StringConverter.to_string(element)

            if str_value == None and str_element == None:
                return True
            if str_value == None or str_element == None:
                continue
            
            if str_value == str_element:
                return True

        return False


    def contains_as_type(self, value_type, value):
        """
        Checks if this array contains a value.
        The check before comparison converts elements and the value to type specified by type code.

        :param value_type: a type code that defines a type to convert values before comparison

        :param value: a value to be checked

        :return: true if this array contains the value or false otherwise.
        """
        typed_value = TypeConverter.to_nullable_type(value_type, value)

        for element in self:
            typed_element = TypeConverter.to_type(value_type, element)

            if typed_value == None and typed_element == None:
                return True
            if typed_value == None or typed_element == None:
                continue
            
            if typed_value == typed_element:
                return True

        return False

    def clone(self):
        """
        Creates a binary clone of this object.

        :return: a clone of this object.
        """
        array = AnyValueArray()
        array.set_as_array(self)
        return array

    def __str__(self):
        """
        Gets a string representation of the object.
        The result is a comma-separated list of string representations of individual elements as
        "value1,value2,value3"

        :return: a string representation of the object.
        """
        result = ''

        for element in self:
            if len(result) > 0:
                result += ','
            result += StringConverter.to_string_with_default(element, '')

        return result

    @staticmethod
    def from_values(*values):
        """
        Creates a new AnyValueArray from a list of values

        :param values: a list of values to initialize the created AnyValueArray

        :return: a newly created AnyValueArray.
        """
        return AnyValueArray(values)

    @staticmethod
    def from_value(value):
        """
        Converts specified value into AnyValueArray.

        :param value: value to be converted

        :return: a newly created AnyValueArray.
        """
        value = ArrayConverter.to_nullable_array(value)
        if value != None:
            return AnyValueArray(value)
        return AnyValueArray()

    @staticmethod
    def from_string(values, separator, remove_duplicates = False):
        """
        Splits specified string into elements using a separator and assigns
        the elements to a newly created AnyValueArray.

        :param values: a string value to be split and assigned to AnyValueArray

        :param separator: a separator to split the string

        :param remove_duplicates: (optional) true to remove duplicated elements

        :return: a newly created AnyValueArray.
        """
        result = AnyValueArray()

        if values == None or len(values) == 0:
            return result

        items = str(values).split(separator)
        for item in items:
            if (item != None and len(item) > 0) or remove_duplicates == False:
                result.append(item)

        return result
    