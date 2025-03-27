# Script that creates 103 yaml files with different values of "variation" for the PDF weights

template = """
JetEnergy Corrections:
    name: JERC
    path: Wprime.Modules.JetCorrections
    parameters:
        isMC: self.dataset.process.isMC
        year: self.config.year
        runPeriod: self.dataset.runPeriod
        runEra: self.dataset.runEra

Type-I MET correction:
    name: TypeICorrectedMET
    path: Wprime.Modules.METcorrections
    parameters:
        isMC: self.dataset.process.isMC
        year: self.config.year
        runPeriod: self.dataset.runPeriod
        runEra: self.dataset.runEra

Jet cleanup:
    name: jetCleanup
    path: Wprime.Modules.plotUtils

APPLY KINEMATIC SELECTION:
    name: kinSel
    path: Wprime.Modules.kinematicSelection
    parameters:
        year: self.config.year
        runPeriod: self.dataset.runPeriod

PUweight from correctionlib:
    name: puWeightRun3
    path: Wprime.Modules.puWeightCor
    parameters:
        isMC: self.dataset.process.isMC
        year: self.config.year
        runPeriod: self.dataset.runPeriod

For the PDF weight:
    name: UseWeight
    path: Wprime.Modules.ForPDFvariationHistograms
    parameters:
        isMC: self.dataset.process.isMC
        variation: "{variation}"
"""

# Creates the 103 files
for i in range(103):
    content = template.format(variation=i)
    filename = f"../config/PDFreweight_{i}.yaml"
    
    with open(filename, 'w') as f:
        f.write(content)

    print(f"Archivo {filename} creado.")
