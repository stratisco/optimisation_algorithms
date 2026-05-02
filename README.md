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
