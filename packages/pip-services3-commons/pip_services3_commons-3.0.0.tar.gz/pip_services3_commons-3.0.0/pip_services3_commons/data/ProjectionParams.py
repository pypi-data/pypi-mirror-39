# -*- coding: utf-8 -*-
"""
    pip_services3_commons.data.ProjectionParams
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Data projection parameters implementation

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import numpy as np
from pip_services3_commons.data import AnyValueArray


class ProjectionParams(list):
    """
    Defines projection parameters with list if fields to include into query results.

    The parameters support two formats: dot format and nested format.

    The dot format is the standard way to define included fields and subfields using
    dot object notation: <code>"field1,field2.field21,field2.field22.field221"</code>.

    As alternative the nested format offers a more compact representation:
    <code>"field1,field2(field21,field22(field221))"</code>.

    Example:
         filter = FilterParams.fromTuples("type", "Type1")
         paging = PagingParams(0, 100)
         projection = ProjectionParams.from_value("field1,field2(field21,field22)")

         myDataClient.get_data_by_filter(filter, paging, projection)
    """
    default_delimiter = ','

    def __init__(self, values = None):
        """
        Creates a new instance of the projection parameters and assigns its value.

        :param values: (optional) values to initialize this object.
        """
        super(ProjectionParams, self).__init__()

        if values != None:
            for value in values:
                self.append("" + value)

    @staticmethod
    def from_value(value = None):
        """
        Converts specified value into ProjectionParams.

        :param value: value to be converted

        :return: a newly created ProjectionParams.
        """
        if isinstance(value, ProjectionParams):
            return value
        array = AnyValueArray.from_value(value) if value != None else AnyValueArray()
        return ProjectionParams(array)

    @staticmethod
    def from_values(*values):
        """
        Parses comma-separated list of projection fields.

        :param values: one or more comma-separated lists of projection fields

        :return: a newly created ProjectionParams.
        """
        result = ProjectionParams()
        result._from_values(',', values)
        return result

    def _from_values(self, delimiter, *values):
        return ProjectionParams(self.parse(delimiter, values))

    def to_string(self):
        """
        Gets a string representation of the object.
        The result is a comma-separated list of projection fields
        "field1,field2.field21,field2.field22.field221"

        :return: a string representation of the object.
        """
        builder = ""

        index = 0
        while index < self.__len__():
            if index > 0:
                builder = builder + ','
            builder = builder + super(ProjectionParams, self).__getitem__(index)
            index = index + 1

        return builder

    def parse(self, delimiter, *values):
        result = []
        prefix = ""

        for value in values:
            self.parse_value(prefix, result, value.strip(), delimiter)

        return result
        #
        # array_result = np.asarray(result)
        # return array_result

    def parse_value(self, prefix, result, value, delimiter):
        value = value.strip()

        open_bracket = 0
        open_bracket_index = -1
        close_bracket_index = -1
        comma_index = -1

        break_cycle_required = False

        index = 0
        while index < len(value):
            value_char = value[index]
            if value_char == '(':
                if open_bracket == 0:
                    open_bracket_index = index
                open_bracket = open_bracket + 1

            elif value_char == ')':
                open_bracket = open_bracket - 1

                if open_bracket == 0:
                    close_bracket_index = index

                    if open_bracket_index >= 0 and close_bracket_index > 0:
                        previous_prefix = prefix

                        if prefix != None and len(prefix) > 0:
                            prefix = prefix + '.' + value[0:open_bracket_index]
                        else:
                            prefix = value[0:open_bracket_index]

                        sub_value = value[open_bracket_index+1:close_bracket_index]
                        self.parse_value(prefix, result, sub_value, delimiter)

                        sub_value = value[close_bracket_index+1:]
                        self.parse_value(previous_prefix, result, sub_value, delimiter)
                        break_cycle_required = True

            elif value_char == delimiter:
                if open_bracket == 0:
                    comma_index = index

                    sub_value = value[0:comma_index]
                    if sub_value != None and len(sub_value) > 0:
                        if prefix != None and len(prefix) > 0:
                            result.append(prefix + '.' + sub_value)
                        else:
                            result.append(sub_value)

                    sub_value = value[comma_index + 1:]

                    if sub_value != None and len(sub_value) > 0:
                        self.parse_value(prefix, result, sub_value, delimiter)
                        break_cycle_required = True

            if break_cycle_required:
                break

        if value != None and len(value) > 0 and open_bracket_index == -1 and comma_index == -1:
            if prefix != None and len(prefix) > 0:
                result.append(prefix + '.' + value)
            else:
                result.append(value)