import os

masses = [400, 600, 1000, 1600, 2000, 2600, 3000, 3600, 4000, 4600, 5000, 5600, 6000, 6600]
couplings = [0.01, 0.1, 1, 2, 3, 5]

for mass in masses:
    for coup in couplings:
        if coup == 1:
            # Caso especial: sin kR1 en el nombre
            cmd = (
                f"combineCards.py "
                f"muon22=../../../2022/muon/fullCuts/datacard_Wprime{mass}.txt "
                f"muon23=../../../2023/muon/fullCuts/datacard_Wprime{mass}.txt "
                f"> datacard_Wprime{mass}.txt"
            )
        else:
            # General: incluye kR[coupling]
            cmd = (
                f"combineCards.py "
                f"muon22=../../../2022/muon/fullCuts/datacard_Wprime{mass}_kR{coup}.txt "
                f"muon23=../../../2023/muon/fullCuts/datacard_Wprime{mass}_kR{coup}.txt "
                f"> datacard_Wprime{mass}_kR{coup}.txt"
            )
        
        print(cmd)

        os.system(cmd)
