from itertools import product

from genetic import genetic_algorithm
from chromosome import resetCostCache
import time


def run_parameter_test(trials=10, **kwargs):
    combos = list(product(*kwargs.values()))

    total_trials = trials * len(combos)
    print(f"Running {len(combos)} combinations over {total_trials} total trials")

    time_results = {}
    cost_results = {}
    trial_i = 0

    est_duration_start = time.time()

    for combo in combos:
        combo_ht = dict(zip(kwargs.keys(), combo))
        key = ', '.join(f'{k}={v}' for k, v in combo_ht.items() if k not in ['generations', 'pop_size'])

        time_results[key] = 0
        cost_results[key] = 0

        params = {}
        for k, v in combo_ht.items():
            if k not in ('generations', 'pop_size'):
                params[k] = v

        for _ in range(trials):
            resetCostCache()
            
            start = time.time()
            result = genetic_algorithm(combo_ht['generations'], combo_ht['pop_size'], **params)
            end = time.time()

            time_results[key] += end - start
            cost_results[key] += result.getCost()

            trial_i += 1
            est_duration =   (time.time() - est_duration_start) / trial_i * (total_trials - trial_i)
            
            print(f'trial {trial_i}/{total_trials} (est {est_duration:.2f}s)', end='\r', flush=True)

    print()

    print()
    print('Time results (avg)')
    for k, v in sorted(time_results.items(), key=lambda x: x[1]):
        print(f'   {k}:  {time_results[k]/trials:.4f}s ({cost_results[k]/trials:.2f} cost)')

    print()
    print('Cost results (avg)')
    for k, v in sorted(cost_results.items(), key=lambda x: x[1]):
        print(f'   {k}:  {cost_results[k]/trials:.2f} cost ({time_results[k]/trials:.4f}s)')



if __name__ == '__main__':    
    run_parameter_test(
        generations=[10],
        pop_size=[10],

        mutation_prob=[0.07, 0.1, 0.13],
        eletism=[0.01, 0.04, 0.07],
        tornament_size=[4, 5, 6]
    )


# Time results (avg)
#    mutation_prob=0.1, eletism=0.04, tornament_size=6:  0.1138s (0.06 cost)
#    mutation_prob=0.07, eletism=0.04, tornament_size=4:  0.1240s (0.08 cost)
#    mutation_prob=0.13, eletism=0.04, tornament_size=5:  0.1253s (0.06 cost)
#    mutation_prob=0.07, eletism=0.01, tornament_size=4:  0.1259s (0.06 cost)
#    mutation_prob=0.07, eletism=0.07, tornament_size=4:  0.1283s (0.08 cost)
#    mutation_prob=0.07, eletism=0.01, tornament_size=5:  0.1300s (0.10 cost)
#    mutation_prob=0.1, eletism=0.07, tornament_size=5:  0.1326s (0.06 cost)
#    mutation_prob=0.1, eletism=0.01, tornament_size=4:  0.1335s (0.10 cost)
#    mutation_prob=0.07, eletism=0.07, tornament_size=6:  0.1337s (0.08 cost)
#    mutation_prob=0.13, eletism=0.07, tornament_size=5:  0.1349s (0.10 cost)
#    mutation_prob=0.07, eletism=0.04, tornament_size=5:  0.1585s (0.10 cost)
#    mutation_prob=0.07, eletism=0.04, tornament_size=6:  0.1637s (0.10 cost)
#    mutation_prob=0.13, eletism=0.01, tornament_size=5:  0.1638s (0.10 cost)
#    mutation_prob=0.1, eletism=0.01, tornament_size=6:  0.1674s (0.08 cost)
#    mutation_prob=0.13, eletism=0.01, tornament_size=4:  0.1680s (0.08 cost)
#    mutation_prob=0.1, eletism=0.07, tornament_size=4:  0.1692s (0.12 cost)
#    mutation_prob=0.1, eletism=0.04, tornament_size=4:  0.1751s (0.12 cost)
#    mutation_prob=0.13, eletism=0.04, tornament_size=4:  0.1812s (0.12 cost)
#    mutation_prob=0.13, eletism=0.07, tornament_size=4:  0.1815s (0.12 cost)
#    mutation_prob=0.1, eletism=0.04, tornament_size=5:  0.1856s (0.14 cost)
#    mutation_prob=0.1, eletism=0.01, tornament_size=5:  0.1921s (0.12 cost)
#    mutation_prob=0.13, eletism=0.04, tornament_size=6:  0.2080s (0.14 cost)
#    mutation_prob=0.1, eletism=0.07, tornament_size=6:  0.2243s (0.12 cost)
#    mutation_prob=0.07, eletism=0.07, tornament_size=5:  0.2263s (0.22 cost)
#    mutation_prob=0.13, eletism=0.07, tornament_size=6:  0.2297s (0.14 cost)
#    mutation_prob=0.07, eletism=0.01, tornament_size=6:  0.2554s (0.20 cost)
#    mutation_prob=0.13, eletism=0.01, tornament_size=6:  0.2638s (0.16 cost)

# Cost results (avg)
#    mutation_prob=0.07, eletism=0.01, tornament_size=4:  0.06 cost (0.1259s)
#    mutation_prob=0.1, eletism=0.04, tornament_size=6:  0.06 cost (0.1138s)
#    mutation_prob=0.1, eletism=0.07, tornament_size=5:  0.06 cost (0.1326s)
#    mutation_prob=0.13, eletism=0.04, tornament_size=5:  0.06 cost (0.1253s)
#    mutation_prob=0.07, eletism=0.04, tornament_size=4:  0.08 cost (0.1240s)
#    mutation_prob=0.07, eletism=0.07, tornament_size=4:  0.08 cost (0.1283s)
#    mutation_prob=0.07, eletism=0.07, tornament_size=6:  0.08 cost (0.1337s)
#    mutation_prob=0.1, eletism=0.01, tornament_size=6:  0.08 cost (0.1674s)
#    mutation_prob=0.13, eletism=0.01, tornament_size=4:  0.08 cost (0.1680s)
#    mutation_prob=0.07, eletism=0.01, tornament_size=5:  0.10 cost (0.1300s)
#    mutation_prob=0.07, eletism=0.04, tornament_size=5:  0.10 cost (0.1585s)
#    mutation_prob=0.07, eletism=0.04, tornament_size=6:  0.10 cost (0.1637s)
#    mutation_prob=0.1, eletism=0.01, tornament_size=4:  0.10 cost (0.1335s)
#    mutation_prob=0.13, eletism=0.01, tornament_size=5:  0.10 cost (0.1638s)
#    mutation_prob=0.13, eletism=0.07, tornament_size=5:  0.10 cost (0.1349s)
#    mutation_prob=0.1, eletism=0.01, tornament_size=5:  0.12 cost (0.1921s)
#    mutation_prob=0.1, eletism=0.04, tornament_size=4:  0.12 cost (0.1751s)
#    mutation_prob=0.1, eletism=0.07, tornament_size=4:  0.12 cost (0.1692s)
#    mutation_prob=0.1, eletism=0.07, tornament_size=6:  0.12 cost (0.2243s)
#    mutation_prob=0.13, eletism=0.04, tornament_size=4:  0.12 cost (0.1812s)
#    mutation_prob=0.13, eletism=0.07, tornament_size=4:  0.12 cost (0.1815s)
#    mutation_prob=0.1, eletism=0.04, tornament_size=5:  0.14 cost (0.1856s)
#    mutation_prob=0.13, eletism=0.04, tornament_size=6:  0.14 cost (0.2080s)
#    mutation_prob=0.13, eletism=0.07, tornament_size=6:  0.14 cost (0.2297s)
#    mutation_prob=0.13, eletism=0.01, tornament_size=6:  0.16 cost (0.2638s)
#    mutation_prob=0.07, eletism=0.01, tornament_size=6:  0.20 cost (0.2554s)
#    mutation_prob=0.07, eletism=0.07, tornament_size=5:  0.22 cost (0.2263s)