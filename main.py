import sys, time
from genetic import genetic_algorithm
from particle import particleSwarm

start = time.time()

if '-g' in sys.argv:
    print('Genetic Algorithm')

    print(genetic_algorithm(100, 100))

# elif '-p' in sys.argv:
#     print('Particle Swarm')

#     print(particleSwarm(None, None)
# )

else:
    print('# No arguments given')
    print(f'Usage: python {sys.argv[0]} [args]')
    print('   -g   genetic algorithm')
    print('   -p   particle swarm')
    print()
    print('eg: "python main.py -g"')
    exit()

elapsed = time.time() - start

print(f'{elapsed:.2f} Seconds')