# -*- coding: utf-8 -*-
"""
    pip_services3_commons.data.IVersioned
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for versioned data objects
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IVersioned:
    """
    Interface for data objects that can be versioned.

    Versioning is often used as optimistic concurrency mechanism.

    The version doesn't have to be a number, but it is recommended to use sequential
    values to determine if one object has newer or older version than another one.

    It is a common pattern to use the time of change as the object version

    Example:
        class MyData(IStringIdentifiable, IVersioned):
            id = None
            version = None
            ...

            def update_data(item):
                ...
                if item.version < old_item.version:
                    raise ConcurrencyException(null, "VERSION_CONFLICT", "The change has older version stored value")
            ...
    """
    # version = None
    pass
