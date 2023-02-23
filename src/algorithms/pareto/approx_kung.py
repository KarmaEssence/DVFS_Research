import sys
import time

import src.const as const
import src.method_const as mconst


def search_approx_kung(Lambda, pstates):  # Methode2 : "Approx + Fast" Pareto Optimal, for any Pstates
    """
    The function `search_approx_kungs` takes as input a list of `pstates` and a `Lambda` and returns the
    Pareto optimal solutions for the given `pstates` and `Lambda`

    @param Lambda the arrival rate of the jobs
    @param pstates a list of pstates, e.g. [1,2,3,4,5,6]
    @return the Pareto optimal solutions and the time taken to compute them.
    """

    n = len(pstates)
    if n < 2 or n > 6:
        sys.exit("This is not a valid pstates model !")

    start = time.perf_counter()
    final_result = None
    for i in range(1, len(pstates)):
        Npstates = pstates[0:i + 1]
        bound = const.B - n + i
        if i == 1:
            final_result = mconst.kung_search(Lambda, Npstates)
        else:
            new_sols = []
            for sol in final_result[2]:
                for th in range(sol[0][-1] + 1, bound + 1):
                    new_th = list(sol[0])
                    new_th.append(th)
                    N, T, P, PALL_list, R = mconst.solve_dvfs(Lambda, Npstates, new_th)
                    new_sols.append((new_th.copy(), N, T, P, PALL_list[-1], PALL_list, R))

            new_sols = sorted(new_sols, key=lambda member: member[2])  # Sorting in function of time response
            final_result = (Lambda, pstates, mconst.pareto_front(new_sols), time.perf_counter() - start)

    return final_result
