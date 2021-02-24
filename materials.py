import numpy as np
from abc import ABCMeta, abstractmethod
from copy import copy


class AbstractMaterial(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self,
                 e_v,
                 m_dos,
                 eg_g,
                 permitivity,
                 mu_max):
        pass

    @abstractmethod
    def __copy__(self):
        pass

    def mutate(self):
        new = copy(self)
        i = np.random.randint(0, 5)
        if i == 0:
            new.e_v = np.random.uniform(self.e_v_limits[0],
                                        self.e_v_limits[1])
        elif i == 1:
            new.m_dos = np.random.uniform(self.m_dos_limits[0],
                                          self.m_dos_limits[1])
        elif i == 2:
            new.eg_g = np.random.uniform(self.eg_g_limits[0],
                                         self.eg_g_limits[1])
        elif i == 3:
            new.permitivity = np.random.uniform(self.permitivity_limits[0],
                                                self.permitivity_limits[1])
        else:
            new.mu_max = (np.random.uniform(self.mu_max_limits[0],
                                            self.mu_max_limits[1]),
                          np.random.uniform(self.mu_max_limits[0],
                                            self.mu_max_limits[1]))
        return new

    @abstractmethod
    def print_to_file(self, out):
        pass


class Pedot(AbstractMaterial):
    def __init__(self, e_v, m_dos, eg_g, permitivity, mu_max):
        self.e_v = e_v
        self.e_v_limits = (5.0, 5.4)
        self.m_dos = m_dos
        self.m_dos_limits = (1.0, 1.0)
        self.eg_g = eg_g
        self.eg_g_limits = (1.5, 2)
        self.permitivity = 5
        self.permitivity_limits = (5.0, 5.0)
        self.mu_max = mu_max
        self.mu_max_limits = (0.001, 20)

    def __copy__(self):
        return Pedot(copy(self.e_v), copy(self.m_dos), copy(self.eg_g),
                     copy(self.permitivity), copy(self.mu_max))

    def print_to_file(self, out):
        file_contents = f'''
# pedot_mes

[conductionband]
m_G = 1

[valenceband]
E_v = -{self.e_v}
m_dos = {self.m_dos}

[bandgap]
Eg_G = {self.eg_g}

[permittivity] # [3]
permittivity = {self.permitivity}

# mobility
[mobility/constant] #[2]
mu_max   = {self.mu_max}
'''
        with open(out, 'w') as f:
            f.write(file_contents)


class FAPbBr2I(AbstractMaterial):
    def __init__(self, e_v, m_dos, eg_g, permittivity, mu_max):
        self.e_v = e_v
        self.e_v_limits = (5.4, 5.8)
        self.m_dos = m_dos
        self.m_dos_limits = (0.01, 0.9)
        self.eg_g = eg_g
        self.eg_g_limits = (1.95, 2.05)
        self.permitivity = permittivity
        self.permitivity_limits = (3.5, 7)
        self.mu_max = mu_max
        self.mu_max_limits = (0.001, 10)

    def __copy__(self):
        return FAPbBr2I(copy(self.e_v), copy(self.m_dos), copy(self.eg_g),
                        copy(self.permitivity), copy(self.mu_max))

    def print_to_file(self, out):
        file_contents = f'''
structure = zb

[lattice]
a = 0.88
c = 1.265

[conductionband]
m_G = 0.156
m_dos = 0.156

[valenceband]
E_v = -{self.e_v}
m_dos = {self.m_dos}



[bandgap]
# T=0 K optical [5]
Eg_G = {self.eg_g}

[deformation_potentials] # [3]
a_c = 0.0
a_v = 0.0
b = 0.0
d = 0.0

abs_def_pot_X = 0.0
uniax_def_pot_X = 0.0
abs_def_pot_L = 0.0
uniax_def_pot_L = 0.0

[permittivity]
permittivity = {self.permitivity}

[mobility/constant]
mu_max   = {self.mu_max}


[mobility/doping_dependent]
mobility_formula = 1
mumin1 = (52.2,		44.9)
mumin2 = (52.2,		0.0)
mu1    = (43.4,		29)
Pc     = (0.0,		9.23e16)
Cr     = (9.68e16,	2.23e17)
Cs     = (3.43e20,	6.1e20)
alpha  = (0.68,		0.719)
beta   = (2,		2)


[mobility/field_dependent]
Vsat_Formula = 1
beta0   = (1.109,	1.213)
betaexp = (0.66,	0.17)
vsat0   = (1.07e7,	8.37e6)
vsatexp = (0.87,	0.52)


[recombination/direct]
C = 2e-9



[recombination/SRH]
Etrap  = 0.0
taumin = (0.0,		0.0)
taumax = (1.0e-5,	3.0e-6)
Nref   = (1.0e+16,	1.0e+16)
gamma  = (1,		1)
Talpha = (-1.5,		-1.5)
Tcoeff = (2.55,		2.55)


[atomistic_structure]
lattice_type = cubic
n_basis_specie = 4
specie_1 = Pb
specie_2 = I
specie_5 = Br
specie_3 = N
specie_4 = C
n_1 = 4
n_2 = 4
n_5 = 8
n_3 = 4
n_4 = 4

#Basis vectors T_"specie"_"#of atom"_"direction"
# Pb
T_1_1_a = 0.0
T_1_1_b = 0.0
T_1_1_c = 0.0
T_1_1_a = 0.0
T_1_1_b = 1.0
T_1_1_c = 0.0
T_1_1_a = 0.0
T_1_1_b = 0.0
T_1_1_c = 1.0
T_1_1_a = 0.0
T_1_1_b = 1.0
T_1_1_c = 1.0

# I
T_2_1_a = 0.5
T_2_1_b = 0.0
T_2_1_c = 0.0
# T_2_2_a = 0.0
# T_2_2_b = 0.5
# T_2_2_c = 0.0
# T_2_3_a = 0.0
# T_2_3_b = 0.0
# T_2_3_c = 0.5

# Br
T_5_1_a = 0.0
T_5_1_b = 0.5
T_5_1_c = 0.0
T_5_2_a = 0.0
T_5_2_b = 0.0
T_5_2_c = 0.5

# NC
T_3_1_a = 0.4
T_3_1_b = 0.5
T_3_1_c = 0.5
T_4_1_a = 0.6
T_4_1_b = 0.5
T_4_1_c = 0.5

'''
        with open(out, 'w') as f:
            f.write(file_contents)


class C60(AbstractMaterial):
    def __init__(self, e_v, m_dos, eg_g, permittivity, mu_max):
        self.e_v = e_v
        self.e_v_limits = (5.8, 5.8)
        self.m_dos = m_dos
        self.m_dos_limits = (0, 0)
        self.eg_g = eg_g
        self.eg_g_limits = (1.8, 2.2)
        self.permitivity = permittivity
        self.permitivity_limits = (4.25, 4.25)
        self.mu_max = mu_max
        self.mu_max_limits = (0.001, 20)

    def __copy__(self):
        return C60(copy(self.e_v), copy(self.m_dos), copy(self.eg_g),
                   copy(self.permitivity), copy(self.mu_max))

    def print_to_file(self, out):
        file_contents = f'''
# C60

[conductionband]
m_G = 1

[valenceband]
E_v = -{self.e_v}

[bandgap]
Eg_G = {self.eg_g}

[permittivity] # [3]
permittivity = {self.permitivity}
# mobility
[mobility/constant] #[2]
mu_max   = {self.mu_max}
'''
        with open(out, 'w') as f:
            f.write(file_contents)
