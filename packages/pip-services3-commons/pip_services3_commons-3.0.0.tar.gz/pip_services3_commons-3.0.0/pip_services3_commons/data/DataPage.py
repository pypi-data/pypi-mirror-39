# -*- coding: utf-8 -*-
"""
    pip_services3_commons.data.DataPage
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Data page implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class DataPage():
    """
    Data transfer object that is used to pass results of paginated queries.
    It contains items of retrieved page and optional total number of items.

    Most often this object type is used to send responses to paginated queries.
    Pagination parameters are defined by [[PagingParams]] object.
    The <code>skip</code> parameter in the PagingParams there means how many items to skip.
    The <code>takes</code> parameter sets number of items to return in the page.
    And the optional <code>total</code> parameter tells to return total number of items in the query.

    Remember: not all implementations support the <code>total</code> parameter
    because its generation may lead to severe performance implications.

    Example:
        myDataClient.get_data_by_filter("123",
                                        FilterParams.fromTuples("completed", true),
                                        PagingParams(0, 100, true),
                                        page)
        for item in page.get_data():
            print item
    """

    total = None
    data = None

    def __init__(self, data, total = None):
        """
        Creates a new instance of data page and assigns its values.

        :param data: a list of items from the retrieved page.

        :param total: total amount of items in a request.
        """
        self.data = data
        self.total = total

    def to_json(self):
        return {
            'data': self.data,
            'total': self.total
        }

    @staticmethod
    def from_json(value):
        if not isinstance(value, dict):
            return value

        data = value['data'] if 'data' in value else []
        total = value['total'] if 'total' in value else None
        return DataPage(data, total)