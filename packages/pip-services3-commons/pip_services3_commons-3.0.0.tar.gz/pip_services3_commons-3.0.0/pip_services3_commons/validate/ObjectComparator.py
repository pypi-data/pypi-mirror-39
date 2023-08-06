# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.ObjectComparator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Object comparator implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import re

from ..convert.FloatConverter import FloatConverter

class ObjectComparator(object):
    """
    Helper class to perform comparison operations over arbitrary values.

    Example:
        ObjectComparator.compare(2, "GT", 1)        // Result: true
        ObjectComparator.areEqual("A", "B")         // Result: false
    """
    @staticmethod
    def compare(value1, operation, value2):
        """
        Perform comparison operation over two arguments.
        The operation can be performed over values of any type.

        :param value1: the first argument to compare

        :param operation: the comparison operation: "==" ("=", "EQ"), "!= " ("<>", "NE"); "<"/">"
                                                    ("LT"/"GT"), "<="/">=" ("LE"/"GE"); "LIKE".

        :param value2: the second argument to compare

        :return: result of the comparison operation
        """
        if operation == None:
            return False
        
        operation = operation.upper()

        if operation in ["=", "==", "EQ"]:
            return ObjectComparator.are_equal(value1, value2)
        if operation in ["!=", "<>", "NE"]:
            return ObjectComparator.are_not_equal(value1, value2)
        if operation in ["<", "LT"]:
            return ObjectComparator.less(value1, value2)
        if operation in ["<=", "LE"]:
            return ObjectComparator.are_equal(value1, value2) or ObjectComparator.less(value1, value2)
        if operation in [">", "GT"]:
            return ObjectComparator.more(value1, value2)
        if operation in [">=", "GE"]:
            return ObjectComparator.are_equal(value1, value2) or ObjectComparator.more(value1, value2)
        if operation == "LIKE":
            return ObjectComparator.match(value1, value2)

        return True

    @staticmethod
    def are_equal(value1, value2):
        """
        Checks if two values are equal. The operation can be performed over values of any type.

        :param value1: the first value to compare

        :param value2: the second value to compare

        :return: true if values are equal and false otherwise
        """
        if value1 == None or value2 == None:
            return True
        if value1 == None or value2 == None:
            return False
        return value1 == value2

    @staticmethod
    def are_not_equal(value1, value2):
        """
        Checks if two values are NOT equal. The operation can be performed over values of any type.

        :param value1: the first value to compare

        :param value2: the second value to compare

        :return: true if values are NOT equal and false otherwise
        """
        return not ObjectComparator.are_equal(value1, value2)

    @staticmethod
    def less(value1, value2):
        """
        Checks if first value is less than the second one.
        The operation can be performed over numbers or strings.

        :param value1: the first value to compare

        :param value2: the second value to compare

        :return: true if the first value is less than second and false otherwise.
        """
        number1 = FloatConverter.to_nullable_float(value1)
        number2 = FloatConverter.to_nullable_float(value2)

        if number1 == None or number2 == None:
            return False

        return number1 < number2

    @staticmethod
    def more(value1, value2):
        """
        Checks if first value is greater than the second one.
        The operation can be performed over numbers or strings.

        :param value1: the first value to compare

        :param value2: the second value to compare

        :return: true if the first value is greater than second and false otherwise.
        """
        number1 = FloatConverter.to_nullable_float(value1)
        number2 = FloatConverter.to_nullable_float(value2)

        if number1 == None or number2 == None:
            return False

        return number1 > number2

    @staticmethod
    def match(value1, value2):
        """
        Checks if string matches a regular expression

        :param value1: a string value to match

        :param value2: a regular expression string

        :return: true if the value matches regular expression and false otherwise.
        """
        if value1 == None and value2 == None:
            return True
        if value1 == None or value2 == None:
            return False

        string1 = str(value1)
        string2 = str(value2)
        return re.match(string2, string1) != None
