from tibercad import run_tibercad


def calc_fitness(model, work_dir):
    vac, vac_inv = run_tibercad(model, work_dir)
    v0, i0, fill_factor = calc_fitness_parts(vac, vac_inv)
    return (0.5 * v0 + 0.3 * i0 + 0.2 * fill_factor, v0, i0, fill_factor)


def calc_fitness_parts(vac, vac_inv):
    i0 = abs(vac[min(vac.keys())])
    v0 = abs(vac_inv[min(vac_inv.keys(), key=abs)])
    max_power_point = max(vac.items(), key=lambda x: abs(x[0] * x[1]))
    fill_factor = abs(max_power_point[0] * max_power_point[1] / (i0 * v0))
    return v0, i0, fill_factor
