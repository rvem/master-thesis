import os, subprocess
from time import time
import numpy as np
import pygmo as pg
from copy import copy, deepcopy

from util import calc_fitness_model, calc_fitness_model_3d, calc_fitness_3d
from print import print_model

EPS = 1e-6
HV_EPS = 1e-6
MAX_IT = 100
MAX_TRAMPLING_STEPS = 20


def oneplusone(initial_model, target_fitness):
    current_seed = np.random.get_state()[1][0]
    current_model = initial_model
    current_fitness = calc_fitness_model(current_model,
                                         os.path.join(os.getcwd(), f"seed{current_seed}", "epoch0"))
    print(f"Initial fitness: {current_fitness}")
    print(f"Target fitness,: {target_fitness}")
    it = 0
    while (abs(current_fitness - target_fitness) > EPS and it < MAX_IT):
        try:
            it += 1
            new_model = current_model.mutate()
            start = time()
            process_model = True
            try:
                new_fitness = calc_fitness_model(new_model,
                                                 os.path.join(os.getcwd(), f"seed{current_seed}", f"epoch{it}"))
            except subprocess.CalledProcessError as _:
                print("tibercad suddenly failed:(")
                process_model = False
            finish = time()
            if process_model:
                print(f"Epoch {it}, fitness: {new_fitness}, time to calculate {finish - start}")
                if abs(new_fitness - target_fitness) < abs(current_fitness - target_fitness):
                    current_fitness = new_fitness
                    current_model = new_model
        except KeyboardInterrupt:
            print("Interrupting 1+1, returning current model")
            return current_model
    return current_model


def mutate_until_success(front, it, seed):
    subj_it = 0
    while True:
        subj_to_mutate = np.random.choice([x[1] for x in front])
        new_subj = subj_to_mutate.mutate()
        try:
            new_subj_values = calc_fitness_model_3d(new_subj,
                                                     os.path.join(os.getcwd(), f"seed{seed}", f"epoch{it}_ind{subj_it}"))
        except subprocess.CalledProcessError as _:
            print("tibercad suddenly failed:(")
            subj_it += 1
            continue
        return (new_subj_values, new_subj)


def get_dominance_mask(front):
    costs = np.array([x[0] for x in front])
    is_efficient = np.ones(costs.shape[0], dtype = bool)
    for i, c in enumerate(costs):
        if is_efficient[i]:
            is_efficient[is_efficient] = np.any(costs[is_efficient] < c, axis=1)
            is_efficient[i] = True
    return is_efficient


def calc_hv(front):
    costs = np.array([[y for y in x[0]] for x in front])
    hv = pg.hypervolume(costs)
    return hv.compute([2, 2, 2], hv_algo=pg.hv3d())


def calc_target_difference(model_values, target_values):
    res = []
    tmp = calc_fitness_3d(target_values[0], target_values[1], target_values[2])
    for i in range(3):
        res.append(round(abs(model_values[i] - tmp[i]), 6))
    return res


def print_front(front, epoch, seed):
    for i, front_elem in enumerate(front):
        model = front_elem[1]
        print_model(model, os.path.join(os.getcwd(), f"seed{seed}",
                                        f"epoch{epoch}", f"model{i}"))


def log_epoch(front, hv, log_file, epoch, seed):
    with open(log_file, 'a') as f:
        f.write(f"Epoch {epoch}, hypervolume: {hv}\n")
        for i, front_elem in enumerate(front):
            scores = front_elem[0]
            f.write(f"{scores} seed{seed}/epoch{epoch}/model{i}\n")
        f.write("\n")


def semo(initial_model, target_values):
    current_seed = np.random.get_state()[1][0]
    log_file = f"semo-{current_seed}.log"
    initial_value = calc_fitness_model_3d(initial_model,
                                            os.path.join(os.getcwd(), f"seed{current_seed}", "epoch0_ind0"))
    front = [(calc_target_difference(initial_value, target_values), initial_model)]
    hv = calc_hv(front)
    terminate = False
    it = 0
    trampling_steps = 0
    print(f"Initial hypervolume: {hv}")
    while not terminate:
        try:
            it += 1
            new_subj_values, new_subj = mutate_until_success(front, it, current_seed)
            extended_front = deepcopy(front)
            extended_front.append((calc_target_difference(new_subj_values, target_values), new_subj))
            mask = get_dominance_mask(extended_front)
            new_front = []
            for i in range(len(mask)):
                if mask[i]:
                    new_front.append(extended_front[i])
            new_hv = calc_hv(new_front)
            print(f"Epoch {it}, hypervolume = {new_hv}")
            print_front(new_front, it, current_seed)
            log_epoch(new_front, new_hv, log_file, it, current_seed)
            if abs(new_hv - hv) > HV_EPS:
                front = new_front
                hv = new_hv
                print(f"Front updated, new front size: {len(new_front)}, new front fitnesses:")
                print(", ".join([x[0].__str__() for x in new_front]))
                trampling_steps = 0
            else:
                trampling_steps += 1
                if trampling_steps > MAX_TRAMPLING_STEPS:
                    terminate = True
        except KeyboardInterrupt:
            print("Interrupting SEMO, returning current pareto-front")
            res_subjects = [x[1] for x in front]
            return res_subjects
    res_subjects = [x[1] for x in front]
    return res_subjects
