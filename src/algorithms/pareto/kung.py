import sys
import time

import src.const as const
import src.method_const as mconst


def dominate(Ti, Pi, Tj, Pj):
    """
    Return true if i dominates j

    @param Ti time of the ith solution
    @param Pi the power consumption of the ith solution
    @param Tj time of the jth solution
    @param Pj the power consumption of the jth solution

    @return True if Ti < Tj and Pi < Pj or Ti == Tj and Pi < Pj or Pi == Pj and Ti < Tj
    """
    return True if (Ti < Tj and Pi < Pj) or (Ti == Tj and Pi < Pj) or (Pi == Pj and Ti < Tj) else False


def is_dominated_by_any(member, t):
    """
    "If any space_member of the set t dominates the space_member, return True, otherwise return False."

    The function is_dominated_by_any is used to determine if a space_member of the population is dominated by any other
    space_member of the population. If it is, then it is not a space_member of the Pareto front

    @param member a tuple of (fitness, x, y)
    @param t the current population

    @return A list of tuples. Each tuple contains the index of the space_member, the x value, and the y value.
    """
    for member2 in t:
        if dominate(member2[1], member2[2], member[1], member[2]):
            return True
    return False


def front(Space):
    """
    It takes a list of points, sorts them by their third coordinate, then recursively splits the list in half
    and checks if the points in the second half are dominated by any of the points in the first half.
    If they are not, they are added to the final list

    @param Space the list of all the points in the space

    @return the Pareto front of the given space.
    """
    if len(Space) == 1:
        return Space
    else:
        # Sorting in function of power consumption
        Space = sorted(Space, key=lambda space_member: space_member[3] if const.Type == 0 else space_member[4])
        t = front(Space[0: int(len(Space) / 2)])
        b = front(Space[int(len(Space) / 2): len(Space)])
        m = []  # Matrix containing final results
        for member in b:
            if not is_dominated_by_any(member, t):
                m.append(member)
    return m + t


def search(Lambda, pstates):  # Method 1 : "Fast" Pareto Optimal for any Pstates
    """
    It takes a list of tuples, each tuple representing a space_member of the decision set,
    and returns a list of tuples, each tuple representing a space_member of the Pareto optimal set

    @param Lambda the number of tasks in the system
    @param pstates the number of pstates to consider

    @return The set of Pareto optimal solutions.
    """
    n = len(pstates)
    if n < 2 or n > 6:
        sys.exit("This is not a valid pstates model !")

    start = time.perf_counter()
    keys = mconst.decision_space.keys()
    if len(keys) == 0 or (Lambda, str(pstates)) not in keys:
        mconst.init_decision_space(Lambda, pstates)

    decision_space = mconst.decision_space[(Lambda, str(pstates))][0]
    decision_space = sorted(decision_space, key=lambda member: member[2])  # Sorting in function of time response
    final_result = (Lambda, pstates, front(decision_space), time.perf_counter() - start)
    return final_result

def compare_pareto_methods(Approx, Opt):
    """
    It compares two lists of solutions and returns the number of solutions that are common to both lists
    and the percentage of common solutions

    @param Approx The list of solutions found by the heuristic
    @param Opt the optimal solution

    @return The number of similar points and the percentage of similarity.
    """
    nOpt, nApprox = len(Opt), len(Approx)
    if nOpt <= nApprox:
        list1, list2 = Opt, Approx
        n1, n2 = nOpt, nApprox
    else:
        list1, list2 = Approx, Opt
        n1, n2 = nApprox, nOpt

    c = [0] * n1
    for i in range(0, n1):
        for j in range(0, n2):
            if len(list1[i][0]) == len(list2[j][0]) and len(list1[i][0]) == \
                    sum([1 for x, y in zip(list1[i][0], list2[j][0]) if x == y]):
                c[i] = 1

    similarity_points = sum(c)
    similarity_percent = (similarity_points / (n1 + n2 - similarity_points)) * 100
    return similarity_points, similarity_percent
