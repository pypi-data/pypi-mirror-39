"""
Author: qiacai
"""

from ada_core import exceptions, constants, utils
from ada_core.algorithms import Algorithm
from ada_core.data_model.io_data_type import AlgorithmIODataType
from ada_core.data_model.time_series import TimeSeries


class NOTLogic(Algorithm):
    def __init__(self):
        super(NOTLogic, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):

        return False if input_value else True


class HardThreshold(Algorithm):
    def __init__(self):
        super(HardThreshold, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value, operator, threshold, local_window=None, timezone=None):

        if local_window is None:
            local_window = constants.ALGORITHM_DEFAULT_HARD_THRESHOLD_LOCAL_WINDOW

        if timezone is None:
            timezone = constants.ALGORITHM_DEFAULT_HARD_THRESHOLD_TIMEZONE

        from ada_core.handler import Handler
        try:
            if type(input_value) == AlgorithmIODataType.ENTRY.value.native_type:
                compare_value = input_value.value
            elif type(input_value) == AlgorithmIODataType.TIME_SERIES.value.native_type:
                local_ts = input_value.splitByWindow(window=local_window, timezone=timezone)
                mean_handler = Handler(algorithm_name='mean', handler_input=local_ts)
                compare_value = mean_handler.get_result()
            else:
                compare_value = input_value
        except (ValueError, AttributeError, Exception) as e:
            raise exceptions.AlgorithmCalculationError("Error when calculate compare value: {}".format(e))

        try:
            op_input_type = AlgorithmIODataType.BINARY_NUM_INPUT.value()
            op_input = op_input_type.to_native({'left': compare_value, 'right': threshold})
            op_handler = Handler(algorithm_name=operator, handler_input=op_input)
            return op_handler.get_result()

        except (ValueError, AttributeError, Exception) as e:
            raise exceptions.AlgorithmCalculationError("Error when doing operator value: {}".format(e))


class SoftThreshold(Algorithm):
    def __init__(self):
        super(SoftThreshold, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value, operator, factor=None, local_window=None, benchmark_size=None, benchmark_method=None,
                       bound_method=None, timezone=None, period_window=None, period_method=None):

        if operator in ['>', '>=']:
            sign = 1
        else:
            sign = -1

        if local_window is None:
            local_window = constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_LOCAL_WINDOW

        if benchmark_size is None:
            benchmark_size = constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_BENCHMARK_SIZE

        if benchmark_method is None:
            benchmark_method = constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_BENCHMARK_METHOD

        if bound_method is None:
            bound_method = constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_BOUND_METHOD

        if factor is None:
            factor = constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_FACTOR

        if timezone is None:
            timezone = constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_TIMEZONE

        if period_window is None:
            period_window = constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_PERIOD_WINDOW

        if str(period_window)[0] == '0' or str(period_window)[:2] == '-0':
            period_window = None

        if period_method is None:
            period_method = constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_PERIOD_METHOD


        from ada_core.handler import Handler

        # preprocess for seasonal decompose
        if period_window and period_method=='seasonal_decompose':
            input_value = Handler(algorithm_name='seasonal_decompose', handler_input=input_value, params={'trend_only': True, 'is_fillna': True, 'period_window': period_window}).get_result()

        elif period_window and period_method=='filter_by_period':
            input_value = Handler(algorithm_name='sma_smoothing', handler_input=input_value, params={'smoothing_window':local_window}).get_result()
            input_value = Handler(algorithm_name='filter_by_period', handler_input=input_value, params={'period_window': period_window, 'timezone': timezone}).get_result()
        else:
            pass

        try:
            input_value = TimeSeries(input_value)
            if period_window and period_method=='filter_by_period':
                local_ts = input_value.splitByWindow(window='1', direct=True, timezone=timezone)
            else:
                local_ts = input_value.splitByWindow(window=local_window, direct=True, timezone=timezone)
            mean_handler = Handler(algorithm_name='mean', handler_input=local_ts)
            compare_value = mean_handler.get_result()
        except (ValueError, AttributeError, Exception) as e:
            raise exceptions.AlgorithmCalculationError("Error when calculate compare value: {}".format(e))

        try:
            bnckmk_ts = input_value.splitByWindow(window=benchmark_size, direct=False, left_in_flag=True, timezone=timezone)
            bnckmk_handler = Handler(algorithm_name=benchmark_method, handler_input=bnckmk_ts)
            bnckmk_value = bnckmk_handler.get_result()
        except (ValueError, AttributeError, Exception) as e:
            raise exceptions.AlgorithmCalculationError("Error when calculate bnckmk value: {}".format(e))

        try:
            if bound_method == 'hard':
                bound_value = sign * factor + bnckmk_value
            elif bound_method == 'ratio':
                bound_value = bnckmk_value * (1 + sign * factor / 100.0)
            else:
                bound_handler = Handler(algorithm_name=bound_method, handler_input=bnckmk_ts)
                bound_value = bound_handler.get_result()
                bound_value = sign * factor * bound_value + bnckmk_value
        except (ValueError, AttributeError, Exception) as e:
            raise exceptions.AlgorithmCalculationError("Error when calculate bound value: {}".format(e))

        try:
            op_input_type = AlgorithmIODataType.BINARY_NUM_INPUT.value()
            op_input = op_input_type.to_native({'left': compare_value, 'right': bound_value})
            op_handler = Handler(algorithm_name=operator, handler_input=op_input)
            return op_handler.get_result()
        except (ValueError, AttributeError, Exception) as e:
            raise exceptions.AlgorithmCalculationError("Error when doing operator value: {}".format(e))


class CushionThreshold(SoftThreshold):
    def _run_algorithm(self, input_value, operator, local_window=None, benchmark_size=None, benchmark_method=None, bound_method=None,
                       factor=None, timezone=None, upper_percentile=None, lower_percentile=None):

        if upper_percentile is None and lower_percentile is None:
            upper_percentile = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_UPPER_PERCENTILE
            lower_percentile = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_LOWER_PERCENTILE
        elif lower_percentile is None:
            lower_percentile = 100 - upper_percentile
        elif upper_percentile is None:
            upper_percentile = 100 - lower_percentile

        if upper_percentile < lower_percentile:
            raise exceptions.ParametersNotPassed("The upper_percentile smaller than lower_percentile")

        if operator in ['>', '>=']:
            sign = 1
        else:
            sign = -1

        if local_window is None:
            local_window = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_LOCAL_WINDOW

        if benchmark_size is None:
            benchmark_size = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_BENCHMARK_SIZE

        if benchmark_method is None:
            benchmark_method = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_BENCHMARK_METHOD

        if bound_method is None:
            bound_method = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_BOUND_METHOD

        if factor is None:
            factor = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_FACTOR

        if timezone is None:
            timezone = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_TIMEZONE

        from ada_core.handler import Handler

        try:
            input_value = TimeSeries(input_value)
            local_ts = input_value.splitByWindow(window=local_window, direct=True, timezone=timezone)
            mean_handler = Handler(algorithm_name='mean', handler_input=local_ts)
            compare_value = mean_handler.get_result()
        except (ValueError, AttributeError, Exception) as e:
            raise exceptions.AlgorithmCalculationError("Error when calculate compare value: {}".format(e))

        try:
            bnckmk_ts = input_value.splitByWindow(window=benchmark_size, direct=False, left_in_flag=True, timezone=timezone)
            bnckmk_handler = Handler(algorithm_name=benchmark_method, handler_input=bnckmk_ts)
            bnckmk_value = bnckmk_handler.get_result()
        except (ValueError, AttributeError, Exception) as e:
            raise exceptions.AlgorithmCalculationError("Error when calculate bnckmk value: {}".format(e))

        try:
            upper_handler = Handler(algorithm_name='percentile', handler_input=bnckmk_ts, params={"percent": upper_percentile})
            upper_value = upper_handler.get_result()
            lower_handler = Handler(algorithm_name='percentile', handler_input=bnckmk_ts, params={"percent": lower_percentile})
            lower_value = lower_handler.get_result()
            if upper_value == lower_value:
                cushion_value = 0.5
            else:
                if sign < 0:
                    cushion_value = (bnckmk_value - lower_value) / (upper_value - lower_value)
                else:
                    cushion_value = (upper_value - bnckmk_value) / (upper_value - lower_value)

        except (ValueError, AttributeError, Exception) as e:
            raise exceptions.AlgorithmCalculationError("Error when calculate upper/lower value and cushion value: {}".format(e))

        try:
            bound_handler = Handler(algorithm_name=bound_method, handler_input=bnckmk_ts)
            base_bound_value = bound_handler.get_result()
        except (ValueError, AttributeError, Exception) as e:
            raise exceptions.AlgorithmCalculationError("Error when calculate base bound valuee: {}".format(e))

        try:
            if sign < 0:
                bound_value = sign * factor * base_bound_value * cushion_value + lower_value
            else:
                bound_value = sign * factor * base_bound_value * cushion_value + upper_value
        except (ValueError, AttributeError, Exception) as e:
            raise exceptions.AlgorithmCalculationError("Error when calculate bound value: {}".format(e))

        try:
            op_input_type = AlgorithmIODataType.BINARY_NUM_INPUT.value()
            op_input = op_input_type.to_native({'left': compare_value, 'right': bound_value})
            op_handler = Handler(algorithm_name=operator, handler_input=op_input)
            return op_handler.get_result()
        except (ValueError, AttributeError, Exception) as e:
            raise exceptions.AlgorithmCalculationError("Error when doing operator value: {}".format(e))