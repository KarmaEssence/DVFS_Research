import os

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import src.method_const as mconst
import src.const as const


def create_folder_if_he_doesnt_exist(folder_name):
    """
    If the folder doesn't exist, create it.

    @param folder_name The name of the folder you want to create.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def example_number_has_not_been_attributed(folder, filename="example_", extension=".txt"):
    """
    It returns the name of a file that doesn't exist in a given folder.

    @param folder The folder where the file will be saved.
    @param filename The name of the file you want to create.
    @param extension The extension of the file you want to create.

    @return The name of the file that has not been attributed yet.
    """
    i = 0
    if os.path.exists(folder):
        for element in os.listdir(folder):
            if not os.path.isfile(element) and extension == element[-4:]:
                i += 1
    return folder + filename + str(i) + extension


def save_multi_image(filename, limit_start, limit_end):
    """
    It takes a filename, a start index, and an end index, and saves all the figures between the start and end
    indices to the filename.

    @param filename The name of the file to save the images to.
    @param limit_start The first figure number to save.
    @param limit_end The number of the last figure you want to save.
    """
    open(filename, "x")
    pp = PdfPages(filename)
    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums if limit_start <= n < limit_end]
    for fig in figs:
        fig.savefig(pp, format='pdf')
        fig.clf()
    pp.close()

def save_wsm_method_as_csv(method_name, filename, min_vector_list, time, delta=None):
    """
    It takes the method name, the filename, the list of minimum vectors, the time it took to run the method,
    and the delta value (if the method is greedy) and saves the results in a csv file.

    @param method_name The name of the method.
    @param filename The name of the file to save the results.
    @param min_vector_list List of tuples (thresholds, objective function value).
    @param time The time it took to run the algorithm.
    @param delta The step size for the greedy algorithm.
    """
    raw_data = {'Name': [], 'B': [], 'C': [], 'Type': [], 'Lambda': [], 'Alpha': [], 'pstates': [], 'Thresholds': [],
                'Average Task': [], 'Response Time (s)': [], 'Power Consumption (w)': [], 'Reject Probability': [],
                'Objective Function Value (0-1)': [], 'Execution Time (s)': []}

    if method_name == "greedy":
        raw_data['Delta'] = []

    for value in min_vector_list:
        data_tuple = mconst.operations_materials[value[1]]
        raw_data['Name'].append(method_name)
        raw_data['B'].append(const.B)
        raw_data['C'].append(const.C)
        raw_data['Type'].append(const.Type)
        raw_data['Lambda'].append(data_tuple[0])
        raw_data['Alpha'].append(data_tuple[1])
        raw_data['pstates'].append(data_tuple[2])
        raw_data['Thresholds'].append(value[0])
        raw_data['Average Task'].append("{:.10f}".format(data_tuple[4]))
        raw_data['Response Time (s)'].append("{:.10f}".format(data_tuple[5]))
        raw_data['Power Consumption (w)'].append("{:.10f}".format(data_tuple[6] if const.Type == 0 else data_tuple[7]))
        raw_data['Reject Probability'].append("{:.10f}".format(data_tuple[11]))
        raw_data['Objective Function Value (0-1)'].append("{:.10f}".format(value[1]))
        raw_data['Execution Time (s)'].append("{:.5f}".format(time))
        if method_name == "greedy":
            raw_data['Delta'].append(delta)

    df = pd.DataFrame.from_dict(raw_data)
    df.to_csv(filename, index=False)
    print("{} results has been saved in : {}".format(method_name, filename))

def save_pareto_method_as_csv(method_name, filename, results):
    """
    It takes the results of a pareto method and saves it as a csv file.

    @param method_name The name of the method.
    @param filename The name of the file to save the results.
    @param results A result to save in csv file
    """
    raw_data = {'Name': [], 'B': [], 'C': [], 'Type': [], 'Lambda': [], 'pstates': [], 'Thresholds': [],
                'Average Task': [], 'Response Time (s)': [], 'Power Consumption (w)': [], 'Reject Probability': [],
                'Execution Time (s)': []}

    for value in results[2]:
        raw_data['Name'].append(method_name)
        raw_data['B'].append(const.B)
        raw_data['C'].append(const.C)
        raw_data['Type'].append(const.Type)
        raw_data['Lambda'].append(results[0])
        raw_data['pstates'].append(results[1])
        raw_data['Thresholds'].append(value[0])
        raw_data['Average Task'].append("{:.10f}".format(value[1]))
        raw_data['Response Time (s)'].append("{:.10f}".format(value[2]))
        raw_data['Power Consumption (w)'].append("{:.10f}".format(value[3] if const.Type == 0 else value[4]))
        raw_data['Reject Probability'].append("{:.10f}".format(value[6]))
        raw_data['Execution Time (s)'].append("{:.5f}".format(results[3]))

    df = pd.DataFrame.from_dict(raw_data)
    df.to_csv(filename, index=False)
    print("{} results has been saved in : {}".format(method_name, filename))
