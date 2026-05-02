# Optimisation Algorithms

## Installation and Execution
1. Clone the repository

```
git clone https://github.com/stratisco/optimisation_algorithms.git
```

2. Enter directory
```
cd optimisation_algorithms
```

3. Ensure pip packages `matplotlib` and and `numpy` are installed
```
pip install matplotlib
pip install numpy
```

4. Run the main script
```
python main.py
```

```
Usage: python main.py [args]
   -g    genetic algorithm
   -g q  genetic algorithm (no quick finish)
   -g+   genetic algorithm with graph output (slower)
   -p    particle swarm
   -p+   particle swarm with graph output (slower)
   -a    ant colony optimisation
   -t    test algorithms

eg: "python main.py -t"
```

<!--
## Contribution
Just submit a pull request. I'll add you as a collaborator once I know your account. *also try not to change other peoples algorithms*


> [!IMPORTANT]
> Make sure all algorithms run correctly before pushing any changes using `python main.py -t`
-->

## Common Commands
Run genetic algorithm
```
python main.py -g
```

Run particle swarm
```
python main.py -p
```

Run ant colony
```
python main.py -a
```

## Files
```
optimisation_algorithms
|
├── main.py                   -  main python script
├── context.py                -  context info for projects and staff
|
├── genetic.py                -  main genetic algorithm
├── chromosome.py             -  genetic algorithm chromosomes
├── genetic_optimisations.py  -  genetic parameter tuning
|
├── swarm.py                  -  main swarm algorithm
├── particle.py               -  swarm particles
├── particle_test.py          -  particle parameter tuning
|
├── ACO_ASS1.py               -  main ant colony script
|
└── README.md                 -  readme
```
