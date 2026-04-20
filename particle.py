import random
import time
from copy import deepcopy
from context import *
from collections import defaultdict

taskKeys = list(task.id for task in PROJECTS_LIST)
EMPKeys  = list(employee.id for employee in STAFF_LIST)
nEMP     = len(EMPKeys)
nTasks   = len(taskKeys)

class Particle:
    def __init__(self):
        self.position = [[random.uniform(0, 1) for _ in range(nEMP)] for _ in range(nTasks)]
        self.velocity = [[random.uniform(-1, 1) for _ in range(nEMP)] for _ in range(nTasks)]
        self.bestPosition = [row[:] for row in self.position]
        self.bestFitness = self.fitness(.2, .2, .2, .2)

    def returnBinary(self, position):
        binary_position = []
        for task_values in position:
            max_index = task_values.index(max(task_values))
            binary_row = [0] * nEMP
            binary_row[max_index] = 1
            binary_position.append(binary_row)
        return binary_position
    
    def decodeParticle(self, position) -> dict[str, str]:
        assignment = {}
        for i in range(nTasks):
            task = taskKeys[i]
            task_values = position[i]
            # Select the employee with the highest value (argmax)
            emp_idx = task_values.index(max(task_values))
            assignment[task] = EMPKeys[emp_idx]
        return assignment
    
    def fitness(self, alfa, beta, delta, gamma):
        # α × (Overload Penalty) + β × (Skill Mismatch Penalty)
        # + δ × (Difficulty Violation Penalty) + γ × (Deadline Violation Penalty)
        # + σ × (Unique Assignment Violation Penalty)
        
        hoursUsed = {staff.id: 0 for staff in STAFF_LIST}
        overload = 0
        skillMismatch = 0
        difficultyViolation = 0
        deadlineViolation = 0

        assignment = self.decodeParticle(self.position)

        for task, staff in assignment.items():
            if PROJECTS_DICT[task].required_skill not in STAFF_DICT[staff].skills:
                skillMismatch += 3
            difficultyViolation += max(0, PROJECTS_DICT[task].difficulty - STAFF_DICT[staff].skill_level)
            hoursUsed[staff] += PROJECTS_DICT[task].estimated_time

        # Deadline violation
        assigned_to_staff = defaultdict(list)
        for task, staff in assignment.items():
            assigned_to_staff[staff].append(PROJECTS_DICT[task])

        for emp_id, projects in assigned_to_staff.items():
            sorted_projects = sorted(projects, key=lambda p: p.estimated_time)
            current_time = 0
            for proj in sorted_projects:
                current_time += proj.estimated_time
                deadlineViolation += max(0, current_time - proj.deadline)

        for staff in STAFF_LIST:
            overload += max(0, hoursUsed[staff.id] - staff.available_hours)

        return alfa * overload + beta * skillMismatch + delta * difficultyViolation + gamma * deadlineViolation
    
    def __str__(self):
        return("hi")    
