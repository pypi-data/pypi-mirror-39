# -*- coding: utf-8 -*-
"""
    pip_services3_commons.run.IParameterized
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for parameterized components
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IParameterized:
    """
    Interface for components that require execution parameters.
    """

    def set_parameters(self, parameters):
        """
        Sets execution parameters.

        :param parameters: execution parameters.
        """
        raise NotImplementedError('Method from interface definition')
