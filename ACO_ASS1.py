#assignment 1: Ant Colony Optimization for task based heuristic stuff

#===============================Task Data=========================

#Task ID Estimated Time (hrs) Difficulty Deadline (hrs from now) Required Skill
#T1------- 4 -------------------- 3 ------ 8 ------------------------- A
#T2------- 6 -------------------- 5 ------ 12 ------------------------- B
#T3------- 2 -------------------- 2 ------ 6 ------------------------- A
#T4------- 5 -------------------- 4 ------ 10 ------------------------- C
#T5------- 3 -------------------- 1 ------ 7 ------------------------- A
#T6------- 8 -------------------- 6 ------ 15 ------------------------- B
#T7------- 4 -------------------- 3 ------ 9 ------------------------- C
#T8------- 7 -------------------- 5 ------ 14 ------------------------- B
#T9------- 2 -------------------- 2 ------ 5 ------------------------- A
#T10------ 6 -------------------- 4 ------ 11 ------------------------- C


#============================Employee Data===========================
#Employee ID Available Hours Skill Level Skills
#E1 ---------------- 10 -------- 4 ----- A, C
#E2 ---------------- 12 -------- 6 ----- A, B, C
#E3 ---------------- 8 --------- 3 ----- A
#E4 ---------------- 15 -------- 7 ----- B, C
#E5 ---------------- 9 --------- 5 ----- A, C

#============================ACO Parameters===========================
#N_ANTS = 10
#N_ITERATIONS = 100
#ALPHA = 1.0
#BETA = 2.0
#RHO = 0.5
#Q = 10.0
#TAU_INIT = 1.0
# PROGRAM PARTS TO GET DONE; DATA,  PENALTIES WEIGHTS, ACO PARAMTERS, HEURISTIC VALUE TINGS, PENALTIES
#TASK CALCS, SOLUTION CALCS,COST FUNCTION, ACO ALGORITHM,PHEROMONE UPDATE, MAIN FUNCTION WITH DATA PRINT OUT

import random
import time
import numpy as np
import tracemalloc
import math
import matplotlib.pyplot as plt #ADDED BECAUSE I MIS READ, IT NEEDS GRAPHS NOT tABLESSESESESESSESE



#======================================================================================================================
#                                               DATA
#======================================================================================================================
TASKS = {
    "T1": {"estimated_time": 4, "difficulty": 3, "deadline": 8, "required_skill": "A"},
    "T2": {"estimated_time": 6, "difficulty": 5, "deadline": 12, "required_skill": "B"},
    "T3": {"estimated_time": 2, "difficulty": 2, "deadline": 6, "required_skill": "A"},
    "T4": {"estimated_time": 5, "difficulty": 4, "deadline": 10, "required_skill": "C"},
    "T5": {"estimated_time": 3, "difficulty": 1, "deadline": 7, "required_skill": "A"},
    "T6": {"estimated_time": 8, "difficulty": 6, "deadline": 15, "required_skill": "B"},
    "T7": {"estimated_time": 4, "difficulty": 3, "deadline": 9, "required_skill": "C"},
    "T8": {"estimated_time": 7, "difficulty": 5, "deadline": 14, "required_skill": "B"},
    "T9": {"estimated_time": 2, "difficulty": 2, "deadline": 5, "required_skill": "A"},
    "T10": {"estimated_time": 6, "difficulty": 4, "deadline": 11, "required_skill": "C"}
}

EMPLOYEES = {
    "E1": {"available_hours": 10, "skill_level": 4, "skills": ["A", "C"]},
    "E2": {"available_hours": 12, "skill_level": 6, "skills": ["A", "B", "C"]},
    "E3": {"available_hours": 8, "skill_level": 3, "skills": ["A"]},
    "E4": {"available_hours": 15, "skill_level": 7, "skills": ["B", "C"]},
    "E5": {"available_hours": 9, "skill_level": 5, "skills": ["A", "C"]}
}

#=============================PENALTY WEIGHTS==================================
#all 0.2 as per rubric sheet
w_oload = 0.20 #OVERLOAD
w_stype = 0.20 #MISMATCH SKILL
w_difficulty = 0.20 #DIFFICULTY MULTIPLIER
w_otime = 0.20 #DEADLINE VIOLATION
w_unique = 0.20 #UNIQUE ASSIGNMENT WEIGHT

#=============================PARAMETERS FOR ANT COLONY OPTIMIZATION STUFF AND THINGS===========================
N_ANTS = 10
N_ITERATIONS = 500 # PRETTY SELF EXPLANATORY
ALPHA = 1.0 #pheromone importance. Higher alpha means more influenced by pheromone trails, higher beta means more greedy, higher alpha means more influenced by pheromone trails. Adjusting these can help balance exploration vs exploitation in the search process.
BETA = 2.0 # relative importance of heuristic vs pheromone. Higher beta means more greedy, higher alpha means more influenced by pheromone trails. Adjusting these can help balance exploration vs exploitation in the search process.
RHO = 0.5 # evaporation rate per iteration - THIS IS VERY HEAVY, 5 ITERATIONS IT FINDS BEST COST.
Q = 10.0 # how much pheromone gets deposited
TAU_INIT = 1.0 #Starting edge / pheromone level
DELTA = 0.5 

#============================= LAZY MANS INTEGER LISTS =====================
TASK_IDS = list(TASKS.keys()) #T1 thru T10
EMPLOYEE_IDS = list(EMPLOYEES.keys()) #E1 thru E5
N_TASKS = len(TASK_IDS)
N_EMPLOYEES = len(EMPLOYEE_IDS)

#======================================================================================================================
#                                              HEURISTIC VALUE CALCULATIONS FOR ACO
#======================================================================================================================

def heuristic(task_id, emp_id):
    task = TASKS[task_id]
    emp = EMPLOYEES[emp_id]
    eta = 0.1 #baseline value, stops edges from being 0

    #==================MATCH SKILL===================
    if task["required_skill"] in emp["skills"]:
        eta += 0.5 #good match
    
    #==================DIFFICULTY===================
    if emp["skill_level"] >= task["difficulty"]:
        eta += 0.3 #difficulty below skill level. 
    else:
        eta -= (task["difficulty"] - emp["skill_level"]) * DELTA #difficulty above skill level, penalize)

    #==================HOURS CALCULATION / SPARE TIME===================
    spare_time = emp["available_hours"] - task["estimated_time"]
    if spare_time > 0:
        eta += min (spare_time / emp["available_hours"], 1.0) #more spare time, better

    return max(eta, 0.01) #stops negatives in calculation

def h_tablebuild():
    table = np.zeros((N_TASKS, N_EMPLOYEES))
    for i in range (N_TASKS):
        for j in range(N_EMPLOYEES):
            table[i][j] = heuristic(TASK_IDS[i], EMPLOYEE_IDS[j])
    return table

#======================================================================================================================
#                                              overtime/overuse/poor skill match calcs, cost function
#======================================================================================================================
def violation_costs(emp_id, assigned_task_ids): #single employee calculation report
    if not assigned_task_ids:
        return 0.0 #Shows no tasks, no costs

    s_tasks = sorted(assigned_task_ids, key=lambda t: TASKS[t]["deadline"]) #sort tasks by deadline for better calculation ascending

    time_total = np.array ([TASKS[t]["estimated_time"] for t in s_tasks], dtype = float)#numpy array for processing time
    
    deadlines = np.array([TASKS[t]["deadline"] for t in s_tasks], dtype = float) #numpy array for deadlines

    finish_times = np.cumsum(time_total) #cumulative times for tasks

    violations = np.maximum(0.0, finish_times - deadlines) #calculate deadline violations

    return float(np.sum(violations)) #total violation cost for employee

def cost_function(assignment):
    emp_tasks = {emp_id: [] for emp_id in EMPLOYEE_IDS} #initialize employee task mapping
    for task_id, emp_id in assignment.items():
        emp_tasks[emp_id].append(task_id) #assign tasks to employees

    overload_penalty = 0.0
    skill_penalty = 0.0
    difficulty_penalty = 0.0    #starting penalties before any sort of calculation
    deadline_penalty = 0.0
    unique_assignment_penalty = 0.0

    #==================UNIQUE TASKS===================
    assigned_counts = {}
    for task_id in assignment:
        assigned_counts[task_id] = assigned_counts.get(task_id, 0) + 1
    for task_id, count in assigned_counts.items():
        if count > 1:
            unique_assignment_penalty += (count - 1) 

    #================== CHECKS FOR EACH EMPLOYEE ===================


    for emp_id in EMPLOYEE_IDS:
        emp = EMPLOYEES[emp_id]
        my_tasks = emp_tasks[emp_id]

        total_hours = sum(TASKS[t]["estimated_time"] for t in my_tasks) #total hours assigned to employee
        if total_hours > emp["available_hours"]:
            overload_penalty += total_hours - emp["available_hours"]

        for task_id in my_tasks:
            task = TASKS[task_id]

            if task["required_skill"] not in emp["skills"]:
                skill_penalty += 1.0

            if emp["skill_level"] < task["difficulty"]:
                difficulty_penalty += task["difficulty"] - emp["skill_level"]

        deadline_penalty += violation_costs(emp_id, my_tasks) #calculate deadline violation costs for employee


        #================================ WORKING OUT THE TOTAL COST CALCULATION ====================================
    total_cost = (w_oload * overload_penalty + #MOVED THIS BECAUSE IT WAS STUCK OUTSIDE THE FOR TASK_ID LOOP, SILLY BOY
        w_stype * skill_penalty + 
        w_difficulty * difficulty_penalty + 
        w_otime * deadline_penalty + 
        w_unique * unique_assignment_penalty)
    breakdown = {
        "overload": overload_penalty,
        "skill": skill_penalty,
        "difficulty": difficulty_penalty,
        "deadline": deadline_penalty,
        "unique": unique_assignment_penalty,
        "total": total_cost
        }

    return total_cost, breakdown



#=============================================================================================================================
#                                             ACO ALGORITHM
#=============================================================================================================================

def calculate_solution(pheromone, h_table):
    solution = np.zeros(N_TASKS, dtype=int)
    order = np.random.permutation(N_TASKS) #random order of tasks for assignment

    for i in order:
        weights = (pheromone[i] ** ALPHA) * (h_table[i] ** BETA) #calculate weights for each employee based on pheromone and heuristic
        probabilities = weights / weights.sum()
        solution[i] = np.random.choice(N_EMPLOYEES, p=probabilities) #assign task to employee based on probabilities

    return solution

def solution_dict(solution):
    return {TASK_IDS[i]: EMPLOYEE_IDS[int(solution[i])] for i in range (N_TASKS)}

#=============================================================================================================================
##                                             PHEROMONE UPDATE 
##=============================================================================================================================
#
def p_update(pheromone, all_solutions):
    pheromone *= (1 - RHO) #evaporation using numpy
    np.clip(pheromone, 0.01, None, out=pheromone) #prevent pheromone from going too low

    for solution, cost in all_solutions:
        deposit = Q if cost == 0 else Q / cost #more pheromone mean BETTER GOOD SOLUTION
        pheromone[np.arange(N_TASKS), solution] += deposit #more pheromone for solution quality


#=============================================================================================================================
#                                             PRINT OUT
#       F VALUES REMINDER ----- >#(Right Align)  | <#(Left Align)  | .#f (Decimal Places)
#=============================================================================================================================

def print_sol(solution, total_cost, breakdown):
    print("\n" + "=" * 50) #for that delicious looking format
    print("SOLUTION FOUND:")
    print("=" * 50)


    employee_tasks = {e: [] for e in EMPLOYEE_IDS}
    for task_id, emp_id in solution.items(): #create mapping of employees to their assigned tasks
        employee_tasks[emp_id].append(task_id) # assign tasks - done by visual studio, check this works first.

    for emp_id in EMPLOYEE_IDS:
        emp = EMPLOYEES[emp_id]
        my_tasks = employee_tasks[emp_id]
        total_time = sum(TASKS[t]["estimated_time"] for t in my_tasks) #total time assigned to employee 
         
        print(f"\n{emp_id} - Hours Available: {emp['available_hours']} | Skill Level: {emp['skill_level']} | Skills: {emp['skills']}") #should look like E1 - Hours Available: 10 | Skill Level: 4 | Skills: ['A', 'C']

        if not my_tasks:
            print ("No Tasks Assigned")

        else: #CHECK PRINT FORMATTING,
            print(f" {'task' :>10} | {'Est. Time':>10} | {'Difficulty':>10} | {'Deadline':>10} | {'Required Skill':>15}") #header for task details
            print("-" * 70)

            for t in sorted(my_tasks):
                task = TASKS[t]
                skill_correct = "OK" if task["required_skill"] in emp["skills"] else "MISMATCH"
                difficulty_correct = "OK" if emp["skill_level"] >= task["difficulty"] else "TOO HARD"

                print(f" {t:>10} | {task['estimated_time']:>10} | {task['difficulty']:>10} | {task['deadline']:>10} | {task['required_skill']:>10} | {skill_correct:>15} | {difficulty_correct:>15}")
            print(f" Hours Used: {total_time} / {emp['available_hours']}")
    print("\n" + "=" * 50)
    print(f"TOTAL COST: {total_cost:.2f}")
    print("-" * 50)


#HOW TO SHOW THE HISTORY. ASHAMEDLY THIS TOOK ME FOREVER, THANKYOU NUMPY. #REMOVED BECAUSE TABLE, NOT GRAPH
# def print_history(history):
#     history_array = np.array(history)

#     print("\n" + "=" * 50)
#     print ("HISTORY STATS AS FOLLOWS:")
#     print("=" * 50)

#     print(f" Start Cost : {history_array[0]:.4f}")
#     print(f" Final Cost : {history_array[-1]:.4f}")
#     print(f" Best Cost : {np.min(history_array):.4f} (iteration {np.argmin(history_array) + 1})")
#     print(f" Average : {np.mean(history_array):.4f}")
#     print(f" Deviation : {np.std(history_array):.4f}")
#     print (f"\n {'Iteration'} {'Best Cost'}")
    
def plot_output(history, violation_history, elapsed_time):
    history_array = np.array(history)
    violation_array = np.array(violation_history)
    iterations = np.arange(1, len(history) + 1)
    
    fig, axes = plt.subplots(1,3, figsize=(18, 5))
    fig.suptitle("ACO RESULTS AND PERFORMANCE", fontsize=16)
    
    #=============================== ITERATIONS VS BEST COST GRAPH ==============================
    axes[0].plot(iterations, history_array, marker='o')
    axes[0].set_title("Best Cost Over Iterations")
    axes[0].set_xlabel("Iteration")
    axes[0].set_ylabel("Best Cost")
    axes[0].grid(True)

    #=============================== ITERATIONS VS TIME GRAPH ==============================
    time_per_iteration = elapsed_time / len(history_array)
    total_time_cum = np.arange (1, len(history_array) +1) * time_per_iteration

    axes[1].plot(iterations, total_time_cum, marker='o', color='orange')
    axes[1].set_title("Cumulative Time Over Iterations")
    axes[1].set_xlabel("Iteration")
    axes[1].set_ylabel("Cumulative Time (s)")
    axes[1].grid(True)

    #=============================== ITERATIONS VS TOTAL VIOLATIONS IN BEST SOLUTIONS ==============================
    axes[2].plot(iterations, violation_array, marker='o', color='green')
    axes[2].set_title("Total Violations in Best Solutions Over Iterations")
    axes[2].set_xlabel("Iteration")
    axes[2].set_ylabel("Total Violations")
    axes[2].grid(True)

    plt.tight_layout()
    plt.savefig("aco_results.png") #save the plot as an image file
    print("\n PLOTS SAVED AS 'aco_results.png' IN CURRENT DIRECTORY.")
    plt.show()







#=============================================================================================================================
#                                             MAIN FUNCTION
#=============================================================================================================================

print("=" * 50)
print("ACO Assignment 1")
print("=" * 50)

print(f"Tasks: {N_TASKS} | Employees: {N_EMPLOYEES}")
print(f"Ants: {N_ANTS} | Iterations: {N_ITERATIONS}")
print(f"Alpha: {ALPHA} | Beta: {BETA} | Rho: {RHO} | Q: {Q} | Tau Init: {TAU_INIT}")
print()

pheromone = np.full((N_TASKS, N_EMPLOYEES), TAU_INIT, dtype=float) #initialize pheromone levels))

h_table = h_tablebuild()

best_solution = None
best_cost = math.inf
best_breakdown = None
history = []
violation_history = [] #ADDED FOR PLOTTING AND VIOLATION HISTORY LIST

tracemalloc.start()
start_time = time.time()

for iteration in range(N_ITERATIONS):
    all_solutions = []

    for ant in range(N_ANTS):
        sol = calculate_solution(pheromone, h_table)
        cost, breakdown = cost_function(solution_dict(sol))
        all_solutions.append((sol, cost))

        if cost < best_cost:
            best_solution = sol.copy()
            best_cost = cost
            best_breakdown = breakdown

    p_update(pheromone, all_solutions)
    history.append(best_cost)
    violations = sum(1 for k, v in best_breakdown.items() if k != "total" and v > 0) #count number of violation types in best solution
    violation_history.append(violations)#ADDED FOR VIOLATION PRINTOUTS
    if (iteration+1) % 10 == 0 or iteration == 0:
        print(f"Iteration {iteration + 1}/{N_ITERATIONS} | Best Cost: {best_cost:.2f}")

end_time = time.time()
mem_peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
elapsed_time = end_time - start_time # ADDED FOR PLOT AND FINAL OUTPUT
print(f"\nDone in {end_time - start_time:.2f} seconds | Peak Memory: {mem_peak[1] / 1024:.2f} KB")

best_dict = solution_dict(best_solution)
print_sol(best_dict, best_cost, best_breakdown)
# print_history(history)
plot_output(history, violation_history, elapsed_time)


