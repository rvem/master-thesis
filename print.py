import os, shutil
from model import Model


def print_model(model, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    print_pero_solarcell(model, out_dir)
    print_C60(model, out_dir)
    print_FAPbBr2I(model, out_dir)
    print_pedot(model, out_dir)
    shutil.copy("MAPbBr2I_SC_400nm.msh", os.path.join(out_dir, "MAPbBr2I_SC_400nm.msh"))

def print_pero_solarcell(model, out_dir):
    features = model.get_values()
    file_contents = f'''
Device pero_solarcell
{{
	meshfile = MAPbBr2I_SC_400nm.msh		#название с mesh
	mesh_units = 1e-9

	Region pedot
	{{
		material = pedot_ #file
		Doping
		{{
		density = {features["pedot_density"]}
		type = acceptor
		}}
	}}

	Region perovskite_surf1
	{{
		material = FAPbBr2I
	}}

	Region perovskite
	{{
		material = FAPbBr2I #file
	}}

	Region perovskite_surf2
	{{
		material = FAPbBr2I
	}}


	Region fullerene
	{{
		material = C60_ #file
		Doping
		{{
		density =  {features["fullerene_density"]}
		type = donor
		}}
	}}

}}

Module driftdiffusion
{{
  name = dd
  plot = (ContactCurrents)
  Solver
	{{
	   max_iterations = 100 # максим кол-во итераций
	   relative_tolerance = 1e-2 # допустимые ошибки метода
	   absolute_tolerance = 1e-2 
	}}

	Physics
    {{

		recombination direct
		{{
		  regions = perovskite
		  C = {features["perovskite_C"]}
		}}
		
		recombination direct
		{{
		  regions = perovskite_surf1,perovskite_surf2
		  C = {features["perovskite_surf_C"]}
		}}

		recombination srh
		{{
		  regions = perovskite
		  tau_n = {features["perovskite_tau_n"]}
		  tau_p = {features["perovskite_tau_p"]}
	}}
		
		recombination srh
		{{
		  regions = perovskite_surf1,perovskite_surf2
		  tau_n = {features["perovskite_surf_tau_n"]}
		  tau_p = {features["perovskite_surf_tau_p"]}
		}}
		

		recombination srh 
	  {{
		regions = pedot
		tau_n = {features["pedot_tau_n"]}
		tau_p = {features["pedot_tau_p"]}
	  }}

		recombination srh
		{{
		regions = fullerene
		tau_n = {features["fullerene_tau_n"]}
		tau_p = {features["fullerene_tau_p"]}
		}}

		generation optical
		{{
		  regions = perovskite,perovskite_surf1,perovskite_surf2
		  generation = {features["generation"]}
		}}
	
    }}

  Contact cathode
  {{
    type = schottky
	barrier_lowering = {features["cathode_barrier_lowering"].__str__().lower()}
    band = c
    barrier = 0.005
    voltage = 0
	work_function = {features["cathode_work_function"]}
    #metal_fermilevel = -4.2	#work funtion
    #metal_fermilevel = -5.1
    #area_factor = 20000
  }}

  Contact anode
  {{
  	barrier_lowering = {features["anode_barrier_lowering"].__str__().lower()}
    type = schottky
    barrier = 0.005
    band = v
    voltage = $Vb
    work_function = {features["anode_work_function"]}
  }}
}}



Module sweep
{{
  name = reverse
  solve = dd
  variable = $Vb
  start =  1e-15  #Это старт и начало отрисовки ВАХ по ОХ
  stop = 1.5
  steps = 30 # количество точек. в эксперименте чаще всего идёт шаг 0,1V немного влияет на скорость счета
  plot_data = true
}}
  
  
 Simulation
{{
  resultpath = result
  searchpath = .
  solve = (reverse)
  output_format = grace
}}
'''
    with open(os.path.join(os.getcwd(), out_dir, "pero_solarcell.tib"), 'w') as f:
        f.write(file_contents)


def print_C60(model, out_dir):
    features = model.get_values()
    file_contents = f'''
[conductionband]
m_G = 1

[valenceband]
E_v = {features["C60_E_v"]}

[bandgap]
Eg_G = {features["C60_Eg_G"]}

[permittivity]
permittivity = 4.25

[mobility/constant]
mu_max   = ({features["C60_mu_max_0"]}, {features["C60_mu_max_0"]})
'''
    with open(os.path.join(os.getcwd(), out_dir, "C60_.dat"), 'w') as f:
        f.write(file_contents)


def print_FAPbBr2I(model, out_dir):
    features = model.get_values()
    file_contents = f'''
structure = zb

[lattice]
a = 0.88
c = 1.265

[conductionband]
m_G = 0.156
m_dos = 0.156

[valenceband]
E_v = {features["FAPbBr2I_E_v"]}
m_dos = 0.17

[bandgap]
Eg_G = {features["FAPbBr2I_Eg_G"]}

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
permittivity = {features["FAPbBr2I_permitivity"]}

[mobility/constant]
mu_max   = ({features["FAPbBr2I_mu_max_0"]}, {features["FAPbBr2I_mu_max_0"]})


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
    with open(os.path.join(os.getcwd(), out_dir, "FAPbBr2I.dat"), 'w') as f:
        f.write(file_contents)


def print_pedot(model, out_dir):
    features = model.get_values()
    file_contents = f'''
[conductionband]
m_G = 1

[valenceband]
E_v = {features["pedot_E_v"]}
m_dos = 1

[bandgap]
Eg_G = {features["pedot_Eg_G"]}

[permittivity] # [3]
permittivity = 5

# mobility
[mobility/constant] #[2]
mu_max   = ({features["pedot_mu_max_0"]}, {features["pedot_mu_max_0"]})
'''
    with open(os.path.join(os.getcwd(), out_dir, "pedot_.dat"), 'w') as f:
        f.write(file_contents)
