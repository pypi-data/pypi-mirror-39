# -*- coding: utf-8 -*-
"""
    pip_services3_commons.run.IExecutable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for executable components with parameters
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IExecutable:
    """
    Interface for components that can be called to execute work.
    """

    def execute(self, correlation_id, args):
        """
        Executes component with arguments and receives execution result.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param args: execution arguments.

        :return: execution result
        """
        raise NotImplementedError('Method from interface definition')
