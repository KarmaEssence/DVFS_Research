import random

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from src import const
from src import method_const as mconst

# Dictionary of curves limits : key = pstates, value = {Alpha :(min_x, max_x, min_y, max_y), ...}
limit_in_function_of_pstates = \
    {
        str([2, 3, 4]):
            {
                10: [(0.46, 0.50, 1000, 1200), (0.48, 0.52, 950, 1050), (0.51, 0.53, 700, 900)],
                20: [(0.473, 0.479, 1100, 1150), (0.49, 0.50, 1150, 1200), (0.495, 0.50, 1120, 1150)],
                30: [(0.48, 0.50, 1350, 1500), (0.50, 0.52, 1250, 1350), (0.52, 0.56, 1100, 1300)],
                40: [(0.50, 0.70, 1550, 1600), (0.74, 0.76, 1430, 1450), (0.95, 1, 1300, 1500)]
            },
        str([2, 3, 4, 5]):
            {
                20: [(0.468, 0.479, 1280, 1300), (0.47, 0.49, 1190, 1210), (0.448, 0.45, 1360, 1380)],
                40: [(0.50, 0.55, 1915, 1930), (0.60, 0.61, 1615, 1630), (0.89, 0.91, 1815, 1830)]
            },
        str([2, 3, 4, 5, 6]):
            {
                10: [(0.47, 0.475, 1190, 1210), (0.46, 0.49, 1100, 1300), (0.455, 0.475, 1290, 1310)],
                20: [(0.459, 0.46, 1400, 1420), (0.45, 0.4750, 1350, 1450), (0.452, 0.453, 1280, 1290)],
                30: [(0.442, 0.443, 1610, 1620), (0.45, 0.46, 1480, 1520), (0.445, 0.448, 1710, 1720)],
                40: [(0.515, 0.516, 1740, 1745), (0.50, 0.70, 1600, 1800), (0.499, 0.4995, 1740, 1745)]
            }
    }


def find_point_in_solution_set(Lambda, Space, pstates, position):
    """
    It takes a list of points in the solution set, and returns a list of points in the solution set that are in the
    specified position

    @param Lambda the number of states in the HMM
    @param Space The solution set of the problem.
    @param pstates The number of states in the Markov chain.
    @param position "All", "Begin", "Middle", "End"

    @return A list of points that are in the solution set.
    """
    points = [[], [], []] if position == "All" else []
    for element in Space:
        if (position == "All" or position == "Begin") and limit_in_function_of_pstates[str(pstates)][Lambda][0][0] <= \
                element[1] <= limit_in_function_of_pstates[str(pstates)][Lambda][0][1] \
                and limit_in_function_of_pstates[str(pstates)][Lambda][0][2] <= element[2] <= \
                limit_in_function_of_pstates[str(pstates)][Lambda][0][3]:
            points[0].append(element[0]) if position == "All" else points.append(element[0])

        if (position == "All" or position == "Middle") and limit_in_function_of_pstates[str(pstates)][Lambda][1][0] <= \
                element[1] <= limit_in_function_of_pstates[str(pstates)][Lambda][1][1] \
                and limit_in_function_of_pstates[str(pstates)][Lambda][1][2] <= element[2] <= \
                limit_in_function_of_pstates[str(pstates)][Lambda][1][3]:
            points[1].append(element[0]) if position == "All" else points.append(element[0])

        if (position == "All" or position == "End") and limit_in_function_of_pstates[str(pstates)][Lambda][2][0] <= \
                element[1] <= limit_in_function_of_pstates[str(pstates)][Lambda][2][1] \
                and limit_in_function_of_pstates[str(pstates)][Lambda][2][2] <= element[2] <= \
                limit_in_function_of_pstates[str(pstates)][Lambda][2][3]:
            points[2].append(element[0]) if position == "All" else points.append(element[0])
    return points


def draw_2Dcurves(Space, Approx, Opt, results, fig_id, not_zoom):
    """
    It takes in a list of points, and plots them on a 2D graph

    @param Space the objective space
    @param Approx The approximate Pareto front
    @param Opt the Pareto front
    @param results a list of tuples, list of tuple.
    @param fig_id the figure number
    @param not_zoom if True, the plot will be zoomed in to the region of interest.
    """
    plt.figure(fig_id)
    Space, Approx, Opt = np.array(Space, dtype=object), np.array(Approx, dtype=object), np.array(Opt, dtype=object)
    Space = Space[Space[:, 2].argsort()]  # Sorting in function of the time response
    Opt = Opt[Opt[:, 2].argsort()]  # Sorting in function of the time response
    Approx = Approx[Approx[:, 2].argsort()]  # Sorting in function of the time response

    time, power = Space[:, 2], Space[:, 3] if const.Type == 0 else Space[:, 4]
    plt.scatter(time, power, c="green", marker='+', label="Objective space")
    time, power = Approx[:, 2], Approx[:, 3] if const.Type == 0 else Approx[:, 4]
    plt.scatter(time, power, s=40, marker='x', c="blue", label="Approx Pareto Front")
    time, power = Opt[:, 2], Opt[:, 3] if const.Type == 0 else Opt[:, 4]
    plt.scatter(time, power, c="red", s=10, marker=".", label="Pareto Front")

    for result in results:
        plt.scatter(result[0], result[1], c=result[3], s=result[4], marker=result[5], label=result[6])

    plt.xlabel('Response Time (s)')
    plt.ylabel('Power consumption (w)')

    if not_zoom:
        ax, x_lim, y_lim = plt.gca(), plt.xlim(), plt.ylim()
        ax.set_ylim([y_lim[0], 2300])
        ax.set_xlim([x_lim[0], 1])

    plt.legend(loc="upper right")
    print("generating curves")

def generate_curves_1(Lambda, pstates, greedy_Alpha_list, tabu_Alpha_list, Delta, positions, separate_start):
    """
    It generates the curves for the first plot

    @param Lambda the number of requests per second
    @param pstates the number of power states
    @param greedy_Alpha_list a list of values for the weight parameter, Alpha, for the greedy search.
    @param tabu_Alpha_list list of weights for the tabu search
    @param Delta the distance between the points in the decision space
    @param positions a list of positions of the starting points for the tabu search.
    @param separate_start if True, then the starting point for each tabu search is randomly chosen from the solution
    set.

    @return decision_space, raw_data, results, Approx, Opt
    """
    keys = mconst.decision_space.keys()
    if len(keys) == 0 or (Lambda, str(pstates)) not in keys:
        mconst.init_decision_space(Lambda, pstates)

    decision_space = mconst.decision_space[(Lambda, str(pstates))][0]
    results = [[[], [], [], "orange", 60, "h", r'Greedy Search ($\Delta$ = 0)']]
    raw_data = {'Function': [], 'Threshold': [], 'Alpha': [], 'Response Time': [], 'Power Consumption': [],
                'Objective Function Value': []}

    # greedy search
    for Alpha in greedy_Alpha_list:
        th_h1v2s, val_h1v2s, time_h1v2s = mconst.greedy_search(Lambda, Alpha, pstates, Delta)
        time = mconst.operations_materials[val_h1v2s][5]
        power = mconst.operations_materials[val_h1v2s][6] if const.Type == 0 else \
                mconst.operations_materials[val_h1v2s][7]

        results[0][0].append(time)
        results[0][1].append(power)
        results[0][2].append("w = {}".format(Alpha))

        raw_data['Function'].append("Greedy Search"), raw_data['Threshold'].append(th_h1v2s)
        raw_data['Alpha'].append(Alpha), raw_data['Response Time'].append("{:.10f}".format(time))
        raw_data['Power Consumption'].append("{:.10f}".format(power)),
        raw_data['Objective Function Value'].append("{:.10f}".format(val_h1v2s))
        mconst.min_vector_greedy.clear()


    # tabu search
    n = len(tabu_Alpha_list)
    symbols = ["H"] * n
    color_list = ["brown", "black", "purple", "yellow"]
    random_threshold = None
    if not separate_start:
        random_threshold = mconst.generate_random_threshold(pstates)
    for i in range(n):
        results_to_append = [[], [], [], color_list[i], 25, symbols[i],
                             "Tabu Search (w = {})".format(tabu_Alpha_list[i])]
        if separate_start:
            points = find_point_in_solution_set(Lambda, decision_space, pstates, positions[i])
            random_threshold = points[random.randint(0, len(points) - 1)] if len(points) > 0\
            else mconst.generate_random_threshold(pstates)
        th_tr, val_tr, _ = mconst.tabu_search(Lambda, tabu_Alpha_list[i], pstates, random_threshold)
        for element in mconst.min_vector_tabu:
            time = mconst.operations_materials[element[1]][5]
            power = mconst.operations_materials[element[1]][6] if const.Type == 0 else \
                mconst.operations_materials[element[1]][7]

            results_to_append[0].append(time)
            results_to_append[1].append(power)

            raw_data['Function'].append("Tabu Search"), raw_data['Threshold'].append(element[0])
            raw_data['Alpha'].append(tabu_Alpha_list[i]), raw_data['Response Time'].append("{:.10f}".format(time))
            raw_data['Power Consumption'].append("{:.10f}".format(power)),
            raw_data['Objective Function Value'].append("{:.10f}".format(element[1]))

        results_to_append[2].append("w = {}".format(tabu_Alpha_list[i]))
        results.append(results_to_append)
        mconst.min_vector_tabu.clear()

    Approx = mconst.approx_kung_search(Lambda, pstates)[2]
    Opt = mconst.kung_search(Lambda, pstates)[2]
    return decision_space, raw_data, results, Approx, Opt

def test_1():
    """
    It generates the curves for the first test
    """
    function_name = mconst.curves_test_1
    mconst.create_folder_if_he_doesnt_exist(function_name)

    Lambdas = [10, 20, 30, 40]
    pstates = [2, 3, 4]
    greedy_Alpha_list = [x * 0.01 for x in range(0, 101, 2)]
    tabu_Alpha_list = [0.05, 0.8]
    positions = ["Begin", "Middle", "End"]
    separate_start = [False, True]
    same_scale = [False, True]

    for start in separate_start:
        for element in same_scale:
            for Lambda in Lambdas:
                decision_space, raw_data, results, Approx, Opt = generate_curves_1(Lambda, pstates, greedy_Alpha_list,
                                                                                   tabu_Alpha_list, 0, positions, start)
                filename = "curves_"
                pdf_filename = mconst.example_number_has_not_been_attributed(function_name, filename, ".pdf")
                csv_filename = pdf_filename[:-3] + "csv"

                df = pd.DataFrame.from_dict(raw_data)
                print(csv_filename)
                df.to_csv(csv_filename, index=False)
                print("csv results has been saved in : {}".format(csv_filename))
                draw_2Dcurves(decision_space, Approx, Opt, results, 0, element)
                mconst.save_img_as_pdf(pdf_filename, 0, 1000)
                print("pdf results has been saved in : {}".format(pdf_filename))
                plt.clf()
                mconst.operations_materials.clear()


def launch():
    """
    Launch the tests
    """
    # To generate the folder which contains the results
    mconst.create_folder_if_he_doesnt_exist(mconst.curves)
    test_1()
