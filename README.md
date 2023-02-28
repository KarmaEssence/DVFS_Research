# DVFS-Research

## I - Goal
 
This framework addresses the problem of performance-energy trade-off in DVFS (Dynamic Voltage Frequency Scaling) systems. Today processor, Virtual Machine and Servers activity bring environmental question, more accurately some services doesn't need a high capacity of ressources. DVFS technique allows a system to remain switched ON while changing frequency to match the traffic. This avoids successive shutdown and restoration costs of big systems that can result in waste additional power and further latency to restore the same regime. The proposed DVFS model consideres a vector of thresholds that controls switch UP or DOWN of the frequency of the system. Thus, we seek to find the optimal vector of thresholds for performance and power consumption control. The system is modeled by a birth-death process that we propose, solved analytically and efficiently. Then we start a Multi-Objective Optimization to find the optimal thresholds. The optimization process considers a scalarization approach (WSM - Weighted Sum Method) and a non-dominated set approach (Pareto method). For more details, refer to the original paper [1].

## II - Project architecture

Tree of the most important files and folder in the project's repository :

```
/
├─┬─resources/: To store all generated results.
│ ├──curves/: To store all curves.
│ ├──latex/: To store all latex content.
│ └──single/: To store all single results.
├───screenshots/: All screenshots used in README.md.
├─┬─src/: Source folder.
│ ├─┬─algorithms/: Algorithms folder.
│ │ ├─┬─wsm/: Weighted sum methods.
│ │ │ ├──exhaustive.py: Exhaustive search.
│ │ │ ├──greedy.py: Greedy proposed method.
│ │ │ ├──local.py: Local search.
│ │ │ └──tabu.py: Tabu search. 
│ │ └─┬─pareto/: Pareto methods.
│ │   ├──kung.py: Kung front method.
│ │   └──approx_kung.py: Approx greedy Pareto method.
│ ├─┬─others/: Other methods.
│ │ ├──save_data_in_file.py: To save results in resources file.
│ │ └──utils.py: Utils functions.
│ └─┬─tests/: Tests folder.
│   ├──curves.py: To generates curves.
│   ├──latex.py: To generates latex content.
│   └──single.py: Test of each componant of projet.
├───.gitignore: To avoid junk files on git repository. 
├───README.md: This file.
└───launcher.py: To run all content from src/.
```

## III - Build and run

Before running code, you need to download all package needed :

    pip install matplotlib==3.5.3
    pip install pandas
    pip install numpy

Uncomment and run function from launcher.py : 

    python launcher.py

## IV - Usage

In this project, there are three type of tests you can run :

### A) Test 1 : Curves

Allows to generate a graph to compare the efficiency of all weight sum and pareto methods.
To use this test, you need to uncomment the function `cu.launch()` in `launcher.py`, after that, you can go to `curves.py`
to uncomment the actual function to use, moreover you can add or remove your own test in this file.

<br>
<div align="center">
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/curves_uncomment_in_launcher.png" width="400" height="150"/>
</div>
<br>

There is only one test, but you can generate different types of graphs with different configurations. 
In particular, you can choose the number of wsm curves displayed, to start at the same point or not, to show all 
curves with the same scale and the position where the points should be selected.

<br>
<div align="center">
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/curves_uncomment_in_test_1.png" width="400" height="250"/>
</div>
<br>

Once your tests are finished, you can check in `resources/curves/<test>/` to see the generated graphs and their data (respectively in pdf and csv files).
For example, here is the result of the test 1 :

<br>
<div align="center">
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/curves_test_1_results.png" width="500" height="200"/>
</div>
<br>

### B) Test 2 : Single

Allows to show all algorithms already implemented in action.
To use this test, you need to uncomment the function `si.launch()` in `launcher.py`, after that, you can go to `single.py` 
to uncomment the actual function to use, moreover you can add or remove
your own test in this file.

<br>
<div align="center">
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/single_uncomment_in_launcher.png" width="400" height="150"/>
</div>
<br>

Once your tests are finished, you can check in `resources/single/<method>/` to see the generated graphs and their data (respectively in pdf and csv files).
For example, here is the result of the exhaustive search :

<br>
<div align="center">
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/single_exhaustive_results_1.png" width="500" height="125"/>
</div>
<br>
<div align="center">
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/single_exhaustive_results_2.png" width="500" height="25"/>
</div>
<br>

### C) Test 3 : Latex

Allows to generate a latex file to compare the efficiency of all wsm and pareto method.
To use this test, you need to uncomment the function `la.launch()` in `launcher.py`, after that, you can go to `latex.py`
to uncomment the actual function to use, moreover you can add or remove
your own test in this file.

<br>
<div align="center">
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/latex_uncomment_in_launcher.png" width="400" height="150"/>
</div>
<br>

There is only one test, but you can generate different types of latex documents, about which weight sum methods are 
better than others, also you can count the exhaustive search or not. For the pareto methods there is the same option, 
but it’s to compare the efficiency of each solution set found.

Once your tests are finished, you can check in `resources/latex/<test>/` to see the generated data <br> (in csv file).
For example, here is the result of the test 1, you can open the file created and copy the content to paste it in
your latex editor like overleaf :

<br>
<div align="center">
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/latex_test_1_results_1.png" width="500" height="20"/>
</div>
<br>
<div align="center">
        <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/latex_test_1_results_2.png" width="1000" height="350"/>
</div>
<br>

This test may take a little longer as it compares all methods for all proposed instances.

## V - Illustration

In this section all screenshots related to the test are displayed here.

### A) Curves 

<div align="center">
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/curves_example_1.png" width="300" height="250"/>
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/curves_example_2.png" width="300" height="250"/>
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/curves_example_3.png" width="300" height="250"/>
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/curves_example_4.png" width="300" height="250"/>
</div>    

### B) Latex (example of a small instance)

<div align="center">
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/latex_example_1.png" width="600" height="140"/>
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/latex_example_2.png" width="600" height="70"/>
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/latex_example_3.png" width="600" height="120"/>
    <img src="https://github.com/KarmaEssence/DVFS_Internship/blob/5-final-branch/screenshots/latex_example_4.png" width="600" height="50"/>

</div>



##  Contributors & Copyright

- [Leo LE CORRE](https://github.com/KarmaEssence)
- [Youssef AIT EL MAHJOUB](https://github.com/ossef)

- This code is open source. However, one can cite the original document [1] submitted to ECMS 2023.

[1] "STOCHASTIC MODELING AND OPTIMIZATION FOR POWER AND PERFORMANCE CONTROL IN DVFS SYSTEMS", Youssef AIT EL MAHJOUB, Leo LE CORRE and Hind CASTEL-TALEB". The paper was submitted to "MaSPECS" track of 37th ECMS - International Conference on Modelling and Simulation, 2023.
