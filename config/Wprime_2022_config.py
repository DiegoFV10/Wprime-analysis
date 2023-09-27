from analysis_tools import ObjectCollection, Category, Process, Dataset, Feature, Systematic
from analysis_tools.utils import DotDict
from analysis_tools.utils import join_root_selection as jrs
from plotting_tools import Label
from collections import OrderedDict
import ROOT
import math

class Config():
    def __init__(self, name, year, ecm, lumi_fb=None, lumi_pb=None, **kwargs):
        self.name=name
        self.year=year
        self.ecm=ecm
        assert lumi_fb or lumi_pb
        if lumi_fb:
            self.lumi_fb = lumi_fb
            self.lumi_pb = lumi_fb * 1000.
        else:
            self.lumi_fb = lumi_pb / 1000.
            self.lumi_pb = lumi_pb 

        self.x = kwargs

        self.postEE = kwargs.pop("postEE")
        if self.postEE:
            #self.lumi_fb = 26.337 # EFG
            #self.lumi_pb = 26337  # EFG
            # Only FG
            self.lumi_fb = 20.665
            self.lumi_pb = 20665
        else:
            self.lumi_fb = 7.875
            self.lumi_pb = 7875

        self.channels = self.add_channels()
        self.regions = self.add_regions()
        self.categories = self.add_categories()
        self.processes, self.process_group_names = self.add_processes()
        self.datasets = self.add_datasets()
        if 'xrd_redir' in kwargs:
            self.prefix_datasets(self.datasets, kwargs['xrd_redir'])
        self.features = self.add_features()
        self.versions = self.add_versions()
        self.weights = self.add_weights()
        self.systematics = self.add_systematics()

    def join_selection_channels(self, selection):
        return jrs([jrs(jrs(selection[ch.name], op="and"), ch.selection, op="and")
            for ch in self.channels], op="or")

    def combine_selections_per_channel(self, selection1, selection2):
        selection = DotDict()
        for channel in selection1:
            selection[channel] = jrs(selection1[channel], selection2[channel], op="or")
        return selection

    def get_aux(self, name, default=None):
        return self.x.get(name, default)

    def add_regions(self):
        pass

    def add_channels(self):
        pass

    def add_categories(self):

        categories = [
            Category("base", "base category", selection = ""),
            Category("preselection", "category for the single muon preselection step", selection = ""),
            Category("kin_selection", "category for the kinematic selection + top veto step", 
                     #selection = "Muon_tunepRelPt[goodMuIdx]*Muon_pt[goodMuIdx]/PuppiMET_pt > 0.4 && Muon_tunepRelPt[goodMuIdx]*Muon_pt[goodMuIdx]/PuppiMET_pt < 1.5 && deltaPhi_MuMET > 2.5 && nJet < 6 && Jet_btagDeepFlavB[0] < 0.73"),
                     selection = "Muon_tunepRelPt[goodMuIdx]*Muon_pt[goodMuIdx]/PuppiMET_pt > 0.4 && Muon_tunepRelPt[goodMuIdx]*Muon_pt[goodMuIdx]/PuppiMET_pt < 1.5 && deltaPhi_MuMET > 2.5 && nJet < 6"),
        ]
        return ObjectCollection(categories)

    def add_processes(self):

        processes = [
            ### Signal Processes ###
            Process("Wprime2000", Label("W' M = 2.0 TeV"), color=ROOT.kAzure+1, isSignal=True),
            Process("Wprime2000_postEE", Label("W' M = 2.0 TeV"), color=ROOT.kAzure+1, isSignal=True),
            Process("Wprime3600", Label("W' M = 3.6 TeV"), color=ROOT.kGreen+1, isSignal=True),
            Process("Wprime3600_postEE", Label("W' M = 3.6 TeV"), color=ROOT.kGreen+1, isSignal=True),
            Process("Wprime5600", Label("W'M_{W'} = 5.6 TeV"), color=ROOT.kMagenta+1, isSignal=True),
            Process("Wprime5600_postEE", Label("W'M_{W'} = 5.6 TeV"), color=ROOT.kMagenta+1, isSignal=True),

            ### Background Processes ###
            # W off-shell
            Process("W_boson", Label("W-boson"), color=ROOT.kAzure+1),
            Process("W_preEE", Label("W-boson"), color=ROOT.kAzure+1, parent_process="W_boson"),
            Process("W_postEE", Label("W-boson"), color=ROOT.kAzure+1, parent_process="W_boson"),
            Process("Wmunu", Label("off-shell W #rightarrow #mu#nu"), color=ROOT.kAzure+1, parent_process="W_preEE"),
            Process("Wmunu_postEE", Label("off-shell W #rightarrow #mu#nu"), color=ROOT.kAzure+1, parent_process="W_postEE"),
            Process("Wtaunu", Label("off-shell W #rightarrow #tau#nu"), color=ROOT.kAzure+3, parent_process="W_preEE"),
            Process("Wtaunu_postEE", Label("off-shell W #rightarrow #tau#nu"), color=ROOT.kAzure+3, parent_process="W_postEE"),

            # W on-shell
            Process("Wonshell", Label("W #rightarrow #mu#nu + jets"), color=ROOT.kAzure+10, parent_process="W_preEE", isWjets=True),
            Process("Wonshell_postEE", Label("W #rightarrow #mu#nu + jets"), color=ROOT.kAzure+10, parent_process="W_postEE", isWjets=True),

            # Top
            Process("Top", Label("Top"), color=(255,255,0)),
            Process("Top_preEE", Label("Top"), color=(255,255,0), parent_process="Top"),
            Process("Top_postEE", Label("Top"), color=(255,255,0), parent_process="Top"),
            Process("TTbar", Label("t#bar{t}"), color=(255,255,0), parent_process="Top_preEE"),
            Process("TTbar_postEE", Label("t#bar{t}"), color=(255,255,0), parent_process="Top_postEE"),
            Process("ST", Label("single t"), color=(255,255,0), parent_process="Top_preEE"),
            Process("ST_postEE", Label("single t"), color=(255,255,0), parent_process="Top_postEE"),

            # Z boson
            Process("Z_boson", Label("Z/#gamma #rightarrow ll"), color=(206, 30, 30)),
            Process("Z_boson_preEE", Label("Z/#gamma #rightarrow ll"), color=(206, 30, 30), parent_process="Z_boson"),
            Process("Z_boson_postEE", Label("Z/#gamma #rightarrow ll"), color=(206, 30, 30), parent_process="Z_boson"),
            Process("Zmumu", Label("Z/#gamma #rightarrow #mu#mu"), color=(206, 30, 30), parent_process="Z_boson_preEE"),
            Process("Zmumu_postEE", Label("Z/#gamma #rightarrow #mu#mu"), color=(206, 30, 30), parent_process="Z_boson_postEE"),

            # Di-Boson
            Process("DiBoson", Label("DiBoson"), color=(36, 147, 25)),
            Process("DiBoson_preEE", Label("DiBoson"), color=(36, 147, 25), parent_process="DiBoson"),
            Process("DiBoson_postEE", Label("DiBoson"), color=(36, 147, 25), parent_process="DiBoson"),
            Process("WW", Label("WW"), color=(36, 147, 25), parent_process="DiBoson_preEE"),
            Process("WW_postEE", Label("WW"), color=(36, 147, 25), parent_process="DiBoson_postEE"),
            Process("WZ", Label("WZ"), color=(36, 147, 25), parent_process="DiBoson_preEE"),
            Process("WZ_postEE", Label("WZ"), color=(36, 147, 25), parent_process="DiBoson_postEE"),
            Process("ZZ", Label("ZZ"), color=(36, 147, 25), parent_process="DiBoson_preEE"),
            Process("ZZ_postEE", Label("ZZ"), color=(36, 147, 25), parent_process="DiBoson_postEE"),

            # QCD
            Process("QCD", Label("QCD"), color=(0, 0, 153)),
            Process("QCD_preEE", Label("QCD"), color=(0, 0, 153), parent_process="QCD"),
            Process("QCD_postEE", Label("QCD"), color=(0, 0, 153), parent_process="QCD"),
            Process("QCD_Pt", Label("QCD"), color=(0, 0, 153), parent_process="QCD_preEE"),
            Process("QCD_Pt_postEE", Label("QCD"), color=(0, 0, 153), parent_process="QCD_postEE"),


            ### DATA ###
            Process("Data2022", Label("Data"), color=(0, 0, 0)),
            Process("Data2022_preEE", Label("Data"), color=(0, 0, 0), isData=True, parent_process="Data2022"),
            Process("Data2022_postEE", Label("Data"), color=(0, 0, 0), isData=True, parent_process="Data2022"),

        ]

        process_group_names = {

            "2022_preEE": [
                "Wprime3600",
                "Wprime5600",
                "W_preEE",
                "Top_preEE",
                "DiBoson_preEE",
                "QCD_preEE",
                "Z_boson_preEE",
                "Data2022_preEE",
            ],
            "2022_postEE": [
                "Wprime3600_postEE",
                "Wprime5600_postEE",
                "W_postEE",
                "Top_postEE",
                "DiBoson_postEE",
                "QCD_postEE",
                "Z_boson_postEE",
                "Data2022_postEE",
            ],

        }

        return ObjectCollection(processes), process_group_names


    def prefix_datasets(self, datasets, prefix):

        for dataset in datasets:
            dataset.prefix = prefix + '//'


    def add_datasets(self):
        datasets = [
 
            ### Signal: Wprime ###

            Dataset("Wprime2000",
                dataset="/WprimetoMuNu_M-2000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.189790,), # From AN-21-096, all of them (NNLO)

            Dataset("Wprime2000_postEE",
                dataset="/WprimetoMuNu_M-2000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.189790,
                tags=["postEE"]),

            Dataset("Wprime3600",
                dataset="/WprimetoMuNu_M-3600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.006262,),

            Dataset("Wprime3600_postEE",
                dataset="/WprimetoMuNu_M-3600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.006262,
                tags=["postEE"]),

            Dataset("Wprime5600",
                dataset="/WprimetoMuNu_M-5600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.000411,),

            Dataset("Wprime5600_postEE",
                dataset="/WprimetoMuNu_M-5600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.000411,
                tags=["postEE"]),

            ### W off-shell ###

            Dataset("Wmunu100to200",
                dataset="/WtoMuNu_M-100to200_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=175.1,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wmunu100to200_postEE",
                dataset="/WtoMuNu_M-100to200_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=175.1,
                tags=["postEE"]),

            Dataset("Wmunu200to500",
                dataset="/WtoMuNu_M-200to500_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=7.423,),

            Dataset("Wmunu200to500_postEE",
                dataset="/WtoMuNu_M-200to500_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=7.423,
                tags=["postEE"]),

            Dataset("Wmunu500to1000",
                dataset="/WtoMuNu_M-500to1000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.254,),

            Dataset("Wmunu500to1000_postEE",
                dataset="/WtoMuNu_M-500to1000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.254,
                tags=["postEE"]),

            Dataset("Wmunu1000to2000",
                dataset="/WtoMuNu_M-1000to2000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.01586,),

            Dataset("Wmunu1000to2000_postEE",
                dataset="/WtoMuNu_M-1000to2000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.01586,
                tags=["postEE"]),

            Dataset("Wmunu2000to3000",
                dataset="/WtoMuNu_M-2000to3000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.0004680,),

            Dataset("Wmunu2000to3000_postEE",
                dataset="/WtoMuNu_M-2000to3000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.0004680,
                tags=["postEE"]),

            Dataset("Wmunu3000to4000",
                dataset="/WtoMuNu_M-3000to4000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.00003197,),

            Dataset("Wmunu3000to4000_postEE",
                dataset="/WtoMuNu_M-3000to4000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.00003197,
                tags=["postEE"]),

            Dataset("Wmunu4000to5000",
                dataset="/WtoMuNu_M-4000to5000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.000002953,),

            Dataset("Wmunu4000to5000_postEE",
                dataset="/WtoMuNu_M-4000to5000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.000002953,
                tags=["postEE"]),

            Dataset("Wmunu5000to6000",
                dataset="/WtoMuNu_M-5000to6000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.0000004031,),

            Dataset("Wmunu5000to6000_postEE",
                dataset="/WtoMuNu_M-5000to6000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.0000004031,
                tags=["postEE"]),

            Dataset("Wmunu6000",
                dataset="/WtoMuNu_M-6000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.0000001049,),

            Dataset("Wmunu6000_postEE",
                dataset="/WtoMuNu_M-6000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.0000001049,
                tags=["postEE"]),

            ## WtoTauNu 

            Dataset("Wtaunu100to200",
                dataset="/WtoTauNu_M-100to200_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=174.7,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu100to200_postEE",
                dataset="/WtoTauNu_M-100to200_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=174.7,
                tags=["postEE"]),

            Dataset("Wtaunu200to500",
                dataset="/WtoTauNu_M-200to500_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=7.485,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu200to500_postEE",
                dataset="/WtoTauNu_M-200to500_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=7.485,
                tags=["postEE"]),

            Dataset("Wtaunu500to1000",
                dataset="/WtoTauNu_M-500to1000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.2479,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu500to1000_postEE",
                dataset="/WtoTauNu_M-500to1000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.2479,
                tags=["postEE"]),

            Dataset("Wtaunu1000to2000",
                dataset="/WtoTauNu_M-1000to2000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.01584,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu1000to2000_postEE",
                dataset="/WtoTauNu_M-1000to2000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.01584,
                tags=["postEE"]),

            Dataset("Wtaunu2000to3000",
                dataset="/WtoTauNu_M-2000to3000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.000482,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu2000to3000_postEE",
                dataset="/WtoTauNu_M-2000to3000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.000482,
                tags=["postEE"]),

            Dataset("Wtaunu3000to4000",
                dataset="/WtoTauNu_M-3000to4000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.0000311,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu3000to4000_postEE",
                dataset="/WtoTauNu_M-3000to4000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.0000311,
                tags=["postEE"]),

            Dataset("Wtaunu4000to5000",
                dataset="/WtoTauNu_M-4000to5000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.00000297,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu4000to5000_postEE",
                dataset="/WtoTauNu_M-4000to5000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.00000297,
                tags=["postEE"]),

            Dataset("Wtaunu5000to6000",
                dataset="/WtoTauNu_M-5000to6000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.000000409,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu5000to6000_postEE",
                dataset="/WtoTauNu_M-5000to6000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.000000409,
                tags=["postEE"]),

            Dataset("Wtaunu6000",
                dataset="/WtoTauNu_M-6000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.000000101,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu6000_postEE",
                dataset="/WtoTauNu_M-6000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.000000101,
                tags=["postEE"]),

            ### W + jets ###

            Dataset("Wjets",
                dataset="/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wonshell"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=67710.0,),

            Dataset("Wjets_postEE",
                dataset="/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wonshell_postEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=67710.0,
                tags=["postEE"]),

            ### Top ###

            # TTbar

            Dataset("TT_2l2nu",
                dataset="/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=96.9,), # From TOP-22-012

            Dataset("TT_2l2nu_postEE",
                dataset="/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=96.9,
                tags=["postEE"]),

            Dataset("TT_lnu2q",
                dataset="/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("TTbar"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=404.0,), # From TOP-22-012

            Dataset("TT_lnu2q_postEE",
                dataset="/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("TTbar_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=404.0,
                tags=["postEE"]),

            # Single Top

            Dataset("ST_tW-lnu2q",
                dataset="/TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=19.31,), # From https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopNNLORef x BR

            Dataset("ST_tW-lnu2q_postEE",
                dataset="/TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("ST_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=19.31,
                tags=["postEE"]),

            Dataset("ST_tW-2l2nu",
                dataset="/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=4.663,),

            Dataset("ST_tW-2l2nu_postEE",
                dataset="/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("ST_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=4.663,
                tags=["postEE"]),

            Dataset("ST_tW-4q",
                dataset="/TWminusto4Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("ST"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=19.98,),

            Dataset("ST_tW-4q_postEE",
                dataset="/TWminusto4Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=19.98,
                tags=["postEE"]),

            Dataset("ST_tbarW-lnu2q",
                dataset="/TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=19.31,), 

            Dataset("ST_tbarW-lnu2q_postEE",
                dataset="/TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("ST_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=19.31,
                tags=["postEE"]),

            Dataset("ST_tbarW-2l2nu",
                dataset="/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("ST"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=4.663,), 

            Dataset("ST_tbarW-2l2nu_postEE",
                dataset="/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("ST_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=4.663,
                tags=["postEE"]),

            Dataset("ST_tbarW-4q",
                dataset="/TbarWplusto4Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=19.98,),

            Dataset("ST_tbarW-4q_postEE",
                dataset="/TbarWplusto4Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=19.98,
                tags=["postEE"]),


            ### Drell-Yan ###

            Dataset("Zmumu_M-50to120",
                dataset="/DYto2Mu_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/"
                    "NANOAODSIM ",
                process=self.processes.get("Zmumu"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=2219.0,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-50to120_postEE",
                dataset="/DYto2Mu_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=2219.0,
                tags=["postEE"]),

            Dataset("Zmumu_M-120to200",
                dataset="/DYto2Mu_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/"
                    "NANOAODSIM ",
                process=self.processes.get("Zmumu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=21.65,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-120to200_postEE",
                dataset="/DYto2Mu_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=21.65,
                tags=["postEE"]),

            Dataset("Zmumu_M-200to400",
                dataset="/DYto2Mu_MLL-200to400_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/"
                    "NANOAODSIM ",
                process=self.processes.get("Zmumu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=3.058,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-200to400_postEE",
                dataset="/DYto2Mu_MLL-200to400_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=3.058,
                tags=["postEE"]),

            Dataset("Zmumu_M-400to800",
                dataset="/DYto2Mu_MLL-400to800_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/"
                    "NANOAODSIM ",
                process=self.processes.get("Zmumu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.2691,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-400to800_postEE",
                dataset="/DYto2Mu_MLL-400to800_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.2691,
                tags=["postEE"]),

            Dataset("Zmumu_M-800to1500",
                dataset="/DYto2Mu_MLL-800to1500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/"
                    "NANOAODSIM ",
                process=self.processes.get("Zmumu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.01915,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-800to1500_postEE",
                dataset="/DYto2Mu_MLL-800to1500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.01915,
                tags=["postEE"]),

            Dataset("Zmumu_M-1500to2500",
                dataset="/DYto2Mu_MLL-1500to2500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/"
                    "NANOAODSIM ",
                process=self.processes.get("Zmumu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.001111,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-1500to2500_postEE",
                dataset="/DYto2Mu_MLL-1500to2500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.001111,
                tags=["postEE"]),

            Dataset("Zmumu_M-2500to4000",
                dataset="/DYto2Mu_MLL-2500to4000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/"
                    "NANOAODSIM ",
                process=self.processes.get("Zmumu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.00005949,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-2500to4000_postEE",
                dataset="/DYto2Mu_MLL-2500to4000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.00005949,
                tags=["postEE"]),

            Dataset("Zmumu_M-4000to6000",
                dataset="/DYto2Mu_MLL-4000to6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/"
                    "NANOAODSIM ",
                process=self.processes.get("Zmumu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.000001558,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-4000to6000_postEE",
                dataset="/DYto2Mu_MLL-4000to6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.000001558,
                tags=["postEE"]),

            Dataset("Zmumu_M-6000",
                dataset="/DYto2Mu_MLL-6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/"
                    "NANOAODSIM ",
                process=self.processes.get("Zmumu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.00000003519,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-6000_postEE",
                dataset="/DYto2Mu_MLL-6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=0.00000003519,
                tags=["postEE"]),


            ### DiBoson ###

            Dataset("WW_2l2nu",
                dataset="/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/"
                    "NANOAODSIM ",
                process=self.processes.get("WW"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=12.98,), # From 13 TeV value with 4% expected increase with MCFM x BR

            Dataset("WW_2l2nu_postEE",
                dataset="/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM ",
                process=self.processes.get("WW_postEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=12.98,
                tags=["postEE"]),

            Dataset("WW_lnu2q",
                dataset="/WWtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WW"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=53.73,),

            Dataset("WW_lnu2q_postEE",
                dataset="/WWtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WW_postEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=53.73,
                tags=["postEE"]),

            Dataset("WW_4q",
                dataset="/WWto4Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WW"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=55.59,),

            Dataset("WW_4q_postEE",
                dataset="/WWto4Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WW_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=55.59,
                tags=["postEE"]),

            Dataset("WZ_2l2q",
                dataset="/WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=3.661,), # From MATRIX (SMP-22-017 at NNLO) x BR

            Dataset("WZ_2l2q_postEE",
                dataset="/WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ_postEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=3.661,
                tags=["postEE"]),

            Dataset("WZ_3lnu",
                dataset="/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.769,),  

            Dataset("WZ_3lnu_postEE",
                dataset="/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ_postEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.769,
                tags=["postEE"]),

            Dataset("WZ_lnu2q",
                dataset="/WZtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=12.39,),  

            Dataset("WZ_lnu2q_postEE",
                dataset="/WZtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ_postEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=12.39,
                tags=["postEE"]),

            Dataset("ZZ",
                dataset="/ZZ_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("ZZ"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=16.7,), # From MATRIX (SMP-22-017 at NNLO)

            Dataset("ZZ_postEE",
                dataset="/ZZ_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ZZ_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=16.7,
                tags=["postEE"]),


            ### QCD ###

            Dataset("QCD_Pt-470to600",
                dataset="/QCD_PT-470to600_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=48.1,), # BAD! Value at 13 TeV (LO) x 0.85

            Dataset("QCD_Pt-470to600_postEE",
                dataset="/QCD_PT-470to600_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=48.1,
                tags=["postEE"]),

            Dataset("QCD_Pt-600to800",
                dataset="/QCD_PT-600to800_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=21.37,), # From XSDB

            Dataset("QCD_Pt-600to800_postEE",
                dataset="/QCD_PT-600to800_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=21.37,
                tags=["postEE"]),

            Dataset("QCD_Pt-800to1000",
                dataset="/QCD_PT-800to1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=3.913,), # From XSDB

            Dataset("QCD_Pt-800to1000_postEE",
                dataset="/QCD_PT-800to1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=3.913,
                tags=["postEE"]),

            Dataset("QCD_Pt-1000",
                dataset="/QCD_PT-1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.377,), # BAD! Value at 13 TeV (LO) x 0.85

            Dataset("QCD_Pt-1000_postEE",
                dataset="/QCD_PT-1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.377,
                tags=["postEE"]),

 
            ### DATA ###

            Dataset("Data2022_C_SingleMuon",
                dataset="/SingleMuon/Run2022C-PromptNanoAODv10_v1-v1/NANOAOD",
                process=self.processes.get("Data2022_preEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                ),

            Dataset("Data2022_C_Muon",
                dataset="/Muon/Run2022C-PromptNanoAODv10_v1-v1/NANOAOD",
                process=self.processes.get("Data2022_preEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                ),

            Dataset("Data2022_D_v1",
                dataset="/Muon/Run2022D-PromptNanoAODv10_v1-v1/NANOAOD",
                process=self.processes.get("Data2022_preEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                ),

            Dataset("Data2022_D_v2",
                dataset="/Muon/Run2022D-PromptNanoAODv10_v2-v1/NANOAOD",
                process=self.processes.get("Data2022_preEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                ),

            Dataset("Data2022_E",
                dataset="/Muon/Run2022E-PromptNanoAODv10_v1-v3/NANOAOD",
                process=self.processes.get("Data2022_postEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                ),

            Dataset("Data2022_F",
                dataset="/Muon/Run2022F-PromptNanoAODv11_v1-v2/NANOAOD",
                process=self.processes.get("Data2022_postEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                ),

            Dataset("Data2022_G",
                dataset="/Muon/Run2022G-PromptNanoAODv11_v1-v2/NANOAOD",
                process=self.processes.get("Data2022_postEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                ),



        ]
        return ObjectCollection(datasets)

    def add_features(self):
 
        ### Preselection Plots ###

        features_presel = [

            Feature("muon_pt", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)", binning=(50, 50, 2000),
                x_title=Label("p_{T}^{#mu}"),
                units="GeV"),

            Feature("muon_eta", "Muon_eta.at(goodMuIdx)", binning=(50, -2.4, 2.4),
                x_title=Label("#mu #eta")),

            Feature("muon_phi", "Muon_phi.at(goodMuIdx)", binning=(50, -math.pi, math.pi),
                x_title=Label("#mu #phi"),
                units="rad"),

            Feature("MET_pt", "PuppiMET_pt", binning=(50, 0, 4000),
                x_title=Label("p_{T}^{miss}"),
                units="GeV"),

            Feature("MET_phi", "PuppiMET_phi", binning=(50, -math.pi, math.pi),
                x_title=Label("p_{T}^{miss} #phi"),
                units="rad"),

            Feature("mT", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*PuppiMET_pt*(1 - cos(deltaPhi_MuMET)) )", binning=(60, 0, 7000),
                x_title=Label("M_{T}"),
                units="GeV"),

            Feature("muonPt_over_MET", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)/PuppiMET_pt", binning=(50, 0, 6),
                x_title=Label("p_{T}^{#mu}/p_{T}^{miss}")),

            Feature("deltaPhi", "deltaPhi_MuMET", binning=(50, 0, math.pi),
                x_title=Label("#Delta#phi(p_{T}^{#mu},p_{T}^{miss})"),
                units="rad"),

            # Plots only for preselection
            Feature("Njets", "nJet", binning=(20, 0, 20),
                x_title=Label("Njets")),

            Feature("btag_score", "Jet_btagDeepFlavB[0]", binning=(50, 0, 1),
                selection="nJet > 0",
                x_title=Label("DeepJet score of leading jet")),

            Feature("nVertices", "PV_npvsGood", binning=(80, 0, 80),
                x_title=Label("# of vertices")),

        ]


        ### Kinematic-Selection Plots ###

        features_kinsel = [

            Feature("muon_pt", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)", binning=(50, 50, 2000),
                x_title=Label("p_{T}^{#mu}"),
                units="GeV"),

            Feature("muon_eta", "Muon_eta.at(goodMuIdx)", binning=(50, -2.4, 2.4),
                x_title=Label("#mu #eta")),

            Feature("muon_phi", "Muon_phi.at(goodMuIdx)", binning=(50, -math.pi, math.pi),
                x_title=Label("#mu #phi"),
                units="rad"),

            Feature("MET_pt", "PuppiMET_pt", binning=(50, 0, 4000),
                x_title=Label("p_{T}^{miss}"),
                units="GeV"),

            Feature("MET_phi", "PuppiMET_phi", binning=(50, -math.pi, math.pi),
                x_title=Label("p_{T}^{miss} #phi"),
                units="rad"),

            Feature("mT", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*PuppiMET_pt*(1 - cos(deltaPhi_MuMET)) )", binning=(60, 0, 7000),
                x_title=Label("M_{T}"),
                units="GeV"),

            Feature("muonPt_over_MET", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)/PuppiMET_pt", binning=(40, 0.4, 1.5),
                x_title=Label("p_{T}^{#mu}/p_{T}^{miss}")),

            Feature("deltaPhi", "deltaPhi_MuMET", binning=(40, 2.5, math.pi),
                x_title=Label("#Delta#phi(p_{T}^{#mu},p_{T}^{miss})"),
                units="rad"),

            Feature("nVertices", "PV_npvsGood", binning=(80, 0, 80),
                x_title=Label("# of vertices")),

        ]


        return ObjectCollection(features_presel)

    def add_versions(self):
        versions = {}
        return versions

    def add_weights(self):
        weights = DotDict()
        weights.default = "1"

        weights.total_events_weights = ["genWeight", "puWeight"]

        weights.preselection = ["genWeight", "puWeight"]
        weights.kin_selection = ["genWeight", "puWeight"]

        return weights

    def add_systematics(self):
        systematics = []

        return ObjectCollection(systematics)

    # feature methods

    def get_central_value(self, feature):
        """
        Return the expression from the central value of a feature
        """
        if feature.central == "":
            return self.central
        return self.systematics.get(feature.central).expression

    def get_object_expression(self, feature, isMC=False,
            syst_name="central", systematic_direction=""):
        """
        Returns a feature or category's expression including the systematic considered
        """

        def get_expression(obj):
            if isinstance(obj, Feature):
                return obj.expression
            elif isinstance(obj, Category):
                return obj.selection
            else:
                raise ValueError("Object %s cannot be used in method get_feature_expression" % obj)

        def add_systematic_tag(feat_expression, tag):
            """
            Includes systematic tag in the feature expression.
                - Directly if it does not come from a vector
                - Before ".at" if it comes from a vector
            """
            if ".at" in feat_expression:
                index = feat_expression.find(".at")
                return feat_expression[:index] + tag + feat_expression[index:]
            else:
                return feat_expression + tag

        feature_expression = get_expression(feature)
        if "{{" in feature_expression:  # derived expression
            while "{{" in feature_expression:
                initial = feature_expression.find("{{")
                final = feature_expression.find("}}")
                feature_name_to_look = feature_expression[initial + 1: final]
                feature_to_look = self.features.get(feature_name_to_look)
                feature_to_look_expression = feature_to_look.expression
                if not isMC:
                    tag = ""
                elif syst_name in feature_to_look.systematics:
                    syst = self.systematics.get(syst_name)
                    if type(syst.expression) == tuple:
                        feature_to_look_expression = feature_to_look_expression.replace(
                            syst.expression[0], syst.expression[1])
                        tag = ""
                    else:
                        tag = syst.expression
                    tag += eval("syst.%s" % systematic_direction)
                else:
                    if feature_to_look.central == "":
                        tag = ""
                    else:
                        central = self.systematics.get(feature_to_look.central)
                        if type(central.expression) == tuple:
                            feature_to_look_expression = feature_to_look_expression.replace(
                                central.expression[0], central.expression[1])
                            tag = ""
                        else:
                            tag = central.expression

                feature_to_look_expression = add_systematic_tag(feature_to_look_expression, tag)
                feature_expression = feature_expression.replace(feature_expression[initial: final + 1],
                    feature_to_look_expression)
            return feature_expression

        elif isinstance(feature, Feature):  # not derived expression and not a category
            if not isMC:
                return add_systematic_tag(feature.expression, "")
            feature_expression = feature.expression
            tag = ""
            if syst_name in feature.systematics:
                syst = self.systematics.get(syst_name)
                if type(syst.expression) == tuple:
                    feature_expression = feature_expression.replace(syst.expression[0],
                        syst.expression[1])
                    tag = ""
                else:
                    tag = syst.expression
                tag += eval("syst.%s" % systematic_direction)
            else:
                if feature.central != "":
                    central = self.systematics.get(feature.central)
                    if type(central.expression) == tuple:
                        feature_expression = feature_expression.replace(central.expression[0],
                            central.expression[1])
                        tag = ""
                    else:
                        tag = central.expression
            return add_systematic_tag(feature_expression, tag)
        else:
            return get_expression(feature)

    def get_weights_systematics(self, list_of_weights, isMC=False):
        systematics = []
        if isMC:
            for weight in list_of_weights:
                try:
                    feature = self.features.get(weight)
                    for syst in feature.systematics:
                        if syst not in systematics:
                            systematics.append(syst)
                except ValueError:
                    continue
        return systematics

    def get_weights_expression(self, list_of_weights, syst_name="central", systematic_direction=""):
        weights = []
        for weight in list_of_weights:
            try:
                feature = self.features.get(weight)
                weights.append(self.get_object_expression(
                    feature, True, syst_name, systematic_direction))
            except ValueError:
                weights.append(weight)
        return "*".join(weights)


config = Config("base", year=2022, ecm=13.6, lumi_pb=34212, postEE=True)
