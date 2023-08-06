# -*- coding: utf-8 -*-
"""
    pip_services3_commons.data.StringValueMap
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    StringValueMap implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from ..data import AnyValueMap
from ..convert.TypeConverter import TypeConverter
from ..convert.StringConverter import StringConverter
from ..convert.BooleanConverter import BooleanConverter
from ..convert.IntegerConverter import IntegerConverter
from ..convert.LongConverter import LongConverter
from ..convert.FloatConverter import FloatConverter
from ..convert.DateTimeConverter import DateTimeConverter
from ..convert.ArrayConverter import ArrayConverter
from ..convert.MapConverter import MapConverter
from ..reflect.RecursiveObjectReader import RecursiveObjectReader

class StringValueMap(dict):
    """
    Cross-language implementation of a map (dictionary) where all keys and values are strings.
    The stored values can be converted to different types using variety of accessor methods.

    The string map is highly versatile. It can be converted into many formats, stored and sent over the wire.

    This class is widely used in Pip.Services as a basis for variety of classes, such as
    ConfigParams, ConnectionParams, CredentialParams and others.

    Example:
        value1 = StringValueMap.fromString("key1=1;key2=123.456;key3=2018-01-01")
        value1.get_as_boolean("key1")   // Result: true
        value1.get_as_integer("key2")   // Result: 123
        value1.get_as_float("key2")     // Result: 123.456
        value1.get_as_datetime("key3")  // Result: Date 2018,0,1
    """
    def __init__(self, map = None):
        """
        Creates a new instance of the map and assigns its value.

        :param map: (optional) values to initialize this map.
        """
        super(StringValueMap, self).__init__()
        if isinstance(map, dict):
            for (k, v) in map.items():
                self.put(k, v)

    def get_key_names(self):
        """
        Gets keys of all elements stored in this map.

        :return: a list with all map keys.
        """
        names = []
        for (k, _) in self.items():
            names.append(k)
        return names

    def get(self, key):
        """
        Gets a map element specified by its key.

        :param key: a key of the element to get.

        :return: the value of the map element.
        """
        return self[key] if key in self else None

    def put(self, key, value):
        """
        Puts a new value into map element specified by its key.

        :param key: a key of the element to put.

        :param value: a new value for map element.
        """
        self[key] = StringConverter.to_nullable_string(value)

    def remove(self, key):
        """
        Removes a map element specified by its key

        :param key: a key of the element to remove.
        """
        self.pop(key)

    def append(self, map):
        """
        Appends new elements to this map.

        :param map: a map with elements to be added.
        """
        if isinstance(map, dict):
            for (k, v) in map.items():
                self.put(k, v)

    def get_as_object(self, key = None):
        """
        Gets the value stored in map element without any conversions.
        When element key is not defined it returns the entire map value.

        :param key: (optional) a key of the element to get

        :return: the element value or value of the map when index is not defined.
        """
        if key == None:
            return self.get_as_map()
        else:
            return self.get(key)

    def set_as_object(self, *args):
        """
        Sets a new value to map element specified by its index.
        When the index is not defined, it resets the entire map value.
        This method has double purpose because method overrides are not supported in JavaScript.

        :param args: objects to set
        """
        if len(args) == 1:
            self.set_as_map(args[0])
        elif len(args) == 2:
            self.put(args[0], args[1])

    def get_as_map(self, key):
        """
        Converts map element into an AnyValueMap or returns empty AnyValueMap if conversion is not possible.

        :param key: a key of element to get.

        :return: AnyValueMap value of the element or empty AnyValueMap if conversion is not supported.
        """
        if key == None:
            map = {}
            for (k, v) in self.items():
                map[k] = v
            return map
        else:
            value = self.get(key)
            return MapConverter.to_map(value)

    def set_as_map(self, values):
        """
        Sets values to map

        :param values: values to set
        """
        self.clear()
        for (k, v) in values.items():
            self.put(k, v)

    def get_as_nullable_string(self, key):
        """
        Converts map element into a string or returns None if conversion is not possible.

        :param key: an index of element to get.

        :return: string value of the element or None if conversion is not supported.
        """
        value = self.get(key)
        return StringConverter.to_nullable_string(value)

    def get_as_string(self, key):
        """
        Converts map element into a string or returns "" if conversion is not possible.

        :param key: an index of element to get.

        :return: string value ot the element or "" if conversion is not supported.
        """
        value = self.get(key)
        return StringConverter.to_string(value)

    def get_as_string_with_default(self, key, default_value):
        """
        Converts map element into a string or returns default value if conversion is not possible.

        :param key: an index of element to get.

        :param default_value: the default value

        :return: string value ot the element or default value if conversion is not supported.
        """
        value = self.get(key)
        return StringConverter.to_string_with_default(value, default_value)

    def get_as_nullable_boolean(self, key):
        """
        Converts map element into a boolean or returns None if conversion is not possible

        :param key: an index of element to get.

        :return: boolean value of the element or None if conversion is not supported.
        """
        value = self.get(key)
        return BooleanConverter.to_nullable_boolean(value)

    def get_as_boolean(self, key):
        """
        Converts map element into a boolean or returns false if conversion is not possible.

        :param key: an index of element to get.

        :return: boolean value ot the element or false if conversion is not supported.
        """
        value = self.get(key)
        return BooleanConverter.to_boolean(value)

    def get_as_boolean_with_default(self, key, default_value):
        """
        Converts map element into a boolean or returns default value if conversion is not possible.

        :param key: an index of element to get.

        :param default_value: the default value

        :return: boolean value ot the element or default value if conversion is not supported.
        """
        value = self.get(key)
        return BooleanConverter.to_boolean_with_default(value, default_value)

    def get_as_nullable_integer(self, key):
        """
        Converts map element into an integer or returns None if conversion is not possible.

        :param key: an index of element to get.

        :return: integer value of the element or None if conversion is not supported.
        """
        value = self.get(key)
        return IntegerConverter.to_nullable_integer(value)

    def get_as_integer(self, key):
        """
        Converts map element into an integer or returns 0 if conversion is not possible.

        :param key: an index of element to get.

        :return: integer value ot the element or 0 if conversion is not supported.
        """
        value = self.get(key)
        return IntegerConverter.to_integer(value)

    def get_as_integer_with_default(self, key, default_value):
        """
        Converts map element into an integer or returns default value if conversion is not possible.

        :param key: an index of element to get.

        :param default_value: the default value

        :return: integer value ot the element or default value if conversion is not supported.
        """
        value = self.get(key)
        return IntegerConverter.to_integer_with_default(value, default_value)

    def get_as_nullable_long(self, key):
        value = self.get(key)
        return LongConverter.to_nullable_long(value)

    def get_as_long(self, key):
        value = self.get(key)
        return LongConverter.to_long(value)

    def get_as_long_with_default(self, key, default_value):
        value = self.get(key)
        return LongConverter.to_long_with_default(value, default_value)

    def get_as_nullable_float(self, key):
        """
        Converts map element into a float or returns None if conversion is not possible.

        :param key: an index of element to get.

        :return: float value of the element or None if conversion is not supported.
        """
        value = self.get(key)
        return FloatConverter.to_nullable_float(value)

    def get_as_float(self, key):
        """
        Converts map element into a float or returns 0 if conversion is not possible.

        :param key: an index of element to get.

        :return: float value ot the element or 0 if conversion is not supported.
        """
        value = self.get(key)
        return FloatConverter.to_float(value)

    def get_as_float_with_default(self, key, default_value):
        """
        Converts map element into a float or returns default value if conversion is not possible.

        :param key: an index of element to get.

        :param default_value: the default value

        :return: float value ot the element or default value if conversion is not supported.
        """
        value = self.get(key)
        return FloatConverter.to_float_with_default(value, default_value)

    def get_as_nullable_datetime(self, key):
        """
        Converts map element into a Date or returns None if conversion is not possible.

        :param key: an index of element to get.

        :return: Date value of the element or None if conversion is not supported.
        """
        value = self.get(key)
        return DateTimeConverter.to_nullable_datetime(value)

    def get_as_datetime(self, key):
        """
        Converts map element into a Date or returns the current date if conversion is not possible.

        :param key: an index of element to get.

        :return: Date value ot the element or the current date if conversion is not supported.
        """
        value = self.get(key)
        return DateTimeConverter.to_datetime(value)

    def get_as_datetime_with_default(self, key, default_value):
        """
        Converts map element into a Date or returns default value if conversion is not possible.

        :param key: an index of element to get.

        :param default_value: the default value

        :return: Date value ot the element or default value if conversion is not supported.
        """
        value = self.get(key)
        return DateTimeConverter.to_datetime_with_default(value, default_value)

    def get_as_nullable_type(self, key, value_type):
        """
        Converts map element into a value defined by specied typecode.
        If conversion is not possible it returns None.

        :param key: an index of element to get.

        :param value_type: the TypeCode that defined the type of the result

        :return: element value defined by the typecode or None if conversion is not supported.
        """
        value = self.get(key)
        return TypeConverter.to_nullable_type(value_type, value)

    def get_as_type(self, key, value_type):
        """
        Converts map element into a value defined by specied typecode.
        If conversion is not possible it returns default value for the specified type.

        :param key: an index of element to get.

        :param value_type: the TypeCode that defined the type of the result

        :return: element value defined by the typecode or default if conversion is not supported.
        """
        value = self.get(key)
        return TypeConverter.to_type(value_type, value)

    def get_as_type_with_default(self, key, value_type, default_value):
        """
        Converts map element into a value defined by specied typecode.
        If conversion is not possible it returns default value.

        :param key: an index of element to get.

        :param value_type: the TypeCode that defined the type of the result

        :param default_value: the default value

        :return: element value defined by the typecode or default value if conversion is not supported.
        """
        value = self.get(key)
        return TypeConverter.to_type_with_default(value_type, value, default_value)

    def get_as_array(self, key):
        """
        Converts map element into an AnyValueMap or returns empty AnyValueMap if conversion is not possible.

        :param key: an index of element to get.

        :return: AnyValueMap value of the element or empty AnyValueMap if conversion is not supported.
        """
        value = self.get(key)
        return AnyValueMap.from_value(value)

    def get_as_nullable_map(self, key):
        """
        Converts map element into an AnyValueMap or returns None if conversion is not possible.

        :param key: a key of element to get.

        :return: AnyValueMap value of the element or None if conversion is not supported.
        """
        value = self.get_as_object(key)
        return AnyValueMap.from_value(value)

    # def get_as_map(self, key):
    #     value = self.get(key)
    #     return AnyValueMap.from_value(value)

    def get_as_map_with_default(self, key, default_value):
        """
        Converts map element into an AnyValueMap or returns default value if conversion is not possible.

        :param key: a key of element to get.

        :param default_value: the default value

        :return: AnyValueMap value of the element or default value if conversion is not supported.
        """
        value = self.get_as_nullable_map(key)
        return MapConverter.to_map_with_default(value, default_value)


    def clone(self):
        """
        Creates a binary clone of this object.

        :return: a clone of this object.
        """
        map = StringValueMap()
        map.set_as_map(self)
        return map

    def __str__(self):
        """
        Gets a string representation of the object.
        The result is a semicolon-separated list of key-value pairs as
        "key1=value1;key2=value2;key=value3"

        :return: a string representation of the object.
        """
        result = ''

        for (k, v) in self.items():
            if len(result) > 0:
                result += ';'

            if v != None:
                result += k + '=' + StringConverter.to_string_with_default(v, '')
            else:
                result += k

        return result

    @staticmethod
    def from_value(value):
        """
        Converts specified value into StringValueMap.

        :param value: value to be converted

        :return: a newly created StringValueMap.
        """
        # map = RecursiveObjectReader.get_properties(value)
        return StringValueMap(value)

    @staticmethod
    def from_tuples(*tuples):
        """
        Creates a new StringValueMap from a list of key-value pairs called tuples.

        :param tuples: a list of values where odd elements are keys and the following even elements are values

        :return: a newly created StringValueMap.
        """
        return StringValueMap.from_tuples_array(*tuples)

    @staticmethod
    def from_tuples_array(tuples):
        """
        Creates a new StringValueMap from a list of key-value pairs called tuples.
        The method is similar to [[fromTuples]] but tuples are passed as array instead of parameters.

        :param tuples: a list of values where odd elements are keys and the following even elements are values

        :return: a newly created StringValueMap.
        """
        result = StringValueMap()

        if tuples == None or len(tuples) == 0:
            return result

        index = 0
        while index < len(tuples):
            if index + 1 >= len(tuples):
                break

            key = StringConverter.to_string(tuples[index])
            value = StringConverter.to_nullable_string(tuples[index + 1])
            index += 2

            result.put(key, value)

        return result

    @staticmethod
    def from_string(line):
        """
        Parses semicolon-separated key-value pairs and returns them as a StringValueMap.

        :param line: semicolon-separated key-value list to initialize StringValueMap.

        :return: a newly created StringValueMap.
        """
        result = StringValueMap()
        
        if line == None or len(line) == 0:
            return result

        tokens = str(line).split(';')
        for token in tokens:
            if len(token) == 0:
                continue
            index = token.find('=')
            key = token[0:index] if index >= 0 else token
            value = token[index + 1:] if index >= 0 else None
            result.put(key, value)

        return result


    @staticmethod
    def from_maps(*maps):
        """
        Creates a new AnyValueMap by merging two or more maps.
        Maps defined later in the list override values from previously defined maps.

        :param maps: an array of maps to be merged

        :return: a newly created AnyValueMap.
        """
        result = StringValueMap()
        
        if maps == None or len(maps) == 0:
            return result

        for map in maps:
            for (k, v) in map.items():
                key = StringConverter.to_string(k)
                result.put(key, v)

        return result
        