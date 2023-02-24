import src.method_const as mconst

def displaying_results(method_name, thresholds, value, time, Delta=None, th_opt=None):
    """
    It prints the results of the optimization.

    @param method_name The name of the method used to solve the problem.
    @param thresholds The thresholds used to generate the sample.
    @param value The value of the objective function.
    @param time The time it took to run the algorithm.
    @param Delta The difference between the optimal value and the value of the solution found by the algorithm.
    @param th_opt The starting thresholds for the optimization.
    """
    print("Method name: {}".format(method_name))
    print("Thresholds: {}".format(thresholds))
    print("Value: {:.10f}".format(value))
    print("Time: {:.10f}".format(time))
    if Delta is not None:
        print("Delta: {}".format(Delta))
    if th_opt is not None:
        print("Starting thresholds: {}".format(th_opt))

def exhaustive(Lambda, Alpha, pstates):
    """
    It takes in the parameters of the problem, and returns the optimal thresholds, the optimal value,
    and the time it took to compute the optimal thresholds.

    @param Lambda The rate of arrival task.
    @param Alpha The weight of the response time objectif.
    @param pstates A list of the power state.

    @return The name of the method, the thresholds, the value, and the time.
    """
    mconst.create_folder_if_he_doesnt_exist(mconst.single_exhaustive)
    method_name = "exhaustive"
    thresholds, value, time = mconst.exhaustive_search(Lambda, Alpha, pstates)
    filename = mconst.example_number_has_not_been_attributed(mconst.single_exhaustive, method_name + "_", ".csv")
    mconst.save_method_as_csv(method_name, filename, mconst.min_vector_exhaustive, time, delta=None)
    displaying_results(method_name, thresholds, value, time)
    return method_name, thresholds, value, time

def greedy(Lambda, Alpha, pstates, Delta):
    """
    It takes in the parameters of the problem and returns the thresholds, value, time, and Delta.

    @param Lambda The rate of arrival task.
    @param Alpha The weight of the response time objective.
    @param pstates A list of the power state.
    @param Delta The size of the neighborhood.

    @return The name of the method, the thresholds, the value, the time, and the Delta.
    """
    mconst.create_folder_if_he_doesnt_exist(mconst.single_greedy)
    method_name = "greedy"
    thresholds, value, time = mconst.greedy_search(Lambda, Alpha, pstates, Delta)
    filename = mconst.example_number_has_not_been_attributed(mconst.single_greedy, method_name + "_", ".csv")
    mconst.save_method_as_csv(method_name, filename, mconst.min_vector_greedy, time, delta=Delta)
    displaying_results(method_name, thresholds, value, time, Delta)
    return method_name, thresholds, value, time, Delta

def local(Lambda, Alpha, pstates, th_opt=None):
    """
    It takes in the parameters of the problem, and returns the optimal thresholds and the value of the objective
    function

    @param Lambda The rate of arrival task.
    @param Alpha The weight of the response time objective.
    @param pstates A list of the power state.
    @param th_opt The optimal threshold for the given parameters. If not given, it will be calculated.

    @return The name of the method, the thresholds, the value, the time, and the optimal threshold.
    """
    mconst.create_folder_if_he_doesnt_exist(mconst.single_local)
    method_name = "local"
    thresholds, value, time = mconst.loca_search(Lambda, Alpha, pstates, th_opt)
    filename = mconst.example_number_has_not_been_attributed(mconst.single_local, method_name + "_", ".csv")
    mconst.save_method_as_csv(method_name, filename, mconst.min_vector_local, time, delta=None)
    displaying_results(method_name, thresholds, value, time, th_opt=th_opt)
    return method_name, thresholds, value, time, th_opt

def tabu(Lambda, Alpha, pstates, th_opt=None):
    """
    It takes in the parameters of the problem, and returns the results of the tabu search algorithm

    @param Lambda The rate of arrival task.
    @param Alpha The weight of the response time objective.
    @param pstates A list of the power state.
    @param th_opt The optimal threshold value. If not provided, it will be calculated.

    @return The name of the method, the thresholds, the value, the time, and the optimal threshold.
    """
    mconst.create_folder_if_he_doesnt_exist(mconst.single_tabu)
    method_name = "tabu"
    thresholds, value, time = mconst.tabu_search(Lambda, Alpha, pstates, th_opt)
    filename = mconst.example_number_has_not_been_attributed(mconst.single_tabu, method_name + "_", ".csv")
    mconst.save_method_as_csv(method_name, filename, mconst.min_vector_tabu, time, delta=None)
    displaying_results(method_name, thresholds, value, time, th_opt=th_opt)
    return method_name, thresholds, value, time, th_opt

def kung(Lambda, pstates):
    """
    It takes a list of states and a list of objectives, and returns a list of states that are pareto optimal.

    @param Lambda The rate of arrival task.
    @param pstates A list of the power state.
    """
    mconst.create_folder_if_he_doesnt_exist(mconst.singe_kung)
    method_name = "kung"
    results = mconst.kung_search(Lambda, pstates)
    filename = mconst.example_number_has_not_been_attributed(mconst.singe_kung, method_name + "_", ".csv")
    mconst.save_pareto_method_as_csv(method_name, filename, results)

def approx_kung(Lambda, pstates):
    """
    It takes a Lambda and a list of pstates, and then it saves the results of the approx_kung method to a csv file.

    @param Lambda The rate of arrival task.
    @param pstates A list of the power state.
    """
    mconst.create_folder_if_he_doesnt_exist(mconst.single_approx_kung)
    method_name = "approx_kung"
    results = mconst.approx_kung_search(Lambda, pstates)
    filename = mconst.example_number_has_not_been_attributed(mconst.single_approx_kung, method_name + "_", ".csv")
    mconst.save_pareto_method_as_csv(method_name, filename, results)


def launch():
    """
    It runs the algorithm of your choice on the given parameters.
    """
    mconst.create_folder_if_he_doesnt_exist(mconst.single)
    Lambda, Alpha, pstates = 20, 0, [1, 2, 3]
    Delta, th_opt = 0, mconst.generate_random_threshold(pstates)

    # Exhaustive search
    exhaustive(Lambda, Alpha, pstates)

    # Greedy search
    greedy(Lambda, Alpha, pstates, Delta)

    # Local search
    local(Lambda, Alpha, pstates, th_opt)

    # Tabu search
    tabu(Lambda, Alpha, pstates, th_opt)

    # Kung's algorithm
    kung(Lambda, pstates)

    # Approximate Kung's algorithm
    approx_kung(Lambda, pstates)
