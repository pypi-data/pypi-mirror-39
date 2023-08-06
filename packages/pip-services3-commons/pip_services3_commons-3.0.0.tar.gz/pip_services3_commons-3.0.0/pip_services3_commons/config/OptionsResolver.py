# -*- coding: utf-8 -*-
"""
    pip_services3_commons.config.OptionsResolver
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Options resolver implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ConfigParams import ConfigParams
from ..refer.Descriptor import Descriptor

class OptionsResolver(object):
    """
    A helper class to parameters from "options" configuration section.

    Example:
        [code]
        config = ConfigParams.fromTuples(
          ...
          "options.param1", "ABC",
          "options.param2", 123)

        options = OptionsResolver.resolve(config)
        [/code]
    """
    @staticmethod
    def resolve(config, config_as_default = False):
        """
        Resolves an "options" configuration section from component configuration parameters.

        :param config: configuration parameters

        :param config_as_default: (optional) When set true the method returns the entire parameter
                                  set when "options" section is not found. Default: false

        :return: configuration parameters from "options" section
        """
        options = config.get_section("options")

        if len(options) == 0 and config_as_default:
            options = config

        return options