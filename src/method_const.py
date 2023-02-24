# External modules
import decimal

# All constants are defined here
import src.const as const

# All search methods are defined here
import src.algorithms.wsm.exhaustive as exs
import src.algorithms.wsm.greedy as grs
import src.algorithms.wsm.local as los
import src.algorithms.pareto.kung as kus
import src.algorithms.pareto.approx_kung as aks
import src.algorithms.wsm.tabu as ts

# All utils methods are defined here
import src.other.save as sdi
import src.other.solve as sudvfs

# Count the number of WSM methods.
method_number = 7

# Distance between two solutions
pi = [decimal.Decimal(0)] * (const.B + 1)

# Number of iteration when the minimal threshold doesn't change
tabu_max_iteration_without_change = 100

# Size of the list (used in local and tabu search)
tabu_max_size_list = const.B * 4

# Store all value of function objective.
operations_materials = {}

# Decision space.
decision_space = {}

# Store all exhaustive search's minimal vector found.
min_vector_exhaustive = []

# Store all greedy search's minimal vector found.
min_vector_greedy = []

# Store all local search's minimal value found.
min_vector_local = []

# Store all tabu search's minimal vector found.
min_vector_tabu = []

# Arguments used for wsm methods in latex array
file_top_field = "Method name = {}\nDelta = {}\nAlpha = {}\nPstates = {}\nC = {}\nB = {}\nType= {}\n" \
                 "get_number_of_servers_in_service = {}\nen = {}\nen_idle = {}\nEs = {}\n\n"

# Arguments used for wsm methods in latex array
file_top_field_compare_delta = "Method name = {}\nDelta = {}\nAlpha = {}\nLambda = {}\nPstates = {}" \
                               "\nC = {}\nB = {}\nType= {}\nMu = {}\nen = {}" \
                               "\nen_idle = {}\nEs = {}\n\n"

# Test folder
resource = "resources/"
curves = resource + "curves/"
single = resource + "single/"
latex = resource + "latex/"

curves_test_1 = curves + "test_1/"

single_exhaustive = single + "exhaustive/"
single_greedy = single + "greedy/"
single_local = single + "local/"
single_tabu = single + "tabu/"
singe_kung = single + "kung/"
single_approx_kung = single + "approx_kung/"

latex_test_1 = latex + "test_1/"

# Exhaustive search method.
exhaustive_search = exs.search

# Greedy search method.
greedy_search = grs.search

# Local search methods.
loca_search = los.search
operation_on_threshold = los.operation_on_threshold
add_to_list = los.add_to_list
generate_random_threshold = los.generate_random_threshold

# Tabu search method.
tabu_search = ts.search

# Kung's search method.
kung_search = kus.search
approx_kung_search = aks.search_approx_kung
pareto_front = kus.front
compare_pareto_search = kus.compare_pareto_methods

# Function from other package.
create_folder_if_he_doesnt_exist = sdi.create_folder_if_he_doesnt_exist
example_number_has_not_been_attributed = sdi.example_number_has_not_been_attributed
save_img_as_pdf = sdi.save_multi_image
save_method_as_csv = sdi.save_wsm_method_as_csv
save_pareto_method_as_csv = sdi.save_pareto_method_as_csv
init_decision_space = sudvfs.init_decision_space
solve_dvfs = sudvfs.solve
solve_time_and_power_dvfs = sudvfs.solve_time_and_power
find_obj_func = sudvfs.find_obj_func
