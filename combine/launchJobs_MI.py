#!/usr/bin/env python3
import os
import argparse

# mT min
masses = [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600,
          1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800,
          2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600]

# rMax dict
rmax_base = {
    400: 70,
    500: 34.5,
    600: 20.5,
    700: 13.5,
    800: 9.5,
    900: 7.3,
    1000: 5.3,
    1100: 4.5,
    1200: 4.0,
    1300: 4.0,
    1400: 4.0,
    1500: 3.8,
    1600: 3.0,
    1700: 3.0,
    1800: 2.2,
    1900: 2.1,
    2000: 1.7,
    2100: 0.9,
    2200: 0.9,
    2300: 0.9,
    2400: 0.8,
    2500: 0.8,
    2600: 0.8,
    2700: 0.7,
    2800: 0.7,
    2900: 0.7,
    3000: 0.5,
    3100: 0.4,
    3200: 0.4,
    3300: 0.4,
    3400: 0.35,
    3500: 0.35,
    3600: 0.35
}

def main():
    parser = argparse.ArgumentParser(description="Launch jobs for MI limits with Combine")
    parser.add_argument("--year", type=int, choices=[2022, 2023, 2223], required=True,
                        help="Dataset year (2022, 2023 or 22+23)")
    args = parser.parse_args()

    year = args.year

    if year == 2022:
        lumi = 34.65
    elif year == 2023:
        lumi = 27.10

    # Loop over mTmins
    for mass in masses:

        if year == 2022 or year == 2023:
            datacard = f"datacard_mTmin_{mass}_lumi_{lumi:.2f}.txt"
        else:
            datacard = f"datacard_mTmin_{mass}.txt"
        tag = f"mTmin{mass}"
        unblind_tag = f"UnblindMTmin{mass}"

        # rMax for each case
        rmax_exp = rmax_base[mass]
        rmax_unblind = rmax_base[mass]

        # Run expected
        cmd_expected = (
            f"combineTool.py -M MarkovChainMC {datacard} "
            f"--tries 15 -t 250 -s -1 -i 10000 --noDefaultPrior=0 "
            f"--rMax {rmax_exp:.3f} --job-mode condor "
            f"--task-name {tag} --sub-opts='+JobFlavour=\"workday\"'"
        )

        # Run unblinded
        cmd_unblind = (
            f"combineTool.py -M MarkovChainMC {datacard} "
            f"--tries 300 -s -1 -i 10000 --noDefaultPrior=0 "
            f"--rMax {rmax_unblind:.3f} --job-mode condor "
            f"--task-name {unblind_tag} --sub-opts='+JobFlavour=\"longlunch\"'"
        )

        # Launch commands
        print(f"Lanzando expected: {cmd_expected}")
        os.system(cmd_expected)

        print(f"Lanzando unblinded: {cmd_unblind}")
        os.system(cmd_unblind)

if __name__ == "__main__":
    main()
