# -*- coding: utf-8 -*-
"""
    pip_services3_commons.convert.LongConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Long conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class LongConverter():

    @staticmethod
    def to_nullable_long(value):
        # Shortcuts
        if value == None:
            return None

        try:
            value = float(value)
            return int(value)
        except:
            return None

    @staticmethod
    def to_long(value):
        return LongConverter.to_long_with_default(value, 0)

    @staticmethod
    def to_long_with_default(value, default_value):
        result = LongConverter.to_nullable_long(value)
        return result if result != None else default_value

