#!/usr/bin/env python3
import os

# Masas y couplings
masses = [400, 600, 1000, 1600, 2000, 2600, 3000, 3600,
          4000, 4600, 5000, 5600, 6000, 6600]
couplings = [0.01, 0.1, 1, 2, 3, 5]

# rMax base para coupling <= 1
rmax_base = {
    400: 320,
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
rmax_base_unblind = {
    400: 320,
    600: 50,
    1000: 14,
    1600: 5.0,
    2000: 3.0,
    2600: 2.5,
    3000: 2.5,
    3600: 2.5,
    4000: 2.5,
    4600: 2.5,
    5000: 2.5,
    5600: 3.0,
    6000: 3.0,
    6600: 3.5
}

# Bucle sobre masas y couplings
for mass in masses:
    for coup in couplings:

        # Nombre del datacard
        if coup == 1:
            datacard = f"datacard_Wprime{mass}.txt"
            tag = f"Wprime{mass}_kR{coup}"
            unblind_tag = f"UnblindM{mass}_kR{coup}"
        else:
            datacard = f"datacard_Wprime{mass}_kR{coup}.txt"
            tag = f"Wprime{mass}_kR{coup}"
            unblind_tag = f"UnblindM{mass}_kR{coup}"

        # Calcular rMax
        if coup <= 1:
            rmax = rmax_base[mass]
            rmax_unblind = rmax_base_unblind[mass]
        else:
            # Factor multiplicativo 1.8^(coup - 1)
            factor = 1.8 ** (coup - 1)
            rmax = rmax_base[mass] * factor
            rmax_unblind = rmax_base_unblind[mass] * factor

        # Comando para expected
        cmd_expected = (
            f"combineTool.py -M MarkovChainMC {datacard} "
            f"--tries 15 -t 250 -s -1 -i 10000 --noDefaultPrior=0 "
            f"--rMax {rmax:.3f} --job-mode condor "
            f"--task-name {tag} --sub-opts='+JobFlavour=\"workday\"'"
        )

        # Comando para unblinded
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
