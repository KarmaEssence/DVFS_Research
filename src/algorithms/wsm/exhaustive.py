import sys
import time

import src.const as const
import src.method_const as mconst

def fill_list_with_optimal_threshold(Lambda, Alpha, pstates, time_response_min, time_response_max,
                                     power_min, power_max, min_thresholds, thresholds):
    """
    It takes a list of thresholds, and recursively adds a new threshold to the list, and then calls itself with the new
    list

    @param Lambda the arrival rate of the jobs
    @param Alpha The weight of the response time in the objective function.
    @param pstates list of power states
    @param time_response_min the minimum time response for each pstate
    @param time_response_max the maximum time response of the system
    @param power_min the minimum power consumption of the system
    @param power_max Maximum power consumption of the system
    @param min_thresholds the list of thresholds that minimizes the objective function
    @param thresholds list of thresholds

    @return The thresholds and the objective function value
    """
    m, n = len(thresholds), len(pstates)
    if m < n - 1:
        index = thresholds[-1] + 1 if m > 0 else 1
        for i in range(index, const.B - (n - 2 - m)):
            thresholds.append(i)
            min_thresholds = fill_list_with_optimal_threshold(Lambda, Alpha, pstates, time_response_min,
                                                              time_response_max, power_min, power_max,
                                                              min_thresholds, thresholds)
            thresholds.pop()
    else:
        obj_func = mconst.find_obj_func(Lambda, Alpha, pstates, thresholds, time_response_min, time_response_max,
                                        power_min, power_max)
        if obj_func < min_thresholds[1]:
            min_thresholds = thresholds.copy(), obj_func
            mconst.min_vector_exhaustive.append((min_thresholds[0].copy(), min_thresholds[1]))

    return min_thresholds


def search(Lambda, Alpha, pstates):
    """
    It takes in the arrival rate, the service rate, and the number of pstates, and returns the optimal thresholds, the
    optimal response time, and the time it took to run the function

    @param Lambda the arrival rate of the jobs
    @param Alpha The weight of the response time in the objective function.
    @param pstates list of pstates

    @return The thresholds, the total power, and the time it took to run the algorithm.
    """
    n = len(pstates)
    if n < 2 or n > 6:
        sys.exit("This is not a valid pstates model !")

    start_timer = time.perf_counter()
    time_response_min, time_response_max, power_min, power_max = mconst.solve_time_and_power_dvfs(Lambda, pstates)
    min_thresholds = ([], 1e5)
    min_thresholds = fill_list_with_optimal_threshold(Lambda, Alpha, pstates, time_response_min, time_response_max,
                                                      power_min, power_max, min_thresholds, [])
    return min_thresholds[0], min_thresholds[1], time.perf_counter() - start_timer
