# DVFS-Research

## Goal

Today processor activity bring environmental question, more accurately some services doesn't need a high capacity of
this one. For that we introduce the idea of "Dynamic voltage and frequency scaling" which allow converting power in 
function of energy of CPU. 

## Build and run

Before running code you need to download all package needed :

    pip install matplotlib==3.5.3
    pip install pandas
    pip install numpy

Uncomment and run function from launcher.py : 

    python launcher.py

## Architecture

Tree of the most important files and folder in the project's repository hierarchy:

```
/
├─┬─resources/: To store all generated results.
│ ├──curves/: To store all curves.
│ ├──latex/: To store all latex content.
│ └──single/: To store all single results.
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

##  Contributors

- [Leo LE CORRE]
- [Youssef AIT EL MAHJOUB]

## Copyright

This code is open source. However, one can cite the original document submitted to ECMS 2023 : 
"STOCHASTIC MODELING AND OPTIMIZATION FOR POWER AND PERFORMANCE CONTROL IN DVFS SYSTEMS", 
Youssef AIT EL MAHJOUB, Leo LE CORRE and Hind CASTEL-TALEB.

