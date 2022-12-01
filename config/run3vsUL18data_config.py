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
            Category("preselRun3_Mu50", "GEMethod Preselection for Run3 2022 HLT_Mu50", selection = "nMuon > 1 && (HLT_Mu50 == 1)"),
            Category("preselRun3_HighPtPath", "GEMethod Preselection for Run3 2022 full path for HighPt muons", selection = "nMuon > 1 && (HLT_Mu50 == 1 || HLT_HighPtTkMu100 == 1 || HLT_CascadeMu100 == 1)"),
        ]
        return ObjectCollection(categories)

    def add_processes(self):

        processes = [
            Process("DataUL18", Label("Data UL18"), color=ROOT.kAzure+1),
            Process("Data2022", Label("Data 2022 CDEF"), color=(0, 0, 0), isData=True),
        ]

        process_group_names = {

            "2022vsUL18": [
                "DataUL18",
                "Data2022",
            ],

        }

        return ObjectCollection(processes), process_group_names

    def add_datasets(self):
        datasets = [

            Dataset("DataUL18_A",
                dataset="/SingleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD",
                process=self.processes.get("DataUL18"),
                # prefix="xrootd-cms.infn.it//",
                xs=1.0,
                tags=["ul"]),

            Dataset("DataUL18_B",
                dataset="/SingleMuon/Run2018B-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD",
                process=self.processes.get("DataUL18"),
                # prefix="xrootd-cms.infn.it//",
                xs=1.0,
                tags=["ul"]),

            Dataset("DataUL18_C",
                dataset="/SingleMuon/Run2018C-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD",
                process=self.processes.get("DataUL18"),
                # prefix="xrootd-cms.infn.it//",
                xs=1.0,
                tags=["ul"]),

            Dataset("DataUL18_D",
                dataset="/SingleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD",
                process=self.processes.get("DataUL18"),
                # prefix="xrootd-cms.infn.it//",
                xs=1.0,
                tags=["ul"]),

            Dataset("SingleMu2022_C",
                dataset="/SingleMuon/Run2022C-PromptNanoAODv10_v1-v1/NANOAOD",
                process=self.processes.get("Data2022"),
                # prefix="xrootd-cms.infn.it//",
                ),

            Dataset("Muon2022_C",
                dataset="/Muon/Run2022C-PromptNanoAODv10_v1-v1/NANOAOD",
                process=self.processes.get("Data2022"),
                # prefix="xrootd-cms.infn.it//",
                ),

            Dataset("Muon2022_D_v1",
                dataset="/Muon/Run2022D-PromptNanoAODv10_v1-v1/NANOAOD",
                process=self.processes.get("Data2022"),
                # prefix="xrootd-cms.infn.it//",
                ),

            Dataset("Muon2022_D_v2",
                dataset="/Muon/Run2022D-PromptNanoAODv10_v2-v1/NANOAOD",
                process=self.processes.get("Data2022"),
                # prefix="xrootd-cms.infn.it//",
                ),

            Dataset("Muon2022_E",
                dataset="/Muon/Run2022E-PromptNanoAODv10_v1-v3/NANOAOD",
                process=self.processes.get("Data2022"),
                # prefix="xrootd-cms.infn.it//",
                ),

            Dataset("Muon2022_F",
                dataset="/Muon/Run2022F-PromptNanoAODv10_v1-v2/NANOAOD",
                process=self.processes.get("Data2022"),
                # prefix="xrootd-cms.infn.it//",
                ),

        ]
        return ObjectCollection(datasets)

    def add_features(self):
        
        ### Feature selections ###
        barrel_dimu   = "fabs(Muon_eta.at(mu1_index)) < 1.2 && fabs(Muon_eta.at(mu2_index)) < 1.2"
        endcap_dimu   = "fabs(Muon_eta.at(mu1_index)) > 1.2 && fabs(Muon_eta.at(mu1_index)) < 2.1 && fabs(Muon_eta.at(mu2_index)) > 1.2 && fabs(Muon_eta.at(mu2_index)) < 2.1"
        forwardE_dimu = "fabs(Muon_eta.at(mu1_index)) > 2.1 && fabs(Muon_eta.at(mu2_index)) > 2.1"

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

            Feature("kappa_barrel", "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)), 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))})", binning=(50, -5., 5.),
                selection=barrel_dimu,
                x_title=Label("#kappa"+axis_barrel),
                units="TeV^{-1}"),
            Feature("kappa_endcap", "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)), 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))})", binning=(50, -5., 5.),
                selection=endcap_dimu,
                x_title=Label("#kappa"+axis_endcap),
                units="TeV^{-1}"),
            Feature("kappa_forwardE", "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)), 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))})", binning=(50, -5., 5.),
                selection=forwardE_dimu,
                x_title=Label("#kappa"+axis_forwardE),
                units="TeV^{-1}"),
            
            # pT single muons
            Feature("pt_mu1", "Muon_pt.at(mu1_index)", binning=(50, 0, 2200),
                x_title=Label("#mu_{1} p_{T}"),
                units="GeV"),
            Feature("pt_mu2", "Muon_pt.at(mu2_index)", binning=(50, 0, 2200),
                x_title=Label("#mu_{2} p_{T}"),
                units="GeV"),
            Feature("pt_muPlus", "(Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == 1)) + (Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == 1))",
                binning=(50, 0, 2200),
                x_title=Label("#mu^{+} p_{T}"),
                units="GeV"),
            Feature("pt_muMinus", "(Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == -1)) + (Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == -1))",
                binning=(50, 0, 2200),
                x_title=Label("#mu^{-} p_{T}"),
                units="GeV"),

            Feature("pt_muPlus_barrel", "(Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == 1)) + (Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == 1))", 
                binning=(50, 0, 2200),
                selection=barrel_dimu,
                x_title=Label("#mu^{+} p_{T}"+axis_barrel),
                units="GeV"),
            Feature("pt_muMinus_barrel", "(Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == -1)) + (Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == -1))", 
                binning=(50, 0, 2200),
                selection=barrel_dimu,
                x_title=Label("#mu^{-} p_{T}"+axis_barrel),
                units="GeV"),
            Feature("pt_muPlus_endcap", "(Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == 1)) + (Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == 1))", 
                binning=(50, 0, 2200),
                selection=endcap_dimu,
                x_title=Label("#mu^{+} p_{T}"+axis_endcap),
                units="GeV"),
            Feature("pt_muMinus_endcap", "(Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == -1)) + (Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == -1))", 
                binning=(50, 0, 2200),
                selection=endcap_dimu,
                x_title=Label("#mu^{-} p_{T}"+axis_endcap),
                units="GeV"),
            Feature("pt_muPlus_forwardE", "(Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == 1)) + (Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == 1))", 
                binning=(50, 0, 2200),
                selection=forwardE_dimu,
                x_title=Label("#mu^{+} p_{T}"+axis_forwardE),
                units="GeV"),
            Feature("pt_muMinus_forwardE", "(Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == -1)) + (Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == -1))", 
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

            
            ### GEN LEVEL PLOTS ###

            #Feature("mu1_genPt", "GenPart_pt.at(Muon_genPartIdx.at(mu1_index))", binning=(50, 0, 2200),
            #    x_title=Label("gen #mu_{1} p_{T}"),
            #    selection="Muon_genPartIdx.at(mu1_index)>-1",
            #    units="GeV"),
            #Feature("mu2_genPt", "GenPart_pt.at(Muon_genPartIdx.at(mu2_index))", binning=(50, 0, 2200),
            #    x_title=Label("gen #mu_{2} p_{T}"),
            #    selection="Muon_genPartIdx.at(mu2_index)>-1",
            #    units="GeV"),

#UNCOMMENT
            #Feature("Z_genPt_tail", "sqrt((GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))+(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))+2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index)))*cos(GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))+sin(GenPart_phi.at(Muon_genPartIdx.at(mu1_index)))*sin(GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))))", binning=(50, 0, 2200),
            #    x_title=Label("gen p_{T_{#mu#mu}}"),
            #    selection="Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1",
            #    units="GeV"),

#UNCOMMENT
            #Feature("Z_genM_tail_1", "sqrt(2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cosh(GenPart_eta.at(Muon_genPartIdx.at(mu1_index))-GenPart_eta.at(Muon_genPartIdx.at(mu2_index)))-cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index))-2*3.1416)))", binning=(50, 0, 5000),
            #    selection="(Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1) && (GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))>3.1416",
            #    x_title=Label("gen M_{#mu#mu}"),
            #    units="GeV"),
            #Feature("Z_genM_tail_2", "sqrt(2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cosh(GenPart_eta.at(Muon_genPartIdx.at(mu1_index))-GenPart_eta.at(Muon_genPartIdx.at(mu2_index)))-cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index))+2*3.1416)))", binning=(50, 0, 5000),
            #    selection="(Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1) && (GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))<-3.1416",
            #    x_title=Label("gen M_{#mu#mu}"),
            #    units="GeV"),
#UNCOMMENT
            #Feature("Z_genM_peak_1", "sqrt(2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cosh(GenPart_eta.at(Muon_genPartIdx.at(mu1_index))-GenPart_eta.at(Muon_genPartIdx.at(mu2_index)))-cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index))-2*3.1416)))", binning=(50, 0, 300),
            #    selection="(Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1) && (GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))>3.1416",
            #    x_title=Label("gen M_{#mu#mu}"),
            #    units="GeV"),
#UNCOMMENT
            #Feature("LHE_HT_tail", "LHE_HT", binning=(50, 0, 4000),
            #    x_title=Label("LHE HT"),
            #    units="GeV"),
            #Feature("LHE_HT_peak", "LHE_HT", binning=(50, 0, 500),
            #    x_title=Label("LHE HT"),
            #    units="GeV"),
            
        ]
    
        ### Curvature with Bias ###
        #biases = []

        #for i in range (161):
        #    biases.append(round(-0.8 + 0.01*i, 2))
        #for bias in biases:
        #    features.append( Feature("kappa_%s" %bias, "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)) + (float)%s, 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)) + (float)%s})" %(bias, bias), binning=(50, -5., 5.),
        #        x_title=Label("#kappa"),
        #        units="TeV^{-1}"), )

        return ObjectCollection(features)

    def add_versions(self):
        versions = {}
        return versions

    def add_weights(self):
        weights = DotDict()
        weights.default = "1"

        weights.total_events_weights = ["1"]

        weights.preselection_UL18 = ["genWeight", "puWeight", "mu_idSF_weight", "mu_isoSF_weight", "mu_trigSF_weight"]

        #weights.mutau = ["genWeight", "puWeight", "prescaleWeight", "trigSF",
        #    "L1PreFiringWeight_Nom", "PUjetID_SF"]

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
        if "{{" in feature_expression:  # derived expression
            while "{{" in feature_expression:
                initial = feature_expression.find("{{")
                final = feature_expression.find("}}")
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
                return add_systematic_tag(feature.expression, "")
            tag = ""
            if syst_name in feature.systematics:
                syst = self.systematics.get(syst_name)
                tag = "%s%s" % (syst.expression, eval("syst.%s" % systematic_direction))
            else:
                if feature.central != "":
                    tag = "%s" % self.systematics.get(feature.central).expression

            return add_systematic_tag(feature.expression, tag)
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

config = Config("base", year=2018, ecm=13, lumi_pb=59741)
