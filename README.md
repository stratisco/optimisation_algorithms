## Installing and Execution
1. Clone the repository

```
git clone https://github.com/stratisco/optimisation_algorithms.git
```

2. Run the main script

```
python main.py [args]
```

```
Usage: "python main.py [args]"
   -g   genetic algorithm
   -g+  genetic algorithm with graph output (slower)
   -p   particle swarm
   -p+  particle swarm with graph output (slower)    
   -a   ant colony optimisation
   -t   test algorithms

eg: "python main.py -t"
```

## Contribution
Just submit a pull request. I'll add you as a collaborator once I know your account. *also try not to change other peoples algorithms*


> [!IMPORTANT]
> Make sure all algorithms run correctly before pushing any changes using `python main.py -t`

## Repository contents
* `main.py` - main script to run all programs
* `context.py` - context for situation (staff/project info)

*genetic algorithm*
* `genetic.py` - main genetic algorithm script
* `chromosome.py` - chromosome/vector script
* `genetic_optimisations.py` - for optimising genetic algorithm parameters

*particle swarm*
* `particle.py` - 
* `swarm.py` -
* `particle_test` -

*ant colony optimisation*
* `ACO_ASS1.py` -


<!--
## Vector representation *(for genetic algorithm)*:

uses a 3d vector of bits such that `vector[projectId][staffId]` equals `1` if the staff member is assigned to the project and `0` if not

```
# example with 4 projects and 5 staff members

vector = [
    [0, 1, 0, 0, 0],   # Project 1 -> Staff 2
    [0, 1, 0, 1, 0],   # Project 2 -> Staff 2, Staff 4 (over assigned)
    [1, 0, 0, 0, 0],   # Project 3 -> Staff 1
    [0, 0, 0, 0, 0],   # Project 4 -> (under assigned)
]
```
-->
