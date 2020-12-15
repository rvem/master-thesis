from tibercad import run_tibercad


def calc_fitness(model, work_dir):
    vac, vac_inv = run_tibercad(model, work_dir)
    v0, i0, fill_factor = calc_fitness_parts(vac, vac_inv)
    return (0.5 * v0 + 0.3 * i0 + 0.2 * fill_factor, v0, i0, fill_factor)


def calc_fitness_parts(vac, vac_inv):
    i0 = abs(vac[0.0])
    v0 = abs(vac_inv[min(vac_inv.keys(), key=abs)])
    fill_factor = abs(max(vac.keys()) * max(vac_inv.keys()) / (v0 * i0))
    return v0, i0, fill_factor
