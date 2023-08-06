# -*- coding: utf-8 -*-
"""
    pip_services3_commons.data.IChangeable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for changeable data objects
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IChangeable:
    """
    Interface for data objects that contain their latest change time.

    Example:
        class MyData(IStringIdentifiable, IChangeable):
            id = None
            change_time = None
            ...

    """
    # change_time = None
    pass
