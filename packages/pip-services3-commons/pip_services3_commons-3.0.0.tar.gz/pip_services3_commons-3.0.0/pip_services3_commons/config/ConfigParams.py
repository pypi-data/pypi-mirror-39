# -*- coding: utf-8 -*-
"""
    pip_services3_commons.config.ConfigParams
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Config params implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..data.StringValueMap import StringValueMap
from ..reflect.RecursiveObjectReader import RecursiveObjectReader

class ConfigParams(StringValueMap):
    """
    Contains a key-value map with configuration parameters.
    All values stored as strings and can be serialized as JSON or string forms.
    When retrieved the values can be automatically converted on read using GetAsXXX methods.

    The keys are case-sensitive, so it is recommended to use consistent C-style as: <code>"my_param"</code>

    Configuration parameters can be broken into sections and subsections using dot notation as:
    <code>"section1.subsection1.param1"</code>. Using GetSection method all parameters from specified section
    can be extracted from a ConfigMap.

    The ConfigParams supports serialization from/to plain strings as:
    <code>"key1=123;key2=ABC;key3=2016-09-16T00:00:00.00Z"</code>

    ConfigParams are used to pass configurations to [[IConfigurable]] objects.
    They also serve as a basis for more concrete configurations such as ConnectionParams
    or CredentialParams (in the Pip.Services components package).

    Example:
        [code]
        config = ConfigParams.fromTuples("section1.key1", "AAA",
                                         "section1.key2", 123,
                                         "section2.key1", true)
        config.get_as_string("section1.key1") // Result: AAA
        config.get_as_integer("section1.key1") // Result: 0

        section1 = config.get_section("section1")
        section1.__str__() // Result: key1=AAA;key2=123
        [/code]
    """

    def __init__(self, values = None):
        """
        Creates a new ConfigParams and fills it with values.

        :param values: (optional) an object to be converted into key-value pairs to initialize this config map.
        """
        super(ConfigParams, self).__init__(values)

    def get_section_names(self):
        """
        Gets a list with all 1st level section names.

        :return: a list of section names stored in this ConfigMap.
        """
        sections = []
        
        for (key, value) in self.items():
            pos = key.find('.')
            if pos > 0:
                key = key[0 : pos]

            # Perform case sensitive search
            found = False
            for section in sections:
                if section == key:
                    found = True
                    break
                
            if not found:
                sections.append(key)
        
        return sections


    def get_section(self, section):
        """
        Gets parameters from specific section stored in this ConfigMap.
        The section name is removed from parameter keys.

        :param section: name of the section to retrieve configuration parameters from.

        :return: all configuration parameters that belong to the section named 'section'.
        """
        result = ConfigParams()
        prefix = section + "."
        
        for (key, value) in self.items():
            # Prevents exception on the next line
            if len(key) < len(prefix):
                continue
            
            # Perform case sensitive match
            key_prefix = key[: len(prefix)]
            if key_prefix == prefix:
                key = key[len(prefix): ]
                result[key] = value
        
        return result


    def _is_shadow_name(self, name):
        return name == None or len(name) == 0 or name[0] == "#" or name[0] == "!"


    def add_section(self, section, section_params):
        """
        Adds parameters into this ConfigParams under specified section.
        Keys for the new parameters are appended with section dot prefix.

        :param section: name of the section where add new parameters

        :param section_params: new parameters to be added.
        """
        if section == None:
            raise Exception("Section name cannot be null")

        section = "" if self._is_shadow_name(section) else section 
        
        if section_params == None or len(section_params) == 0:
            return

        for (key, value) in section_params.items():
            key = "" if self._is_shadow_name(key) else key
            
            if len(key) > 0 and len(section) > 0:
                key = section + "." + key
            elif len(key) == 0:
                key = section

            self[key] = value


    def override(self, config_params):
        """
        Overrides parameters with new values from specified ConfigParams and returns a new ConfigParams object.

        :param config_params: ConfigMap with parameters to override the current values.

        :return: a new ConfigParams object.
        """
        map = StringValueMap.from_maps(self, config_params)
        return ConfigParams(map)


    def set_defaults(self, default_config_params):
        """
        Set default values from specified ConfigParams and returns a new ConfigParams object.

        :param default_config_params: ConfigMap with default parameter values.

        :return: a new ConfigParams object.
        """
        map = StringValueMap.from_maps(default_config_params, self)
        return ConfigParams(map)


    @staticmethod
    def from_value(value):
        """
        Creates a new ConfigParams object filled with key-value pairs from specified object.

        :param value: an object with key-value pairs used to initialize a new ConfigParams.

        :return: a new ConfigParams object.
        """
        map = RecursiveObjectReader.get_properties(value)
        return ConfigParams(map)

    
    @staticmethod
    def from_tuples(*tuples):
        """
        Creates a new ConfigParams object filled with provided key-value pairs called tuples.
        Tuples parameters contain a sequence of key1, value1, key2, value2, ... pairs.

        :param tuples: the tuples to fill a new ConfigParams object.

        :return: a new ConfigParams object.
        """
        map = StringValueMap.from_tuples_array(tuples)
        return ConfigParams(map)

    
    @staticmethod
    def from_string(line):
        """
        Creates a new ConfigParams object filled with key-value pairs serialized as a string.

        :param line: a string with serialized key-value pairs as "key1=value1;key2=value2;..."

        :return: a new ConfigParams object.
        """
        map = StringValueMap.from_string(line)
        return ConfigParams(map)


    @staticmethod
    def merge_configs(*configs):
        """
        Merges two or more ConfigParams into one. The following ConfigParams override previously defined parameters.

        :param configs: a list of ConfigParams objects to be merged.

        :return: a new ConfigParams object.
        """
        map = StringValueMap.from_maps(*configs)
        return ConfigParams(map)
