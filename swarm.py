from context import *
from particle import *
from genetic import plot
import random, tracemalloc, time

def optimiseParticleSwarm(numParticles=100, max_iterations=500, cost_graph=None, memory_graph=None, time_graph=None, w=.7, C1=2, C2=1.2):
    particles = []
    for i in range(numParticles):
        new_particle = Particle()
        particles.append(new_particle)

    # Initialize the swarm's global best using the best of the randomly created particles.
    globalBest = min(particles, key=lambda p: p.bestFitness)
    globalPos = [row[:] for row in globalBest.bestPosition]
    globalFitness = globalBest.bestFitness

    start_time = time.time()
    avg_fitnesses = []
    best_fitnesses = []
    memory_mb = []
    cumulative_times = []
    avg_vel = 1

    # Start memory tracing only when memory graph output is requested.
    if memory_graph is not None and memory_graph != '':
        tracemalloc.start()

    # Main PSO iteration loop over the requested number of iterations.
    for i in range(max_iterations):
        #checks every particle in the swarm and updates its velocity and position based on its own best position and the global best position.
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

            # Evaluate particle fitness after updating position.
            f = particle.fitness(.2, .2, .2, .2)

            #update personal best if current fitness is better
            if f < particle.bestFitness:
                particle.bestFitness = f
                particle.bestPosition = [row[:] for row in new_pos]

            #update global best if current fitness is better
            if f < globalFitness:
                globalFitness = f
                globalPos = [row[:] for row in new_pos]
        
        # Log cumulative runtime for each iteration, if requested.
        if time_graph is not None and time_graph != '':
            cumulative_times.append(time.time() - start_time)

        # If cost graph output is enabled, record average and best fitness for this iteration.
        if cost_graph is not None and cost_graph != '':
            fitness_values = [particle.fitness(.2, .2, .2, .2) for particle in particles]
            avg_fitnesses.append(sum(fitness_values) / len(fitness_values))
            best_fitnesses.append(min(fitness_values))

        # If memory graph output is enabled, record the current peak memory usage.
        if memory_graph is not None and memory_graph != '':
            _, peak = tracemalloc.get_traced_memory()
            memory_mb.append(peak / 1024 / 1024)

        if globalFitness == 0 and not cost_graph and not memory_graph and not time_graph:
            break

    best_assignment = particle.decodeParticle(globalPos)

    print(avg_vel)

    if cost_graph is not None and cost_graph != '':
        # Plot fitness history when cost graph output is requested.
        plot(
            cost_graph,
            [
                [avg_fitnesses, 'avg fitness'],
                [best_fitnesses, 'best fitness']
            ],
            'Particle Swarm Optimization Fitness',
            'Iteration',
            'Fitness',
            f"(particles={numParticles}, iterations={len(avg_fitnesses)})"
        )

    if memory_graph is not None and memory_graph != '':
        # Plot peak memory usage recorded during the run.
        plot(
            memory_graph,
            [
                [memory_mb, 'peak memory (MB)']
            ],
            'Particle Swarm Memory Usage',
            'Iteration',
            'Memory (MB)',
            f"(particles={numParticles}, iterations={len(memory_mb)})"
        )

    if time_graph is not None and time_graph != '':
        # Plot cumulative runtime per iteration when time graph output is requested.
        plot(
            time_graph,
            [
                [cumulative_times, 'cumulative time']
            ],
            'Particle Swarm Optimization Cumulative Time Usage',
            'Iteration',
            'Time (s)',
            f"(particles={numParticles}, iterations={len(cumulative_times)})"
        )

    # Stop memory tracing if it was started for graphing.
    if memory_graph is not None and memory_graph != '':
        tracemalloc.stop()

    # Return the decoded best assignment and the corresponding fitness.
    return best_assignment, globalFitness

if __name__ == '__main__':
    startTime = time.time()
    print(optimiseParticleSwarm(
        100, 500,
        # cost_graph='swarm_cost.png',
        # memory_graph='swarm_memory.png',
        # time_graph='swarm_time.png',
    ))
    print(f"Execution Time: {time.time() - startTime:.4f} seconds")