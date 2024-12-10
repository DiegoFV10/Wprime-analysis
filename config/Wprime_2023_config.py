from analysis_tools import ObjectCollection, Category, Process, Dataset, Feature, Systematic
from analysis_tools.utils import DotDict
from analysis_tools.utils import join_root_selection as jrs
from plotting_tools import Label
from collections import OrderedDict
import ROOT
import math
from cmt.config.base_config import Config as base_config

class Config(base_config):
    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)

        # Define the lumi dict
        preBPix = {
            "C" : 17794,
        }
        postBPix = {
            "D" : 9451,
        }
        lumi_pb = {
            "preBPix"  : preBPix,
            "postBPix" : postBPix,
        }

        if lumi_pb and not type(lumi_pb) == dict:
            self.lumi_fb = lumi_pb / 1000.
            self.lumi_pb = lumi_pb 

        else:
            lumi_fb = {}
            for period, period_dict in lumi_pb.items():
                period_dict_fb = {}
                for era, lum in period_dict.items():
                    period_dict_fb[era] = lum / 1000
                lumi_fb[period] = period_dict_fb
            self.lumi_fb = lumi_fb
            self.lumi_pb = lumi_pb

        self.x = kwargs

        self.channels = self.add_channels()
        self.regions = self.add_regions()
        self.categories = self.add_categories()
        self.processes, self.process_group_names, _ = self.add_processes()
        self.datasets = self.add_datasets()
        if 'xrd_redir' in kwargs:
            self.prefix_datasets(self.datasets, kwargs['xrd_redir'])
        self.features = self.add_features()
        self.versions = self.add_versions()
        self.weights = self.add_weights()
        self.systematics = self.add_systematics()
        self.default_module_files = self.add_default_module_files()

        self.upper_left_text = "Work in progress"
        self.label_size = 1.2

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
                     selection = "Muon_tunepRelPt[goodMuIdx]*Muon_pt[goodMuIdx]/PuppiMET_pt > 0.4 && Muon_tunepRelPt[goodMuIdx]*Muon_pt[goodMuIdx]/PuppiMET_pt < 1.5 && deltaPhi_MuMET > 2.5 && nJet < 6"), # DEPRECATED
        ]
        return ObjectCollection(categories)

    def add_processes(self):

        processes = [
            ### Signal Processes ###
            Process("Wprime2000", Label("W' M = 2.0 TeV"), color=ROOT.kAzure+1, isSignal=True),
            Process("Wprime2000_preBPix", Label("W' M = 2.0 TeV"), color=ROOT.kAzure+1, isSignal=True, parent_process="Wprime2000"),
            Process("Wprime2000_postBPix", Label("W' M = 2.0 TeV"), color=ROOT.kAzure+1, isSignal=True, parent_process="Wprime2000"),
            Process("Wprime3600", Label("W' M = 3.6 TeV"), color=ROOT.kGreen+1, isSignal=True),
            Process("Wprime3600_preBPix", Label("W' M = 3.6 TeV"), color=ROOT.kGreen+1, isSignal=True, parent_process="Wprime3600"),
            Process("Wprime3600_postBPix", Label("W' M = 3.6 TeV"), color=ROOT.kGreen+1, isSignal=True, parent_process="Wprime3600"),
            Process("Wprime5600", Label("W'M_{W'} = 5.6 TeV"), color=ROOT.kMagenta+1, isSignal=True),
            Process("Wprime5600_preBPix", Label("W'M_{W'} = 5.6 TeV"), color=ROOT.kMagenta+1, isSignal=True, parent_process="Wprime5600"),
            Process("Wprime5600_postBPix", Label("W'M_{W'} = 5.6 TeV"), color=ROOT.kMagenta+1, isSignal=True, parent_process="Wprime5600"),
            Process("Wprime200", Label("W' M = 0.2 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime400", Label("W' M = 0.4 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime600", Label("W' M = 0.6 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime1000", Label("W' M = 1.0 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime1600", Label("W' M = 1.6 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime2600", Label("W' M = 2.6 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime3000", Label("W' M = 3.0 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime4000", Label("W' M = 4.0 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime4600", Label("W' M = 4.6 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime5000", Label("W' M = 5.0 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime6000", Label("W' M = 6.0 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime6600", Label("W' M = 6.6 TeV"), color=(0, 0, 0), isSignal=True),

            ### Background Processes ###
            
            ## W boson ##
            Process("W_boson", Label("W-boson"), color=(63, 144, 218)),
            Process("W_preBPix", Label("W-boson"), color=(63, 144, 218), parent_process="W_boson"),
            Process("W_postBPix", Label("W-boson"), color=(63, 144, 218), parent_process="W_boson"),

            # W off-shell madgraph
            # For W splitting
            Process("Wlnu_full", Label("off-shell W #rightarrow l#nu"), color=ROOT.kAzure+1, parent_process="W_boson"),
            Process("Wlnu", Label("off-shell W #rightarrow l#nu"), color=ROOT.kAzure+1, parent_process="Wlnu_full"),
            Process("Wlnu_postBPix", Label("off-shell W #rightarrow l#nu"), color=ROOT.kAzure+1, parent_process="Wlnu_full"),
            # Old - original
            #Process("Wlnu", Label("off-shell W #rightarrow l#nu"), color=ROOT.kAzure+1, parent_process="W_preBPix"),
            Process("Wlnu1", Label("W #rightarrow l#nu M_{W} 120to200"), color=(255, 241, 0), parent_process="Wlnu"),
            Process("Wlnu2", Label("W #rightarrow l#nu M_{W} 200to400"), color=(255, 140, 0), parent_process="Wlnu"),
            Process("Wlnu3", Label("W #rightarrow l#nu M_{W} 400to800"), color=(232, 17, 35), parent_process="Wlnu"),
            Process("Wlnu4", Label("W #rightarrow l#nu M_{W} 800to1500"), color=(236, 0, 140), parent_process="Wlnu"),
            Process("Wlnu5", Label("W #rightarrow l#nu M_{W} 1500to2500"), color=(104, 33, 122), parent_process="Wlnu"),
            Process("Wlnu6", Label("W #rightarrow l#nu M_{W} 2500to4000"), color=(0, 24, 143), parent_process="Wlnu"),
            Process("Wlnu7", Label("W #rightarrow l#nu M_{W} 4000to6000"), color=(0, 188, 242), parent_process="Wlnu"),
            Process("Wlnu8", Label("W #rightarrow l#nu M_{W} 6000"), color=(0, 178, 148), parent_process="Wlnu"),
            #Process("Wlnu_postBPix", Label("off-shell W #rightarrow l#nu"), color=ROOT.kAzure+1, parent_process="W_postBPix"),

            # W on-shell
            # For W splitting
            Process("Wonshell_full", Label("onshell W #rightarrow l#nu"), color=ROOT.kAzure+10, parent_process="W_boson", isWjets=True),
            Process("Wonshell", Label("onshell W #rightarrow l#nu"), color=ROOT.kAzure+10, parent_process="Wonshell_full", isWjets=True),
            Process("Wonshell_postBPix", Label("onshell W #rightarrow l#nu"), color=ROOT.kAzure+10, parent_process="Wonshell_full", isWjets=True),
            # Old - original
            #Process("Wonshell", Label("W #rightarrow l#nu + jets"), color=ROOT.kAzure+10, parent_process="W_preBPix", isWjets=True),
            #Process("Wonshell_postBPix", Label("W #rightarrow l#nu + jets"), color=ROOT.kAzure+10, parent_process="W_postBPix", isWjets=True),
            # W+2j jet-binned ==> Deprecated
            Process("W+2j_binned", Label("W #rightarrow l#nu + jets"), color=ROOT.kAzure+10, parent_process="W_preBPix", isWjets=True),
            Process("W+2j_binned_postBPix", Label("W #rightarrow l#nu + jets"), color=ROOT.kAzure+10, parent_process="W_postBPix", isWjets=True),

            # W boosted --> HT-binned LO
            Process("Wboost", Label("boosted W #rightarrow l#nu"), color=(206, 30, 30), isHTbin=True, parent_process="W_preBPix"),
            Process("Wboost0", Label("W #rightarrow l#nu HT 40to100"), color=(255, 140, 0), isHTbin=True, parent_process="Wboost"),
            Process("Wboost1", Label("W #rightarrow l#nu HT 100to400"), color=(232, 17, 35), isHTbin=True, parent_process="Wboost"),
            Process("Wboost2", Label("W #rightarrow l#nu HT 400to800"), color=(236, 0, 140), isHTbin=True, parent_process="Wboost"),
            Process("Wboost3", Label("W #rightarrow l#nu HT 800to1500"), color=(104, 33, 122), isHTbin=True, parent_process="Wboost"),
            Process("Wboost4", Label("W #rightarrow l#nu HT 1500to2500"), color=(0, 24, 143), isHTbin=True, parent_process="Wboost"),
            Process("Wboost5", Label("W #rightarrow l#nu HT 2500"), color=(0, 188, 242), isHTbin=True, parent_process="Wboost"),
            Process("Wboost_postBPix", Label("boosted W #rightarrow l#nu"), color=(206, 30, 30), isHTbin=True, parent_process="W_postBPix"),
            # W boosted --> ptLNu-binned NLO
            # For W splitting
            Process("W_ptW_full", Label("boosted W #rightarrow l#nu"), color=(255, 165, 0), isWboost=True, parent_process="W_boson"),
            Process("W_ptW", Label("boosted W #rightarrow l#nu"), color=(206, 30, 30), isWboost=True, parent_process="W_ptW_full"),
            Process("W_ptW_postBPix", Label("boosted W #rightarrow l#nu"), color=(206, 30, 30), isWboost=True, parent_process="W_ptW_full"),
            # Old - original            
            #Process("W_ptW", Label("boosted W #rightarrow l#nu"), color=(206, 30, 30), isWboost=True, parent_process="W_preBPix"),
            Process("W_ptW1", Label("W #rightarrow l#nu p_{T}^{l#nu} 40to100"), color=(255, 140, 0), isWboost=True, parent_process="W_ptW"),
            Process("W_ptW2", Label("W #rightarrow l#nu p_{T}^{l#nu} 100to200"), color=(232, 17, 35), isWboost=True, parent_process="W_ptW"),
            Process("W_ptW3", Label("W #rightarrow l#nu p_{T}^{l#nu} 200to400"), color=(236, 0, 140), isWboost=True, parent_process="W_ptW"),
            Process("W_ptW4", Label("W #rightarrow l#nu p_{T}^{l#nu} 400to600"), color=(104, 33, 122), isWboost=True, parent_process="W_ptW"),
            Process("W_ptW5", Label("W #rightarrow l#nu p_{T}^{l#nu} 600"), color=(0, 24, 143), isWboost=True, parent_process="W_ptW"),
            #Process("W_ptW_postBPix", Label("boosted W #rightarrow l#nu"), color=(206, 30, 30), isWboost=True, parent_process="W_postBPix"),

            # Top
            Process("Top", Label("Top"), color=(189, 31, 1)),
            Process("Top_preBPix", Label("Top"), color=(189, 31, 1), parent_process="Top"),
            Process("Top_postBPix", Label("Top"), color=(189, 31, 1), parent_process="Top"),
            Process("TTbar", Label("t#bar{t}"), color=(255,255,0), parent_process="Top_preBPix"),
            Process("TTbar_postBPix", Label("t#bar{t}"), color=(255,255,0), parent_process="Top_postBPix"),
            Process("ST", Label("single t"), color=(255,255,0), parent_process="Top_preBPix"),
            Process("ST_postBPix", Label("single t"), color=(255,255,0), parent_process="Top_postBPix"),

            # Z boson
            Process("Z_boson", Label("Z/#gamma #rightarrow ll"), color=(169, 107, 89)),
            Process("Z_boson_preBPix", Label("Z/#gamma #rightarrow ll"), color=(169, 107, 89), parent_process="Z_boson"),
            Process("Z_boson_postBPix", Label("Z/#gamma #rightarrow ll"), color=(169, 107, 89), parent_process="Z_boson"),
            Process("Zmumu", Label("Z/#gamma #rightarrow #mu#mu"), color=(206, 30, 30), parent_process="Z_boson_preBPix"),
            Process("Zmumu_postBPix", Label("Z/#gamma #rightarrow #mu#mu"), color=(206, 30, 30), parent_process="Z_boson_postBPix"),
            Process("Ztautau", Label("Z/#gamma #rightarrow #tau#tau"), color=(208, 196, 31), parent_process="Z_boson_preBPix"),
            Process("Ztautau_postBPix", Label("Z/#gamma #rightarrow #tau#tau"), color=(208, 196, 31), parent_process="Z_boson_postBPix"),
            Process("Znunu", Label("Z/#gamma #rightarrow #nu#nu"), color=(255, 128, 0), parent_process="Z_boson_preBPix"),
            Process("Znunu_postBPix", Label("Z/#gamma #rightarrow #nu#nu"), color=(255, 128, 0), parent_process="Z_boson_postBPix"),

            # Di-Boson
            Process("DiBoson", Label("DiBoson"), color=(131, 45, 182)),
            Process("DiBoson_preBPix", Label("DiBoson"), color=(131, 45, 182), parent_process="DiBoson"),
            Process("DiBoson_postBPix", Label("DiBoson"), color=(131, 45, 182), parent_process="DiBoson"),
            Process("WW", Label("WW"), color=(36, 147, 25), parent_process="DiBoson_preBPix"),
            Process("WW_postBPix", Label("WW"), color=(36, 147, 25), parent_process="DiBoson_postBPix"),
            Process("WZ", Label("WZ"), color=(36, 147, 25), parent_process="DiBoson_preBPix"),
            Process("WZ_postBPix", Label("WZ"), color=(36, 147, 25), parent_process="DiBoson_postBPix"),
            Process("ZZ", Label("ZZ"), color=(36, 147, 25), parent_process="DiBoson_preBPix"),
            Process("ZZ_postBPix", Label("ZZ"), color=(36, 147, 25), parent_process="DiBoson_postBPix"),
            Process("Wgamma", Label("W#gamma"), color=(14, 75, 7), parent_process="DiBoson_preBPix"),
            Process("Wgamma_postBPix", Label("W#gamma"), color=(14, 75, 7), parent_process="DiBoson_postBPix"),

            # QCD
            Process("QCD", Label("QCD"), color=(255, 169, 14)),
            Process("QCD_preBPix", Label("QCD"), color=(255, 169, 14), parent_process="QCD"),
            Process("QCD_postBPix", Label("QCD"), color=(255, 169, 14), parent_process="QCD"),
            Process("QCD_Pt", Label("QCD"), color=(0, 0, 153), parent_process="QCD_preBPix"),
            Process("QCD_Pt_postBPix", Label("QCD"), color=(0, 0, 153), parent_process="QCD_postBPix"),


            ### DATA ###
            Process("PromptData2023", Label("Data"), color=(0, 0, 0), isData=True),
            Process("PromptData2023_preBPix", Label("Data"), color=(0, 0, 0), isData=True, parent_process="PromptData2023"),
            Process("PromptData2023_postBPix", Label("Data"), color=(0, 0, 0), isData=True, parent_process="PromptData2023"),


        ]

        process_group_names = {

            "2023_preBPix": [
                "Wprime2000_preBPix",
                "Wprime3600_preBPix",
                "Wprime5600_preBPix",
                "W_preBPix",
                "Top_preBPix",
                "DiBoson_preBPix",
                "QCD_preBPix",
                "Z_boson_preBPix",
                "PromptData2023_preBPix",
            ],
            "2023_postBPix": [
                "Wprime2000_postBPix",
                "Wprime3600_postBPix",
                "Wprime5600_postBPix",
                "W_postBPix",
                "Top_postBPix",
                "DiBoson_postBPix",
                "QCD_postBPix",
                "Z_boson_postBPix",
                "PromptData2023_postBPix",
            ],

            "2023_full": [
                "Wprime2000",
                "Wprime3600",
                "Wprime5600",
                "W_boson",
                "Top",
                "DiBoson",
                "QCD",
                "Z_boson",
                "PromptData2023",
            ],

            ## For W' SSM limits ##

            "SSMlimits2023": [
                "Wprime200",
                "Wprime400",
                "Wprime600",
                "Wprime1000",
                "Wprime1600",
                "Wprime2000",
                "Wprime2600",
                "Wprime3000",
                "Wprime3600",
                "Wprime4000",
                "Wprime4600",
                "Wprime5000",
                "Wprime5600",
                "Wprime6000",
                "Wprime6600",
                "W_boson",
                "Top",
                "DiBoson",
                "QCD",
                "Z_boson",
                "PromptData2023",
            ],

            ########## CHECKS W SAMPLES ##########

            "Woffshell_madgraph": [
                "Wlnu1",
                "Wlnu2",
                "Wlnu3",
                "Wlnu4",
                "Wlnu5",
                "Wlnu6",
                "Wlnu7",
                "Wlnu8",
            ],

            "Wbkg_madgraph": [
                "Wlnu",
                "Wonshell",
            ],

            "W_boosted": [
                "Wboost0",
                "Wboost1",
                "Wboost2",
                "Wboost3",
                "Wboost4",
                "Wboost5",
            ],

            "Wbkg_all": [
                "Wonshell",
                "Wlnu",
                "Wboost",
            ],

            ######################################

            "2023full_Wsplit": [
                "Wprime2000",
                "Wprime3600",
                "Wprime5600",
                "Wonshell_full",
                "Wlnu_full",
                "W_ptW_full",
                "Top",
                "DiBoson",
                "QCD",
                "Z_boson",
                "PromptData2023",
            ],

        }

        return ObjectCollection(processes), process_group_names, []


    def prefix_datasets(self, datasets, prefix):

        for dataset in datasets:
            dataset.prefix = prefix + '//'


    def add_datasets(self):
        datasets = [
 
            ### Signal: Wprime ###

            Dataset("Wprime200",
                dataset="/WprimeToMuNu_M-200_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime200"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                #xs=1106.4,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime200_postBPix",
                dataset="/WprimeToMuNu_M-200_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime200"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                #xs=1106.4,
                xs=0.001,
                tags=["postBPix"]),

            Dataset("Wprime400",
                dataset="/WprimeToMuNu_M-400_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime400"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                #xs=115.91,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime400_postBPix",
                dataset="/WprimeToMuNu_M-400_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime400"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                #xs=115.91,
                xs=0.001,
                tags=["postBPix"]),
            
            Dataset("Wprime600",
                dataset="/WprimeToMuNu_M-600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                #xs=28.204,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime600_postBPix",
                dataset="/WprimeToMuNu_M-600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                #xs=28.204,
                xs=0.001,
                tags=["postBPix"]),
            
            Dataset("Wprime1000",
                dataset="/WprimeToMuNu_M-1000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                #xs=4.1127,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime1000_postBPix",
                dataset="/WprimeToMuNu_M-1000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                #xs=4.1127,
                xs=0.001,
                tags=["postBPix"]),
            
            Dataset("Wprime1600",
                dataset="/WprimeToMuNu_M-1600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                #xs=0.55518,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime1600_postBPix",
                dataset="/WprimeToMuNu_M-1600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                #xs=0.55518,
                xs=0.001,
                tags=["postBPix"]),

            Dataset("Wprime2000",
                dataset="/WprimeToMuNu_M-2000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                #xs=0.189790,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime2000_postBPix",
                dataset="/WprimeToMuNu_M-2000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000_postBPix"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                #xs=0.189790,
                xs=0.001,
                tags=["postBPix"]),
          
            Dataset("Wprime2600",
                dataset="/WprimeToMuNu_M-2600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                #xs=0.04641,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime2600_postBPix",
                dataset="/WprimeToMuNu_M-2600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2600"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                #xs=0.04641,
                xs=0.001,
                tags=["postBPix"]),

            Dataset("Wprime3000",
                dataset="/WprimeToMuNu_M-3000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                #xs=0.01988,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime3000_postBPix",
                dataset="/WprimeToMuNu_M-3000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                #xs=0.01988,
                xs=0.001,
                tags=["postBPix"]),

            Dataset("Wprime3600",
                dataset="/WprimeToMuNu_M-3600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                #xs=0.006262,),
                xs=0.001,), # For datacards

            Dataset("Wprime3600_postBPix",
                dataset="/WprimeToMuNu_M-3600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600_postBPix"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                #xs=0.006262,
                xs=0.001,
                tags=["postBPix"]),
           
            Dataset("Wprime4000",
                dataset="/WprimeToMuNu_M-4000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                #xs=0.003148,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime4000_postBPix",
                dataset="/WprimeToMuNu_M-4000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4000"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                #xs=0.003148,
                xs=0.001,
                tags=["postBPix"]),
            
            Dataset("Wprime4600",
                dataset="/WprimeToMuNu_M-4600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                #xs=0.001289,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime4600_postBPix",
                dataset="/WprimeToMuNu_M-4600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                #xs=0.001289,
                xs=0.001,
                tags=["postBPix"]),
            
            Dataset("Wprime5000",
                dataset="/WprimeToMuNu_M-5000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                #xs=0.000779,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime5000_postBPix",
                dataset="/WprimeToMuNu_M-5000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                #xs=0.000779,
                xs=0.001,
                tags=["postBPix"]),

            Dataset("Wprime5600",
                dataset="/WprimeToMuNu_M-5600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600_preBPix"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                #xs=0.000411,),
                xs=0.001,), # For datacards

            Dataset("Wprime5600_postBPix",
                dataset="/WprimeToMuNu_M-5600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600_postBPix"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                #xs=0.000411,
                xs=0.001,
                tags=["postBPix"]),

            Dataset("Wprime6000",
                dataset="/WprimeToMuNu_M-6000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                #xs=0.000284,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime6000_postBPix",
                dataset="/WprimeToMuNu_M-6000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                #xs=0.000284,
                xs=0.001,
                tags=["postBPix"]),
            
            Dataset("Wprime6600",
                dataset="/WprimeToMuNu_M-6600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                #xs=0.000174,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime6600_postBPix",
                dataset="/WprimeToMuNu_M-6600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                #xs=0.000174,
                xs=0.001,
                tags=["postBPix"]),
            

            ### W off-shell ###

            Dataset("Wlnu120to200",
                dataset="/WtoLNu-4Jets_MLNu-120to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v5/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu1"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="preBPix",
                xs=167.1*1.143,), # From Jeongeun --> GenXSecAnalyzer (LO) x k-factor for madgraph // NOTE: Using final additive + mixed k-factors updated in October2024

            Dataset("Wlnu120to200_postBPix",
                dataset="/WtoLNu-4Jets_MLNu-120to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=167.1*1.143, 
                tags=["postBPix"]),

            Dataset("Wlnu200to400",
                dataset="/WtoLNu-4Jets_MLNu-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v5/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu2"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=20.43*1.217,), 

            Dataset("Wlnu200to400_postBPix",
                dataset="/WtoLNu-4Jets_MLNu-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=20.43*1.217, 
                tags=["postBPix"]),

            Dataset("Wlnu400to800",
                dataset="/WtoLNu-4Jets_MLNu-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu3"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=1.596*1.215,), 

            Dataset("Wlnu400to800_postBPix",
                dataset="/WtoLNu-4Jets_MLNu-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v5/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=1.596*1.215,
                tags=["postBPix"]),

            Dataset("Wlnu800to1500",
                dataset="/WtoLNu-4Jets_MLNu-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu4"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.1095*1.214,),

            Dataset("Wlnu800to1500_postBPix",
                dataset="/WtoLNu-4Jets_MLNu-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.1095*1.214,
                tags=["postBPix"]),

            Dataset("Wlnu1500to2500",
                dataset="/WtoLNu-4Jets_MLNu-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu5"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.006377*1.168,), 

            Dataset("Wlnu1500to2500_postBPix",
                dataset="/WtoLNu-4Jets_MLNu-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.006377*1.168,
                tags=["postBPix"]),

            Dataset("Wlnu2500to4000",
                dataset="/WtoLNu-4Jets_MLNu-2500to4000_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v5/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu6"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.0003464*1.148,),

            Dataset("Wlnu2500to4000_postBPix",
                dataset="/WtoLNu-4Jets_MLNu-2500to4000_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v5/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.0003464*1.148,
                tags=["postBPix"]),

            Dataset("Wlnu4000to6000",
                dataset="/WtoLNu-4Jets_MLNu-4000to6000_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v5/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu7"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.00001074*1.102,), 

            Dataset("Wlnu4000to6000_postBPix",
                dataset="/WtoLNu-4Jets_MLNu-4000to6000_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.00001074*1.102,
                tags=["postBPix"]),

            Dataset("Wlnu6000",
                dataset="/WtoLNu-4Jets_MLNu-6000_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu8"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.0000004198*1.084,), 

            Dataset("Wlnu6000_postBPix",
                dataset="/WtoLNu-4Jets_MLNu-6000_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v5/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.0000004198*1.084,
                tags=["postBPix"]),

        
            ### W + jets inclusive (NLO) ###

            Dataset("Wjets",
                dataset="/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wonshell"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=67710.0*0.9214,), # From SMP-22-017: Theoretical xs at NNNLO(QCD)xNLO(EWK) is 62390 pb ==> k-fact = 0.9214

            Dataset("Wjets_postBPix",
                dataset="/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wonshell_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=67710.0*0.9214,
                tags=["postBPix"]),

            ## DEPRECATED ==> The jet-binned samples are not needed anymore ##
            Dataset("Wjets_0J",
                dataset="/WtoLNu-2Jets_0J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W+2j_binned"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="preBPix",
                xs=55710,), 

            Dataset("Wjets_0J_postBPix",
                dataset="/WtoLNu-2Jets_0J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W+2j_binned_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="postBPix",
                xs=55710,
                tags=["postBPix"]),

            Dataset("Wjets_1J",
                dataset="/WtoLNu-2Jets_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("W+2j_binned"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preBPix",
                xs=9482,), 

            Dataset("Wjets_1J_postBPix",
                dataset="/WtoLNu-2Jets_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("W+2j_binned_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postBPix",
                xs=9482,
                tags=["postBPix"]),

            Dataset("Wjets_2J",
                dataset="/WtoLNu-2Jets_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("W+2j_binned"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preBPix",
                xs=3556,), 

            Dataset("Wjets_2J_postBPix",
                dataset="/WtoLNu-2Jets_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("W+2j_binned_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postBPix",
                xs=3556,
                tags=["postBPix"]),

            
            ### W boosted --> HT-binned ==> DEPRECATED ###

            Dataset("Wlnu_HT-40to100",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-40to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost0"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preBPix",
                xs=4265,), # From GenXSecAnalyzer (LO)

            Dataset("Wlnu_HT-40to100_postBPix",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-40to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postBPix",
                xs=4265, # inclusive k-factor from LO to NNLO
                tags=["postBPix"]),

            Dataset("Wlnu_HT-100to400",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost1"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preBPix",
                xs=1636,),

            Dataset("Wlnu_HT-100to400_postBPix",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postBPix",
                xs=1636,
                tags=["postBPix"]),

            Dataset("Wlnu_HT-400to800",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost2"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=59.70,),

            Dataset("Wlnu_HT-400to800_postBPix",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=59.70,
                tags=["postBPix"]),

            Dataset("Wlnu_HT-800to1500",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v5/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost3"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=6.211,),

            Dataset("Wlnu_HT-800to1500_postBPix",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=6.211,
                tags=["postBPix"]),

            Dataset("Wlnu_HT-1500to2500",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost4"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.4500,),

            Dataset("Wlnu_HT-1500to2500_postBPix",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.4500,
                tags=["postBPix"]),

            Dataset("Wlnu_HT-2500",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost5"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.03080,),

            Dataset("Wlnu_HT-2500_postBPix",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.03080,
                tags=["postBPix"]),

            ### W boosted --> ptLNu-binned ###
            
            Dataset("Wlnu_ptW-40to100_1J",
                dataset="/WtoLNu-2Jets_PTLNu-40to100_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW1"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preBPix",
                xs=4379*0.9214,), # From GenXSecAnalyzer (NLO) x NNLO k-factor from inclusive W+2j sample

            Dataset("Wlnu_ptW-40to100_1J_postBPix",
                dataset="/WtoLNu-2Jets_PTLNu-40to100_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postBPix",
                xs=4379*0.9214,
                tags=["postBPix"]),
            
            Dataset("Wlnu_ptW-40to100_2J",
                dataset="/WtoLNu-2Jets_PTLNu-40to100_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW1"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preBPix",
                xs=1604*0.9214,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-40to100_2J_postBPix",
                dataset="/WtoLNu-2Jets_PTLNu-40to100_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postBPix",
                xs=1604*0.9214,
                tags=["postBPix"]),
            
            Dataset("Wlnu_ptW-100to200_1J",
                dataset="/WtoLNu-2Jets_PTLNu-100to200_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW2"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preBPix",
                xs=367.5*0.9214,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-100to200_1J_postBPix",
                dataset="/WtoLNu-2Jets_PTLNu-100to200_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postBPix",
                xs=367.5*0.9214,
                tags=["postBPix"]),
            
            Dataset("Wlnu_ptW-100to200_2J",
                dataset="/WtoLNu-2Jets_PTLNu-100to200_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW2"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preBPix",
                xs=420.7*0.9214,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-100to200_2J_postBPix",
                dataset="/WtoLNu-2Jets_PTLNu-100to200_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postBPix",
                xs=420.7*0.9214,
                tags=["postBPix"]),
                    
            Dataset("Wlnu_ptW-200to400_1J",
                dataset="/WtoLNu-2Jets_PTLNu-200to400_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW3"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="preBPix",
                xs=25.63*0.9214,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-200to400_1J_postBPix",
                dataset="/WtoLNu-2Jets_PTLNu-200to400_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="postBPix",
                xs=25.63*0.9214,
                tags=["postBPix"]),
            
            Dataset("Wlnu_ptW-200to400_2J",
                dataset="/WtoLNu-2Jets_PTLNu-200to400_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW3"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="preBPix",
                xs=54.60*0.9214,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-200to400_2J_postBPix",
                dataset="/WtoLNu-2Jets_PTLNu-200to400_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="postBPix",
                xs=54.60*0.9214,
                tags=["postBPix"]),
                                    
            Dataset("Wlnu_ptW-400to600_1J",
                dataset="/WtoLNu-2Jets_PTLNu-400to600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW4"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.873*0.9214,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-400to600_1J_postBPix",
                dataset="/WtoLNu-2Jets_PTLNu-400to600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.873*0.9214,
                tags=["postBPix"]),
            
            Dataset("Wlnu_ptW-400to600_2J",
                dataset="/WtoLNu-2Jets_PTLNu-400to600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW4"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=3.124*0.9214,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-400to600_2J_postBPix",
                dataset="/WtoLNu-2Jets_PTLNu-400to600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=3.124*0.9214,
                tags=["postBPix"]),
                                                
            Dataset("Wlnu_ptW-600_1J",
                dataset="/WtoLNu-2Jets_PTLNu-600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW5"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.1025*0.9214,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-600_1J_postBPix",
                dataset="/WtoLNu-2Jets_PTLNu-600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.1025*0.9214,
                tags=["postBPix"]),
            
            Dataset("Wlnu_ptW-600_2J",
                dataset="/WtoLNu-2Jets_PTLNu-600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW5"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.5262*0.9214,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-600_2J_postBPix",
                dataset="/WtoLNu-2Jets_PTLNu-600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.5262*0.9214,
                tags=["postBPix"]),
            

            ### Top ###

            # TTbar

            Dataset("TT_2l2nu",
                dataset="/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="preBPix",
                xs=96.9,), # From TOP-22-012

            Dataset("TT_2l2nu_postBPix",
                dataset="/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="postBPix",
                xs=96.9,
                tags=["postBPix"]),

            Dataset("TT_lnu2q",
                dataset="/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preBPix",
                xs=404.0,), # From TOP-22-012

            Dataset("TT_lnu2q_postBPix",
                dataset="/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postBPix",
                xs=404.0,
                tags=["postBPix"]),

            # Single Top

            Dataset("ST_tW-lnu2q",
                dataset="/TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=19.31,), # From https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopNNLORef x BR

            Dataset("ST_tW-lnu2q_postBPix",
                dataset="/TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=19.31,
                tags=["postBPix"]),

            Dataset("ST_tW-2l2nu",
                dataset="/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=4.663,),

            Dataset("ST_tW-2l2nu_postBPix",
                dataset="/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=4.663,
                tags=["postBPix"]),

            Dataset("ST_tbarW-lnu2q",
                dataset="/TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v4/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=19.31,), 

            Dataset("ST_tbarW-lnu2q_postBPix",
                dataset="/TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=19.31,
                tags=["postBPix"]),

            Dataset("ST_tbarW-2l2nu",
                dataset="/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v4/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=4.663,), 

            Dataset("ST_tbarW-2l2nu_postBPix",
                dataset="/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=4.663,
                tags=["postBPix"]),

            Dataset("ST_s-top",
                dataset="/TBbartoLplusNuBbar-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=3.623,),

            Dataset("ST_s-top_postBPix",
                dataset="/TBbartoLplusNuBbar-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=3.623,
                tags=["postBPix"]),

            Dataset("ST_s-tbar",
                dataset="/TbarBtoLminusNuB-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=3.623,),

            Dataset("ST_s-tbar_postBPix",
                dataset="/TbarBtoLminusNuB-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postBPix"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=3.623,
                tags=["postBPix"]),

            Dataset("ST_t-top",
                dataset="/TBbarQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=145.0,),

            Dataset("ST_t-top_postBPix",
                dataset="/TBbarQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postBPix"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=145.0,
                tags=["postBPix"]),

            Dataset("ST_t-tbar",
                dataset="/TbarBQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=87.2,),

            Dataset("ST_t-tbar_postBPix",
                dataset="/TbarBQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postBPix"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=87.2,
                tags=["postBPix"]),

            ### Drell-Yan ###

            # ZtoMuMu

            Dataset("Zmumu_M-50to120",
                dataset="/DYto2Mu_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=2219.0,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-50to120_postBPix",
                dataset="/DYto2Mu_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=2219.0,
                tags=["postBPix"]),

            Dataset("Zmumu_M-120to200",
                dataset="/DYto2Mu_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=21.65,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-120to200_postBPix",
                dataset="/DYto2Mu_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=21.65,
                tags=["postBPix"]),

            Dataset("Zmumu_M-200to400",
                dataset="/DYto2Mu_MLL-200to400_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=3.058,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-200to400_postBPix",
                dataset="/DYto2Mu_MLL-200to400_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=3.058,
                tags=["postBPix"]),

            Dataset("Zmumu_M-400to800",
                dataset="/DYto2Mu_MLL-400to800_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.2691,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-400to800_postBPix",
                dataset="/DYto2Mu_MLL-400to800_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.2691,
                tags=["postBPix"]),

            Dataset("Zmumu_M-800to1500",
                dataset="/DYto2Mu_MLL-800to1500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.01915,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-800to1500_postBPix",
                dataset="/DYto2Mu_MLL-800to1500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.01915,
                tags=["postBPix"]),

            Dataset("Zmumu_M-1500to2500",
                dataset="/DYto2Mu_MLL-1500to2500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.001111,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-1500to2500_postBPix",
                dataset="/DYto2Mu_MLL-1500to2500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.001111,
                tags=["postBPix"]),

            Dataset("Zmumu_M-2500to4000",
                dataset="/DYto2Mu_MLL-2500to4000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.00005949,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-2500to4000_postBPix",
                dataset="/DYto2Mu_MLL-2500to4000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.00005949,
                tags=["postBPix"]),

            Dataset("Zmumu_M-4000to6000",
                dataset="/DYto2Mu_MLL-4000to6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.000001558,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-4000to6000_postBPix",
                dataset="/DYto2Mu_MLL-4000to6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.000001558,
                tags=["postBPix"]),

            Dataset("Zmumu_M-6000",
                dataset="/DYto2Mu_MLL-6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.00000003519,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-6000_postBPix",
                dataset="/DYto2Mu_MLL-6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.00000003519,
                tags=["postBPix"]),

            # ZtoTauTau

            Dataset("Ztautau_M-50to120",
                dataset="/DYto2Tau_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=2219.0,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-50to120_postBPix",
                dataset="/DYto2Tau_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=2219.0,
                tags=["postBPix"]),

            Dataset("Ztautau_M-120to200",
                dataset="/DYto2Tau_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=21.65,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-120to200_postBPix",
                dataset="/DYto2Tau_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=21.65,
                tags=["postBPix"]),

            Dataset("Ztautau_M-200to400",
                dataset="/DYto2Tau_MLL-200to400_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=3.058,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-200to400_postBPix",
                dataset="/DYto2Tau_MLL-200to400_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=3.058,
                tags=["postBPix"]),

            Dataset("Ztautau_M-400to800",
                dataset="/DYto2Tau_MLL-400to800_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.2691,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-400to800_postBPix",
                dataset="/DYto2Tau_MLL-400to800_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.2691,
                tags=["postBPix"]),

            Dataset("Ztautau_M-800to1500",
                dataset="/DYto2Tau_MLL-800to1500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.01915,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-800to1500_postBPix",
                dataset="/DYto2Tau_MLL-800to1500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.01915,
                tags=["postBPix"]),

            Dataset("Ztautau_M-1500to2500",
                dataset="/DYto2Tau_MLL-1500to2500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.001111,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-1500to2500_postBPix",
                dataset="/DYto2Tau_MLL-1500to2500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.001111,
                tags=["postBPix"]),

            Dataset("Ztautau_M-2500to4000",
                dataset="/DYto2Tau_MLL-2500to4000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.00005949,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-2500to4000_postBPix",
                dataset="/DYto2Tau_MLL-2500to4000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.00005949,
                tags=["postBPix"]),

            Dataset("Ztautau_M-4000to6000",
                dataset="/DYto2Tau_MLL-4000to6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.000001558,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-4000to6000_postBPix",
                dataset="/DYto2Tau_MLL-4000to6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.000001558,
                tags=["postBPix"]),

            Dataset("Ztautau_M-6000",
                dataset="/DYto2Tau_MLL-6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.00000003519,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-6000_postBPix",
                dataset="/DYto2Tau_MLL-6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.00000003519,
                tags=["postBPix"]),

            # ZtoNuNu

            Dataset("Znunu_HT-100to200",
                dataset="/Zto2Nu-4Jets_HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=273.5,), # From GenXSecAnalyzer (NLO)

            Dataset("Znunu_HT-100to200_postBPix",
                dataset="/Zto2Nu-4Jets_HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=273.5,
                tags=["postBPix"]),

            Dataset("Znunu_HT-200to400",
                dataset="/Zto2Nu-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=76.09,), # From GenXSecAnalyzer (NLO)

            Dataset("Znunu_HT-200to400_postBPix",
                dataset="/Zto2Nu-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=76.09,
                tags=["postBPix"]),

            Dataset("Znunu_HT-400to800",
                dataset="/Zto2Nu-4Jets_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=13.19,), # From GenXSecAnalyzer (NLO)

            Dataset("Znunu_HT-400to800_postBPix",
                dataset="/Zto2Nu-4Jets_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=13.19,
                tags=["postBPix"]),

            Dataset("Znunu_HT-800to1500",
                dataset="/Zto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=1.364,), # From GenXSecAnalyzer (NLO)

            Dataset("Znunu_HT-800to1500_postBPix",
                dataset="/Zto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=1.364,
                tags=["postBPix"]),

            Dataset("Znunu_HT-1500to2500",
                dataset="/Zto2Nu-4Jets_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.09843,), # From GenXSecAnalyzer (NLO)

            Dataset("Znunu_HT-1500to2500_postBPix",
                dataset="/Zto2Nu-4Jets_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.09843,
                tags=["postBPix"]),

            Dataset("Znunu_HT-2500",
                dataset="/Zto2Nu-4Jets_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.006699,), # From GenXSecAnalyzer (NLO)

            Dataset("Znunu_HT-2500_postBPix",
                dataset="/Zto2Nu-4Jets_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.006699,
                tags=["postBPix"]),


            ### DiBoson ###

            Dataset("WW_2l2nu",
                dataset="/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v4/"
                    "NANOAODSIM",
                process=self.processes.get("WW"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=12.98,), # From 13 TeV value with 4% expected increase with MCFM x BR

            Dataset("WW_2l2nu_postBPix",
                dataset="/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("WW_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=12.98,
                tags=["postBPix"]),

            Dataset("WW_lnu2q",
                dataset="/WWtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("WW"),
                runPeriod="preBPix",
                prefix="xrootd-es-cie.ciemat.es:1096//",
                xs=53.73,),

            Dataset("WW_lnu2q_postBPix",
                dataset="/WWtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("WW_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=53.73,
                tags=["postBPix"]),

            Dataset("WZ_2l2q",
                dataset="/WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("WZ"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=3.661,), # From MATRIX (SMP-22-017 at NNLO) x BR

            Dataset("WZ_2l2q_postBPix",
                dataset="/WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=3.661,
                tags=["postBPix"]),

            Dataset("WZ_3lnu",
                dataset="/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=1.769,),  

            Dataset("WZ_3lnu_postBPix",
                dataset="/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=1.769,
                tags=["postBPix"]),

            Dataset("WZ_lnu2q",
                dataset="/WZtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=12.39,),  

            Dataset("WZ_lnu2q_postBPix",
                dataset="/WZtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=12.39,
                tags=["postBPix"]),

            Dataset("ZZ",
                dataset="/ZZ_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ZZ"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=16.7,), # From MATRIX (SMP-22-017 at NNLO)

            Dataset("ZZ_postBPix",
                dataset="/ZZ_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ZZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=16.7,
                tags=["postBPix"]),

            ## Wgamma

            Dataset("Wg_pT-10to100",
                dataset="/WGtoLNuG-1Jets_PTG-10to100_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=668.6,), 

            Dataset("Wg_pT-10to100_postBPix",
                dataset="/WGtoLNuG-1Jets_PTG-10to100_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma_postBPix"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=668.6,
                tags=["postBPix"]),

            Dataset("Wg_pT-100to200",
                dataset="/WGtoLNuG-1Jets_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=2.224,), 

            Dataset("Wg_pT-100to200_postBPix",
                dataset="/WGtoLNuG-1Jets_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma_postBPix"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=2.224,
                tags=["postBPix"]),

            Dataset("Wg_pT-200to400",
                dataset="/WGtoLNuG-1Jets_PTG-200to400_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.2914,), 

            Dataset("Wg_pT-200to400_postBPix",
                dataset="/WGtoLNuG-1Jets_PTG-200to400_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.2914,
                tags=["postBPix"]),

            Dataset("Wg_pT-400to600",
                dataset="/WGtoLNuG-1Jets_PTG-400to600_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.02232,), 

            Dataset("Wg_pT-400to600_postBPix",
                dataset="/WGtoLNuG-1Jets_PTG-400to600_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.02232,
                tags=["postBPix"]),

            Dataset("Wg_pT-600",
                dataset="/WGtoLNuG-1Jets_PTG-600_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.004910,), 

            Dataset("Wg_pT-600_postBPix",
                dataset="/WGtoLNuG-1Jets_PTG-600_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.004910,
                tags=["postBPix"]),


            ### QCD ###

            Dataset("QCD_Pt-120to170",
                dataset="/QCD_PT-120to170_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=23150,), # From GenXSecAnalyzer

            Dataset("QCD_Pt-120to170_postBPix",
                dataset="/QCD_PT-120to170_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=23150,
                tags=["postBPix"]),

            Dataset("QCD_Pt-170to300",
                dataset="/QCD_PT-170to300_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=7760,), # From GenXSecAnalyzer

            Dataset("QCD_Pt-170to300_postBPix",
                dataset="/QCD_PT-170to300_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=7760,
                tags=["postBPix"]),

            Dataset("QCD_Pt-300to470",
                dataset="/QCD_PT-300to470_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=698.9,), # From GenXSecAnalyzer

            Dataset("QCD_Pt-300to470_postBPix",
                dataset="/QCD_PT-300to470_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=698.9,
                tags=["postBPix"]),

            Dataset("QCD_Pt-470to600",
                dataset="/QCD_PT-470to600_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=67.79,), # From GenXSecAnalyzer

            Dataset("QCD_Pt-470to600_postBPix",
                dataset="/QCD_PT-470to600_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=67.79,
                tags=["postBPix"]),

            Dataset("QCD_Pt-600to800",
                dataset="/QCD_PT-600to800_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=21.24,), # From GenXSecAnalyzer

            Dataset("QCD_Pt-600to800_postBPix",
                dataset="/QCD_PT-600to800_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=21.24,
                tags=["postBPix"]),

            Dataset("QCD_Pt-800to1000",
                dataset="/QCD_PT-800to1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=3.891,), # From GenXSecAnalyzer

            Dataset("QCD_Pt-800to1000_postBPix",
                dataset="/QCD_PT-800to1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=3.891,
                tags=["postBPix"]),

            Dataset("QCD_Pt-1000",
                dataset="/QCD_PT-1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=1.320,), # From GenXSecAnalyzer

            Dataset("QCD_Pt-1000_postBPix",
                dataset="/QCD_PT-1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=1.320,
                tags=["postBPix"]),

 
            ### DATA ###

            # PromptData: ReMini + ReNano CD

            Dataset("Data0_2023C_v1",
                dataset="/Muon0/Run2023C-22Sep2023_v1-v1/NANOAOD",
                process=self.processes.get("PromptData2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                runEra="Cv123",),

            Dataset("Data0_2023C_v2",
                dataset="/Muon0/Run2023C-22Sep2023_v2-v1/NANOAOD",
                process=self.processes.get("PromptData2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                runEra="Cv123",),

            Dataset("Data0_2023C_v3",
                dataset="/Muon0/Run2023C-22Sep2023_v3-v1/NANOAOD",
                process=self.processes.get("PromptData2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                runEra="Cv123",),

            Dataset("Data0_2023C_v4",
                dataset="/Muon0/Run2023C-22Sep2023_v4-v1/NANOAOD",
                process=self.processes.get("PromptData2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                runEra="Cv4",),

            Dataset("Data1_2023C_v1",
                dataset="/Muon1/Run2023C-22Sep2023_v1-v1/NANOAOD",
                process=self.processes.get("PromptData2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                runEra="Cv123",),

            Dataset("Data1_2023C_v2",
                dataset="/Muon1/Run2023C-22Sep2023_v2-v1/NANOAOD",
                process=self.processes.get("PromptData2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                runEra="Cv123",),

            Dataset("Data1_2023C_v3",
                dataset="/Muon1/Run2023C-22Sep2023_v3-v1/NANOAOD",
                process=self.processes.get("PromptData2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                runEra="Cv123",),

            Dataset("Data1_2023C_v4",
                dataset="/Muon1/Run2023C-22Sep2023_v4-v2/NANOAOD",
                process=self.processes.get("PromptData2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                runEra="Cv4",),

            Dataset("Data0_2023D_v1",
                dataset="/Muon0/Run2023D-22Sep2023_v1-v1/NANOAOD",
                process=self.processes.get("PromptData2023_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                runEra="D",
                tags=["postBPix"]),

            Dataset("Data0_2023D_v2",
                dataset="/Muon0/Run2023D-22Sep2023_v2-v1/NANOAOD",
                process=self.processes.get("PromptData2023_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                runEra="D",
                tags=["postBPix"]),

            Dataset("Data1_2023D_v1",
                dataset="/Muon1/Run2023D-22Sep2023_v1-v1/NANOAOD",
                process=self.processes.get("PromptData2023_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                runEra="D",
                tags=["postBPix"]),

            Dataset("Data1_2023D_v2",
                dataset="/Muon1/Run2023D-22Sep2023_v2-v1/NANOAOD",
                process=self.processes.get("PromptData2023_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                runEra="D",
                tags=["postBPix"]),


        ]
        return ObjectCollection(datasets)

    def add_features(self):
 
        ### Preselection Plots ###

        features_presel = [

            Feature("muon_pt", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)", binning=(50, 50, 2000),
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{#mu}"),
                units="GeV"),

            Feature("muon_eta", "Muon_eta.at(goodMuIdx)", binning=(50, -2.4, 2.4),
                x_title=Label("#mu #eta")),

            Feature("muon_eta_pt200", "Muon_eta.at(goodMuIdx)", binning=(50, -2.4, 2.4),
                selection="Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx) > 200.0",
                    x_title=Label("#mu #eta (p_{T}^{#mu} > 200 GeV)")),

            Feature("muon_phi", "Muon_phi.at(goodMuIdx)", binning=(50, -math.pi, math.pi),
                x_title=Label("#mu #phi"),
                units="rad"),

            Feature("muon_phi_pt200", "Muon_phi.at(goodMuIdx)", binning=(50, -math.pi, math.pi),
                selection="Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx) > 200.0",
                x_title=Label("#mu #phi (p_{T}^{#mu} > 200 GeV)"),
                units="rad"),

            Feature("MET_pt", "PuppiMET_pt", binning=(50, 0, 2000),
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{miss}"),
                units="GeV"),

            Feature("MET_phi", "PuppiMET_phi", binning=(50, -math.pi, math.pi),
                x_title=Label("p_{T}^{miss} #phi"),
                units="rad"),

            Feature("mT", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*PuppiMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - PuppiMET_phi)) )", binning=(60, 0, 4000),
                blinded_range=[1500,10000],
                x_title=Label("m_{T}"),
                units="GeV"),

            Feature("muonPt_over_MET", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)/PuppiMET_pt", binning=(50, 0, 6),
                x_title=Label("p_{T}^{#mu}/p_{T}^{miss}")),

            Feature("deltaPhi", "acos(cos(Muon_phi.at(goodMuIdx) - PuppiMET_phi))", binning=(50, 0, math.pi),
                x_title=Label("#Delta#phi(p_{T}^{#mu}, p_{T}^{miss})"),
                units="rad"),

            # PileUp plot
            Feature("nVertices", "PV_npvsGood", binning=(80, 0, 80),
                x_title=Label("# of vertices")),

            # Same plots with mT cut
            Feature("muon_pt_mT50", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)", binning=(50, 50, 2000),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{#mu} (m_{T} > 50 GeV)"),
                units="GeV"),

            Feature("muon_pt_mT50_tail", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)", binning=(50, 50, 4000),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{#mu} (m_{T} > 50 GeV)"),
                units="GeV"),

            Feature("muon_eta_mT50", "Muon_eta.at(goodMuIdx)", binning=(50, -2.4, 2.4),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("#mu #eta (m_{T} > 50 GeV)")),

            Feature("muon_phi_mT50", "Muon_phi.at(goodMuIdx)", binning=(50, -math.pi, math.pi),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("#mu #phi (m_{T} > 50 GeV)"),
                units="rad"),

            Feature("MET_pt_mT50", "PuppiMET_pt", binning=(50, 0, 2000),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{miss} (m_{T} > 50 GeV)"),
                units="GeV"),

           Feature("MET_pt_mT50_tail", "PuppiMET_pt", binning=(50, 0, 4000),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{miss} (m_{T} > 50 GeV)"),
                units="GeV"),

            Feature("MET_phi_mT50", "PuppiMET_phi", binning=(50, -math.pi, math.pi),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("p_{T}^{miss} #phi (m_{T} > 50 GeV)"),
                units="rad"),

            Feature("mT_mT50", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*PuppiMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - PuppiMET_phi)) )", binning=(60, 50, 4000),
                blinded_range=[1500,10000],
                x_title=Label("m_{T}"),
                units="GeV"),

            Feature("mT_mT50_tail", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*PuppiMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - PuppiMET_phi)) )", binning=(60, 50, 7000),
                blinded_range=[1500,10000],
                x_title=Label("m_{T}"),
                units="GeV"),

            Feature("muonPt_over_MET_mT50", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)/PuppiMET_pt", binning=(50, 0, 6),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("p_{T}^{#mu}/p_{T}^{miss} (m_{T} > 50 GeV)")),

            Feature("deltaPhi_mT50", "acos(cos(Muon_phi.at(goodMuIdx) - PuppiMET_phi))", binning=(50, 0, math.pi),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("#Delta#phi(p_{T}^{#mu}, p_{T}^{miss}) (m_{T} > 50 GeV)"),
                units="rad"),

            # Jet plots
            Feature("Njets", "nGoodJets", binning=(15, 0, 15),
                x_title=Label("Njets")),

            Feature("jet1_btagScore", "Jet_btagDeepFlavB.at(goodJets.at(0))", binning=(50, 0, 1),
                selection="nGoodJets > 0",
                x_title=Label("leading jet DeepJet score")),

            Feature("jet1_pt", "Jet_pt.at(goodJets.at(0))", binning=(50, 30, 1500),
		selection="nGoodJets > 0",
                x_title=Label("leading jet p_{T}"),
                units="GeV"),

	    Feature("jet1_eta", "Jet_eta.at(goodJets.at(0))", binning=(50, -2.5, 2.5),
		selection="nGoodJets > 0",
                x_title=Label("leading jet #eta")),

            Feature("jet1_phi", "Jet_phi.at(goodJets.at(0))", binning=(50, -math.pi, math.pi),
		selection="nGoodJets > 0",
                x_title=Label("leading jet #phi")),

            # Jet plots with mT cut
            Feature("Njets_mT50", "nGoodJets", binning=(15, 0, 15),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("Njets (m_{T} > 50 GeV)")),

            Feature("jet1_btagScore_mT50", "Jet_btagDeepFlavB.at(goodJets.at(0))", binning=(50, 0, 1),
                selection="nGoodJets > 0 && sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("leading jet DeepJet score (m_{T} > 50 GeV)")),

            Feature("jet1_pt_mT50", "Jet_pt.at(goodJets.at(0))", binning=(50, 30, 1500),
		selection="nGoodJets > 0 && sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("leading jet p_{T} (m_{T} > 50 GeV)"),
                units="GeV"),

	    Feature("jet1_eta_mT50", "Jet_eta.at(goodJets.at(0))", binning=(50, -2.5, 2.5),
		selection="nGoodJets > 0 && sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("leading jet #eta (m_{T} > 50 GeV)")),

            Feature("jet1_phi_mT50", "Jet_phi.at(goodJets.at(0))", binning=(50, -math.pi, math.pi),
		selection="nGoodJets > 0 && sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("leading jet #phi")),

            ##### JERC corrected jets #####

            Feature("CorrNjets", "nGoodJets_corr", binning=(15, 0, 15),
                x_title=Label("Njets corr.")),

            Feature("CorrJet1_btagScore", "Jet_btagDeepFlavB.at(goodJets_corr.at(0))", binning=(50, 0, 1),
                selection="nGoodJets_corr > 0",
                x_title=Label("leading jet DeepJet score corr.")),

            Feature("CorrJet1_pt", "CorrJet_pt.at(goodJets_corr.at(0))", binning=(50, 30, 1500),
		selection="nGoodJets_corr > 0",
                x_title=Label("leading jet p_{T} corr."),
                units="GeV"),

	    Feature("CorrJet1_eta", "Jet_eta.at(goodJets_corr.at(0))", binning=(50, -2.5, 2.5),
		selection="nGoodJets_corr > 0",
                x_title=Label("leading jet #eta corr.")),

            Feature("CorrJet1_phi", "Jet_phi.at(goodJets_corr.at(0))", binning=(50, -math.pi, math.pi),
		selection="nGoodJets_corr > 0",
                x_title=Label("leading jet #phi corr.")),

            # With mT cut
            Feature("CorrNjets_mT50", "nGoodJets_corr", binning=(15, 0, 15),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("Njets corr. (m_{T} > 50 GeV)")),

            Feature("CorrJet1_btagScore_mT50", "Jet_btagDeepFlavB.at(goodJets_corr.at(0))", binning=(50, 0, 1),
                selection="nGoodJets_corr > 0 && sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("leading jet DeepJet score corr. (m_{T} > 50 GeV)")),

            Feature("CorrJet1_pt_mT50", "CorrJet_pt.at(goodJets_corr.at(0))", binning=(50, 30, 1500),
		selection="nGoodJets_corr > 0 && sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("leading jet p_{T} corr. (m_{T} > 50 GeV)"),
                units="GeV"),

	    Feature("CorrJet1_eta_mT50", "Jet_eta.at(goodJets_corr.at(0))", binning=(50, -2.5, 2.5),
		selection="nGoodJets_corr > 0 && sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("leading jet #eta corr. (m_{T} > 50 GeV)")),

            Feature("CorrJet1_phi_mT50", "Jet_phi.at(goodJets_corr.at(0))", binning=(50, -math.pi, math.pi),
		selection="nGoodJets_corr > 0 && sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("leading jet #phi corr. (m_{T} > 50 GeV)")),

            ###### Type-I CorrMET ######

            Feature("T1CorrMET_pt", "TypeICorrMET_pt", binning=(50, 0, 2000),
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{miss} TypeI-corr."),
                units="GeV"),

            Feature("T1CorrMET_phi", "TypeICorrMET_phi", binning=(50, -math.pi, math.pi),
                x_title=Label("p_{T}^{miss} #phi TypeI-corr."),
                units="rad"),

            Feature("mT_T1CorrMET", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*TypeICorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - TypeICorrMET_phi)) )", binning=(60, 0, 4000),
                blinded_range=[1500,10000],
                x_title=Label("m_{T} TypeI-corr."),
                units="GeV"),

            Feature("muonPt_over_T1CorrMET", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)/TypeICorrMET_pt", binning=(50, 0, 6),
                x_title=Label("p_{T}^{#mu}/p_{T}^{miss} TypeI-corr.")),

            Feature("deltaPhi_T1Corr", "acos(cos(Muon_phi.at(goodMuIdx) - TypeICorrMET_phi))", binning=(50, 0, math.pi),
                x_title=Label("#Delta#phi(p_{T}^{#mu}, p_{T}^{miss}) TypeI-corr."),
                units="rad"),

            # With mT cut
            Feature("T1CorrMET_pt_mT50", "TypeICorrMET_pt", binning=(50, 0, 2000),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{miss} TypeI-corr. (m_{T} > 50 GeV)"),
                units="GeV"),

            Feature("T1CorrMET_phi_mT50", "TypeICorrMET_phi", binning=(50, -math.pi, math.pi),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("p_{T}^{miss} #phi TypeI-corr. (m_{T} > 50 GeV)"),
                units="rad"),

            Feature("mT_T1CorrMET_mT50", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*TypeICorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - TypeICorrMET_phi)) )", binning=(60, 50, 4000),
                blinded_range=[1500,10000],
                x_title=Label("m_{T} TypeI-corr."),
                units="GeV"),

            Feature("muonPt_over_T1CorrMET_mT50", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)/TypeICorrMET_pt", binning=(50, 0, 6),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("p_{T}^{#mu}/p_{T}^{miss} TypeI-corr. (m_{T} > 50 GeV)")),

            Feature("deltaPhi_T1Corr_mT50", "acos(cos(Muon_phi.at(goodMuIdx) - TypeICorrMET_phi))", binning=(50, 0, math.pi),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("#Delta#phi(p_{T}^{#mu}, p_{T}^{miss}) TypeI-corr. (m_{T} > 50 GeV)"),
                units="rad"),
            
            ###### Fully Corrected MET: Type-I + TuneP ######
            
            Feature("CorrMET_pt", "CorrMET_pt", binning=(50, 0, 2000),
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{miss} Corr."),
                units="GeV"),

            Feature("CorrMET_phi", "CorrMET_phi", binning=(50, -math.pi, math.pi),
                x_title=Label("p_{T}^{miss} #phi Corr."),
                units="rad"),

            Feature("mT_CorrMET", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) )", binning=(60, 0, 4000),
                blinded_range=[1500,10000],
                x_title=Label("m_{T} Corr."),
                units="GeV"),

            Feature("muonPt_over_CorrMET", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)/CorrMET_pt", binning=(50, 0, 6),
                x_title=Label("p_{T}^{#mu}/p_{T}^{miss} Corr.")),

            Feature("deltaPhi_Corr", "acos(cos(Muon_phi.at(goodMuIdx) - CorrMET_phi))", binning=(50, 0, math.pi),
                x_title=Label("#Delta#phi(p_{T}^{#mu}, p_{T}^{miss}) Corr."),
                units="rad"),

            # With mT cut
            Feature("CorrMET_pt_mT50", "CorrMET_pt", binning=(50, 0, 2000),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{miss} Corr. (m_{T} > 50 GeV)"),
                units="GeV"),
            
            Feature("CorrMET_pt_mT50_tail", "CorrMET_pt", binning=(50, 0, 4000),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{miss} Corr. (m_{T} > 50 GeV)"),
                units="GeV"),
            
            Feature("CorrMET_phi_mT50", "CorrMET_phi", binning=(50, -math.pi, math.pi),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("p_{T}^{miss} #phi Corr. (m_{T} > 50 GeV)"),
                units="rad"),

            Feature("mT_CorrMET_mT50", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) )", binning=(60, 50, 4000),
                blinded_range=[1500,10000],
                x_title=Label("m_{T} Corr."),
                units="GeV"),
            
            Feature("mT_CorrMET_mT50_tail", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) )", binning=(60, 50, 7000),
                blinded_range=[1500,10000],
                x_title=Label("m_{T} Corr."),
                units="GeV"),

            Feature("muonPt_over_CorrMET_mT50", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)/CorrMET_pt", binning=(50, 0, 6),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("p_{T}^{#mu}/p_{T}^{miss} Corr. (m_{T} > 50 GeV)")),

            Feature("deltaPhi_Corr_mT50", "acos(cos(Muon_phi.at(goodMuIdx) - CorrMET_phi))", binning=(50, 0, math.pi),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("#Delta#phi(p_{T}^{#mu}, p_{T}^{miss}) Corr. (m_{T} > 50 GeV)"),
                units="rad"),

            
            ### CHECKS FEDERICA ###
            Feature("muon_eta_pt200_MET0-30", "Muon_eta.at(goodMuIdx)", binning=(50, -2.4, 2.4),
                selection="Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx) > 200.0 && CorrMET_pt < 30.0",
                x_title=Label("#mu #eta (p_{T}^{#mu} > 200 GeV, p_{T}^{miss} < 30 GeV)")),

            Feature("muon_eta_pt200_MET30-100", "Muon_eta.at(goodMuIdx)", binning=(50, -2.4, 2.4),
                selection="Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx) > 200.0 && CorrMET_pt > 30.0 && CorrMET_pt < 100.0",
                x_title=Label("#mu #eta (p_{T}^{#mu} > 200 GeV, 30 GeV < p_{T}^{miss} < 100 GeV)")),

           Feature("muon_eta_pt200_MET100", "Muon_eta.at(goodMuIdx)", binning=(50, -2.4, 2.4),
                selection="Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx) > 200.0 && CorrMET_pt > 100.0",
                x_title=Label("#mu #eta (p_{T}^{#mu} > 200 GeV, p_{T}^{miss} > 100 GeV)")),
            #######################

        ]


        ### Kinematic-Selection Plots ###

        features_kinsel = [

            Feature("muon_pt", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)", binning=(50, 50, 2000),
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{#mu}"),
                units="GeV"),
            
            Feature("muon_pt_tail", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)", binning=(50, 50, 4000),
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{#mu}"),
                units="GeV"),
            
            ## Check!!
            Feature("muon_pt_eta2.1", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)", binning=(50, 50, 2000),
                selection="fabs(Muon_eta.at(goodMuIdx)) < 2.1",
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{#mu} (|#eta| < 2.1)"),
                units="GeV"),
            
            Feature("muon_eta", "Muon_eta.at(goodMuIdx)", binning=(50, -2.4, 2.4),
                x_title=Label("#mu #eta")),

            Feature("muon_eta_pt200", "Muon_eta.at(goodMuIdx)", binning=(50, -2.4, 2.4),
                selection="Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx) > 200.0",
                x_title=Label("#mu #eta (p_{T}^{#mu} > 200 GeV)")),

            Feature("muon_phi", "Muon_phi.at(goodMuIdx)", binning=(50, -math.pi, math.pi),
                x_title=Label("#mu #phi"),
                units="rad"),

            Feature("muon_phi_pt200", "Muon_phi.at(goodMuIdx)", binning=(50, -math.pi, math.pi),
                selection="Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx) > 200.0",
                x_title=Label("#mu #phi (p_{T}^{#mu} > 200 GeV)"),
                units="rad"),

            Feature("MET_pt", "PuppiMET_pt", binning=(50, 35, 2000),
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{miss}"),
                units="GeV"),

            Feature("MET_phi", "PuppiMET_phi", binning=(50, -math.pi, math.pi),
                x_title=Label("p_{T}^{miss} #phi"),
                units="rad"),

            Feature("mT", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*PuppiMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - PuppiMET_phi)) )", binning=(60, 80, 4000),
                blinded_range=[1500,10000],
                x_title=Label("m_{T}"),
                units="GeV"),
            
            ## Check!!
            Feature("mT_eta2.1", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*PuppiMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - PuppiMET_phi)) )", binning=(60, 80, 4000),
                selection="fabs(Muon_eta.at(goodMuIdx)) < 2.1",
                blinded_range=[1500,10000],
                x_title=Label("m_{T} (#mu |#eta| < 2.1)"),
                units="GeV"),

            Feature("muonPt_over_MET", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)/PuppiMET_pt", binning=(40, 0.4, 1.5),
                x_title=Label("p_{T}^{#mu}/p_{T}^{miss}")),

            Feature("deltaPhi", "acos(cos(Muon_phi.at(goodMuIdx) - PuppiMET_phi))", binning=(40, 2.5, math.pi),
                x_title=Label("#Delta#phi(p_{T}^{#mu}, p_{T}^{miss})"),
                units="rad"),

            # Jet plots
            Feature("Njets", "nGoodJets", binning=(8, 0, 8),
                x_title=Label("Njets")),

            Feature("jet1_btagScore", "Jet_btagDeepFlavB.at(goodJets.at(0))", binning=(50, 0, 1),
                selection="nGoodJets > 0",
                x_title=Label("leading jet DeepJet score")),

            Feature("jet1_pt", "Jet_pt.at(goodJets.at(0))", binning=(50, 30, 1500),
		selection="nGoodJets > 0",
                x_title=Label("leading jet p_{T}"),
                units="GeV"),

	    Feature("jet1_eta", "Jet_eta.at(goodJets.at(0))", binning=(50, -2.5, 2.5),
		selection="nGoodJets > 0",
                x_title=Label("leading jet #eta")),

            # PileUp plot
            Feature("nVertices", "PV_npvsGood", binning=(80, 0, 80),
                x_title=Label("# of vertices")),
            
            ##### JERC corrected jets #####
            Feature("CorrNjets", "nGoodJets_corr", binning=(8, 0, 8),
                x_title=Label("Njets corr.")),

            Feature("CorrJet1_btagScore", "Jet_btagDeepFlavB.at(goodJets_corr.at(0))", binning=(50, 0, 1),
                selection="nGoodJets_corr > 0",
                x_title=Label("leading jet DeepJet score corr.")),

            Feature("CorrJet1_pt", "CorrJet_pt.at(goodJets_corr.at(0))", binning=(50, 30, 1500),
		selection="nGoodJets_corr > 0",
                x_title=Label("leading jet p_{T} corr."),
                units="GeV"),

	    Feature("CorrJet1_eta", "Jet_eta.at(goodJets_corr.at(0))", binning=(50, -2.5, 2.5),
		selection="nGoodJets_corr > 0",
                x_title=Label("leading jet #eta corr.")),            

            ###### Type-I CorrMET ######
            Feature("T1CorrMET_pt", "TypeICorrMET_pt", binning=(50, 35, 2000),
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{miss} TypeI-corr."),
                units="GeV"),

            Feature("T1CorrMET_phi", "TypeICorrMET_phi", binning=(50, -math.pi, math.pi),
                x_title=Label("p_{T}^{miss} #phi TypeI-corr."),
                units="rad"),

            Feature("mT_T1CorrMET", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*TypeICorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - TypeICorrMET_phi)) )", binning=(60, 80, 4000),
                blinded_range=[1500,10000],
                x_title=Label("m_{T} TypeI-corr."),
                units="GeV"),

            Feature("muonPt_over_T1CorrMET", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)/TypeICorrMET_pt", binning=(40, 0.4, 1.5),
                x_title=Label("p_{T}^{#mu}/p_{T}^{miss} TypeI-corr.")),

            Feature("deltaPhi_T1Corr", "acos(cos(Muon_phi.at(goodMuIdx) - TypeICorrMET_phi))", binning=(40, 2.5, math.pi),
                x_title=Label("#Delta#phi(p_{T}^{#mu}, p_{T}^{miss}) TypeI-corr."),
                units="rad"),

            ###### Fully Corrected MET: Type-I + TuneP ######            
            Feature("CorrMET_pt", "CorrMET_pt", binning=(50, 35, 2000),
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{miss} Corr."),
                units="GeV"),

            Feature("CorrMET_pt_tail", "CorrMET_pt", binning=(50, 35, 4000),
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{miss} Corr."),
                units="GeV"),
            
            Feature("CorrMET_phi", "CorrMET_phi", binning=(50, -math.pi, math.pi),
                x_title=Label("p_{T}^{miss} #phi Corr."),
                units="rad"),

            Feature("mT_CorrMET", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) )", binning=(60, 80, 4000),
                blinded_range=[1500,10000],
                x_title=Label("m_{T} Corr."),
                units="GeV"),

            Feature("mT_CorrMET_tail", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) )", binning=(60, 80, 7000),
                blinded_range=[1500,10000],
                x_title=Label("m_{T} Corr."),
                units="GeV"),
            
            Feature("muonPt_over_CorrMET", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)/CorrMET_pt", binning=(40, 0.4, 1.5),
                x_title=Label("p_{T}^{#mu}/p_{T}^{miss} Corr.")),

            Feature("deltaPhi_Corr", "acos(cos(Muon_phi.at(goodMuIdx) - CorrMET_phi))", binning=(40, 2.5, math.pi),
                x_title=Label("#Delta#phi(p_{T}^{#mu}, p_{T}^{miss}) Corr."),
                units="rad"),
            
        ]


        ### GEN-Level Plots ###

        gen_features = [

            Feature("muon_pt", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)", binning=(100, 50, 2500),
                x_title=Label("p_{T}^{#mu}"),
                units="GeV"),

            Feature("MET_pt", "PuppiMET_pt", binning=(100, 0, 2500),
                x_title=Label("p_{T}^{miss}"),
                units="GeV"),

            Feature("mT", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*PuppiMET_pt*(1 - cos(deltaPhi_MuMET)) )", binning=(200, 0, 7000),
                x_title=Label("M_{T}"),
                units="GeV"),

            Feature("genJet_HT_peak", "genHT", binning=(200, 0, 400),
                x_title=Label("GenJet HT"),
                units="GeV"),

            Feature("genJet_HT_tail", "genHT", binning=(200, 0, 4000),
                x_title=Label("GenJet HT"),
                units="GeV"),

            # LHE distributions

            Feature("lhe_Wmass_peak", "lhe_Wmass", binning=(200, 0, 500),
                x_title=Label("LHE m_{W}"),
                units="GeV"),

            Feature("lhe_Wmass_tail", "lhe_Wmass", binning=(200, 0, 7000),
                x_title=Label("LHE m_{W}"),
                units="GeV"),

            Feature("lhe_Wpt", "lhe_Wpt", binning=(200, 0, 2000),
                x_title=Label("LHE W p_{T}"),
                units="GeV"),

            Feature("lhe_HT_peak", "LHE_HT", binning=(200, 0, 400),
                x_title=Label("LHE HT"),
                units="GeV"),

            Feature("lhe_HT_tail", "LHE_HT", binning=(200, 0, 4000),
                x_title=Label("LHE HT"),
                units="GeV"),

            Feature("lhe_muonPt", "lhe_muonPt", binning=(100, 50, 2500),
                x_title=Label("LHE p_{T}^{#mu}"),
                units="GeV"),

            Feature("lhe_nuPt", "lhe_nuPt", binning=(100, 0, 2500),
                x_title=Label("LHE p_{T}^{miss}"),
                units="GeV"),

            Feature("lhe_mT", "lhe_mT", binning=(200, 0, 7000),
                x_title=Label("LHE M_{T}"),
                units="GeV"),

            #Feature("lhe_dPhi_munu", "lhe_dPhi_munu", binning=(200, -1.05, 1.05),
            #    x_title=Label("LHE cos(#Delta#phi_{#mu#nu})")),

            #Feature("lhe_dPhi_munu_mT300", "lhe_dPhi_munu", binning=(200, -1.05, 1.05),
            #    selection="lhe_mT > 300",
            #    x_title=Label("LHE cos(#Delta#phi_{#mu#nu})")),

        ]

        
        ### EXTAR: Oscar Plots --> Check behavior of jets ###
        jet_features = [
            Feature("jet1_pt", "Jet_pt.at(0)", binning=(50, 0, 1500),
                selection="nJet > 0",
                x_title=Label("Leading jet p_{T}"),
                units="GeV"),

            Feature("jets_eta", "Jet_eta", binning=(50, -4, 4),
                x_title=Label("jets #eta")),

            Feature("jet1_Id", "Jet_jetId.at(0)", binning=(8, -1, 7),
                selection="nJet > 0",
                x_title=Label("Leading jet ID")),

            Feature("jets_Id", "Jet_jetId", binning=(8, -1, 7),
                x_title=Label("jets ID")),

            Feature("minDphi_mujet", "minDphi_mujet", binning=(50, -math.pi, math.pi),
                selection="nJet > 0",
                x_title=Label("min #Delta#phi(#mu,jet)"),
                units="rad"),

            Feature("dRmin_mujet", "dRmin_mujet", binning=(80, 0, 0.8),
                selection="jet_idx != -1",
                x_title=Label("min #DeltaR(#mu,jet)")),

            Feature("Jet_over_Muon_pt", "Jet_pt.at(jet_idx)/Muon_pt.at(goodMuIdx)", binning=(80, 0, 3),
                selection="jet_idx != -1",
                x_title=Label("p_{T}^{j}/p_{T}^{#mu}")),
        ]
                
        ### EXTRA: MET object review ###

        features_MET = [
                        
            Feature("CorrMET_pt_mT50", "CorrMET_pt", binning=(50, 0, 2000),
                selection="nGoodJets < 2 && sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                blinded_range=[750,10000],
                x_title=Label("p_{T}^{miss} corr. m_{T} > 50 GeV &&  Njets < 2"),
                units="GeV"),

            Feature("CorrMET_phi_mT50", "CorrMET_phi", binning=(50, -math.pi, math.pi),
                selection="nGoodJets < 2 && sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("p_{T}^{miss} #phi corr. m_{T} > 50 GeV && # Njets < 2"),
                units="rad"),
         
            Feature("muonPt_over_CorrMET_mT50", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)/CorrMET_pt", binning=(50, 0, 6),
                selection="nGoodJets < 2 && sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("p_{T}^{#mu}/p_{T}^{miss} corr. m_{T} > 50 GeV && Njets < 2")),

            Feature("deltaPhi_Corr_mT50", "acos(cos(Muon_phi.at(goodMuIdx) - CorrMET_phi))", binning=(50, 0, math.pi),
                selection="nGoodJets < 2 && sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("#Delta#phi(p_{T}^{#mu}, p_{T}^{miss}) corr. m_{T} > 50 GeV && Njets < 2"),
                units="rad"),
            
            Feature("acoplanarity_mT50", "1.0 - acos(cos(Muon_phi.at(goodMuIdx) - CorrMET_phi))/M_PI", binning=(50, 0, 1),
                selection="nGoodJets < 2 && sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("Acoplanarity(#mu, MET) corr. m_{T} > 50 GeV && Njets < 2")),
            
            ### Different MET checks ###
            Feature("PFMET_pt", "MET_pt", binning=(50, 0, 2000),
                blinded_range=[750,10000],
                x_title=Label("PF p_{T}^{miss}"),
                units="GeV"),

            Feature("PFMET_phi", "MET_phi", binning=(50, -math.pi, math.pi),
                x_title=Label("PF p_{T}^{miss} #phi"),
                units="rad"),
            
            Feature("TkMET_pt", "TkMET_pt", binning=(50, 0, 2000),
                blinded_range=[750,10000],
                x_title=Label("Tracker p_{T}^{miss}"),
                units="GeV"),

            Feature("TkMET_phi", "TkMET_phi", binning=(50, -math.pi, math.pi),
                x_title=Label("Tracker p_{T}^{miss} #phi"),
                units="rad"),

            Feature("CaloMET_pt", "CaloMET_pt", binning=(50, 0, 2000),
                blinded_range=[750,10000],
                x_title=Label("Calo p_{T}^{miss}"),
                units="GeV"),

            Feature("CaloMET_phi", "CaloMET_phi", binning=(50, -math.pi, math.pi),
                x_title=Label("Calo p_{T}^{miss} #phi"),
                units="rad"),

            ############################
        ]
        
        features_BtagEff = [
            
            Feature("Jet_pt_b", "Jet_pt_b",
                binning=[30, 50, 70, 100, 140, 200, 300, 600, 1000],
                x_title=Label("b jet p_{T}"),
                units="GeV"),

            Feature("Jet_pt_b_btag", "Jet_pt_b_btag",
                binning=[30, 50, 70, 100, 140, 200, 300, 600, 1000],
                x_title=Label("b-tagged b jet p_{T}"),
                units="GeV"),
                       
            Feature("Jet_pt_c", "Jet_pt_c",
                binning=[30, 50, 70, 100, 140, 200, 300, 600, 1000],
                x_title=Label("c jet p_{T}"),
                units="GeV"),

            Feature("Jet_pt_c_btag", "Jet_pt_c_btag",
                binning=[30, 50, 70, 100, 140, 200, 300, 600, 1000],
                x_title=Label("b-tagged c jet p_{T}"),
                units="GeV"),
                       
            Feature("Jet_pt_uds", "Jet_pt_uds",
                binning=[30, 50, 70, 100, 140, 200, 300, 600, 1000],
                x_title=Label("light jet p_{T}"),
                units="GeV"),

            Feature("Jet_pt_uds_btag", "Jet_pt_uds_btag",
                binning=[30, 50, 70, 100, 140, 200, 300, 600, 1000],
                x_title=Label("b-tagged light jet p_{T}"),
                units="GeV"),
        ]

        #### Features for Top Control Regions ####
        
        features_TopCR = [
            
            Feature("muon_eta", "Muon_eta.at(goodMuIdx)", binning=(50, -2.4, 2.4),
                x_title=Label("#mu #eta")),

            Feature("muon_phi", "Muon_phi.at(goodMuIdx)", binning=(50, -math.pi, math.pi),
                x_title=Label("#mu #phi"),
                units="rad"),

            Feature("CorrNjets", "nGoodJets_corr", binning=(8, 0, 8),
                x_title=Label("Njets")),

            Feature("CorrJets_btagScore", "Jet_btagDeepFlavB", binning=(50, 0, 1),
                x_title=Label("jet DeepJet score")),

            Feature("CorrJet1_btagScore", "Jet_btagDeepFlavB.at(goodJets_corr.at(0))", binning=(50, 0, 1),
                x_title=Label("leading jet DeepJet score")),
            
            Feature("muon_eta_mT50", "Muon_eta.at(goodMuIdx)", binning=(50, -2.4, 2.4),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("#mu #eta (m_{T} > 50 GeV)")),

            Feature("muon_phi_mT50", "Muon_phi.at(goodMuIdx)", binning=(50, -math.pi, math.pi),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("#mu #phi (m_{T} > 50 GeV)"),
                units="rad"),

            Feature("CorrNjets_mT50", "nGoodJets_corr", binning=(8, 0, 8),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("Njets (m_{T} > 50 GeV)")),

            Feature("CorrJets_btagScore_mT50", "Jet_btagDeepFlavB", binning=(50, 0, 1),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("jet DeepJet score (m_{T} > 50 GeV)")),

            Feature("CorrJet1_btagScore_mT50", "Jet_btagDeepFlavB.at(goodJets_corr.at(0))", binning=(50, 0, 1),
                selection="sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) ) > 50.0",
                x_title=Label("leading jet DeepJet score (m_{T} > 50 GeV)")),
            
        ]
        
        #### mT for limit extraction ####
        
        mT_limit = [

            Feature("mT", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*CorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - CorrMET_phi)) )", binning=(67, 300, 7000),
                x_title=Label("m_{T}"),
                units="GeV"),
        ]
        
        return ObjectCollection(mT_limit)

    def add_versions(self):
        versions = {}
        return versions

    def add_weights(self):
        weights = DotDict()
        weights.default = "1"

        weights.total_events_weights = ["genWeight", "puWeight"]

        weights.preselection  = ["genWeight", "puWeight", "mu_idSF_weight", "mu_isoSF_weight", "mu_hltSF_weight", "mu_recoSF_weight", "btag_weight"]

        return weights

    def add_systematics(self):
        systematics = []

        return ObjectCollection(systematics)

    def add_default_module_files(self):
        defaults = {}
        return defaults

    def get_inner_text_for_plotting(self, category, region):
        inner_text = ""
        #inner_text=[category.label + " category"]
        if region:
            if isinstance(region.label, list):
                inner_text += region.label
            else:
                inner_text.append(region.label)
        return inner_text


config = Config("base", year=2023, ecm=13.6, lumi_pb=27101)
