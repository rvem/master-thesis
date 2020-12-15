import subprocess
from time import time
import numpy as np

from util import calc_fitness


EPS = 1e-3
MAX_IT = 100


def oneplusone(initial_model, target_fitness):
    current_seed = np.random.get_state()[1][0]
    current_model = initial_model
    current_fitness, _, _, _ = calc_fitness(current_model, f"./seed{current_seed}/epoch0")
    print(f"Initial fitness: {current_fitness}")
    print(f"Target fitness,: {target_fitness}")
    it = 0
    while (abs(current_fitness - target_fitness) > EPS and it < MAX_IT):
        it += 1
        new_model = current_model.mutate()
        start = time()
        process_model = True
        try:
            new_fitness, _, _, _ = calc_fitness(new_model, f"./seed{current_seed}/epoch{it}")
        except subprocess.CalledProcessError as _:
            print("tibercad suddenly failed:(")
            process_model = False
        finish = time()
        if process_model:
            print(f"Epoch {it}, fitness: {new_fitness}, time to calculate {finish - start}")
            if abs(new_fitness - target_fitness) < \
               abs(current_fitness - target_fitness):
                current_fitness = new_fitness
                current_model = new_model

    return current_model
