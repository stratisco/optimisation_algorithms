import random
import time
from copy import deepcopy
from context import *
from collections import defaultdict

# tasks = {
#     'T1': {'time': 4, 'difficulty': 3, 'deadline': 8, 'skill': 'A'},
#     'T2': {'time': 6, 'difficulty': 5, 'deadline': 12, 'skill': 'B'},
#     'T3': {'time': 2, 'difficulty': 2, 'deadline': 6, 'skill': 'A'},
#     'T4': {'time': 5, 'difficulty': 4, 'deadline': 10, 'skill': 'C'},
#     'T5': {'time': 3, 'difficulty': 1, 'deadline': 7, 'skill': 'A'},
#     'T6': {'time': 8, 'difficulty': 6, 'deadline': 15, 'skill': 'B'},
#     'T7': {'time': 4, 'difficulty': 3, 'deadline': 9, 'skill': 'C'},
#     'T8': {'time': 7, 'difficulty': 5, 'deadline': 14, 'skill': 'B'},
#     'T9': {'time': 2, 'difficulty': 2, 'deadline': 5, 'skill': 'A'},
#     'T10': {'time': 6, 'difficulty': 4, 'deadline': 11, 'skill': 'C'},
# }

# employees = {
#     'E1': {'available_hours': 10, 'skill_level': 4, 'skills': ['A', 'C']},
#     'E2': {'available_hours': 12, 'skill_level': 6, 'skills': ['A', 'B', 'C']},
#     'E3': {'available_hours': 8, 'skill_level': 3, 'skills': ['A']},
#     'E4': {'available_hours': 15, 'skill_level': 7, 'skills': ['B', 'C']},
#     'E5': {'available_hours': 9, 'skill_level': 5, 'skills': ['A', 'C']},
# }

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
            if PROJECTS_LIST[task].required_skill not in STAFF_LIST[staff].skills:
                skillMismatch += 1e6
            difficultyViolation += max(0, PROJECTS_LIST[task].difficulty - STAFF_LIST[staff].skill_level)
            hoursUsed[staff] += PROJECTS_LIST[task].estimated_time

        # Deadline violation
        assigned_to_staff = defaultdict(list)
        for task, staff in assignment.items():
            assigned_to_staff[staff].append(PROJECTS_LIST[task])

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
