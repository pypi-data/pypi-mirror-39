# -*- coding: utf-8 -*-
"""
    pip_services3_commons.data.PagingParams
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Data paging parameters implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..convert.IntegerConverter import IntegerConverter
from ..convert.BooleanConverter import BooleanConverter
from .AnyValueMap import AnyValueMap

class PagingParams():
    """
    Data transfer object to pass paging parameters for queries.

    The page is defined by two parameters:
    - the <code>skip</code> parameter defines number of items to skip.
    - the <code>take</code> parameter sets how many items to return in a page.
    - additionally, the optional <code>total</code> parameter tells to return total number of items in the query.

     Remember: not all implementations support the <code>total</code> parameter
     because its generation may lead to severe performance implications.

     Example:
         filter = FilterParams.fromTuples("type", "Type1")
         paging = PagingParams(0, 100)

         myDataClient.get_data_by_filter(filter, paging)
    """

    skip = None
    take = None
    total = True

    def __init__(self, skip = None, take = None, total = True):
        """
        Creates a new instance and sets its values.

        :param skip: the number of items to skip.

        :param take: the number of items to return.

        :param total: true to return the total number of items.
        """
        self.skip = IntegerConverter.to_nullable_integer(skip)
        self.take = IntegerConverter.to_nullable_integer(take)
        self.total = BooleanConverter.to_boolean_with_default(total, True)

    def get_skip(self, min_skip):
        """
        Gets the number of items to skip.

        :param min_skip: the minimum number of items to skip.

        :return: the number of items to skip.
        """
        if self.skip == None:
            return min_skip
        if self.skip < min_skip:
            return min_skip
        return self.skip 

    def get_take(self, max_take):
        """
        Gets the number of items to return in a page.

        :param max_take: the maximum number of items to return.

        :return: the number of items to return.
        """
        if self.take == None:
            return max_take
        if self.take < 0:
            return 0
        if self.take > max_take:
            return max_take
        return self.take

    def has_total(self):
        return self.total

    def to_json(self):
        return {
            'skip': self.skip,
            'take': self.take,
            'total': self.total
        }

    @staticmethod
    def from_json(value):
        if not isinstance(value, dict):
            return value
        
        skip = value['skip'] if 'skip' in value else None
        take = value['take'] if 'take' in value else None
        total = value['total'] if 'total' in value else None
        return PagingParams(skip, take, total)

    @staticmethod
    def from_value(value):
        """
        Converts specified value into PagingParams.

        :param value: value to be converted

        :return: a newly created PagingParams.
        """
        if isinstance(value, PagingParams):
            return value
        if isinstance(value, AnyValueMap):
            return PagingParams.from_map(value)
        
        map = AnyValueMap.from_value(value)
        return PagingParams.from_map(map)

    @staticmethod
    def from_tuples(*tuples):
        """
        Creates a new PagingParams from a list of key-value pairs called tuples.

        :param tuples: a list of values where odd elements are keys and the following even elements are values

        :return: a newly created PagingParams.
        """
        map = AnyValueMap.from_tuples_array(tuples)
        return PagingParams.from_map(map)

    @staticmethod
    def from_map(map):
        """
        Creates a new PagingParams and sets it parameters from the specified map

        :param map: a AnyValueMap or StringValueMap to initialize this PagingParams

        :return: a newly created PagingParams.
        """
        skip = map.get_as_nullable_integer("skip")
        take = map.get_as_nullable_integer("take")
        total = map.get_as_nullable_boolean("total")
        return PagingParams(skip, take, total)
