import sys, time
from swarm import *
from genetic import genetic_algorithm

start = time.time()

if '-g' in sys.argv:
    quickFinish = 'q' not in sys.argv
    print('Genetic Algorithm')
    if not quickFinish:
        print('*quick finish is off')
    print(genetic_algorithm(500, 500, quickFinish=quickFinish, verbose=True))

elif '-g+' in sys.argv:
    quickFinish = 'q' not in sys.argv
    print('Genetic Algorithm with graph')
    if not quickFinish:
        print('*quick finish is off')
    print(genetic_algorithm(500, 500, graph='genetic_graph.png', quickFinish=quickFinish, verbose=True))
    print("graph is located at 'genetic_graph.png'")

elif '-p' in sys.argv:
    print('Particle Swarm')
    print(optimiseParticleSwarm(100, None, 1000))

elif '-p+' in sys.argv:
    print('Particle Swarm with graph')
    print(optimiseParticleSwarm(100, "swarm_graph.png", 100))
    print("graph is located at 'swarm_graph.png'")

elif '-a' in sys.argv:
    print('Ant colony optimisation')
    import ACO_ASS1

elif '-t' in sys.argv:
    print('Testing')
    print(f'   genetic-algorithm   {genetic_algorithm(500, 500, graph="genetic_graph.png").getCost()}')
    print(f'   particle-swarm      {optimiseParticleSwarm(1000, "swarm_graph.png", 300)[1]}')
    print(f'   ant-colony         :')
    import ACO_ASS1
    print()
    print('No Runtime Errors')
    print()


else:
    print('# No valid arguments given')
    print(f'Usage: python {sys.argv[0]} [args]')
    print('   -g    genetic algorithm')
    print('   -g q  genetic algorithm (no quick finish)')
    print('   -g+   genetic algorithm with graph output (slower)')
    print('   -p    particle swarm')
    print('   -p+   particle swarm with graph output (slower)    ')
    print('   -a    ant colony optimisation')
    print('   -t    test algorithms')
    print()
    print('eg: "python main.py -t"')
    exit()

elapsed = time.time() - start

print(f'{elapsed:.2f} Seconds')