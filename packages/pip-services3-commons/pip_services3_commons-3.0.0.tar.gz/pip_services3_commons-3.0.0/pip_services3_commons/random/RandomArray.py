# -*- coding: utf-8 -*-
"""
    pip_services3_commons.random.RandomArray
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    RandomArray implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random

class RandomArray():
    """
    Random generator for array objects.

    Example:
        value1 = RandomArray.pick([1, 2, 3, 4]) // Possible result: 3
    """
    @staticmethod
    def pick(values):
        """
        Picks a random element from specified array.

        :param values: an array of any type

        :return: a randomly picked item.
        """
        if values == None or len(values) == 0:
            return None

        return random.choice(values)
