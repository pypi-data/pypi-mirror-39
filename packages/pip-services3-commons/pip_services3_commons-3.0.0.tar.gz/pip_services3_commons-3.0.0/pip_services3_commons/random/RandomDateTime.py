# -*- coding: utf-8 -*-
"""
    pip_services3_commons.random.RandomDateTime
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    RandomDateTime implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random
import datetime
import time
import pytz
from pip_services3_commons.random import RandomFloat

from .RandomInteger import RandomInteger

class RandomDateTime(object):
    """
    Random generator for Date time values.

    Example:
        value1 = RandomDateTime.next_date(datetime.datetime(2010,0,1));    // Possible result: 2008-01-03
        value2 = RandomDateTime.next_datetime(datetime.datetime(2017,0.1));// Possible result: 2007-03-11 11:20:32
        value3 = RandomDateTime.update_datetime(datetime.datetime(2010,1,2));// Possible result: 2010-02-05 11:33:23
    """
    @staticmethod
    def next_date(min_year = None, max_year = None):
        """
        Generates a random Date in the range ['minYear', 'maxYear'].
        This method generate dates without time (or time set to 00:00:00)

        :param min_year: (optional) minimum range value

        :param max_year: max range value

        :return: a random Date value.
        """
        current_year = datetime.datetime.utcnow().year
        min_year = min_year if min_year != None else current_year - RandomInteger.next_integer(10)
        max_year = max_year if max_year != None else current_year

        year = RandomInteger.next_integer(min_year, max_year)
        month = RandomInteger.next_integer(1, 13)
        day = RandomInteger.next_integer(1, 32)
        
        if month == 2:
            day = min(28, day)
        elif month in [4, 6, 9, 11]:
            day = min(30, day)

        return datetime.datetime(year, month, day, 0, 0, 0, 0, pytz.utc)

    @staticmethod
    def next_time():
        hour = RandomInteger.next_integer(0, 24)
        min = RandomInteger.next_integer(0, 60)
        sec = RandomInteger.next_integer(0, 60)
        millis = RandomInteger.next_integer(0, 1000)

        return datetime.time(hour, min, sec, millis)

    @staticmethod
    def next_datetime(min_year = None, max_year = None):
        """
        Generates a random Date and time in the range ['minYear', 'maxYear'].
        This method generate dates without time (or time set to 00:00:00)

        :param min_year: (optional) minimum range value

        :param max_year: max range value

        :return: a random Date and time value.
        """
        date = RandomDateTime.next_date(min_year, max_year).date()
        time = RandomDateTime.next_time()
        return datetime.datetime.combine(date, time)

    @staticmethod
    def update_datetime(value, range = None):
        """
        Updates (drifts) a Date value within specified range defined

        :param value: a Date value to drift.

        :param range: (optional) a range in milliseconds. Default: 10 days

        :return: an updated DateTime value.
        """
        range = range if range != None else 10
        if range < 0:
            return value
        
        days = RandomFloat.next_float(-range, range)

        return value + datetime.timedelta(days)
