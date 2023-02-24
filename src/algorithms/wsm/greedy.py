import sys
import time

import src.const as const
import src.method_const as mconst


def define_neighbor(th_opt, Delta):
    """
    It returns the range of possible values for the next threshold.

    @param th_opt The current optimal threshold.
    @param Delta The maximum distance between two consecutive thresholds.

    @return The start and end of the neighbor set.
    """
    neighbor_start = th_opt[-1] - Delta
    neighbor_end = th_opt[-1] + Delta + 1

    if len(th_opt) > 1 and th_opt[-2] >= th_opt[-1] - Delta:
        neighbor_start = th_opt[-2] + 1

    if neighbor_start < 1:
        neighbor_start = 1

    if neighbor_end >= const.B:
        neighbor_end = const.B

    return neighbor_start, neighbor_end


def exhaustive_search_2pstates(Lambda, Alpha, pstates, time_response_min, time_response_max, power_min, power_max):
    """
    It finds the optimal threshold for the first two p-states.

    @param Lambda The arrival rate of the jobs.
    @param Alpha The weight of the response time in the objective function.
    @param pstates List of pstates.
    @param time_response_min Minimum time response.
    @param time_response_max The maximum time response of the system.
    @param power_min Minimum Power consumption of the system.
    @param power_max Maximum Power consumption of the system.

    @return The optimal threshold and the optimal value of the objective function.
    """
    th_opt, val_opt = [], 1e5
    maxBorder = const.B - (len(pstates) - 2)
    for th1 in range(1, maxBorder):
        threshold = [th1]
        obj_func = mconst.find_obj_func(Lambda, Alpha, pstates[:2], threshold, time_response_min, time_response_max,
                                        power_min, power_max)
        if obj_func < val_opt:
            val_opt = obj_func
            th_opt = threshold

    return val_opt, th_opt


def search(Lambda, Alpha, pstates, Delta):
    """
    It's a greedy algorithm that tries to find the best threshold for each iteration.

    @param Lambda The arrival rate of the jobs.
    @param Alpha The weight of the response time in the objective function.
    @param pstates List of power states.
    @param Delta The number of neighbors to consider.

    @return The optimal threshold vector, the optimal objective function value,
    and the time taken to run the algorithm.
    """
    n = len(pstates)
    if n < 2 or n > 6:
        sys.exit("This is not a valid pstates model !")

    start_timer = time.perf_counter()
    time_response_min, time_response_max, power_min, power_max = mconst.solve_time_and_power_dvfs(Lambda, pstates)
    val_opt, th_opt = exhaustive_search_2pstates(Lambda, Alpha, pstates, time_response_min, time_response_max,
                                                 power_min, power_max)
    mconst.min_vector_greedy.append((th_opt.copy(), val_opt))

    for i in range(3, n + 1):
        val_opt = 1e5
        neighbor_start, neighbor_end = define_neighbor(th_opt, Delta)
        th_opt_temp = th_opt.copy()
        for neighbor in range(neighbor_start, neighbor_end):
            if neighbor != neighbor_start:
                th_opt_temp.pop()

            th_opt_temp.pop(), th_opt_temp.append(neighbor), th_opt_temp.append(-1)
            max_border = const.B - (n - i)
            for thi in range(neighbor + 1, max_border):
                th_opt_temp.pop(), th_opt_temp.append(thi)
                objFunc = mconst.find_obj_func(Lambda, Alpha, pstates[0:i], th_opt_temp, time_response_min,
                                               time_response_max, power_min, power_max)

                if objFunc < val_opt:
                    val_opt = objFunc
                    th_opt = th_opt_temp.copy()
                    mconst.min_vector_greedy.append((th_opt.copy(), val_opt))

    end_timer = time.perf_counter()
    return th_opt, val_opt, end_timer - start_timer
