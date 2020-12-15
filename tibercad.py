import os, shutil, subprocess
from print import print_model


def run_tibercad(model, work_dir):
    os.makedirs(f"{work_dir}", exist_ok=True)
    print_model(model, work_dir)
    shutil.copy("MAPbBr2I_SC_400nm.msh", f"{work_dir}/MAPbBr2I_SC_400nm.msh")
    print(f"running tibercad in {work_dir}")
    subprocess.run(["tibercad", f"{work_dir}/pero_solarcell.tib"], check=True,
                   stdout=subprocess.DEVNULL)
    vac = {}
    vac_inv = {}
    result_contents = open(f"{work_dir}/result/reverse_dd.dat", 'r').readlines()
    for line in result_contents:
        if line[0] != '#':
            res = [float(x) for x in line.strip().split()]
            vac[res[0]] = res[2]
            vac_inv[res[2]] = res[0]
    return vac, vac_inv
