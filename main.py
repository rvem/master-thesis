import numpy as np

from model import BoolFeature, FloatFeature, IntFeature, Model
from print import *
from tibercad import run_tibercad
from util import calc_fitness, calc_fitness_parts

from genetic import oneplusone, semo

features = {
    # Solarcell
    "pedot_density": IntFeature(9e1, (1, 1e5), 1e15),
    # Add `enabled=False` as a last parameter of the constructor to disable feature
    # from mutation, e.g.:
    # "pedot_density": IntFeature(9e1, (1, 1e5), 1e15, enabled=False)
    # All features are enabled by default
    "fullerene_density": IntFeature(1e2, (1, 1e5), 1e15),
    "perovskite_C": FloatFeature(2e-8, (1e-10, 1e-4)),
    "perovskite_surf_C": FloatFeature(2e-6, (1e-10, 1e-4)),
    "perovskite_tau_n": FloatFeature(2e-8, (1e-10, 1e-6)),
    "perovskite_tau_p": FloatFeature(2e-8, (1e-10, 1e-6)),
    "perovskite_surf_tau_n": FloatFeature(1e-10, (1e-11, 1e-6)),
    "perovskite_surf_tau_p": FloatFeature(1e-10, (1e-11, 1e-6)),
    "pedot_tau_n": FloatFeature(1e-6, (1e-8, 1e-5)),
    "pedot_tau_p": FloatFeature(1e-6, (1e-8, 1e-5)),
    "fullerene_tau_n": FloatFeature(1e-6, (1e-8, 1e-5)),
    "fullerene_tau_p": FloatFeature(1e-6, (1e-8, 1e-5)),
    "generation": FloatFeature(1.6771203876494165, (1, 2), 1e21),
    "cathode_barrier_lowering": BoolFeature(True),
    "cathode_work_function": FloatFeature(4.2, (3.8, 4.6)),
    "anode_barrier_lowering": BoolFeature(True),
    "anode_work_function": FloatFeature(4.88, (4.6, 5.2)),
    # C60
    "C60_E_v": FloatFeature(-6.0, (-6.3, -5.8)),
    "C60_Eg_G": FloatFeature(2.15, (1.8, 2.2)),
    "C60_mu_max_0": FloatFeature(1.6, (0.001, 20)),
    "C60_mu_max_1": FloatFeature(1.6, (0.001, 20)),
    # FAPbBr2I
    "FAPbBr2I_E_v": FloatFeature(-5.7, (-5.8, -5.4)),
    "FAPbBr2I_Eg_G": FloatFeature(1.97, (1.95, 2.05)),
    "FAPbBr2I_permitivity": FloatFeature(6, (3.5, 7)),
    "FAPbBr2I_mu_max_0": FloatFeature(2, (0.001, 20)),
    "FAPbBr2I_mu_max_1": FloatFeature(2, (0.001, 20)),
    # C60
    "pedot_E_v": FloatFeature(-5.2, (-5.4, -5.0)),
    "pedot_Eg_G": FloatFeature(1.6, (1.5, 2)),
    "pedot_mu_max_0": FloatFeature(0.45, (0.001, 20)),
    "pedot_mu_max_1": FloatFeature(0.45, (0.001, 20)),
}

model = Model(features)

target_v_oc = 0.903
target_j_sc = 11.482 / 1e3
target_ff = 67.572 / 100
target_fitness = calc_fitness(target_v_oc, target_j_sc, target_ff)
target_values = (target_v_oc, target_j_sc, target_ff)
