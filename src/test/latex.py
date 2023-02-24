import src.const as const
import src.method_const as mconst


def latex_start_document(doc_title, doc_authors, doc_date):
    """
    It takes in a title, author, and date, and returns a string that
    contains the LaTeX code to start a document with that information.

    @param doc_title The title of the document.
    @param doc_authors The authors of the document.
    @param doc_date The date of the document.

    @return A string of LaTeX code that will be used to start the document.
    """
    import_class = r"\documentclass{article}" + "\n" + r"\usepackage[english]{babel}" + "\n" + \
                   r"\usepackage[letterpaper,top=2cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=1.75cm]{geometry}" \
                   + "\n" + r"\usepackage{amsmath}" + "\n" + r"\usepackage{graphicx}" + "\n" + \
                   r"\usepackage[colorlinks=true, allcolors=blue]{hyperref}" + "\n" + r"\usepackage{tabularx}"\
                   + "\n\n\n"
    doc_info = r"\title{" + doc_title + "}" + "\n" + r"\author{" + doc_authors + "}" +\
               "\n" + r"\date{" + doc_date + "}" + "\n\n\n"
    begin_doc = r"\begin{document}" + "\n" + r"\maketitle" + "\n\n\n"
    return import_class + doc_info + begin_doc


def latex_pstates_array_args(Alpha_list, flag):
    """
    It takes in a list of Alpha values and a flag, and returns a string that contains the title and
    content of the section.

    @param Alpha_list The list of alpha values.
    @param flag Whether to use the Alpha_list or not.

    @return The title and content of the latex file.
    """
    title = "\section{Generated result}\n"
    if flag:
        content = r"C = {}, B = {}\newline".format(const.C, const.B) + "\n" + \
                  r"Alpha list = {},\newline Lambda list = {},\newline Delta Max = {}\newline".format(Alpha_list,
                                                                                                      range(1, const.B),
                                                                                                      const.B) \
                  + "\n" + r"Mu = {}\newline  en = {}\newline en\_idle = {}" \
                           r"\newline Es = {}\newline\newline".format(const.Mu, const.en, const.en_idle, const.Es)\
                  + "\n\n"
    else:
        content = r"C = {}, B = {}\newline".format(const.C, const.B) + "\n" + \
                  r"Lambda list = {}\newline".format(Alpha_list, range(1, const.B), const.B) \
                  + "\n" + r"Mu = {}\newline  en = {}\newline en\_idle = {}" \
                           r"\newline Es = {}\newline\newline".format(const.Mu, const.en, const.en_idle, const.Es)\
                  + "\n\n"
    return title + content


def write_in_document(filename, content, option):
    """
    The function `write_in_document` takes in three arguments: `filename`, `content`, and `option`. It opens the file
    `filename` with the option `option` and writes the content `content` in the file.

    @param filename The name of the file you want to write to.
    @param content The content that you want to write in the file.
    @param option 'w' for write, 'a' for append, 'r' for read.
    """
    with open(filename, option) as file:
        file.write(content)


def convert_data_to_latex_doc(result, filename, min_len_pstates, flag=True):
    """
    It writes the results of the test in a latex document

    @param result list of lists, each sublist contains the number of successes and
    the total time of execution of the method
    @param filename the name of the file to write to
    @param min_len_pstates the minimum length of the shortest path found by the exhaustive algorithm
    @param flag True if we want to compare the methods to the exhaustive method, False otherwise.
    """
    with open(filename, 'a') as file:
        file.write(r"\begin{center}" + "\n" + r"\begin{tabularx}{\textwidth} { | >{}X | >{\centering\arraybackslash}X |"
                                              r" >{\centering\arraybackslash}X | }" + "\n" + r"\hline" + "\n")
        if flag:
            file.write(r"Method name & Success rate (\%) & Average execution time (s) \\\hline" + "\n")
            file.write(r"Exhaustive search & 100\% & {:.6f}s \\\hline".format(result[0][1] / result[0][0]) + "\n")
        else:
            file.write(r"Method name & Smallest value obtained rate (\%) & Average execution time (s) \\\hline" + "\n")
        file.write(r"Greedy search ($\Delta$ = 0) & {:.0f}\% & {:.6f}s \\\hline"
                   .format((result[1][0] / result[0][0]) * 100, result[1][1] / result[0][0]) + "\n")
        file.write(r"Greedy search ($\Delta$ Max = {}) & {:.0f}\% & {:.6f}s \\\hline"
                   .format(const.B - min_len_pstates, (result[2][0] / result[0][0]) * 100,
                           result[2][1] / result[0][0]) + "\n")
        file.write(r"Local search & {:.0f}\% & {:.6f}s \\\hline"
                   .format((result[3][0] / result[0][0]) * 100, result[3][1] / result[0][0]) + "\n")
        file.write(r"Taboo search & {:.0f}\% & {:.6f}s \\\hline"
                   .format((result[4][0] / result[0][0]) * 100, result[4][1] / result[0][0]) + "\n")
        file.write(r"\end{tabularx}" + "\n" + r"\end{center}" + "\n\n")


def convert_pareto_data_to_latex_doc(result, filename, flag):
    """
    It takes the result of the experiment, the name of the file to
    write to, and a flag indicating whether the experiment was a success rate experiment or
    a Mu experiment. It then writes the result to the file in a LaTeX table format

    @param result a list of lists, where each sublist contains the number of successful runs,
    the average size of the solution,
    @param filename the name of the file to write to
    @param flag True if we want to compare Kung's algorithm with the Pareto approximation algorithm, False otherwise
    """
    with open(filename, 'a') as file:
        file.write(r"\begin{center}" + "\n" + r"\begin{tabularx}{\textwidth} { | >{}X | >{\centering\arraybackslash}X |"
                                              r" >{\centering\arraybackslash}X | }" + "\n" + r"\hline" + "\n")
        if flag:
            file.write(r"Method name & Success rate (\%) & Average execution time (s) \\\hline" + "\n")
            file.write(r"Kung's & 100\% - {:.0f} solutions & {:.6f}s \\\hline"
                       .format(result[0][1] / result[0][0], result[0][2] / result[0][0]) + "\n")
            file.write(r"Pareto approx & {:.0f}\% & {:.6f}s \\\hline"
                       .format(result[1][0] / result[0][0], result[1][1] / result[0][0]) + "\n")
        else:
            file.write(r"Method name & Average solution size & Average execution time (s) \\\hline" + "\n")
            file.write(r"Pareto approx & {:.0f} & {:.6f}s \\\hline"
                       .format(result[0][1] / result[0][0], result[0][2] / result[0][0]) + "\n")
        file.write(r"\end{tabularx}" + "\n" + r"\end{center}" + "\n\n")


def generate_stats_of_methods(pstates_list, Alpha_list, with_seed=True):
    """
    It generates the statistics of the methods.

    @param pstates_list A list of lists of pstates.
    @param Alpha_list The list of alpha values to be tested.
    @param with_seed If True, the random threshold is generated once and used for all the methods.
    """
    res = [[0, 0, 0, 0] for _ in
           range(mconst.method_number)]  # sublist per method : [0] : stats of success, [1] : average time of success.
    res[5][1], res[6][1] = len(Alpha_list), len(Alpha_list)
    for pstates in pstates_list:
        for Lambda in range(1, const.B):
            for Alpha in Alpha_list:
                th_opt, val_opt, time_opt = mconst.exhaustive_search(Lambda, Alpha, pstates)
                res[0][0], res[0][1] = res[0][0] + 1, res[0][1] + time_opt

                th_near, val_near, time_near = mconst.greedy_search(Lambda, Alpha, pstates, 0)
                res[1][1] = res[1][1] + time_near
                if th_opt == th_near:
                    res[1][0] += 1

                th_near, val_near, time_near = mconst.greedy_search(Lambda, Alpha, pstates, const.B - len(pstates))
                res[2][1] = res[2][1] + time_near
                if th_opt == th_near:
                    res[2][0] += 1

                random_th_opt = []
                if with_seed:
                    random_th_opt = mconst.generate_random_threshold(pstates)
                th_near, val_near, time_near = mconst.loca_search(Lambda, Alpha, pstates, random_th_opt)
                res[3][1] = res[3][1] + time_near
                if th_opt == th_near:
                    res[3][0] += 1

                th_near, val_near, time_near = mconst.tabu_search(Lambda, Alpha, pstates, random_th_opt)
                res[4][1] = res[4][1] + time_near
                if th_opt == th_near:
                    res[4][0] += 1
    return res


def generate_stats_of_pareto_methods(pstates_list, flag):
    """
    It generates the statistics of the Kung and Approximate Kung methods.

    @param pstates_list A list of lists of pstates.
    @param flag True if you want to compare the Kung method with the Approximate method.
    False if you want to compare the approximate method with the approximate method.

    @return The return value is a list of lists. Each sublist contains the statistics of a method.
    """
    res = [[0, 0, 0] for _ in range(2)]  # sublist per method : [0] : stats of success, [1] : average time of success.
    for pstates in pstates_list:
        for Lambda in range(1, const.B):
            if flag:
                kung = mconst.kung_search(Lambda, pstates)
                res[0][0], res[0][1], res[0][2] = res[0][0] + 1, res[0][1] + len(kung[2]), res[0][2] + kung[-1]

                approx_kung = mconst.approx_kung_search(Lambda, pstates)
                res[1][0] = res[1][0] + mconst.compare_pareto_search(approx_kung[2], kung[2])[1]
                res[1][1] = res[1][1] + approx_kung[-1]
            else:
                approx_kung = mconst.approx_kung_search(Lambda, pstates)
                res[0][0], res[0][1] = res[0][0] + 1, res[0][1] + len(approx_kung[2])
                res[0][2] = res[0][2] + approx_kung[-1]
    return res


def generate_stats_2_of_methods(pstates_list, Alpha_list, with_seed=True):
    """
    It generates a list of lists, where each sublist contains the number of successes and
    the average time of success for each method.

    @param pstates_list List of pstates to be tested.
    @param Alpha_list the List of alpha values to test.
    @param with_seed if True, the random threshold is generated once and used for all methods.

    @return A list of lists. Each sublist contains the number of times a method was successful and
    the average time it took to run.
    """
    res = [[0, 0, 0, 0] for _ in range(
        mconst.method_number + 1)]  # sublist per method : [0] : stats of success, [1] : average time of success.
    for pstates in pstates_list:
        for Alpha in Alpha_list:
            for Lambda in range(1, const.B):
                res[0][0] = res[0][0] + 1

                th_h1v2s, val_h1v2s, time_h1v2s = mconst.greedy_search(Lambda, Alpha, pstates, 0)
                res[1][1] = res[1][1] + time_h1v2s

                th_h1v2s_B, val_h1v2s_B, time_h1v2s_B = mconst.greedy_search(Lambda, Alpha, pstates,
                                                                             const.B - len(pstates))
                res[2][1] = res[2][1] + time_h1v2s_B

                random_th_opt = []
                if with_seed:
                    random_th_opt = mconst.generate_random_threshold(pstates)

                th_h2v1s, val_h2v1s, time_h2v1s = mconst.loca_search(Lambda, Alpha, pstates, random_th_opt)
                res[3][1] = res[3][1] + time_h2v1s

                th_tr, val_tr, time_tr = mconst.tabu_search(Lambda, Alpha, pstates, random_th_opt)
                res[4][1] = res[4][1] + time_tr

                val_opt_list = [val_h1v2s, val_h1v2s_B, val_h2v1s, val_tr]
                value = min(val_opt_list)
                if value == val_h1v2s:
                    res[1][0] += 1
                if value == val_h1v2s_B:
                    res[2][0] += 1
                if value == val_h2v1s:
                    res[3][0] += 1
                if value == val_tr:
                    res[4][0] += 1
    return res

def test_1():
    """
    It generates a latex document that compares the different methods
    of the library.
    """
    function_name = mconst.latex_test_1
    mconst.create_folder_if_he_doesnt_exist(mconst.latex_test_1)

    pstates_2D_array = [[[1, 2], [1,3], [1,4],[2, 3], [2, 5], [3, 4], [3,5], [4, 5], [4, 6], [5, 6]]]
    # pstates_2D_array = [[ [1, 2, 3], [1, 2, 6], [2, 3, 5], [3, 4, 5], [3, 5, 6], [4, 5, 6]]]
    # pstates_2D_array = [[[1, 2, 3, 4], [3, 4, 5, 6]]]
    Alpha_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    # Function calling
    start_doc = latex_start_document("Compare methods with others", "You", r"\today")
    filename = mconst.example_number_has_not_been_attributed(function_name, "compare_all_method_", ".tex")
    write_in_document(filename, start_doc + latex_pstates_array_args(Alpha_list, False), 'w')

    for pstates_list in pstates_2D_array:
        write_in_document(filename, r"\subsection{Pstates = " + str(pstates_list) + "}\n\n", 'a')

        # Stats 1 function :
        result = generate_stats_of_methods(pstates_list, Alpha_list)
        convert_data_to_latex_doc(result, filename, len(pstates_list[0]))

        # Stats 1 function with pareto methods :
        result = generate_stats_of_pareto_methods(pstates_list, True)
        convert_pareto_data_to_latex_doc(result, filename, True)

        # Stats 2 function :
        result = generate_stats_2_of_methods(pstates_list, Alpha_list)
        convert_data_to_latex_doc(result, filename, len(pstates_list[0]), False)

        # Stats 2 function with pareto approx :
        result = generate_stats_of_pareto_methods(pstates_list, False)
        convert_pareto_data_to_latex_doc(result, filename, False)

    print("latex results has been saved in : {}".format(filename))
    write_in_document(filename, r"\end{document}" + "\n", 'a')

def launch():
    """
    Launch test.
    """
    # To generate the folder which contains the results
    mconst.create_folder_if_he_doesnt_exist(mconst.latex)
    test_1()


