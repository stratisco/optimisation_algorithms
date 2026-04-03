import sys, time
from swarm import *
from genetic import genetic_algorithm

start = time.time()

if '-g' in sys.argv:
    print('Genetic Algorithm')

    print(genetic_algorithm(100, 100))

elif '-p' in sys.argv:
    print('Particle Swarm')

    print(optimiseParticleSwarm())

else:
    print('# No arguments given')
    print(f'Usage: python {sys.argv[0]} [args]')
    print('   -g   genetic algorithm (slow)')
    print('   -p   particle swarm')
    print()
    print('eg: "python main.py -g"')
    exit()

elapsed = time.time() - start

print(f'{elapsed:.2f} Seconds')