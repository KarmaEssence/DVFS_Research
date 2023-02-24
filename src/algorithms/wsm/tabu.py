import random
import sys
import time

import src.method_const as mconst

def compare_list(list_, global_list):
    """
    It compares a list to a list of lists, and returns True if the list is in the list of lists.

    @param list_ The list to be compared.
    @param global_list Main list.

    @return A boolean value.
    """
    if len(global_list) == 0:
        return False
    for i in range(len(global_list)):
        if len(list_) != len(global_list[i][0]):
            continue
        complete = 1
        for j in range(len(global_list[i][0])):
            if list_[j] != global_list[i][0][j]:
                complete = 0
        if complete == 1:
            return True
    return False


def all_neighbour_of_threshold(Lambda, Alpha, pstates, time_response_min, time_response_max,
                               power_min, power_max, min_threshold, number):
    """
    It takes a threshold, and returns a list of all the thresholds that are one step away from it.

    @param Lambda The number of states in the system.
    @param Alpha The weight of the response time in the objective function.
    @param pstates List of all possible states.
    @param time_response_min Minimum time response.
    @param time_response_max The maximum time response of the system.
    @param power_min minimum Power consumption.
    @param power_max Maximum Power consumption of the system.
    @param min_threshold The current best solution.
    @param number The number of thresholds to be changed.

    @return The minimum threshold and the list of all the thresholds that were tested.
    """
    min_threshold_list = [(min_threshold[0], min_threshold[1])]
    count_before_change = 0
    symbol = ["+", "-"]
    mconst.min_vector_tabu.append((min_threshold[0].copy(), min_threshold[1]))
    while count_before_change < mconst.tabu_max_iteration_without_change:
        current_tuple = (min_threshold_list[-1][0], min_threshold_list[-1][1])
        min_tuple = current_tuple
        min_local_tuples = []

        # To obtains all neighbour of the current threshold
        for i in range(len(current_tuple[0])):
            for j in range(2):
                th_opt = mconst.operation_on_threshold(current_tuple[0].copy(), symbol[j], i, number)
                if not compare_list(th_opt, min_threshold_list):
                    val_opt = mconst.find_obj_func(Lambda, Alpha, pstates, th_opt, time_response_min,
                                                   time_response_max, power_min, power_max)

                    min_local_tuples.append((th_opt, val_opt))
                    if val_opt < min_tuple[1]:
                        min_tuple = (th_opt, val_opt)
                        count_before_change = -1

        if min_tuple != current_tuple:
            if min_tuple[1] < min_threshold[1]:
                min_threshold = min_tuple
                count_before_change = -1
                mconst.min_vector_tabu.append((min_threshold[0].copy(), min_threshold[1]))

            min_threshold_list = mconst.add_to_list(pstates, min_threshold_list, min_tuple)

        elif len(min_local_tuples) > 0:
            min_threshold_list = mconst.add_to_list(pstates, min_threshold_list,
                                                    min_local_tuples[random.randint(0, len(min_local_tuples) - 1)])

        count_before_change += 1
    return min_threshold, min_threshold_list


def search(Lambda, Alpha, pstates, th_opt=None):
    """
    It finds the best threshold for the given parameters.

    @param Lambda The number of tasks in the system.
    @param Alpha The weight of the response time in the objective function.
    @param pstates List of tuples of the form (power, frequency).
    @param th_opt Starting threshold chose by the user.

    @return The threshold, the value of the objective function and the time taken to find the threshold.
    """
    n = len(pstates)
    if n < 2 or n > 6:
        sys.exit("This is not a valid pstates model !")

    start_timer = time.perf_counter()
    time_response_min, time_response_max, power_min, power_max = mconst.solve_time_and_power_dvfs(Lambda, pstates)
    th_opt = mconst.generate_random_threshold(pstates) if th_opt is None else th_opt
    val_opt = mconst.find_obj_func(Lambda, Alpha, pstates, th_opt, time_response_min, time_response_max,
                                   power_min, power_max)

    val_opt_min, min_threshold_list = all_neighbour_of_threshold(Lambda, Alpha, pstates, time_response_min,
                                                                 time_response_max, power_min, power_max,
                                                                 (th_opt, val_opt), 1)

    end_timer = time.perf_counter()
    return val_opt_min[0], val_opt_min[1], end_timer - start_timer
