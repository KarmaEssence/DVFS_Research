import decimal
import sys
import time

import src.const as const
import src.method_const as mconst


def get_pstate(x, pstates, thresholds):
    """
    It returns the index of the P-state that should be used for a given load

    @param x the current temperature
    @param pstates the list of P-states available on the CPU
    @param thresholds the thresholds for each P-state

    @return The P-state that corresponds to the given x value.
    """
    npstates = len(pstates)

    if npstates == 1:
        return pstates[0] - 1  # Model Mono-get_pstate ;)

    elif npstates == 2:
        if x <= thresholds[0]:  # level 1
            return pstates[0] - 1
        else:  # level 2
            return pstates[1] - 1

    elif npstates == 3:
        if x <= thresholds[0]:  # level 1
            return pstates[0] - 1
        elif thresholds[0] < x <= thresholds[1]:  # level 2
            return pstates[1] - 1
        else:  # level 3
            return pstates[2] - 1

    elif npstates == 4:
        if x <= thresholds[0]:  # level 1
            return pstates[0] - 1
        elif thresholds[0] < x <= thresholds[1]:  # level 2
            return pstates[1] - 1
        elif thresholds[1] < x <= thresholds[2]:  # level 3
            return pstates[2] - 1
        else:  # level 4
            return pstates[3] - 1

    elif npstates == 5:
        if x <= thresholds[0]:  # level 1
            return pstates[0] - 1
        elif thresholds[0] < x <= thresholds[1]:  # level 2
            return pstates[1] - 1
        elif thresholds[1] < x <= thresholds[2]:  # level 3
            return pstates[2] - 1
        elif thresholds[2] < x <= thresholds[3]:  # level 4
            return pstates[3] - 1
        else:  # level 5
            return pstates[4] - 1

    elif npstates == 6:
        if x <= thresholds[0]:  # level 1
            return pstates[0] - 1
        elif thresholds[0] < x <= thresholds[1]:  # level 2
            return pstates[1] - 1
        elif thresholds[1] < x <= thresholds[2]:  # level 3
            return pstates[2] - 1
        elif thresholds[2] < x <= thresholds[3]:  # level 4
            return pstates[3] - 1
        elif thresholds[3] < x <= thresholds[4]:  # level 5
            return pstates[4] - 1
        else:  # level 6
            return pstates[5] - 1


def get_number_of_servers_in_service(i, pstates, thresholds):
    """
    The function `get_number_of_servers_in_service` returns the mean time to failure of a server with `i`
    users, given the current `pstates` and `thresholds`

    @param i the number of servers in the system
    @param pstates a list of the pstates that the CPU can be in.
    @param thresholds the thresholds for the different pstates

    @return The number of servers in service.
    """
    In_service = min(i, const.C)
    return decimal.Decimal(In_service * const.Mu[get_pstate(i, pstates, thresholds)])


def compute_pi_distance(Lambda, pstates, thresholds):
    """
    It calculates the stationary distribution of the birth-death process

    @param Lambda the arrival rate
    @param pstates the states of the process
    @param thresholds the thresholds for the different states.
    """
    mconst.pi[0] = decimal.Decimal(1.0)

    # ------- Computing of the stability bound of the birth-death process -------------------------- */

    R = max(const.C, thresholds[-1]) if len(pstates) > 1 else const.C

    # ----------- Computing of x probability in [1, R] -------------*/

    mconst.pi[1] = decimal.Decimal(Lambda) / decimal.Decimal(const.Mu[pstates[0] - 1])
    for i in range(2, R + 1):
        try:
            mconst.pi[i] = (mconst.pi[i - 1] * decimal.Decimal(Lambda)) / (
                decimal.Decimal(get_number_of_servers_in_service
                                (i, pstates, thresholds)))
        except OverflowError as e:  # lower value
            print("OverflowError: {}".format(e))
            mconst.pi[i] = decimal.Decimal(0)

    # ----------- Computing of x probability in [R+1, B] -------------*/
    if R < const.B:
        pw = decimal.Decimal(Lambda) / decimal.Decimal(const.C * const.Mu[pstates[-1] - 1])
        mconst.pi[R + 1] = mconst.pi[R] * pw
        for i in range(R + 2, const.B + 1):
            try:
                mconst.pi[i] = mconst.pi[i - 1] * decimal.Decimal(pw)
            except OverflowError as e:  # lower value
                print("OverflowError: {}".format(e))
                mconst.pi[i] = decimal.Decimal(0)

    # ----------- Computing of the first sum: x in [1,R] -------------*/

    s = decimal.Decimal(sum(mconst.pi) - mconst.pi[0])

    # ------------ Normalization of probabilities ----------------------------- */

    pi0 = decimal.Decimal(decimal.Decimal(1.0) / decimal.Decimal(1 + s))
    for i in range(0, const.B + 1):
        mconst.pi[i] *= pi0

    # ------------ Displaying for verification -------------------------- */

    teste = decimal.Decimal(0)
    for i in range(const.B, -1, -1):
        teste += mconst.pi[i]
    if abs(1 - teste) > 1e-10:
        print("Error : lambda = {}, sum of probabilities is far from 1 : {:.20}".format(Lambda, teste))
        sys.exit(0)


def compute_rewards(Lambda, pstates, thresholds):
    """
    It calculates the average number of clients, the average response time, the average power consumption,
    the average power consumption with the power consumption of the P-state switches, and the rejection probability

    @param Lambda the arrival rate of the clients
    @param pstates the list of Pstates that the server can be in.
    @param thresholds the thresholds for the P-states

    @return N, T, consMoy, consMoy + consSw, Reject
    """
    consMoy = decimal.Decimal(0)  # Average power consumption without the power consumption of the P-state switches
    N = decimal.Decimal(0)  # Number of tasks

    for i in range(0, const.B + 1):
        In_service = min(i, const.C)
        Out_service = const.C - In_service
        p = get_pstate(i, pstates, thresholds)
        consMoy += mconst.pi[i] * (decimal.Decimal(In_service * const.en[p] + Out_service * const.en_idle[p]))
        N += decimal.Decimal(i * mconst.pi[i])

    PALL_list = []
    for c in range(10, 110, 10):
        consSw = decimal.Decimal(0)  # Power consumption of the P-state switches (start with 0
        for i in range(0, len(thresholds)):  # Activation cost of the P-states
            e = decimal.Decimal(const.Es[pstates[i + 1] - 1] * c / 100)
            consSw += decimal.Decimal(e * const.C * mconst.pi[thresholds[i]])
        PALL_list.append(consMoy + consSw)

    T = decimal.Decimal(N / (Lambda * (1 - mconst.pi[const.B])))  # time response
    Reject = mconst.pi[const.B]  # Reject probability

    return N, T, consMoy, PALL_list, Reject


def compute_average_power(pstates, thresholds):
    """
    It calculates the average power consumption of the system, given the current state of the system and the power
    states of the system

    @param pstates a list of the power states of the processor
    @param thresholds the thresholds for the power states

    @return The average power consumption of the system.
    """

    consMoy = decimal.Decimal(0)
    for i in range(0, const.B + 1):
        In_service = min(i, const.C)
        Out_service = const.C - In_service
        p = get_pstate(i, pstates, thresholds)
        consMoy += mconst.pi[i] * (decimal.Decimal(In_service * const.en[p] + Out_service * const.en_idle[p]))
    return consMoy


def compute_ignition_power(pstates, thresholds):
    """
    It calculates the average power consumption of the processor when it is in a given P-state

    @param pstates a list of the pstates that the processor is allowed to use.
    @param thresholds the thresholds for each P-state

    @return The power consumption of the processor when it is in the get_pstate 0.
    """

    consMoy = decimal.Decimal(0)  # Initialisation of processor power consumption for get_pstate 0
    for i in range(0, len(thresholds)):  # Activation cost of each P-states
        consMoy += decimal.Decimal(const.Es[pstates[i + 1] - 1] * const.C * mconst.pi[thresholds[i]])
    return consMoy


def get_average_number_of_tasks():
    """
    The function average_number_of_tasks() calculates the average number of tasks in the system

    @return The average number of tasks in the system.
    """
    s = decimal.Decimal(0)
    for i in range(0, const.B + 1):
        s += decimal.Decimal(i * mconst.pi[i])
    return s


def get_time_response(Lambda, N):
    """
    The response time of the system is the average number of tasks in the system divided by the arrival rate

    @param Lambda the arrival rate of tasks
    @param N number of tasks

    @return The average time it takes for a task to be completed.
    """
    return decimal.Decimal(N / (Lambda * (1 - mconst.pi[const.B])))


def get_power_consumption(Lambda, power):
    """
    It takes two arguments, Lambda and power, and returns the value of power divided by Lambda

    @param Lambda The average number of jobs that arrive per minute.
    @param power the power of the machine

    @return The energy of the job.
    """
    return decimal.Decimal(power / Lambda)


def get_reject_proba():
    """
    The probability of rejecting a task is the probability of being in state B

    @return The probability of rejecting a task.
    """
    return mconst.pi[const.B]


def get_pstates_probability(pstates, thresholds):
    """
    It computes the probability of each state, given the state space and the thresholds

    @param pstates the number of states in the Markov chain
    @param thresholds the thresholds for each level
    """
    S = [decimal.Decimal(0)] * len(pstates)
    for i in range(0, const.B + 1):
        S[get_pstate(i, pstates, thresholds)] += mconst.pi[i]
    print("Probability per level : ", S)


def compute_norms(value, min_value, max_value):
    """
    The function takes in a value, a minimum value, and a maximum value, and returns the normalized value
    between 0 and 1

    @param value the value to be normalized
    @param min_value minimum value of the data
    @param max_value The maximum value of the data.

    @return The normalized value of the input value.
    """
    return (value - min_value) / (max_value - min_value)


def get_pstates_bound(Lambda, pstates, index):
    """
    It solves the system of equations for a given set of pstates, and returns the corresponding throughput and power
    consumption

    @param Lambda the rate matrix
    @param pstates a list of pstates
    @param index the index of the pstate you want to calculate the bound for

    @return The return value is the total time and the total power consumption.
    """
    N, T, P, PALL_list, R = solve(Lambda, [pstates[index]], [])  # Mono-get_pstate
    return T, P if const.Type == 0 else PALL_list[-1]


def solve(Lambda, pstates, thresholds):
    """
    It computes the optimal policy for a given set of parameters

    @param Lambda the arrival rate of the Poisson process
    @param pstates the probability of each state
    @param thresholds the thresholds for each state

    @return N, T, P, PAll, R
    """
    compute_pi_distance(Lambda, pstates, thresholds)
    N, T, P, PALL_list, R = compute_rewards(Lambda, pstates, thresholds)
    return N, T, P, PALL_list, R


def solve_time_and_power(Lambda, pstates):
    """
    It computes the time response and power consumption of a server with a given set of P-states, for a given workload

    @param Lambda the arrival rate of the requests
    @param pstates list of P-states available to the server

    @return The time response and power consumption for the lower and upper bounds.
    """
    pmin = const.C * const.en_idle[pstates[0] - 1]  # All server in the "idle" state in "Pstate1"
    pmax = const.C * const.en[pstates[-1] - 1]  # All server in the "active" state in "PstateN"

    for p in pstates:  # +adding power of switching pour "pmax"
        pmax += const.C * const.Es[p - 1]
    pmax -= const.C * const.Es[pstates[0] - 1]

    time_response_max, power_min = get_pstates_bound(Lambda, pstates, 0)  # Mono-get_pstate low
    time_response_min, power_max = get_pstates_bound(Lambda, pstates, len(pstates) - 1)  # Mono-get_pstate high

    power_min = decimal.Decimal(pmin)
    power_max = decimal.Decimal(pmax)
    return time_response_min, time_response_max, power_min, power_max


def find_obj_func(Lambda, Alpha, pstates, thresholds, time_response_min, time_response_max, power_min, power_max):
    """
    It takes in the parameters of the problem, solves the problem, and returns the objective function value

    @param Lambda the arrival rate of the customers
    @param Alpha The weight of the time response in the objective function.
    @param pstates the states of the system
    @param thresholds the thresholds for each state
    @param time_response_min minimum time response
    @param time_response_max the maximum time response of the system
    @param power_min minimum power consumption
    @param power_max maximum power consumption of the system

    @return The objective function value.
    """
    N, T, P, PALL_list, R = solve(Lambda, pstates, thresholds)

    Tnorm = compute_norms(T, time_response_min, time_response_max)  # Normalization : dans [0,1]
    Pnorm = compute_norms(P, power_min, power_max) if const.Type == 0 \
        else compute_norms(PALL_list[-1], power_min, power_max)  # Normalization : dans [0,1]
    val_obj = decimal.Decimal(Alpha) * Tnorm + decimal.Decimal(1 - Alpha) * Pnorm  # Weighted Objective Function

    mconst.operations_materials[val_obj] = (Lambda, Alpha, pstates, thresholds, N, T, P, PALL_list[-1],
                                            PALL_list, Tnorm, Pnorm, R, decimal.Decimal(Alpha) * Tnorm,
                                            decimal.Decimal(1 - Alpha) * Pnorm)
    return val_obj


def get_size_of_exhaustive_method(pstates):  # Decision space N pstates = B!/((N-1)!x(B-N+1)!)
    """
    The number of possible combinations of N pstates is equal to the number of ways to choose N-1 pstates from B pstates

    @param pstates a list of pstates

    @return The number of possible combinations of pstates.
    """
    i, s, n = 0, 1, len(pstates)
    if n < 2:
        print("To have a threshold, system should be >= 2 pstates")
        return 0
    for _ in range(len(pstates) - 1):
        print("i = {}, i + 1 = {}".format(i, i + 1))
        s *= (const.B - i) / (i + 1)
        i += 1
    '''
    #2 pstates : B/1
    #3 pstates : B(B-1)/2
    #4 pstates : B(B-1)(B-2)/6
    #5 pstates : B(B-1)(B-2)(B-3)/24
    #N pstates : a = (B-N+1) => k = (N-1)
    #  ...
    # Formula1 : ((N-1)! x (B! / (N-1)!x(B-N+1)!))/(N-1)!
    # Formula2 : B!/((N-1)!x(B-N+1)!)

    s1 = math.factorial(const.B)/ (math.factorial(n-1)*math.factorial(const.B-n+1))
    print("S facto = ",int(s1)) #B!/((N-1)!x(B-N+1)!)
    '''
    return int(s)


def get_size_of_pareto_method(pstates):  # Decision space for N pstates = (B-1)!/((N-1)!x(B-N+1)!)
    """
    The number of possible combinations of N pstates is equal to the number of ways to choose N-1 elements
    from a set of B-1 elements

    @param pstates a list of the pstates in the system.

    @return The number of possible combinations of pstates.
    """
    s, n = 1, len(pstates)
    if n < 2:
        print("To have a threshold, system should be >= 2 pstates")
        return 0
    for i in range(n - 1):
        s *= (const.B - i - 1) / (i + 1)
    '''
    #2 pstates : (B-1)/1
    #3 pstates : (B-1)(B-2)/2
    #4 pstates : (B-1)(B-2)(B-3)/6
    #5 pstates : (B-1)(B-2)(B-3)(B-4)/24
    #N pstates : (B-1)(B-2)(B-3)(B-4) ... (B-(N-1))/(N-1)!
    #N pstates : a = (B-N+1) et k = (N-2) thus a+k = (B-1)
    #  ...
    # Formula1 : ((N-2)! x ( (B-1)! / (N-2)!x(B-N+1)!))/(N-1)!
    # Formula2 : (B-1)!/((N-1)!x(B-N+1)!)

    s1 = math.factorial(const.B-1)/ (math.factorial(n-1)*math.factorial(const.B-n+1))
    print("S facto = ",int(s1)) #(B-1)!/((N-1)!x(B-N+1)!)
    '''
    return int(s)


def compute_decision_space(Lambda, pstates, value_list, thresholds):
    """
    It computes the space domain for a given set of thresholds

    @param Lambda the arrival rate of the Poisson process
    @param pstates the list of states that are possible to be in
    @param value_list a list of tuples, each tuple contains the following.
    @param thresholds a list of thresholds, e.g. [1, 2, 3]

    @return The thresholds, N, T, P, PALL_list, R
    """
    m, n = len(thresholds), len(pstates)
    if m < n - 1:
        index = thresholds[-1] + 1 if m > 0 else 1
        for i in range(index, const.B - (n - 2 - m)):
            thresholds.append(i)
            value_list = compute_decision_space(Lambda, pstates, value_list, thresholds)
            thresholds.pop()
    else:
        N, T, P, PALL_list, R = solve(Lambda, pstates, thresholds)
        value_list.append((thresholds.copy(), N, T, P, PALL_list[-1], PALL_list, R))

    return value_list


def init_decision_space(Lambda, pstates):
    """
    It computes the space domain of the model

    @param Lambda the number of states in the model
    @param pstates a list of the possible states of the system.
    """
    n = len(pstates)
    if n < 2 or n > 6:
        sys.exit("This is not a valid pstates model !")

    start = time.perf_counter()
    mconst.decision_space[(Lambda, str(pstates))] = (compute_decision_space(Lambda, pstates, [], []),
                                                     time.perf_counter() - start)
