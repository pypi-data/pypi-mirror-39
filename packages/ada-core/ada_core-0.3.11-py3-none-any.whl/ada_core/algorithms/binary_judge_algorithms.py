"""
Author: qiacai
"""


from ada_core.algorithms import Algorithm
from ada_core.data_model.entry import Entry
from ada_core.data_model.time_series import TimeSeries


class Equals(Algorithm):
    def __init__(self):
        super(Equals, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if isinstance(input_value.left, TimeSeries) or isinstance(input_value.left, Entry):
            return input_value.left.equals(input_value.right)
        elif isinstance(input_value.right, TimeSeries) or isinstance(input_value.right, Entry):
            return input_value.right.equals(input_value.left)
        else:
            return True if input_value.left == input_value.right else False


class GreaterThan(Algorithm):
    def __init__(self):
        super(GreaterThan, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if isinstance(input_value.left, TimeSeries) or isinstance(input_value.left, Entry):
            return input_value.left.greaterThan(input_value.right)
        elif isinstance(input_value.right, TimeSeries) or isinstance(input_value.right, Entry):
            return input_value.right.lessThan(input_value.left)
        else:
            return True if input_value.left > input_value.right else False


class GreaterThanOrEquals(Algorithm):
    def __init__(self):
        super(GreaterThanOrEquals, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if isinstance(input_value.left, TimeSeries) or isinstance(input_value.left, Entry):
            return input_value.left.greaterThanOrEquals(input_value.right)
        elif isinstance(input_value.right, TimeSeries) or isinstance(input_value.right, Entry):
            return input_value.right.lessThanOrEquals(input_value.left)
        else:
            return True if input_value.left >= input_value.right else False


class LessThan(Algorithm):
    def __init__(self):
        super(LessThan, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if isinstance(input_value.left, TimeSeries) or isinstance(input_value.left, Entry):
            return input_value.left.lessThan(input_value.right)
        elif isinstance(input_value.right, TimeSeries) or isinstance(input_value.right, Entry):
            return input_value.right.greaterThan(input_value.left)
        else:
            return True if input_value.left < input_value.right else False


class LessThanOrEquals(Algorithm):
    def __init__(self):
        super(LessThanOrEquals, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if isinstance(input_value.left, TimeSeries) or isinstance(input_value.left, Entry):
            return input_value.left.lessThanOrEquals(input_value.right)
        elif isinstance(input_value.right, TimeSeries) or isinstance(input_value.right, Entry):
            return input_value.right.greaterThanOrEquals(input_value.left)
        else:
            return True if input_value.left <= input_value.right else False


class ANDLogic(Algorithm):
    def __init__(self):
        super(ANDLogic, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if input_value.left and input_value.right:
            return True
        else:
            return False


class ORLogic(Algorithm):
    def __init__(self):
        super(ORLogic, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if input_value.left or input_value.right:
            return True
        else:
            return False


class XORLogic(Algorithm):
    def __init__(self):
        super(XORLogic, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if input_value.left and input_value.right:
            return False
        elif not input_value.left and not input_value.right:
            return False
        else:
            return True