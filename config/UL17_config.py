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
            Category("preselection_UL17", "GEMethod Preselection for UL17", selection = "nMuon > 1"),
        ]
        return ObjectCollection(categories)

    def add_processes(self):

        processes = [
            Process("DrellYan", Label("DY"), color=ROOT.kAzure+1),
            Process("DY", Label("Z #rightarrow #tau#tau"), color=(255,255,0), isDY=True, parent_process="DrellYan"), # YA NO SE USA
            #Process("Zmumu", Label("Z #rightarrow #mu#mu off-shell"), color=ROOT.kBlue+1, parent_process="DrellYan"), # Para HT checks
            #Process("DY_HT", Label("Z boosted"), color=(206,30,30), isHTbin=True, parent_process="DrellYan"), # Para HT checks, quitar el indice en los datasets

            # Muestras buenas para plots normales
            Process("Zmumu1", Label("Zmumu_50-120"), color=(255, 241, 0), isFirstMbin=True, parent_process="DrellYan"),
            Process("Zmumu2", Label("Zmumu_120-200"), color=(255, 140, 0), parent_process="DrellYan"),
            Process("Zmumu3", Label("Zmumu_200-400"), color=(232, 17, 35), parent_process="DrellYan"),
            Process("Zmumu4", Label("Zmumu_400-800"), color=(236, 0, 140), parent_process="DrellYan"),
            Process("Zmumu5", Label("Zmumu_800-1400"), color=(104, 33, 122), parent_process="DrellYan"),
            Process("Zmumu6", Label("Zmumu_1400-2300"), color=(0, 24, 143), parent_process="DrellYan"),
            Process("Zmumu7", Label("Zmumu_2300-3500"), color=(0, 188, 242), parent_process="DrellYan"),
            Process("Zmumu8", Label("Zmumu_3500-4500"), color=(0, 178, 148), parent_process="DrellYan"),
            Process("Zmumu9", Label("Zmumu_4500-6000"), color=(0, 158, 73), parent_process="DrellYan"),
            Process("Zmumu10", Label("Zmumu_6000-Inf"), color=(186, 216, 10), parent_process="DrellYan"),

            # Para plots de HT checks
            #Process("Zmumu1", Label("Z #rightarrow #mu#mu on-shell"), color=ROOT.kAzure+10, isFirstMbin=True, parent_process="DrellYan"),
            #Process("Zmumu2", Label("Zmumu_120-200"), color=(255, 140, 0), parent_process="Zmumu"),
            #Process("Zmumu3", Label("Zmumu_200-400"), color=(232, 17, 35), parent_process="Zmumu"),
            #Process("Zmumu4", Label("Zmumu_400-800"), color=(236, 0, 140), parent_process="Zmumu"),
            #Process("Zmumu5", Label("Zmumu_800-1400"), color=(104, 33, 122), parent_process="Zmumu"),
            #Process("Zmumu6", Label("Zmumu_1400-2300"), color=(0, 24, 143), parent_process="Zmumu"),
            #Process("Zmumu7", Label("Zmumu_2300-3500"), color=(0, 188, 242), parent_process="Zmumu"),
            #Process("Zmumu8", Label("Zmumu_3500-4500"), color=(0, 178, 148), parent_process="Zmumu"),
            #Process("Zmumu9", Label("Zmumu_4500-6000"), color=(0, 158, 73), parent_process="Zmumu"),
            #Process("Zmumu10", Label("Zmumu_6000-Inf"), color=(186, 216, 10), parent_process="Zmumu"),

            # Para plots normales
            Process("DY_HT0", Label("DY_HT-100to200"), color=(0, 178, 148), isHTbin=True, parent_process="DrellYan"), #BORRAR
            Process("DY_HT1", Label("DY_HT-200to400"), color=(255, 140, 0), isHTbin=True, parent_process="DrellYan"),
            Process("DY_HT2", Label("DY_HT-400to600"), color=(232, 17, 35), isHTbin=True, parent_process="DrellYan"),
            Process("DY_HT3", Label("DY_HT-600to800"), color=(236, 0, 140), isHTbin=True, parent_process="DrellYan"),
            Process("DY_HT4", Label("DY_HT-800to1200"), color=(104, 33, 122), isHTbin=True, parent_process="DrellYan"),
            Process("DY_HT5", Label("DY_HT-1200to2500"), color=(0, 24, 143), isHTbin=True, parent_process="DrellYan"),
            Process("DY_HT6", Label("DY_HT-2500toInf"), color=(0, 188, 242), isHTbin=True, parent_process="DrellYan"),

            # Nuevas muestras binadas en ptZ
            Process("DY_PtZ", Label("DY_PtZ"), color=(0, 178, 148), isHTbin=True, parent_process="DrellYan"),

            Process("Top", Label("Top"), color=(36, 147, 25)),
            Process("TTbar", Label("TT"), color=(255, 153, 0), isTT=True, parent_process="Top"),
            Process("TTbar_high", Label("TT"), color=(255, 153, 0), parent_process="Top"),
            Process("ST", Label("ST"), color=(255, 153, 0), parent_process="Top"),

            Process("DiBoson", Label("DiBoson"), color=(206, 30, 30)),
            Process("WZ", Label("WZ"), color=(134, 136, 138), parent_process="DiBoson"),
            Process("WW", Label("WW"), color=(134, 136, 138), parent_process="DiBoson"),
            Process("ZZ", Label("ZZ"), color=(134, 136, 138), parent_process="DiBoson"),

            Process("DataUL17", Label("DATA"), color=(0, 0, 0), isData=True),
        ]

        process_group_names = {

            "UL17": [
                "DrellYan",
                "Top",
                "DiBoson",
                "DataUL17",
            ],
            "Zmumu_binned": [
                "Zmumu1",
                "Zmumu2",
                "Zmumu3",
                "Zmumu4",
                "Zmumu5",
                "Zmumu6",
                "Zmumu7",
                "Zmumu8",
                "Zmumu9",
                "Zmumu10",
            ],
            "HT_checks": [
                #"DY",
                "Zmumu1",
                "Zmumu",
                "DY_HT",
            ],
            "HT_binned": [
                #"DY_HT0",
                "DY_HT1",
                "DY_HT2",
                "DY_HT3",
                "DY_HT4",
                "DY_HT5",
                "DY_HT6",
            ],

        }

        return ObjectCollection(processes), process_group_names


    def prefix_datasets(self, datasets, prefix):

        for dataset in datasets:
            dataset.prefix = prefix + '//'


    def add_datasets(self):
        datasets = [
            Dataset("DY",
                dataset="/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/"
                    "NANOAODSIM",
                process=self.processes.get("DY"),
                # prefix="xrootd-cms.infn.it//",
                xs=5765.4, # Paper Zprime AN-2018/011 (NNLO)
                tags=["ul"]),

            Dataset("Zmumu_M-50to120",
                dataset="/ZToMuMu_M-50To120_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu1"),
                # prefix="xrootd-cms.infn.it//",
                xs=2112.904, # Taken from AN-2018/011 (NLO), scalable to NNLO by k-factors?
                tags=["ul"]),

            Dataset("Zmumu_M-120to200",
                dataset="/ZToMuMu_M-120To200_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu2"),
                # prefix="xrootd-cms.infn.it//",
                xs=20.553,
                tags=["ul"]),

            Dataset("Zmumu_M-200to400",
                dataset="/ZToMuMu_M-200To400_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu3"),
                # prefix="xrootd-cms.infn.it//",
                xs=2.886,
                tags=["ul"]),

            Dataset("Zmumu_M-400to800",
                dataset="/ZToMuMu_M-400To800_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu4"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.2517,
                tags=["ul"]),

            Dataset("Zmumu_M-800to1400",
                dataset="/ZToMuMu_M-800To1400_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu5"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.01707,
                tags=["ul"]),

            Dataset("Zmumu_M-1400to2300",
                dataset="/ZToMuMu_M-1400To2300_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu6"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.001366,
                tags=["ul"]),

            Dataset("Zmumu_M-2300to3500",
                dataset="/ZToMuMu_M-2300To3500_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu7"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.00008178,
                tags=["ul"]),

            Dataset("Zmumu_M-3500to4500",
                dataset="/ZToMuMu_M-3500To4500_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu8"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.000003191,
                tags=["ul"]),

            Dataset("Zmumu_M-4500to6000",
                dataset="/ZToMuMu_M-4500To6000_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu9"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.0000002787,
                tags=["ul"]),

            Dataset("Zmumu_M-6000toInf",
                dataset="/ZToMuMu_M-6000ToInf_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu10"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.000000009569,
                tags=["ul"]),

            Dataset("DY_HT-100to200",
                dataset="/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_HT0"),
                # prefix="xrootd-cms.infn.it//",
                #xs=160.7, # DAS
                #xs=147.4, # AN2019-107
                xs=139.2*1.23, # DAS new * kfactor
                tags=["ul"]),

            Dataset("DY_HT-200to400",
                dataset="/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_HT1"),
                # prefix="xrootd-cms.infn.it//",
                #xs=48.63, # DAS
                #xs=40.99, # AN2019-107
                xs=38.4*1.23, # DAS new * kfactor
                tags=["ul"]),

            Dataset("DY_HT-400to600",
                dataset="/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_HT2"),
                # prefix="xrootd-cms.infn.it//",
                #xs=6.993,
                #xs=5.678,
                xs=5.174*1.23, # DAS new * kfactor
                tags=["ul"]),

            Dataset("DY_HT-600to800",
                dataset="/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_HT3"),
                # prefix="xrootd-cms.infn.it//",
                #xs=1.761,
                #xs=1.367,
                xs=1.258*1.23, # DAS new * kfactor
                tags=["ul"]),

            Dataset("DY_HT-800to1200",
                dataset="/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_HT4"),
                # prefix="xrootd-cms.infn.it//",
                #xs=0.8021,
                #xs=0.6304,
                xs=0.5598*1.23, # DAS new * kfactor
                tags=["ul"]),

            Dataset("DY_HT-1200to2500",
                dataset="/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_HT5"),
                # prefix="xrootd-cms.infn.it//",
                #xs=0.1937,
                #xs=0.1514,
                xs=0.1305*1.23, # DAS new * kfactor
                tags=["ul"]),

            Dataset("DY_HT-2500toInf",
                dataset="/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_HT6"),
                # prefix="xrootd-cms.infn.it//",
                #xs=0.003514,
                #xs=0.003565,
                xs=0.002997*1.23, # DAS new * kfactor
                tags=["ul"]),

            Dataset("TT_2l2nu",
                dataset="/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar"),
                # prefix="xrootd-cms.infn.it//",
                xs=87.31, # AN-2018/011 (NNLO)
                tags=["ul"]),

            Dataset("TT_semilep",
                dataset="/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar"),
                # prefix="xrootd-cms.infn.it//",
                xs=365.34, # DAS (NNLO)
                tags=["ul"]),

            Dataset("TT_Mtt-700to1000",
                dataset="/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar_high"),
                # prefix="xrootd-cms.infn.it//",
                xs=66.85, # DAS (NLO)
                tags=["ul"]),

            Dataset("TT_Mtt-1000toInf",
                dataset="/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar_high"),
                # prefix="xrootd-cms.infn.it//",
                xs=16.42, # DAS (NLO)
                tags=["ul"]),

            Dataset("ST_t-top",
                dataset="/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                # prefix="xrootd-cms.infn.it//",
                xs=115.3, # DAS (NLO)
                tags=["ul"]),

            Dataset("ST_t-antitop",
                dataset="/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                # prefix="xrootd-cms.infn.it//",
                xs=69.09, # DAS (NLO)
                tags=["ul"]),

            Dataset("ST_tW-top",
                dataset="/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                # prefix="xrootd-cms.infn.it//",
                xs=35.6, # AN-2018/011 (NNLO)
                tags=["ul"]),

            Dataset("ST_tW-antitop",
                dataset="/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                # prefix="xrootd-cms.infn.it//",
                xs=35.6, # AN-2018/011 (NNLO)
                tags=["ul"]),

            Dataset("ST_s",
                dataset="/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                # prefix="xrootd-cms.infn.it//",
                xs=3.549, # DAS (unknown)
                tags=["ul"]),

            Dataset("WZ",
                dataset="/WZ_TuneCP5_13TeV-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("WZ"),
                # prefix="xrootd-cms.infn.it//",
                    xs=47.13, # AN-2018/011 (NLO) ==> En DAS 27.6 (LO)
                tags=["ul"]),

            Dataset("WW",
                dataset="/WW_TuneCP5_13TeV-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("WW"),
                # prefix="xrootd-cms.infn.it//",
                    xs=118.7, # AN-2018/011 (NNLO) ==> En DAS 75.95 (LO)
                tags=["ul"]),

            Dataset("ZZ",
                dataset="/ZZ_TuneCP5_13TeV-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("ZZ"),
                # prefix="xrootd-cms.infn.it//",
                    xs=16.523, # AN-2018/011 (NLO) ==> En DAS 12.14 (LO)
                tags=["ul"]),



            Dataset("DY_PtZ-0to50",
                dataset="/DYJetsToLL_LHEFilterPtZ-0To50_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_PtZ"),
                # prefix="xrootd-cms.infn.it//",
                xs=1485.0, # DAS (unknown)
                tags=["ul"]),

            Dataset("DY_PtZ-50to100",
                dataset="/DYJetsToLL_LHEFilterPtZ-50To100_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_PtZ"),
                # prefix="xrootd-cms.infn.it//",
                xs=397.4, # DAS (unknown)
                #xs=354.3, # Jan
                tags=["ul"]),

            Dataset("DY_PtZ-100to250",
                dataset="/DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_PtZ"),
                # prefix="xrootd-cms.infn.it//",
                xs=97.2, # DAS (unknown)
                #xs=83.12, # Jan
                tags=["ul"]),

            Dataset("DY_PtZ-250to400",
                dataset="/DYJetsToLL_LHEFilterPtZ-250To400_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_PtZ"),
                # prefix="xrootd-cms.infn.it//",
                xs=3.701, # DAS (unknown)
                #xs=3.047, # Jan
                tags=["ul"]),

            Dataset("DY_PtZ-400to650",
                dataset="/DYJetsToLL_LHEFilterPtZ-400To650_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_PtZ"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.5086, # DAS (unknown)
                #xs=0.3921, # Jan
                tags=["ul"]),

            Dataset("DY_PtZ-650toInf",
                dataset="/DYJetsToLL_LHEFilterPtZ-650ToInf_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/"
                    "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_PtZ"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.04728, # DAS (unknown)
                #xs=0.03636, # Jan
                tags=["ul"]),


            Dataset("DataUL17_B",
                dataset="/SingleMuon/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD",
                process=self.processes.get("DataUL17"),
                # prefix="xrootd-cms.infn.it//",
                tags=["ul"]),

            Dataset("DataUL17_C",
                dataset="/SingleMuon/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD",
                process=self.processes.get("DataUL17"),
                # prefix="xrootd-cms.infn.it//",
                tags=["ul"]),

            Dataset("DataUL17_D",
                dataset="/SingleMuon/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD",
                process=self.processes.get("DataUL17"),
                # prefix="xrootd-cms.infn.it//",
                tags=["ul"]),

            Dataset("DataUL17_E",
                dataset="/SingleMuon/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD",
                process=self.processes.get("DataUL17"),
                # prefix="xrootd-cms.infn.it//",
                tags=["ul"]),

            Dataset("DataUL17_F",
                dataset="/SingleMuon/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD",
                process=self.processes.get("DataUL17"),
                # prefix="xrootd-cms.infn.it//",
                tags=["ul"]),

        ]
        return ObjectCollection(datasets)

    def add_features(self):
        
        ### Feature selections ###
        barrel_dimu   = "fabs(Muon_eta.at(mu1_index)) < 1.2 || fabs(Muon_eta.at(mu2_index)) < 1.2"
        endcap_dimu   = "(fabs(Muon_eta.at(mu1_index)) > 1.2 && fabs(Muon_eta.at(mu1_index)) < 2.1) || (fabs(Muon_eta.at(mu2_index)) > 1.2 && fabs(Muon_eta.at(mu2_index)) < 2.1)"
        forwardE_dimu = "fabs(Muon_eta.at(mu1_index)) > 2.1 || fabs(Muon_eta.at(mu2_index)) > 2.1"

        ### Labels for Selections ###
        axis_barrel   = " |#eta| < 1.2"
        axis_endcap   = " 1.2 < |#eta| < 2.1"
        axis_forwardE = " |#eta| > 2.1"
 
        features = [
            # Curvature
            Feature("kappa_mu1", "1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))", binning=(50, -5., 5.),
                x_title=Label("#mu_{1} #kappa"),
                units="TeV^{-1}"),
            Feature("kappa_mu2", "1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))", binning=(50, -5., 5.),
                x_title=Label("#mu_{2} #kappa"),
                units="TeV^{-1}"),
            Feature("kappa", "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)), 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))})", binning=(50, -5., 5.),
                x_title=Label("#kappa"),
                units="TeV^{-1}"),

            Feature("kappa_barrel", "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(fabs(Muon_eta.at(mu1_index)) <= 1.2)), 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(fabs(Muon_eta.at(mu2_index)) <= 1.2))})", binning=(50, -5., 5.),
                selection=barrel_dimu,
                x_title=Label("#kappa"+axis_barrel),
                units="TeV^{-1}"),
            Feature("kappa_endcap", "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(fabs(Muon_eta.at(mu1_index)) > 1.2 && fabs(Muon_eta.at(mu1_index)) <= 2.1) ), 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(fabs(Muon_eta.at(mu2_index)) > 1.2 && fabs(Muon_eta.at(mu2_index)) <= 2.1) )})", binning=(50, -5., 5.),
                selection=endcap_dimu,
                x_title=Label("#kappa"+axis_endcap),
                units="TeV^{-1}"),
            Feature("kappa_forwardE", "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(fabs(Muon_eta.at(mu1_index)) > 2.1)), 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(fabs(Muon_eta.at(mu2_index)) > 2.1))})", binning=(50, -5., 5.),
                selection=forwardE_dimu,
                x_title=Label("#kappa"+axis_forwardE),
                units="TeV^{-1}"),
            
            # pT single muons
            Feature("pt_mu1", "Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)", binning=(50, 0, 2200),
                x_title=Label("#mu_{1} p_{T}"),
                units="GeV"),
            Feature("pt_mu2", "Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)", binning=(50, 0, 2200),
                x_title=Label("#mu_{2} p_{T}"),
                units="GeV"),
            Feature("pt_muPlus", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == 1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == 1))",
                binning=(50, 0, 2200),
                x_title=Label("#mu^{+} p_{T}"),
                units="GeV"),
            Feature("pt_muMinus", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == -1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == -1))",
                binning=(50, 0, 2200),
                x_title=Label("#mu^{-} p_{T}"),
                units="GeV"),

            Feature("pt_muPlus_barrel", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == 1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == 1))", 
                binning=(50, 0, 2200),
                selection=barrel_dimu,
                x_title=Label("#mu^{+} p_{T}"+axis_barrel),
                units="GeV"),
            Feature("pt_muMinus_barrel", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == -1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == -1))", 
                binning=(50, 0, 2200),
                selection=barrel_dimu,
                x_title=Label("#mu^{-} p_{T}"+axis_barrel),
                units="GeV"),
            Feature("pt_muPlus_endcap", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == 1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == 1))", 
                binning=(50, 0, 2200),
                selection=endcap_dimu,
                x_title=Label("#mu^{+} p_{T}"+axis_endcap),
                units="GeV"),
            Feature("pt_muMinus_endcap", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == -1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == -1))", 
                binning=(50, 0, 2200),
                selection=endcap_dimu,
                x_title=Label("#mu^{-} p_{T}"+axis_endcap),
                units="GeV"),
            Feature("pt_muPlus_forwardE", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == 1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == 1))", 
                binning=(50, 0, 2200),
                selection=forwardE_dimu,
                x_title=Label("#mu^{+} p_{T}"+axis_forwardE),
                units="GeV"),
            Feature("pt_muMinus_forwardE", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == -1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == -1))", 
                binning=(50, 0, 2200),
                selection=forwardE_dimu,
                x_title=Label("#mu^{-} p_{T}"+axis_forwardE),
                units="GeV"),
            
            # pT Z
            Feature("pt_Z_peak", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 400),
                x_title=Label("p_{T_{#mu#mu}}"),
                units="GeV"),
            Feature("pt_Z_tail", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 2200),
                x_title=Label("p_{T_{#mu#mu}}"),
                units="GeV"),

            Feature("pt_Z_peak_barrel", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 400),
                selection=barrel_dimu,
                x_title=Label("p_{T_{#mu#mu}}"+axis_barrel),
                units="GeV"),
            Feature("pt_Z_peak_endcap", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 400),
                selection=endcap_dimu,
                x_title=Label("p_{T_{#mu#mu}}"+axis_endcap),
                units="GeV"),
            Feature("pt_Z_peak_forwardE", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 400),
                selection=forwardE_dimu,
                x_title=Label("p_{T_{#mu#mu}}"+axis_forwardE),
                units="GeV"),
            Feature("pt_Z_tail_barrel", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 2200),
                selection=barrel_dimu,
                x_title=Label("p_{T_{#mu#mu}}"+axis_barrel),
                units="GeV"),
            Feature("pt_Z_tail_endcap", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 2200),
                selection=endcap_dimu,
                x_title=Label("p_{T_{#mu#mu}}"+axis_endcap),
                units="GeV"),
            Feature("pt_Z_tail_forwardE", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 2200),
                selection=forwardE_dimu,
                x_title=Label("p_{T_{#mu#mu}}"+axis_forwardE),
                units="GeV"),
            
            # Mass Z
            Feature("Z_mass_peak", "DiMuon_invM", binning=(50, 60, 120),
                x_title=Label("M_{#mu#mu}"),
                units="GeV"),
            Feature("Z_mass_tail", "DiMuon_invM", binning=(50, 0, 5000),
                x_title=Label("M_{#mu#mu}"),
                units="GeV"),

            Feature("Z_mass_peak_barrel", "DiMuon_invM", binning=(50, 60, 120),
                selection=barrel_dimu,
                x_title=Label("M_{#mu#mu}"+axis_barrel),
                units="GeV"),
            Feature("Z_mass_peak_endcap", "DiMuon_invM", binning=(50, 60, 120),
                selection=endcap_dimu,
                x_title=Label("M_{#mu#mu}"+axis_endcap),
                units="GeV"),
            Feature("Z_mass_peak_forwardE", "DiMuon_invM", binning=(50, 60, 120),
                selection=forwardE_dimu,
                x_title=Label("M_{#mu#mu}"+axis_forwardE),
                units="GeV"),
            Feature("Z_mass_tail_barrel", "DiMuon_invM", binning=(50, 0, 5000),
                selection=barrel_dimu,
                x_title=Label("M_{#mu#mu}"+axis_barrel),
                units="GeV"),
            Feature("Z_mass_tail_endcap", "DiMuon_invM", binning=(50, 0, 5000),
                selection=endcap_dimu,
                x_title=Label("M_{#mu#mu}"+axis_endcap),
                units="GeV"),
            Feature("Z_mass_tail_forwardE", "DiMuon_invM", binning=(50, 0, 5000),
                selection=forwardE_dimu,
                x_title=Label("M_{#mu#mu}"+axis_forwardE),
                units="GeV"),
            
            # Eta and Phi
            Feature("eta", "std::vector<float>({Muon_eta.at(mu1_index), Muon_eta.at(mu2_index)})", binning=(50, -2.5, 2.5),
                x_title=Label("#eta")),
            Feature("phi", "std::vector<float>({Muon_phi.at(mu1_index), Muon_phi.at(mu2_index)})", binning=(50, -3.2, 3.2),
                x_title=Label("#phi"),
                units="rad"),


            # WEIGHTS
            Feature("L1PreFiringWeight", "L1PreFiringWeight", binning=(20, 0, 2),
                x_title=Label("L1PreFiringWeight"),
                central="prefiring_nom"),
                #systematics=["prefiring_syst"]),
        ]

        ### GEN LEVEL PLOTS ###

        gen_features = [

            #Feature("mu1_genPt", "GenPart_pt.at(Muon_genPartIdx.at(mu1_index))", binning=(50, 0, 2200),
            #    x_title=Label("gen #mu_{1} p_{T}"),
            #    selection="Muon_genPartIdx.at(mu1_index)>-1",
            #    units="GeV"),
            #Feature("mu2_genPt", "GenPart_pt.at(Muon_genPartIdx.at(mu2_index))", binning=(50, 0, 2200),
            #    x_title=Label("gen #mu_{2} p_{T}"),
            #    selection="Muon_genPartIdx.at(mu2_index)>-1",
            #    units="GeV"),

#UNCOMMENT
            Feature("Z_genPt_tail", "sqrt((GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))+(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))+2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index)))*cos(GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))+sin(GenPart_phi.at(Muon_genPartIdx.at(mu1_index)))*sin(GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))))", binning=(200, 0, 2200),
                x_title=Label("gen p_{T_{#mu#mu}}"),
                selection="Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1",
                units="GeV"),
            Feature("Z_genPt_peak", "sqrt((GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))+(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))+2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index)))*cos(GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))+sin(GenPart_phi.at(Muon_genPartIdx.at(mu1_index)))*sin(GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))))", binning=(200, 0, 500),
                x_title=Label("gen p_{T_{#mu#mu}}"),
                selection="Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1",
                units="GeV"),

#UNCOMMENT
            Feature("Z_genM_tail_1", "sqrt(2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cosh(GenPart_eta.at(Muon_genPartIdx.at(mu1_index))-GenPart_eta.at(Muon_genPartIdx.at(mu2_index)))-cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index))-2*3.1416)))", binning=(200, 0, 4000),
                selection="(Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1) && (GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))>3.1416",
                x_title=Label("gen M_{#mu#mu}"),
                units="GeV"),
            #Feature("Z_genM_tail_2", "sqrt(2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cosh(GenPart_eta.at(Muon_genPartIdx.at(mu1_index))-GenPart_eta.at(Muon_genPartIdx.at(mu2_index)))-cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index))+2*3.1416)))", binning=(50, 0, 5000),
            #    selection="(Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1) && (GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))<-3.1416",
            #    x_title=Label("gen M_{#mu#mu}"),
            #    units="GeV"),
#UNCOMMENT
            Feature("Z_genM_peak_1", "sqrt(2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cosh(GenPart_eta.at(Muon_genPartIdx.at(mu1_index))-GenPart_eta.at(Muon_genPartIdx.at(mu2_index)))-cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index))-2*3.1416)))", binning=(200, 0, 300),
                selection="(Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1) && (GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))>3.1416",
                x_title=Label("gen M_{#mu#mu}"),
                units="GeV"),
#UNCOMMENT
            Feature("LHE_HT_tail", "LHE_HT", binning=(200, 0, 4000),
                x_title=Label("LHE HT"),
                units="GeV"),
            Feature("LHE_HT_peak", "LHE_HT", binning=(200, 0, 500),
                x_title=Label("LHE HT"),
                units="GeV"),

            Feature("LHE_Zpt_peak", "LHE_Vpt", binning=(200, 0, 500),
                x_title=Label("LHE p_{T_{#mu#mu}}"),
                units="GeV"),
            Feature("LHE_Zpt_tail", "LHE_Vpt", binning=(200, 0, 2200),
                x_title=Label("LHE p_{T_{#mu#mu}}"),
                units="GeV"),


            # WEIGHTS
            Feature("L1PreFiringWeight", "L1PreFiringWeight", binning=(20, 0, 2),
                x_title=Label("L1PreFiringWeight"),
                central="prefiring_nom"),
                #systematics=["prefiring_syst"]),
            
        ]

        ### ptZ Reweight Histo ###
        ptZ_feature = [
            Feature("ptZ", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", 
                binning=(100, 0, 1500),
                x_title=Label("p_{T_{#mu#mu}}"),
                units="GeV"),

            # WEIGHTS
            Feature("L1PreFiringWeight", "L1PreFiringWeight", binning=(20, 0, 2),
                x_title=Label("L1PreFiringWeight"),
                central="prefiring_nom"),
                #systematics=["prefiring_syst"]),

        ]
    
        ### Curvature with Bias ###
        biases = []

        # Curvature regions
        etas = [-2.4, -2.1, -1.2, 0, 1.2, 2.1, 2.4]
        phis_deg = [-180, -60, 60, 180]
        phis = [-math.pi, -math.pi/3.0, math.pi/3.0, math.pi]
        axis = []
        selections = []

        for i in range(len(etas)-1):
            for j in range(len(phis)-1):
                axis.append(str(etas[i])+" < #eta < "+str(etas[i+1]) + " , " + str(phis_deg[j])+" < #phi < "+str(phis_deg[j+1]))

                selections.append( "(Muon_eta.at(mu1_index) > " + str(etas[i]) + " && Muon_eta.at(mu1_index) <= " + str(etas[i+1]) + " && Muon_phi.at(mu1_index) > " + str(phis[j]) + " && Muon_phi.at(mu1_index) <= " + str(phis[j+1]) + ") || (Muon_eta.at(mu2_index) > " + str(etas[i]) + " && Muon_eta.at(mu2_index) <= " + str(etas[i+1]) + " && Muon_phi.at(mu2_index) > " + str(phis[j]) + " && Muon_phi.at(mu2_index) <= " + str(phis[j+1]) + ")" )

        #bin_sel = [(20, -5., 5.) if i==0 or i==1 or i==2 or i==15 or i==16 or i==17 else (50, -5., 5.) for i in range(len(selections))]
        var_bin = [-9,-8.5,-8,-7.5,-7,-6.5,-6,-5.5,-5,-4.5,-4,-3.5,-3,-2,0,2,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9]
        #var_bin = [-7,-6.5,-6,-5.5,-5,-4.5,-4,-3.5,-3,-2,0,2,3,3.5,4,4.5,5,5.5,6,6.5,7]
        #bin_sel = [var_bin if i==0 or i==1 or i==2 or i==15 or i==16 or i==17 else (50, -5., 5.) for i in range(len(selections))] # Nuevo -> Variable
        bin_sel = [(60, -9., 9.) if i==0 or i==1 or i==2 or i==15 or i==16 or i==17 else (60, -5., 5.) for i in range(len(selections))] # General for rebin


        feature_bias = [
            # WEIGHTS
            Feature("L1PreFiringWeight", "L1PreFiringWeight", binning=(20, 0, 2),
                x_title=Label("L1PreFiringWeight"),
                central="prefiring_nom"),
        ]

        for i in range (161):
            biases.append(round(-0.8 + 0.01*i, 2))
        for bias in biases:
            #feature_bias.append( Feature("kappa_%s" %bias, "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)) + (float)%s, 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)) + (float)%s})" %(bias, bias), 
            #    binning=(50, -5., 5.),
            #    x_title=Label("#kappa"),
            #    units="TeV^{-1}"), )
            for x,sel in enumerate(selections):
                feature_bias.append( Feature("kappa_%s_%s" %(x,bias), "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(mu1_region == %s)) + (float)%s, 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(mu2_region == %s)) + (float)%s})" %(x, bias, x, bias), 
                    binning=bin_sel[x],
                    selection=sel,
                    x_title=Label("#kappa  " + axis[x]),
                    units="TeV^{-1}"), )

        return ObjectCollection(feature_bias) #Cambiar

    def add_versions(self):
        versions = {}
        return versions

    def add_weights(self):
        weights = DotDict()
        weights.default = "1"

        weights.total_events_weights = ["genWeight", "puWeight"]

        weights.preselection_UL17 = ["genWeight", "puWeight", "mu_idSF_weight", "mu_isoSF_weight", "mu_trigSF_weight", "mu_recoSF_weight", "L1PreFiringWeight", "ptZweight"]

        return weights

    def add_systematics(self):
        systematics = [
            Systematic("prefiring_nom", "_Nom"),
            #Systematic("perfiring_syst", "", up="_Up", down="_Dn")
            ]

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


config = Config("base", year=2017, ecm=13, lumi_fb=41.48)
