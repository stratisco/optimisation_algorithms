from context import *
from particle import *
from genetic import plot
import random, tracemalloc, time

def optimiseParticleSwarm(numParticles=100, graph=None, max_iterations=1000, w=.5, C1=2, C2=1.5):
    particles = []
    for i in range(numParticles):
        new_particle = Particle()
        particles.append(new_particle)

    globalBest = min(particles, key=lambda p: p.bestFitness)
    globalPos = [row[:] for row in globalBest.bestPosition]
    globalFitness = globalBest.bestFitness

    start_time = time.time()
    avg_fitnesses = []
    best_fitnesses = []
    memory_mb = []
    cumulative_times = []
    avg_vel = 1
    track_memory = (graph is not None and graph != '') or (memory_graph is not None and memory_graph != '')

    if track_memory:
        tracemalloc.start()

    for i in range(max_iterations):
        for particle in particles:
            new_vel = [[0] * nEMP for _ in range(nTasks)]
            new_pos = [[0] * nEMP for _ in range(nTasks)]

            for task_idx in range(nTasks):
                for emp_idx in range(nEMP):
                    r1 = random.random()
                    r2 = random.random()

                    # Vi+1 = w*Vi + C1*r1*(PB - Xi) + C2*r2*(GB - Xi)
                    v = (w * particle.velocity[task_idx][emp_idx]
                        + C1 * r1 * (particle.bestPosition[task_idx][emp_idx] - particle.position[task_idx][emp_idx])
                        + C2 * r2 * (globalPos[task_idx][emp_idx] - particle.position[task_idx][emp_idx]))

                    avg_vel = (avg_vel * (i * numParticles + particles.index(particle)) + abs(v)) / ((i * numParticles) + particles.index(particle) + 1)

                    # Xi+1 = Xi + Vi+1  (clamped to 0-1 for simplicity, as it's continuous)
                    x = particle.position[task_idx][emp_idx] + v
                    x = max(0.0, min(1.0, x))

                    new_vel[task_idx][emp_idx] = v
                    new_pos[task_idx][emp_idx] = x

            particle.velocity = new_vel
            particle.position = new_pos

            f = particle.fitness(.2, .2, .2, .2)

            if f < particle.bestFitness:
                particle.bestFitness = f
                particle.bestPosition = [row[:] for row in new_pos]

            if f < globalFitness:
                globalFitness = f
                globalPos = [row[:] for row in new_pos]
        
        cumulative_times.append(time.time() - start_time)

        if graph != None:
            fitness_values = [particle.fitness(.2, .2, .2, .2) for particle in particles]
            avg_fitnesses.append(sum(fitness_values) / len(fitness_values))
            best_fitnesses.append(min(fitness_values))

        if track_memory:
            _, peak = tracemalloc.get_traced_memory()
            memory_mb.append(peak / 1024 / 1024)

        if globalFitness == 0 and graph == None:
            break

    best_assignment = particle.decodeParticle(globalPos)

    print(avg_vel)

    if graph != None and graph != '':
        plot(
            graph,
            [
                [avg_fitnesses, 'avg fitness'],
                [best_fitnesses, 'best fitness']
            ],
            'Particle swarm optimization',
            'iteration',
            'fitness',
            f"(particles={numParticles}, iterations={len(avg_fitnesses)})"
        )

    if track_memory:
        tracemalloc.stop()

    if memory_graph != None and memory_graph != '':
        plot(
            memory_graph,
            [
                [memory_mb, 'peak memory (MB)']
            ],
            'Particle swarm memory usage',
            'iteration',
            'memory (MB)',
            f"(particles={numParticles}, iterations={len(memory_mb)})"
        )

        # Second graph for cumulative time
        plt.figure(figsize=(9, 5), dpi=400)
        plt.plot(cumulative_times, label="cumulative time")
        plt.title("Particle swarm optimization - Cumulative Time")
        plt.xlabel("iteration")
        plt.ylabel("time (s)")
        plt.legend()
        plt.figtext(0.01, 0.015, f"(particles={numParticles}, iterations={len(cumulative_times)})", fontsize=8, fontstyle="italic", color="dimgrey")
        time_graph = graph.replace('.png', '_pref.png')
        plt.savefig(time_graph)
        plt.close()

    return best_assignment, globalFitness

if __name__ == '__main__':
    startTime = time.time()
    print(optimiseParticleSwarm(100, "swarm_graph.png", 100))
    print(f"Execution Time: {time.time() - startTime:.4f} seconds")