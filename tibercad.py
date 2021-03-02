import os, subprocess
from print import print_model


def run_tibercad(model, work_dir):
    os.makedirs(f"{work_dir}", exist_ok=True)
    print_model(model, work_dir)
    print(f"running tibercad in {work_dir}")
    subprocess.run(["tibercad", "-b", os.path.join(os.getcwd(), work_dir, "pero_solarcell.tib")], check=True,
                   stdout=subprocess.DEVNULL)
    vac = {}
    vac_inv = {}
    result_contents = open(os.path.join(work_dir, "result", "reverse_dd.dat"), 'r').readlines()
    for line in result_contents:
        if line[0] != '#':
            res = [float(x) for x in line.strip().split()]
            vac[res[0]] = res[1]
            vac_inv[res[1]] = res[0]
    return vac, vac_inv
