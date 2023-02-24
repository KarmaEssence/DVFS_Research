# All method constants are defined here
import src.method_const as mconst

# All test are defined here
import src.test.single as si
import src.test.latex as la
import src.test.curves as cu


def main():
    """
    It launches all tests of the project.
    """
    mconst.create_folder_if_he_doesnt_exist(mconst.resource)
    # cu.launch() # Test 1 : Curves
    # si.launch() # Test 2 : Single
    # la.launch() # Test 3 : Latex : this test can take a bit longer because it compares all the methods for all the proposed instances.
    print("All test done !")


# Calling the main function of each module.
main()
