from analysis_tools import ObjectCollection, Category, Process, Dataset, Feature, Systematic
from analysis_tools.utils import DotDict
from analysis_tools.utils import join_root_selection as jrs
from plotting_tools import Label
from collections import OrderedDict
import ROOT

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

        # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation102X
        self.btag=DotDict(tight=0.7264, medium=0.2770, loose=0.0494)

        self.channels = self.add_channels()
        self.regions = self.add_regions()
        self.categories = self.add_categories()
        self.processes, self.process_group_names = self.add_processes()
        self.datasets = self.add_datasets()
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

    def add_regions(self):
        pass

    def add_channels(self):
        pass

    def add_categories(self):

        categories = [
            Category("base", "base category", selection = ""),
            Category("preselection_UL18", "GEMethod Preselection for UL18", selection = "nMuon > 1 && (HLT_Mu50 == 1 || HLT_TkMu100 == 1 || HLT_OldMu100 == 1)")
        ]
        return ObjectCollection(categories)

    def add_processes(self):

        processes = [
            Process("DrellYan", Label("DY"), color=ROOT.kAzure+1), # (13,182,241)
            Process("DY", Label("DY"), color=(255, 102, 102), isDY=True, parent_process="DrellYan"),
            Process("Zmumu", Label("Zmumu"), color=(255, 102, 102), parent_process="DrellYan"),

            Process("Top", Label("Top"), color=(36, 147, 25)), # (17,168,31)
            Process("TTbar", Label("TT"), color=(255, 153, 0), isTT=True, parent_process="Top"),
            Process("TTbar_high", Label("TT"), color=(255, 153, 0), parent_process="Top"),
            Process("ST", Label("ST"), color=(255, 153, 0), parent_process="Top"),

            Process("DiBoson", Label("DiBoson"), color=(206, 30, 30)), # (230,28,28)
            Process("WZ", Label("WZ"), color=(134, 136, 138), parent_process="DiBoson"),
            Process("WW", Label("WW"), color=(134, 136, 138), parent_process="DiBoson"),
            Process("ZZ", Label("ZZ"), color=(134, 136, 138), parent_process="DiBoson"),

            Process("DataUL18", Label("DATA"), color=(0, 0, 0), isData=True),
            Process("DataUL18_BAD", Label("DATA"), color=(0, 0, 0), isData=True),
        ]

        process_group_names = {
            "UL18_bad": [
                "DrellYan",
                "Top",
                "DiBoson",
                "DataUL18_BAD",
            ],
            "UL18_corrected": [
                "DrellYan",
                "Top",
                "DiBoson",
                "DataUL18",
            ]
        }

        return ObjectCollection(processes), process_group_names

    def add_datasets(self):
        datasets = [
            Dataset("DY",
                dataset="/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("DY"),
                # prefix="xrootd-cms.infn.it//",
                xs=5765.4, # Paper Zprime AN-2018/011 (NNLO)
                tags=["ul"]),

            Dataset("Zmumu_M-50to120",
                dataset="/ZToMuMu_M-50To120_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                # prefix="xrootd-cms.infn.it//",
                xs=2112.904, # Taken from AN-2018/011 (NLO), scalable to NNLO by k-factors?
                tags=["ul"]),

            Dataset("Zmumu_M-120to200",
                dataset="/ZToMuMu_M-120To200_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                # prefix="xrootd-cms.infn.it//",
                xs=20.553,
                tags=["ul"]),

            Dataset("Zmumu_M-200to400",
                dataset="/ZToMuMu_M-200To400_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                # prefix="xrootd-cms.infn.it//",
                xs=2.886,
                tags=["ul"]),

            Dataset("Zmumu_M-400to800",
                dataset="/ZToMuMu_M-400To800_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.2517,
                tags=["ul"]),

            Dataset("Zmumu_M-800to1400",
                dataset="/ZToMuMu_M-800To1400_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.01707,
                tags=["ul"]),

            Dataset("Zmumu_M-1400to2300",
                dataset="/ZToMuMu_M-1400To2300_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.001366,
                tags=["ul"]),

            Dataset("Zmumu_M-2300to3500",
                dataset="/ZToMuMu_M-2300To3500_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.00008178,
                tags=["ul"]),

            Dataset("Zmumu_M-3500to4500",
                dataset="/ZToMuMu_M-3500To4500_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.000003191,
                tags=["ul"]),

            Dataset("Zmumu_M-4500to6000",
                dataset="/ZToMuMu_M-4500To6000_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.0000002787,
                tags=["ul"]),

            Dataset("Zmumu_M-6000toInf",
                dataset="/ZToMuMu_M-6000ToInf_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.000000009569,
                tags=["ul"]),

            Dataset("TT_2l2nu",
                dataset="/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar"),
                # prefix="xrootd-cms.infn.it//",
                xs=87.31, # AN-2018/011 (NNLO)
                tags=["ul"]),

            Dataset("TT_semilep",
                dataset="/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar"),
                # prefix="xrootd-cms.infn.it//",
                xs=365.34, # DAS (NNLO)
                tags=["ul"]),

            Dataset("TT_Mtt-700to1000",
                dataset="/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar_high"),
                # prefix="xrootd-cms.infn.it//",
                xs=66.85, # DAS (NLO)
                tags=["ul"]),

            Dataset("TT_Mtt-1000toInf",
                dataset="/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar_high"),
                # prefix="xrootd-cms.infn.it//",
                xs=16.42, # DAS (NLO)
                tags=["ul"]),

            Dataset("ST_t-top",
                dataset="/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                # prefix="xrootd-cms.infn.it//",
                xs=115.3, # DAS (NLO)
                tags=["ul"]),

            Dataset("ST_t-antitop",
                dataset="/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                # prefix="xrootd-cms.infn.it//",
                xs=69.09, # DAS (NLO)
                tags=["ul"]),

            Dataset("ST_tW-top",
                dataset="/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                # prefix="xrootd-cms.infn.it//",
                xs=35.6, # AN-2018/011 (NNLO)
                tags=["ul"]),

            Dataset("ST_tW-antitop",
                dataset="/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                # prefix="xrootd-cms.infn.it//",
                xs=35.6, # AN-2018/011 (NNLO)
                tags=["ul"]),

            Dataset("ST_s",
                dataset="/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                # prefix="xrootd-cms.infn.it//",
                xs=3.549, # DAS (unknown)
                tags=["ul"]),

            Dataset("WZ",
                dataset="/WZ_TuneCP5_13TeV-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("WZ"),
                # prefix="xrootd-cms.infn.it//",
                    xs=47.13, # AN-2018/011 (NLO) ==> En DAS 27.6 (LO)
                tags=["ul"]),

            Dataset("WW",
                dataset="/WW_TuneCP5_13TeV-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("WW"),
                # prefix="xrootd-cms.infn.it//",
                    xs=118.7, # AN-2018/011 (NNLO) ==> En DAS 75.95 (LO)
                tags=["ul"]),

            Dataset("ZZ",
                dataset="/ZZ_TuneCP5_13TeV-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("ZZ"),
                # prefix="xrootd-cms.infn.it//",
                    xs=16.523, # AN-2018/011 (NLO) ==> En DAS 12.14 (LO)
                tags=["ul"]),

            Dataset("DataUL18_A_BAD",
                dataset="/SingleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD",
                process=self.processes.get("DataUL18_BAD"),
                # prefix="xrootd-cms.infn.it//",
                tags=["ul"]),

            Dataset("DataUL18_B_BAD",
                dataset="/SingleMuon/Run2018B-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD",
                process=self.processes.get("DataUL18_BAD"),
                # prefix="xrootd-cms.infn.it//",
                tags=["ul"]),

            Dataset("DataUL18_C_BAD",
                dataset="/SingleMuon/Run2018C-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD",
                process=self.processes.get("DataUL18_BAD"),
                # prefix="xrootd-cms.infn.it//",
                tags=["ul"]),

            Dataset("DataUL18_D_BAD",
                dataset="/SingleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD",
                process=self.processes.get("DataUL18_BAD"),
                # prefix="xrootd-cms.infn.it//",
                tags=["ul"]),

            Dataset("DataUL18_A",
                dataset="/SingleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD",
                process=self.processes.get("DataUL18"),
                # prefix="xrootd-cms.infn.it//",
                tags=["ul"]),

            Dataset("DataUL18_B",
                dataset="/SingleMuon/Run2018B-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD",
                process=self.processes.get("DataUL18"),
                # prefix="xrootd-cms.infn.it//",
                tags=["ul"]),

            Dataset("DataUL18_C",
                dataset="/SingleMuon/Run2018C-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD",
                process=self.processes.get("DataUL18"),
                # prefix="xrootd-cms.infn.it//",
                tags=["ul"]),

            Dataset("DataUL18_D",
                dataset="/SingleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD",
                process=self.processes.get("DataUL18"),
                # prefix="xrootd-cms.infn.it//",
                tags=["ul"]),

        ]
        return ObjectCollection(datasets)

    def add_features(self):
        features = [

            # lepton features
            Feature("kappa_mu1", "1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))", binning=(50, -5., 5.),
                x_title=Label("#mu_{1} #kappa"),
                units="TeV^{-1}"),
            Feature("kappa_mu2", "1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))", binning=(50, -5., 5.),
                x_title=Label("#mu_{2} #kappa"),
                units="TeV^{-1}"),
            Feature("kappa", "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)), 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))})", binning=(50, -5., 5.),
                x_title=Label("#kappa"),
                units="TeV^{-1}"),
            Feature("pt_mu1", "Muon_pt.at(mu1_index)", binning=(50, 0, 1800),
                x_title=Label("#mu_{1} p_t"),
                units="GeV"),
            Feature("pt_mu2", "Muon_pt.at(mu2_index)", binning=(50, 0, 1800),
                x_title=Label("#mu_{2} p_t"),
                units="GeV"),
            Feature("pt_Z_peak", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 400),
                x_title=Label("p_{t_{#mu#mu}}"),
                units="GeV"),
            Feature("pt_Z_tail", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 1800),
                x_title=Label("p_{t_{#mu#mu}}"),
                units="GeV"),
            Feature("Z_mass_peak", "DiMuon_invM", binning=(50, 60, 120),
                x_title=Label("M_{#mu#mu}"),
                units="GeV"),
            Feature("Z_mass_tail", "DiMuon_invM", binning=(50, 0, 6200),
                x_title=Label("M_{#mu#mu}"),
                units="GeV"),
            Feature("eta", "std::vector<float>({Muon_eta.at(mu1_index), Muon_eta.at(mu2_index)})", binning=(50, -2.5, 2.5),
                x_title=Label("#eta")),
            Feature("phi", "std::vector<float>({Muon_phi.at(mu1_index), Muon_phi.at(mu2_index)})", binning=(50, -3.2, 3.2),
                x_title=Label("#phi"),
                units="rad"),

        ]
        return ObjectCollection(features)

    def add_versions(self):
        versions = {}
        return versions

    def add_weights(self):
        weights = DotDict()
        weights.default = "1"
        weights.total_events_weights = ["genWeight", "puWeight"]
        weights.channels = {
            "preselection_UL18": ["genWeight", "puWeight"],
            #"mutau": ["genWeight", "puWeight", "prescaleWeight", "trigSF",
            #    "L1PreFiringWeight_Nom", "PUjetID_SF"
            #],
            # "DYscale_MTT"],
        }
        return weights

    def add_systematics(self):
        systematics = []
            #Systematic("jet_smearing", "_nom"),
            #Systematic("empty", "", up="", down="")
            #]
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
        if "[" in feature_expression:  # derived expression
            while "[" in feature_expression:
                initial = feature_expression.find("[")
                final = feature_expression.find("]")
                feature_name_to_look = feature_expression[initial + 1: final]
                feature_to_look = self.features.get(feature_name_to_look)

                if not isMC:
                    tag = ""
                elif syst_name == "central":
                    if feature_to_look.central != "":
                        tag = ""
                    else:
                        tag = "%s" % self.systematics.get(feature_to_look.central).expression
                elif isMC and syst_name in feature_to_look.systematics:
                    syst = self.systematics.get(syst_name)
                    tag = "%s%s" % (syst.expression, eval("syst.%s" % systematic_direction))

                feature_to_look_expression = add_systematic_tag(feature_to_look.expression, tag)
                feature_expression = feature_expression.replace(feature_expression[initial: final + 1],
                    feature_to_look_expression)
            return feature_expression

        elif isinstance(feature, Feature):  # not derived expression and not a category
            if not isMC:
                tag = ""
            elif syst_name == "central":
                if feature.central != "":
                    tag = "%s" % self.systematics.get(feature.central).expression
                else:
                    tag = ""
            elif isMC and syst_name in feature.systematics:
                syst = self.systematics.get(syst_name)
                tag = "%s%s" % (syst.expression, eval("syst.%s" % systematic_direction))

            return add_systematic_tag(feature.expression, tag)
        else:
            return get_expression(feature)


config = Config("base", year=2018, ecm=13, lumi_pb=59741)
