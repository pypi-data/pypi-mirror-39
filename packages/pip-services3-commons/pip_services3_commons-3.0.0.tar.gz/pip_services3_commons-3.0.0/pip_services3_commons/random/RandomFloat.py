# -*- coding: utf-8 -*-
"""
    pip_services3_commons.random.RandomFloat
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    RandomFloat implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random

class RandomFloat(object):
    """
    Random generator for float values.

    Example:
        value1 = RandomFloat.next_float(5, 10)     // Possible result: 7.3
        value2 = RandomFloat.next_float(10)        // Possible result: 3.7
        value3 = RandomFloat.update_float(10, 3)   // Possible result: 9.2
    """
    @staticmethod
    def next_float(min, max = None):
        """
        Generates a float in the range ['min', 'max']. If 'max' is omitted, then the range will be set to [0, 'min'].

        :param min: minimum value of the float that will be generated.
                   If 'max' is omitted, then 'max' is set to 'min' and 'min' is set to 0.

        :param max: (optional) maximum value of the float that will be generated. Defaults to 'min' if omitted.

        :return: generated random float value.
        """
        if max == None:
            max = min
            min = 0

        if max - min <= 0:
            return min

        return min + random.random() * (max - min)

    @staticmethod
    def update_float(value, range = None):
        """
        Updates (drifts) a float value within specified range defined

        :param value: a float value to drift.

        :param range: (optional) a range. Default: 10% of the value

        :return: updated random float value.
        """
        if range == None:
            range = 0.1 * value
        
        min = value - range
        max = value + range
        return RandomFloat.next_float(min, max)
