import sys, time
from swarm import *
from genetic import genetic_algorithm

start = time.time()

if '-g' in sys.argv:
    print('Genetic Algorithm')
    print(genetic_algorithm(500, 500))

elif '-g+' in sys.argv:
    print('Genetic Algorithm with graph')
    print(genetic_algorithm(500, 500, graph='genetic_graph.png'))
    print("graph is located at 'genetic_graph.png'")

elif '-p' in sys.argv:
    print('Particle Swarm')
    print(optimiseParticleSwarm())

elif '-a' in sys.argv:
    print('Ant colony optimisation')
    import ACO_ASS1

elif '-t' in sys.argv:
    print('Testing')
    print(f'   genetic-algorithm   {genetic_algorithm(500, 500, graph='genetic_graph.png').getCost()}')
    print(f'   particle-swarm      {optimiseParticleSwarm()[1]}')
    print(f'   ant-colony         :')
    import ACO_ASS1
    print()
    print('No Runtime Errors')
    print()


else:
    print('# No valid arguments given')
    print(f'Usage: python {sys.argv[0]} [args]')
    print('   -g   genetic algorithm')
    print('   -g+  genetic algorithm with graph output (slower)')
    print('   -p   particle swarm')
    print('   -a   ant colony optimisation')
    print()
    print('   -t   test algorithms')
    print()
    print('eg: "python main.py -t"')
    exit()

elapsed = time.time() - start

print(f'{elapsed:.2f} Seconds')