# -*- coding: utf-8 -*-
"""
    pip_services3_commons.config.IConfigurable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for components that require configuration
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IConfigurable:
    """
     An interface to set configuration parameters to an object.

     It can be added to any existing class by implementing a single <code>configure()</code> method.

     If you need to emphasis the fact that <code>configure()</code> method can be called multiple times
     to change object configuration in runtime, use [[IReconfigurable]] interface instead.

     Example:
         [code]
         class MyClass(IConfigurable):
            _myParam = "default value"

         def configure(self, config):
            self._myParam = config.get_as_string_with_default("options.param", myParam)
         [/code]
    """

    def configure(self, config):
        """
        Configures object by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        raise NotImplementedError('Method from interface definition')
