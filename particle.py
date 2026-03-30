import random
import time
from copy import deepcopy
import context

tasks = {
    f'T{p.id}': {'time': p.estimated_time, 'difficulty': p.difficulty, 'deadline': p.deadline, 'skill': p.required_skill}
    for p in context.PROJECTS_LIST
}

employees = {
    f'E{s.id}': {'available_hours': s.available_hours, 'skill_level': s.skill_level, 'skills': s.skills}
    for s in context.STAFF_LIST
}

taskKeys = list(tasks.keys())
EMPKeys  = list(employees.keys())
nEMP     = len(EMPKeys)
nTasks   = len(taskKeys)

def decodeParticle(position: list[float]) -> dict[str, str]:
    assignment = {}
    for i in range(nTasks):
        task = taskKeys[i]
        start_idx = i * nEMP
        end_idx = start_idx + nEMP
        task_values = position[start_idx:end_idx]
        # Select the employee with the highest value (argmax)
        emp_idx = task_values.index(max(task_values))
        assignment[task] = EMPKeys[emp_idx]
    return assignment

# Particle Swarm Optimization

def particleSwarm(tasks, employees, num_particles=200, max_iterations=1200, w=0.5, C1=2, C2=2):
    # Initialize particles
    particles = []
    for i in range(num_particles):
        position = [random.uniform(0, 1) for _ in range(nTasks * nEMP)]  # Continuous values for each task-employee pair
        velocity = [random.uniform(-1, 1) for _ in range(nTasks * nEMP)]
        f = fitness(decodeParticle(position), 1, 1, 1, 1)
        particle = {
            'position': position,
            'velocity': velocity,
            'best_position': position[:],
            'best_fitness': f,
        }
        particles.append(particle)

    globalBest = min(particles, key=lambda p: p['best_fitness'])
    globalPos = globalBest['best_position'][:]
    globalFitness = globalBest['best_fitness']

    for i in range(max_iterations):
        for particle in particles:

            new_vel = []
            new_pos = []

            for d in range(nTasks * nEMP):
                r1 = random.random()
                r2 = random.random()

                # Vi+1 = w*Vi + C1*r1*(PB - Xi) + C2*r2*(GB - Xi)
                v = (w  * particle['velocity'][d]
                     + C1 * r1 * (particle['best_position'][d] - particle['position'][d])
                     + C2 * r2 * (globalPos[d] - particle['position'][d]))
 
                # Xi+1 = Xi + Vi+1  (clamped to 0-1 for simplicity, as it's continuous)
                x = particle['position'][d] + v
                x = max(0.0, min(1.0, x))
 
                new_vel.append(v)
                new_pos.append(x)
 
            particle['velocity'] = new_vel
            particle['position'] = new_pos

            f = fitness(decodeParticle(new_pos), 1, 1, 1, 1)

            if f < particle['best_fitness']:
                particle['best_fitness'] = f
                particle['best_position'] = new_pos[:]

            if f < globalFitness:
                globalFitness = f
                globalPos = new_pos[:]

        if globalFitness == 0:
            break

    best_assignment = decodeParticle(globalPos)
    # print("Best Assignment:", best_assignment)
    # print(f"Best Fitness:    {globalFitness:.4f}")
    return best_assignment, globalFitness

def fitness(particle, alfa, beta, delta, gamma):
    # α × (Overload Penalty) + β × (Skill Mismatch Penalty)
    # + δ × (Difficulty Violation Penalty) + γ × (Deadline Violation Penalty)
    # + σ × (Unique Assignment Violation Penalty)
    hoursUsed = {e: 0 for e in employees}
    overload = 0
    skillMismatch = 0
    difficultyViolation = 0
    deadlineViolation = 0

    for task, employee in particle.items():   # ← iterate assignment directly
        if tasks[task]['skill'] not in employees[employee]['skills']:
            skillMismatch += 1e6
        difficultyViolation += max(0, tasks[task]['difficulty'] - employees[employee]['skill_level'])
        hoursUsed[employee] += tasks[task]['time']

    for emp in employees:
        overload += max(0, hoursUsed[emp] - employees[emp]['available_hours'])

    return alfa * overload + beta * skillMismatch + delta * difficultyViolation + gamma * deadlineViolation

startTime = time.time()         
print(particleSwarm(tasks, employees))
print(f"Execution Time: {time.time() - startTime:.4f} seconds")
