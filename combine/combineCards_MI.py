import os

masses = [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600,
          1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800,
          2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600]

lumi22 = 34.65
lumi23 = 27.10

for mass in masses:
    cmd = (
        f"combineCards.py "
        f"muon22=../../../2022/muon/fullCuts/datacard_mTmin_{mass}_lumi_{lumi22:.2f}.txt "
        f"muon23=../../../2023/muon/fullCuts/datacard_mTmin_{mass}_lumi_{lumi23:.2f}.txt "
        f"> datacard_mTmin_{mass}.txt"
    )
    
    print(cmd)
    
    os.system(cmd)
