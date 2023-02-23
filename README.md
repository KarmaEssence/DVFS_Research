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
│ │ ├─┬─wsm/: Weighted sum method.
│ │ │ ├──exhaustive.py: Exhaustive search.
│ │ │ ├──greedy.py: Greedy search.
│ │ │ ├──local.py: Local search.
│ │ │ └──tabu.py: Tabu search. 
│ │ └─┬─pareto/: Pareto method.
│ │   └──kung.py: kung search.
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

Some features of this project uses content of other user and each one is sourced. 

