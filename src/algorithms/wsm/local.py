import random
import sys
import time

import src.const as const
import src.method_const as mconst

def add_to_list(pstates, list_element, element):
    """
    If the length of the list is greater than or equal to the constant of the list,
    return the middle of the list, otherwise return the list.

    @param pstates A list of the pstates of the system.
    @param list_element The list to add the element to.
    @param element The element to be added to the list.

    @return The list_element is being returned.
    """
    list_element.append(element)
    return list_element[len(list_element)//2:] if len(list_element) >= len(pstates) * mconst.tabu_max_size_list \
        else list_element

def generate_random_threshold(pstates):
    """
    It generates a random threshold vector for a given number of pstates.

    @param pstates The list of pstates.

    @return A list of random thresholds.
    """
    n = len(pstates)
    th_opt = []
    for i in range(2, n + 1):
        start_value = th_opt[-1] + 1 if len(th_opt) > 0 else 1
        th_opt.append(
            random.randint(start_value, const.B - 1 - (n - i)))  # random -> start and end points included
    return th_opt

def operation_on_threshold(threshold, operation_type, pos, number):
    """
    It takes a threshold, an operation type, a position, and a number,
    and returns a new threshold with the number added or subtracted from the position.

    @param threshold The threshold array.
    @param operation_type "+" or "-".
    @param pos The position of the threshold to be changed.
    @param number The number of operations to perform.

    @return The threshold after the operation is performed.
    """
    m = len(threshold)
    res = threshold
    add = res[pos] + number
    sub = res[pos] - number
    if operation_type == "+" and ((0 < pos < m - 1 and threshold[pos - 1] < add < threshold[pos + 1])
                                  or (pos == m - 1 and add <= const.B - 1) or (pos == 0 and m > 1
                                  and add < threshold[1])):
        res[pos] += number
    elif operation_type == "-" and ((0 < pos < m - 1 and threshold[pos - 1] < sub < threshold[pos + 1])
                                    or (pos == 0 and sub > 0) or (pos == m - 1 and m > 1
                                    and threshold[pos - 1] < sub)):
        res[pos] -= number
    return res


def all_neighbour_of_threshold(Lambda, Alpha, pstates, time_response_min, time_response_max,
                               power_min, power_max, min_threshold, number):
    """
    It takes a threshold, and returns the best threshold that is
    one step away from the original threshold.

    @param Lambda The number of tasks.
    @param Alpha The weight of the power consumption in the objective function.
    @param pstates List of pstates.
    @param time_response_min Minimum time response.
    @param time_response_max The maximum time response of the system.
    @param power_min Minimum power consumption.
    @param power_max Maximum power consumption of the system.
    @param min_threshold The current best threshold.
    @param number The number of thresholds to be optimized.

    @return the best threshold found.
    """
    already_tested = [min_threshold[0]]
    symbol = ["+", "-"]
    has_changed = True
    while has_changed:
        has_changed = False
        temp_min = min_threshold
        for i in range(len(temp_min[0])):
            for j in range(2):
                th_opt = operation_on_threshold(temp_min[0].copy(), symbol[j], i, number)
                if th_opt not in already_tested:
                    already_tested = add_to_list(pstates, already_tested, th_opt)
                    val_opt = mconst.find_obj_func(Lambda, Alpha, pstates, th_opt, time_response_min,
                                                   time_response_max, power_min, power_max)

                    if val_opt < min_threshold[1]:
                        min_threshold = (th_opt, val_opt)
                        has_changed = True
                        mconst.min_vector_local.append((th_opt.copy(), val_opt))

    return min_threshold


def search(Lambda, Alpha, pstates, th_opt=None):
    """
    It generates a random threshold, then it tries to find a better threshold by looking at all the thresholds
    that are one step away from the current threshold. If it finds a better threshold,
     it sets it as the current threshold and looks at all the thresholds that are one step away
    from the current threshold. It repeats this process until it can't find a better threshold.

    @param Lambda The arrival rate of the jobs.
    @param Alpha The weight of the power consumption in the objective function.
    @param pstates List of power states.
    @param th_opt Starting threshold chose by the user.

    @return The threshold, the objective function value and the time taken to find the solution.
    """
    n = len(pstates)
    if n < 2 or n > 6:
        sys.exit("This is not a valid pstates model !")

    start_timer = time.perf_counter()
    time_response_min, time_response_max, power_min, power_max = mconst.solve_time_and_power_dvfs(Lambda, pstates)
    th_opt = generate_random_threshold(pstates) if th_opt is None else th_opt
    val_opt = mconst.find_obj_func(Lambda, Alpha, pstates, th_opt, time_response_min, time_response_max,
                                   power_min, power_max)

    val_opt_min = all_neighbour_of_threshold(Lambda, Alpha, pstates, time_response_min,
                                             time_response_max, power_min, power_max,
                                             (th_opt, val_opt), 1)

    end_timer = time.perf_counter()
    return val_opt_min[0], val_opt_min[1], end_timer - start_timer
