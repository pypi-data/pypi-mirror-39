# -*- coding: utf-8 -*-
"""
    pip_services3_commons.data.ITrackable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for trackable data objects
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ITrackable:
    """
    Interface for data objects that can track their changes, including logical deletion.

    Example:
        class MyData(IStringIdentifiable, ITrackable):
            id = None
            ...

            change_time = None
            create_time = None
            deleted = None
    """
    # create_time = None
    # change_time = None
    # deleted = None
    pass
