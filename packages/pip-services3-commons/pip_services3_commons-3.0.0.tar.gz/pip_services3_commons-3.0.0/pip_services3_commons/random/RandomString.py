# -*- coding: utf-8 -*-
"""
    pip_services3_commons.random.RandomString
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    RandomString implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random

from .RandomInteger import RandomInteger
from .RandomBoolean import RandomBoolean 

_digits = "01234956789"
_symbols = "_,.:-/.[].{},#-!,$=%.+^.&*-() "
_alpha_lower = "abcdefghijklmnopqrstuvwxyz"
_alpha_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
_alpha = _alpha_upper + _alpha_lower
_chars = _alpha + _digits + _symbols

class RandomString(object):
    """
    Random generator for string values.

    Example:
        value1 = RandomString.pickChar("ABC")     // Possible result: "C"
        value2 = RandomString.pick(["A","B","C"]) // Possible result: "gBW"
    """
    @staticmethod
    def pick(values):
        """
        Picks a random string from an array of string.

        :param values: a string to pick from

        :return: a randomly picked string.
        """
        if values == None or len(values) == 0:
            return None

        return random.choice(values)

    @staticmethod
    def distort(value):
        """
        Distorts a string by randomly replacing characters in it.

        :param value: a string to distort.

        :return: a distored string.
        """
        value = value.lower()

        if (RandomBoolean.chance(1, 5)):
            value = value[0:1].upper() + value[1:]

        if (RandomBoolean.chance(1, 3)):
            value = value + random.choice(_symbols)

        return value

    @staticmethod
    def next_alpha_char():
        """
        Generates random alpha characted [A-Za-z]
        :return: a random characted.
        """
        return random.choice(_alpha)

    @staticmethod
    def next_string(min_size, max_size):
        """
        Generates a random string, consisting of upper and lower case letters (of the English alphabet),
        digits (0-9), and symbols ("_,.:-/.[].{},#-!,$=%.+^.&*-() ").

        :param min_size: (optional) minimum string length.

        :param max_size: maximum string length.

        :return: a random string.
        """
        result = ''
        
        max_size = max_size if max_size != None else min_size
        length = RandomInteger.next_integer(min_size, max_size)
        for i in range(length):
            result += random.choice(_chars)

        return result
