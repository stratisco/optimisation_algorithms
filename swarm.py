from context import *
from particle import *
import random, matplotlib.pyplot as plt
import time

def optimiseParticleSwarm(numParticles=100, graph=None, max_iterations=1000, w=.1, C1=2, C2=1.3):
    particles = []
    for i in range(numParticles):
        new_particle = Particle()
        particles.append(new_particle)

    globalBest = min(particles, key=lambda p: p.bestFitness)
    globalPos = [row[:] for row in globalBest.bestPosition]
    globalFitness = globalBest.bestFitness

    avg_fitnesses = []
    best_fitnesses = []

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
        
        if graph != None:
            fitness_values = [particle.fitness(.2, .2, .2, .2) for particle in particles]
            avg_fitnesses.append(sum(fitness_values) / len(fitness_values))
            best_fitnesses.append(min(fitness_values))

        if globalFitness == 0 and graph == None:
            break

    best_assignment = particle.decodeParticle(globalPos)

    if graph != None and graph != '':
        plt.figure(figsize=(9, 5), dpi=400)
        plt.plot(avg_fitnesses, label="avg fitness")
        plt.plot(best_fitnesses, label="best fitness")
        plt.title("Particle swarm optimization")
        plt.xlabel("iteration")
        plt.ylabel("fitness")
        plt.legend()
        plt.figtext(0.01, 0.015, f"(particles={numParticles}, iterations={len(avg_fitnesses)})", fontsize=8, fontstyle="italic", color="dimgrey")
        plt.savefig(graph)
        plt.close()

    return best_assignment, globalFitness

if __name__ == '__main__':
    startTime = time.time()
    print(optimiseParticleSwarm(100, "swarm_graph.png", 100))
    print(f"Execution Time: {time.time() - startTime:.4f} seconds")