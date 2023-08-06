# -*- coding: utf-8 -*-
"""
    pip_services3_commons.run.IClosable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for closable components
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IClosable:
    """
    Interface for components that require explicit closure.

    For components that require opening as well as closing use [[IOpenable]] interface instead.
    """

    def close(self, correlation_id):
        """
        Closes component and frees used resources.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        raise NotImplementedError('Method from interface definition')
