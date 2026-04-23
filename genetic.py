import random, matplotlib.pyplot as plt
from chromosome import Chromosome, tournament_selection


def genetic_algorithm(
        generations:int,
        pop_size:int,
        mutation_prob:float=0.1,
        eletism:float|int=0.04,
        tornament_size:int=6,
        graph:str=None,
        quickFinish=True,
        verbose:bool=False
    ):
    '''
    to disable graphing set the graph parameter to None or ''
    quickFinish flag denotes whether this function should return the optimal answer once it is found or if it should go to n-generations even after the optimal solution is found
    eletism is the amount of the best answers that keep going forward. if it is less than 1 if is treated as a percent and if its more it is treated as a whole number 
    mutation_prob is the starting chance for mutation and mutation_prob_decay is the amount that mutation_prob will decrease each run
    '''
    elete_count = int(eletism)
    if elete_count < 1:
        elete_count = int(pop_size * eletism)

    population = [Chromosome() for i in range(generations)]
    
    avg_costs = []
    best_costs = []

    generation = 0
    finish = False
    while generation < generations and not finish:
        if verbose:
            print(f'generation {generation+1}/{generations}', end='\r', flush=True)

        if graph != None and graph != '':
            costs = [i.getCost() for i in population]
            avg_costs += [sum(costs) / len(costs)]
            best_costs += [min(costs)]
        
        new_population = []

        # eletism
        best = sorted(population, key=lambda x: x.getCost())[:elete_count]

        new_population += [i.clone() for i in best]

        for _ in range(pop_size - elete_count):

            # tornament selection crossover child
            p_a, p_b = tournament_selection(population, tornament_size)
            child = Chromosome.crossoverChild(p_a, p_b)

            # mutation
            if random.random() <= mutation_prob:
                child.mutate()

            new_population += [child]

        population = new_population
        generation += 1

        if min(population, key=lambda x: x.getCost()).getCost() == 0 and quickFinish:
            finish = True

    if finish and verbose:
        print(f'Quick finished at generation {generation+1}/{generations}')
    elif verbose:
        print()

    if graph != None and graph != '':
        plt.figure(figsize=(9, 5), dpi=400)
        plt.plot(avg_costs, label="avg cost")
        plt.plot(best_costs, label="best cost")
        plt.title("Genetic algorithm")
        plt.xlabel("generation")
        plt.ylabel("cost")
        plt.legend()
        plt.figtext(0.01, 0.015, f"({pop_size=}, {generation=})", fontsize=8, fontstyle="italic", color="dimgrey")
        plt.savefig(graph)
        plt.close()

    return min(population, key=lambda x: x.getCost())


if __name__ == '__main__':
    import time

    start = time.time()
    answer = genetic_algorithm(500, 100)
    end = time.time()

    print(answer)

    print(end-start)