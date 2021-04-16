from tibercad import run_tibercad


def calc_fitness_model(model, work_dir):
    vac, vac_inv = run_tibercad(model, work_dir)
    v_oc, j_sc, ff = calc_fitness_parts(vac, vac_inv)
    return calc_fitness(v_oc, j_sc, ff)


def calc_fitness_model_3d(model, work_dir):
    vac, vac_inv = run_tibercad(model, work_dir)
    v_oc, j_sc, ff = calc_fitness_parts(vac, vac_inv)
    return calc_fitness_3d(v_oc, j_sc, ff)


v_oc_max = 1.683
j_sc_max = 14.59 / 1e3
ff_max = 92.2 / 1e2
v_oc_weight = 1/3
j_sc_weight = 1/3
ff_weight = 1/3


def calc_fitness(v_oc, j_sc, ff):
    fitness = v_oc_weight * v_oc / v_oc_max + j_sc_weight * j_sc / j_sc_max + \
        ff_weight * ff / ff_max
    return fitness


def calc_fitness_3d(v_oc, j_sc, ff):
    return [v_oc / v_oc_max, j_sc / j_sc_max, ff / ff_max]


def calc_fitness_parts(vac, vac_inv):
    i0 = abs(vac[min(vac.keys())])
    v0 = vac_inv[min(filter(lambda x: x >= 0, vac_inv.keys()))]
    max_power_point = max(vac.items(), key=lambda x: x[0] * x[1])
    fill_factor = abs(max_power_point[0] * max_power_point[1] / (i0 * v0))
    return v0, i0, fill_factor

def print_mutations_table(models, out):
    contents = ""
    for i, model in enumerate(models):
        contents += f"Model{i}\n"
        for j, mutation in enumerate(model.mutations):
            contents += f"Mutation {j}\n"
            contents += mutation.__str__()
            contents += "\n"
        contents += "\n"
    with open(out, 'w') as f:
        f.write(contents)
