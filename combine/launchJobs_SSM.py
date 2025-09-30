#!/usr/bin/env python3
import os

# Masas
masses = [400, 600, 1000, 1600, 2000, 2600, 3000,
          3600, 4000, 4600, 5000, 5600, 6000, 6600]

# rMax base para expected
rmax_base = {
    400: 310,
    600: 50,
    1000: 14,
    1600: 5.0,
    2000: 3.0,
    2600: 2.0,
    3000: 1.6,
    3600: 1.3,
    4000: 1.28,
    4600: 1.42,
    5000: 1.5,
    5600: 1.75,
    6000: 1.9,
    6600: 2.5
}
rmax_base2 = {
    400: 750,
    600: 92,
    1000: 27,
    1600: 9.1,
    2000: 6.1,
    2600: 3.9,
    3000: 3.2,
    3600: 2.8,
    4000: 2.8,
    4600: 3.0,
    5000: 3.2,
    5600: 3.5,
    6000: 3.9,
    6600: 5.0
}

# rMax base para unblinded
rmax_base_unblind = {
    400: 400,
    600: 60,
    1000: 20,
    1600: 6.0,
    2000: 4.0,
    2600: 3.0,
    3000: 2.5,
    3600: 2.0,
    4000: 1.8,
    4600: 1.9,
    5000: 2.2,
    5600: 2.5,
    6000: 3.0,
    6600: 3.5
}
rmax_base_unblind2 = {
    400: 750,
    600: 92,
    1000: 27,
    1600: 9.1,
    2000: 6.1,
    2600: 3.9,
    3000: 3.2,
    3600: 2.8,
    4000: 2.8,
    4600: 3.0,
    5000: 3.2,
    5600: 3.5,
    6000: 3.9,
    6600: 5.0
}

# Bucle sobre masas
for mass in masses:

    datacard = f"datacard_Wprime{mass}.txt"
    tag = f"Wprime{mass}"
    unblind_tag = f"UnblindM{mass}"

    # rMax para cada caso
    rmax_exp = rmax_base2[mass]
    rmax_unblind = rmax_base_unblind2[mass]

    # Comando expected
    cmd_expected = (
        f"combineTool.py -M MarkovChainMC {datacard} "
        f"--tries 15 -t 250 -s -1 -i 10000 --noDefaultPrior=0 "
        f"--rMax {rmax_exp:.3f} --job-mode condor "
        f"--task-name {tag} --sub-opts='+JobFlavour=\"workday\"'"
    )

    # Comando unblinded
    cmd_unblind = (
        f"combineTool.py -M MarkovChainMC {datacard} "
        f"--tries 300 -s -1 -i 10000 --noDefaultPrior=0 "
        f"--rMax {rmax_unblind:.3f} --job-mode condor "
        f"--task-name {unblind_tag} --sub-opts='+JobFlavour=\"longlunch\"'"
    )

    # Lanzar comandos
    print(f"Lanzando expected: {cmd_expected}")
    os.system(cmd_expected)

    print(f"Lanzando unblinded: {cmd_unblind}")
    os.system(cmd_unblind)
