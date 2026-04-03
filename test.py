from swarm import *
import time

def test_parameters(num_runs=50, numParticles=50, max_iterations=100):
    w_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    c1_values = [1.0, 1.5, 2.0, 2.5, 3.0]
    c2_values = [1.0, 1.5, 2.0, 2.5, 3.0]
    
    results = []
    
    for w in w_values:
        for c1 in c1_values:
            for c2 in c2_values:
                best_fitnesses = []
                for _ in range(num_runs):
                    _, fitness = optimiseParticleSwarm(numParticles=numParticles, max_iterations=max_iterations, w=w, C1=c1, C2=c2)
                    best_fitnesses.append(fitness)
                avg_fitness = sum(best_fitnesses) / len(best_fitnesses)
                print(f"w={w}, c1={c1}, c2={c2}: avg fitness = {avg_fitness:.4f}")
                results.append((w, c1, c2, avg_fitness))
    
    return results

if __name__ == '__main__':
    start_time = time.time()
    test_parameters()
    print(f"Total execution time: {time.time() - start_time:.2f} seconds")

# tldr high c1 and low c2, w seems agnostic in the range

# w=0.1, c1=1.0, c2=1.0: avg fitness = 0.3400
# w=0.1, c1=1.0, c2=1.5: avg fitness = 8000.4680
# w=0.1, c1=1.0, c2=2.0: avg fitness = 4000.2200
# w=0.1, c1=1.0, c2=2.5: avg fitness = 4000.3400
# w=0.1, c1=1.0, c2=3.0: avg fitness = 12000.2080
# w=0.1, c1=1.5, c2=1.0: avg fitness = 0.1920
# w=0.1, c1=1.5, c2=1.5: avg fitness = 0.2720
# w=0.1, c1=1.5, c2=2.0: avg fitness = 0.1920
# w=0.1, c1=1.5, c2=2.5: avg fitness = 0.1080
# w=0.1, c1=1.5, c2=3.0: avg fitness = 12000.1920
# w=0.1, c1=2.0, c2=1.0: avg fitness = 0.0880
# w=0.1, c1=2.0, c2=1.5: avg fitness = 0.1280
# w=0.1, c1=2.0, c2=2.0: avg fitness = 0.0680
# w=0.1, c1=2.0, c2=2.5: avg fitness = 0.0840
# w=0.1, c1=2.0, c2=3.0: avg fitness = 0.1200
# w=0.1, c1=2.5, c2=1.0: avg fitness = 0.0520
# w=0.1, c1=2.5, c2=1.5: avg fitness = 0.0480
# w=0.1, c1=2.5, c2=2.0: avg fitness = 0.0400
# w=0.1, c1=2.5, c2=2.5: avg fitness = 0.0600
# w=0.1, c1=2.5, c2=3.0: avg fitness = 0.1040
# w=0.1, c1=3.0, c2=1.0: avg fitness = 0.0040
# w=0.1, c1=3.0, c2=1.5: avg fitness = 0.0160
# w=0.1, c1=3.0, c2=2.0: avg fitness = 0.0600
# w=0.1, c1=3.0, c2=2.5: avg fitness = 0.0720
# w=0.1, c1=3.0, c2=3.0: avg fitness = 0.1080
# w=0.3, c1=1.0, c2=1.0: avg fitness = 0.3880
# w=0.3, c1=1.0, c2=1.5: avg fitness = 0.3880
# w=0.3, c1=1.0, c2=2.0: avg fitness = 4000.6560
# w=0.3, c1=1.0, c2=2.5: avg fitness = 0.2800
# w=0.3, c1=1.0, c2=3.0: avg fitness = 8000.3800
# w=0.3, c1=1.5, c2=1.0: avg fitness = 0.1880
# w=0.3, c1=1.5, c2=1.5: avg fitness = 0.1440
# w=0.3, c1=1.5, c2=2.0: avg fitness = 8000.2960
# w=0.3, c1=1.5, c2=2.5: avg fitness = 8000.2280
# w=0.3, c1=1.5, c2=3.0: avg fitness = 0.2080
# w=0.3, c1=2.0, c2=1.0: avg fitness = 0.1280
# w=0.3, c1=2.0, c2=1.5: avg fitness = 0.1280
# w=0.3, c1=2.0, c2=2.0: avg fitness = 0.1040
# w=0.3, c1=2.0, c2=2.5: avg fitness = 0.1080
# w=0.3, c1=2.0, c2=3.0: avg fitness = 0.1960
# w=0.3, c1=2.5, c2=1.0: avg fitness = 0.0520
# w=0.3, c1=2.5, c2=1.5: avg fitness = 0.0760
# w=0.3, c1=2.5, c2=2.0: avg fitness = 0.0360
# w=0.3, c1=2.5, c2=2.5: avg fitness = 0.0880
# w=0.3, c1=2.5, c2=3.0: avg fitness = 0.1520
# w=0.3, c1=3.0, c2=1.0: avg fitness = 0.0080
# w=0.3, c1=3.0, c2=1.5: avg fitness = 0.0360
# w=0.3, c1=3.0, c2=2.0: avg fitness = 0.0640
# w=0.3, c1=3.0, c2=2.5: avg fitness = 0.0960
# w=0.3, c1=3.0, c2=3.0: avg fitness = 0.1440
# w=0.5, c1=1.0, c2=1.0: avg fitness = 0.3000
# w=0.5, c1=1.0, c2=1.5: avg fitness = 0.3800
# w=0.5, c1=1.0, c2=2.0: avg fitness = 12000.3120
# w=0.5, c1=1.0, c2=2.5: avg fitness = 0.2720
# w=0.5, c1=1.0, c2=3.0: avg fitness = 8000.3200
# w=0.5, c1=1.5, c2=1.0: avg fitness = 0.1480
# w=0.5, c1=1.5, c2=1.5: avg fitness = 0.1760
# w=0.5, c1=1.5, c2=2.0: avg fitness = 0.2360
# w=0.5, c1=1.5, c2=2.5: avg fitness = 0.1640
# w=0.5, c1=1.5, c2=3.0: avg fitness = 0.2520
# w=0.5, c1=2.0, c2=1.0: avg fitness = 0.0720
# w=0.5, c1=2.0, c2=1.5: avg fitness = 0.1000
# w=0.5, c1=2.0, c2=2.0: avg fitness = 0.1520
# w=0.5, c1=2.0, c2=2.5: avg fitness = 0.1320
# w=0.5, c1=2.0, c2=3.0: avg fitness = 0.1320
# w=0.5, c1=2.5, c2=1.0: avg fitness = 0.0360
# w=0.5, c1=2.5, c2=1.5: avg fitness = 0.0840
# w=0.5, c1=2.5, c2=2.0: avg fitness = 0.0880
# w=0.5, c1=2.5, c2=2.5: avg fitness = 0.0960
# w=0.5, c1=2.5, c2=3.0: avg fitness = 0.1200
# w=0.5, c1=3.0, c2=1.0: avg fitness = 0.0200
# w=0.5, c1=3.0, c2=1.5: avg fitness = 0.0280
# w=0.5, c1=3.0, c2=2.0: avg fitness = 0.0360
# w=0.5, c1=3.0, c2=2.5: avg fitness = 0.0520
# w=0.5, c1=3.0, c2=3.0: avg fitness = 0.1120
# w=0.7, c1=1.0, c2=1.0: avg fitness = 8000.1800
# w=0.7, c1=1.0, c2=1.5: avg fitness = 0.3280
# w=0.7, c1=1.0, c2=2.0: avg fitness = 0.2280
# w=0.7, c1=1.0, c2=2.5: avg fitness = 4000.2520
# w=0.7, c1=1.0, c2=3.0: avg fitness = 4000.3640
# w=0.7, c1=1.5, c2=1.0: avg fitness = 0.1040
# w=0.7, c1=1.5, c2=1.5: avg fitness = 0.1520
# w=0.7, c1=1.5, c2=2.0: avg fitness = 0.2160
# w=0.7, c1=1.5, c2=2.5: avg fitness = 8000.2680
# w=0.7, c1=1.5, c2=3.0: avg fitness = 0.3240
# w=0.7, c1=2.0, c2=1.0: avg fitness = 0.0600
# w=0.7, c1=2.0, c2=1.5: avg fitness = 0.0760
# w=0.7, c1=2.0, c2=2.0: avg fitness = 0.1040
# w=0.7, c1=2.0, c2=2.5: avg fitness = 0.2040
# w=0.7, c1=2.0, c2=3.0: avg fitness = 0.1720
# w=0.7, c1=2.5, c2=1.0: avg fitness = 0.0240
# w=0.7, c1=2.5, c2=1.5: avg fitness = 0.0280
# w=0.7, c1=2.5, c2=2.0: avg fitness = 0.0800
# w=0.7, c1=2.5, c2=2.5: avg fitness = 4000.1200
# w=0.7, c1=2.5, c2=3.0: avg fitness = 4000.1480
# w=0.7, c1=3.0, c2=1.0: avg fitness = 0.0120
# w=0.7, c1=3.0, c2=1.5: avg fitness = 0.0320
# w=0.7, c1=3.0, c2=2.0: avg fitness = 0.1120
# w=0.7, c1=3.0, c2=2.5: avg fitness = 0.0960
# w=0.7, c1=3.0, c2=3.0: avg fitness = 0.1720
# w=0.9, c1=1.0, c2=1.0: avg fitness = 0.1440
# w=0.9, c1=1.0, c2=1.5: avg fitness = 0.3000
# w=0.9, c1=1.0, c2=2.0: avg fitness = 0.3240
# w=0.9, c1=1.0, c2=2.5: avg fitness = 0.3960
# w=0.9, c1=1.0, c2=3.0: avg fitness = 0.4440
# w=0.9, c1=1.5, c2=1.0: avg fitness = 0.1040
# w=0.9, c1=1.5, c2=1.5: avg fitness = 0.0720
# w=0.9, c1=1.5, c2=2.0: avg fitness = 0.2600
# w=0.9, c1=1.5, c2=2.5: avg fitness = 0.2880
# w=0.9, c1=1.5, c2=3.0: avg fitness = 0.2800
# w=0.9, c1=2.0, c2=1.0: avg fitness = 0.0360
# w=0.9, c1=2.0, c2=1.5: avg fitness = 0.0960
# w=0.9, c1=2.0, c2=2.0: avg fitness = 0.1200
# w=0.9, c1=2.0, c2=2.5: avg fitness = 0.1840
# w=0.9, c1=2.0, c2=3.0: avg fitness = 0.2200
# w=0.9, c1=2.5, c2=1.0: avg fitness = 0.0280
# w=0.9, c1=2.5, c2=1.5: avg fitness = 0.0440
# w=0.9, c1=2.5, c2=2.0: avg fitness = 0.1400
# w=0.9, c1=2.5, c2=2.5: avg fitness = 0.1880
# w=0.9, c1=2.5, c2=3.0: avg fitness = 0.2240
# w=0.9, c1=3.0, c2=1.0: avg fitness = 0.0160
# w=0.9, c1=3.0, c2=1.5: avg fitness = 0.0680
# w=0.9, c1=3.0, c2=2.0: avg fitness = 0.0800
# w=0.9, c1=3.0, c2=2.5: avg fitness = 0.2040
# w=0.9, c1=3.0, c2=3.0: avg fitness = 0.2400
# Total execution time: 732.61 seconds