Hierarchical Consensus Value Aggregation for Value-Aligned Multi-Agent Systems
===================
This Repository contains all code and experiment data for the paper "Hierarchical Consensus Value Aggregation for Value-Aligned Multi-Agent Systems" by Joseph Trevorrow and Nirav Ajmeri. 

This work took inspiration from the paper "Aggregating Value Systems for Decision Support" by Roger X. Lera-Leri, Enrico Liscio, Filippo Bistaffa, Catholijn M. Jonker, Maite Lopez-Sanchez, Pradeep K. Murukannaiah, Juan A. Rodríguez-Aguilar, and Francisco Salas-Molina in Knowledge-Based Systems, 2024. As such, some code here is taken from their original repository.

As part of our experiments we use code from the paper "A general approach for computing a consensus in group decision making that integrates multiple ethical principles" by Francisco Salas-Molina, Filippo Bistaffa and Juan A. Rodríguez-Aguilar that is used to create a baseline method.

We additionally have included a subset of the European Social Study (ESS) round 8 data for our single example, and include a file to process this into a value system, as well as our own data analysis.

Dependencies
----------
 - [Python 3](https://www.python.org/downloads/)
 - [Julia](https://julialang.org/downloads/) and [PyJulia](https://pyjulia.readthedocs.io/en/latest/installation.html)
 - [Pandas](https://pandas.pydata.org/)
 - [Csv library](https://docs.python.org/3/library/csv.html)
 - [Numpy](https://numpy.org/)
 - [CVXPY](https://www.cvxpy.org/)
 - [ECOS](https://web.stanford.edu/~boyd/papers/ecos.html) (Embedded within CVXPY)

Dataset
----------
All experiments consider the [European Social Study Round 8](https://ess.sikt.no/en/datafile/ffc43f48-e15a-4a1c-8813-47eda377c355) 

Execution
----------
This code is tested using Python version 3.11.9, on both Mac and Linux.

To use with conda:
`conda create -n hcva python=3.11.9`
`conda activate hcva`
`python -m pip install -r requirements.txt`

> CVXPY is required, in requirements.txt we install two solvers `[ECOS, GUROBI]`.

Our approach must be executed by means of the [`solve.py`](solve.py) Python script, i.e.,
```
usage: solve.py [-h] [-p P] [-e E] [-f F] [-w W] [-i I] [-o O] [-v] [-l] [-t]
                [-g G]

optional arguments:
  -h, --help  show this help message and exit
  -p P        p-norm (default: 2)
  -e E        epsilon used to compute limit p (default: 1e-4)
  -f F        CSV file with data (default: 'data.csv')
  -w W        weighting countries: 0 for unweighted problem, 1 for considering people that participated in the study and 2 for country population (default: 0)
  -i I        computes equivalent p given an input consensus
  -o O        write consensus to file
  -v          computes the preference aggregation
  -l          compute the limit p
  -t          compute the threshold p
  -g G        store results in csv
  -pf PF      CSV file with principle data (default: None)
  -pv         Compute HCVA
  -smlf       CSV file with data for Salas-Molina method
  -sml        Compute consensuses using Salas-Molina method
```

Acknowledgements
----------
This repository contains the [implementation of the pIRLS algorithm](https://github.com/fast-algos/pIRLS) ([article](https://papers.nips.cc/paper/2019/hash/46c7cb50b373877fb2f8d5c4517bb969-Abstract.html)). This article should also be cited when citing our work.

Running the code
----------
- Install requirements: `pip install -r requirements.txt`
- To run locally with PyJulia compatability issues
  - Run `python-jl -m pip install IPython` to install IPython in Julia
  - Run your command as usual using `python-jl -m IPython` instead of `python`
