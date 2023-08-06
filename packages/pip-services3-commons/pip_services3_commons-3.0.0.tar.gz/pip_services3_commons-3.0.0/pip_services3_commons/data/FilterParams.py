# -*- coding: utf-8 -*-
"""
    pip_services3_commons.data.FilterParams
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Free-form filter parameters implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .StringValueMap import StringValueMap

class FilterParams(StringValueMap):
    """
    Data transfer object used to pass filter parameters as simple key-value pairs.

    Example:
        filter = FilterParams.from_tuples("type", "Type1",
        "from_create_time", datetime.datetime(2000, 0, 1),
        "to_create_time", datetime.datetime.now(),
        "completed", true)
        paging = PagingParams(0, 100)

        myDataClient.get_data_by_filter(filter, paging)
    """

    def __init__(self, map = None):
        super(FilterParams, self).__init__(map)
        # if map != None:
        #     for (key, value) in map.items():
        #         self[key] = value

    @staticmethod
    def from_value(value):
        """
        Converts specified value into FilterParams.

        :param value: value to be converted

        :return: a newly created FilterParams.
        """
        return FilterParams(value)

    @staticmethod
    def from_tuples(*tuples):
        """
        Creates a new FilterParams from a list of key-value pairs called tuples.

        :param tuples: a list of values where odd elements are keys and the following even elements are values

        :return: a newly created FilterParams.
        """
        map = StringValueMap.from_tuples_array(tuples)
        return FilterParams(map)

    @staticmethod
    def from_string(line):
        """
        Parses semicolon-separated key-value pairs and returns them as a FilterParams.

        :param line: semicolon-separated key-value list to initialize FilterParams.

        :return: a newly created FilterParams.
        """
        map = StringValueMap.from_string(line)
        return FilterParams(map)
