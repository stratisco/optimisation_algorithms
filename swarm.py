from context import *
from particle import *
import random
import time

def optimiseParticleSwarm(numParticles=200, max_iterations=1000, w=.5, C1=2, C2=2):
    particles = []
    for i in range(numParticles):
        new_particle = Particle()
        particles.append(new_particle)

    globalBest = min(particles, key=lambda p: p.bestFitness)
    globalPos = [row[:] for row in globalBest.bestPosition]
    globalFitness = globalBest.bestFitness

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

        if globalFitness == 0:
            break

    best_assignment = particle.decodeParticle(globalPos)
    # print("Best Assignment:", best_assignment)
    # print(f"Best Fitness:    {globalFitness:.4f}")
    return best_assignment, globalFitness

startTime = time.time()
print(optimiseParticleSwarm())
print(f"Execution Time: {time.time() - startTime:.4f} seconds")