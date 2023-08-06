"""
Author: qiacai
"""

import numpy as np

from ada_core import exceptions, utils, constants
from ada_core.algorithms import Algorithm
from ada_core.data_model.io_data_type import AlgorithmIODataType


class Mean(Algorithm):

    def __init__(self):
        super(Mean, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value, default=None):
        return input_value.mean(default)


class Median(Algorithm):

    def __init__(self):
        super(Median, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value, default=None):
        return input_value.median(default)


class Max(Algorithm):

    def __init__(self):
        super(Max, self).__init__(self.__class__.__name__)
        # self.name = 'max'

    def _run_algorithm(self, input_value, default=None):
        return input_value.max(default)


class Min(Algorithm):

    def __init__(self):
        super(Min, self).__init__(self.__class__.__name__)
        # self.name = 'min'

    def _run_algorithm(self, input_value, default=None):
        return input_value.min(default)


class Std(Algorithm):

    def __init__(self):
        super(Std, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value, default=None):
        return input_value.std(default)


class Mad(Algorithm):

    def __init__(self):
        super(Mad, self).__init__(self.__class__.__name__)
        # self.name = 'mad'

    def _run_algorithm(self, input_value, default=None):
        return input_value.mad(default)


class Count(Algorithm):

    def __init__(self):
        super(Count, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value, default=None):
        return input_value.count(default)


class Sum(Algorithm):

    def __init__(self):
        super(Sum, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value, default=None):
        return input_value.sum(default)


class Percentile(Algorithm):

    def __init__(self):
        super(Percentile, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value, default=None, percent=None):

        if percent is None:
            percent = constants.ALGORITHM_DEFAULT_CALCULATOR_PERCENTILE_PERCENTILE

        return np.asscalar(
            np.percentile(input_value.getValueList(), percent)) if input_value.getValueList() else default


class Cushion(Algorithm):

    def __init__(self):
        super(Cushion, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value, default=None, upper_percentile=None, lower_percentile=None, is_upper=None):

        if upper_percentile is None and lower_percentile is None:
            upper_percentile = constants.ALGORITHM_DEFAULT_CALCULATOR_CUSHION_UPPER_PERCENTILE
            lower_percentile = constants.ALGORITHM_DEFAULT_CALCULATOR_CUSHION_LOWER_PERCENTILE
        elif lower_percentile is None:
            lower_percentile = 100 - upper_percentile
        elif upper_percentile is None:
            upper_percentile = 100 - lower_percentile

        if is_upper is None:
            is_upper = constants.ALGORITHM_DEFAULT_CALCULATOR_CUSHION_IS_UPPER

        if input_value.getValueList():
            valueList = input_value.getValueList()
            median_value = np.asscalar(np.median(valueList))
            upper_value = np.asscalar(np.percentile(valueList, upper_percentile))
            lower_value = np.asscalar(np.percentile(valueList, lower_percentile))

            if upper_value == lower_value:
                return 0.5
            else:
                if not is_upper:
                    return (median_value - lower_value) / (upper_value - lower_value)
                else:
                    return (upper_value - median_value) / (upper_value - lower_value)
        else:
            return default