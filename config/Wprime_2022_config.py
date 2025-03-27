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
        preEE = {
            "C" : 5010,
            "D" : 2970,
        }
        postEE = {
            "E" : 5807,
            "F" : 17782,
            "G" : 3083,
        }
        lumi_pb = {
            "preEE"  : preEE,
            "postEE" : postEE,
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
        ]
        return ObjectCollection(categories)

    def add_processes(self):

        processes = [
            ### Signal Processes ###
            Process("Wprime200", Label("W' M = 0.2 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime400", Label("W' M = 0.4 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime600", Label("W' M = 0.6 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime1000", Label("W' M = 1.0 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime1600", Label("W' M = 1.6 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime2000", Label("W' M = 2.0 TeV"), color=ROOT.kAzure+1, isSignal=True),
            Process("Wprime2600", Label("W' M = 2.6 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime3000", Label("W' M = 3.0 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime3600", Label("W' M = 3.6 TeV"), color=ROOT.kGreen+1, isSignal=True),
            Process("Wprime4000", Label("W' M = 4.0 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime4600", Label("W' M = 4.6 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime5000", Label("W' M = 5.0 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime5600", Label("W' M = 5.6 TeV"), color=ROOT.kMagenta+1, isSignal=True),
            Process("Wprime6000", Label("W' M = 6.0 TeV"), color=(0, 0, 0), isSignal=True),
            Process("Wprime6600", Label("W' M = 6.6 TeV"), color=(0, 0, 0), isSignal=True),

            ## Variable Coupling ##
            Process("Wprime400_kR0.01", Label("W' M = 0.4 TeV g_{W'}/g_{W} = 0.01"), color=(0, 0, 0), isSignal=True),
            Process("Wprime400_kR0.1", Label("W' M = 0.4 TeV g_{W'}/g_{W} = 0.1"), color=(0, 0, 0), isSignal=True),
            Process("Wprime400_kR2", Label("W' M = 0.4 TeV g_{W'}/g_{W} = 2"), color=(0, 0, 0), isSignal=True),
            Process("Wprime400_kR3", Label("W' M = 0.4 TeV g_{W'}/g_{W} = 3"), color=(0, 0, 0), isSignal=True),
            Process("Wprime400_kR5", Label("W' M = 0.4 TeV g_{W'}/g_{W} = 5"), color=(0, 0, 0), isSignal=True),
            Process("Wprime600_kR0.01", Label("W' M = 0.6 TeV g_{W'}/g_{W} = 0.01"), color=(0, 0, 0), isSignal=True),
            Process("Wprime600_kR0.1", Label("W' M = 0.6 TeV g_{W'}/g_{W} = 0.1"), color=(0, 0, 0), isSignal=True),
            Process("Wprime600_kR2", Label("W' M = 0.6 TeV g_{W'}/g_{W} = 2"), color=(0, 0, 0), isSignal=True),
            Process("Wprime600_kR3", Label("W' M = 0.6 TeV g_{W'}/g_{W} = 3"), color=(0, 0, 0), isSignal=True),
            Process("Wprime600_kR5", Label("W' M = 0.6 TeV g_{W'}/g_{W} = 5"), color=(0, 0, 0), isSignal=True),
            Process("Wprime1000_kR0.01", Label("W' M = 1.0 TeV g_{W'}/g_{W} = 0.01"), color=(0, 0, 0), isSignal=True),
            Process("Wprime1000_kR0.1", Label("W' M = 1.0 TeV g_{W'}/g_{W} = 0.1"), color=(0, 0, 0), isSignal=True),
            Process("Wprime1000_kR2", Label("W' M = 1.0 TeV g_{W'}/g_{W} = 2"), color=(0, 0, 0), isSignal=True),
            Process("Wprime1000_kR3", Label("W' M = 1.0 TeV g_{W'}/g_{W} = 3"), color=(0, 0, 0), isSignal=True),
            Process("Wprime1000_kR5", Label("W' M = 1.0 TeV g_{W'}/g_{W} = 5"), color=(0, 0, 0), isSignal=True),    
            Process("Wprime1600_kR0.01", Label("W' M = 1.6 TeV g_{W'}/g_{W} = 0.01"), color=(0, 0, 0), isSignal=True),
            Process("Wprime1600_kR0.1", Label("W' M = 1.6 TeV g_{W'}/g_{W} = 0.1"), color=(0, 0, 0), isSignal=True),
            Process("Wprime1600_kR2", Label("W' M = 1.6 TeV g_{W'}/g_{W} = 2"), color=(0, 0, 0), isSignal=True),
            Process("Wprime1600_kR3", Label("W' M = 1.6 TeV g_{W'}/g_{W} = 3"), color=(0, 0, 0), isSignal=True),
            Process("Wprime1600_kR5", Label("W' M = 1.6 TeV g_{W'}/g_{W} = 5"), color=(0, 0, 0), isSignal=True),
            Process("Wprime2000_kR0.01", Label("W' M = 2.0 TeV g_{W'}/g_{W} = 0.01"), color=(0, 0, 0), isSignal=True),
            Process("Wprime2000_kR0.1", Label("W' M = 2.0 TeV g_{W'}/g_{W} = 0.1"), color=(0, 0, 0), isSignal=True),
            Process("Wprime2000_kR2", Label("W' M = 2.0 TeV g_{W'}/g_{W} = 2"), color=(0, 0, 0), isSignal=True),
            Process("Wprime2000_kR3", Label("W' M = 2.0 TeV g_{W'}/g_{W} = 3"), color=(0, 0, 0), isSignal=True),
            Process("Wprime2000_kR5", Label("W' M = 2.0 TeV g_{W'}/g_{W} = 5"), color=(0, 0, 0), isSignal=True),
            Process("Wprime2600_kR0.01", Label("W' M = 2.6 TeV g_{W'}/g_{W} = 0.01"), color=(0, 0, 0), isSignal=True),
            Process("Wprime2600_kR0.1", Label("W' M = 2.6 TeV g_{W'}/g_{W} = 0.1"), color=(0, 0, 0), isSignal=True),
            Process("Wprime2600_kR2", Label("W' M = 2.6 TeV g_{W'}/g_{W} = 2"), color=(0, 0, 0), isSignal=True),
            Process("Wprime2600_kR3", Label("W' M = 2.6 TeV g_{W'}/g_{W} = 3"), color=(0, 0, 0), isSignal=True),
            Process("Wprime2600_kR5", Label("W' M = 2.6 TeV g_{W'}/g_{W} = 5"), color=(0, 0, 0), isSignal=True),
            Process("Wprime3000_kR0.01", Label("W' M = 3.0 TeV g_{W'}/g_{W} = 0.01"), color=(0, 0, 0), isSignal=True),
            Process("Wprime3000_kR0.1", Label("W' M = 3.0 TeV g_{W'}/g_{W} = 0.1"), color=(0, 0, 0), isSignal=True),
            Process("Wprime3000_kR2", Label("W' M = 3.0 TeV g_{W'}/g_{W} = 2"), color=(0, 0, 0), isSignal=True),
            Process("Wprime3000_kR3", Label("W' M = 3.0 TeV g_{W'}/g_{W} = 3"), color=(0, 0, 0), isSignal=True),
            Process("Wprime3000_kR5", Label("W' M = 3.0 TeV g_{W'}/g_{W} = 5"), color=(0, 0, 0), isSignal=True),
            Process("Wprime3600_kR0.01", Label("W' M = 3.6 TeV g_{W'}/g_{W} = 0.01"), color=(0, 0, 0), isSignal=True),
            Process("Wprime3600_kR0.1", Label("W' M = 3.6 TeV g_{W'}/g_{W} = 0.1"), color=(0, 0, 0), isSignal=True),
            Process("Wprime3600_kR2", Label("W' M = 3.6 TeV g_{W'}/g_{W} = 2"), color=(0, 0, 0), isSignal=True),
            Process("Wprime3600_kR3", Label("W' M = 3.6 TeV g_{W'}/g_{W} = 3"), color=(0, 0, 0), isSignal=True),
            Process("Wprime3600_kR5", Label("W' M = 3.6 TeV g_{W'}/g_{W} = 5"), color=(0, 0, 0), isSignal=True),
            Process("Wprime4000_kR0.01", Label("W' M = 4.0 TeV g_{W'}/g_{W} = 0.01"), color=(0, 0, 0), isSignal=True),
            Process("Wprime4000_kR0.1", Label("W' M = 4.0 TeV g_{W'}/g_{W} = 0.1"), color=(0, 0, 0), isSignal=True),
            Process("Wprime4000_kR2", Label("W' M = 4.0 TeV g_{W'}/g_{W} = 2"), color=(0, 0, 0), isSignal=True),
            Process("Wprime4000_kR3", Label("W' M = 4.0 TeV g_{W'}/g_{W} = 3"), color=(0, 0, 0), isSignal=True),
            Process("Wprime4000_kR5", Label("W' M = 4.0 TeV g_{W'}/g_{W} = 5"), color=(0, 0, 0), isSignal=True),
            Process("Wprime4600_kR0.01", Label("W' M = 4.6 TeV g_{W'}/g_{W} = 0.01"), color=(0, 0, 0), isSignal=True),
            Process("Wprime4600_kR0.1", Label("W' M = 4.6 TeV g_{W'}/g_{W} = 0.1"), color=(0, 0, 0), isSignal=True),
            Process("Wprime4600_kR2", Label("W' M = 4.6 TeV g_{W'}/g_{W} = 2"), color=(0, 0, 0), isSignal=True),
            Process("Wprime4600_kR3", Label("W' M = 4.6 TeV g_{W'}/g_{W} = 3"), color=(0, 0, 0), isSignal=True),
            Process("Wprime4600_kR5", Label("W' M = 4.6 TeV g_{W'}/g_{W} = 5"), color=(0, 0, 0), isSignal=True),
            Process("Wprime5000_kR0.01", Label("W' M = 5.0 TeV g_{W'}/g_{W} = 0.01"), color=(0, 0, 0), isSignal=True),
            Process("Wprime5000_kR0.1", Label("W' M = 5.0 TeV g_{W'}/g_{W} = 0.1"), color=(0, 0, 0), isSignal=True),
            Process("Wprime5000_kR2", Label("W' M = 5.0 TeV g_{W'}/g_{W} = 2"), color=(0, 0, 0), isSignal=True),
            Process("Wprime5000_kR3", Label("W' M = 5.0 TeV g_{W'}/g_{W} = 3"), color=(0, 0, 0), isSignal=True),
            Process("Wprime5000_kR5", Label("W' M = 5.0 TeV g_{W'}/g_{W} = 5"), color=(0, 0, 0), isSignal=True),
            Process("Wprime5600_kR0.01", Label("W' M = 5.6 TeV g_{W'}/g_{W} = 0.01"), color=(0, 0, 0), isSignal=True),
            Process("Wprime5600_kR0.1", Label("W' M = 5.6 TeV g_{W'}/g_{W} = 0.1"), color=(0, 0, 0), isSignal=True),
            Process("Wprime5600_kR2", Label("W' M = 5.6 TeV g_{W'}/g_{W} = 2"), color=(0, 0, 0), isSignal=True),
            Process("Wprime5600_kR3", Label("W' M = 5.6 TeV g_{W'}/g_{W} = 3"), color=(0, 0, 0), isSignal=True),
            Process("Wprime5600_kR5", Label("W' M = 5.6 TeV g_{W'}/g_{W} = 5"), color=(0, 0, 0), isSignal=True),
            Process("Wprime6000_kR0.01", Label("W' M = 6.0 TeV g_{W'}/g_{W} = 0.01"), color=(0, 0, 0), isSignal=True),
            Process("Wprime6000_kR0.1", Label("W' M = 6.0 TeV g_{W'}/g_{W} = 0.1"), color=(0, 0, 0), isSignal=True),
            Process("Wprime6000_kR2", Label("W' M = 6.0 TeV g_{W'}/g_{W} = 2"), color=(0, 0, 0), isSignal=True),
            Process("Wprime6000_kR3", Label("W' M = 6.0 TeV g_{W'}/g_{W} = 3"), color=(0, 0, 0), isSignal=True),
            Process("Wprime6000_kR5", Label("W' M = 6.0 TeV g_{W'}/g_{W} = 5"), color=(0, 0, 0), isSignal=True),
            Process("Wprime6600_kR0.01", Label("W' M = 6.6 TeV g_{W'}/g_{W} = 0.01"), color=(0, 0, 0), isSignal=True),
            Process("Wprime6600_kR0.1", Label("W' M = 6.6 TeV g_{W'}/g_{W} = 0.1"), color=(0, 0, 0), isSignal=True),
            Process("Wprime6600_kR2", Label("W' M = 6.6 TeV g_{W'}/g_{W} = 2"), color=(0, 0, 0), isSignal=True),
            Process("Wprime6600_kR3", Label("W' M = 6.6 TeV g_{W'}/g_{W} = 3"), color=(0, 0, 0), isSignal=True),
            Process("Wprime6600_kR5", Label("W' M = 6.6 TeV g_{W'}/g_{W} = 5"), color=(0, 0, 0), isSignal=True),

            
            ### Background Processes ###
            Process("background", Label("Background"), color=(63, 144, 218)),
            
            ## W boson ##
            Process("W_boson", Label("W-boson"), color=(63, 144, 218), parent_process="background"),
            Process("W_preEE", Label("W-boson"), color=(63, 144, 218), parent_process="W_boson"),
            Process("W_postEE", Label("W-boson"), color=(63, 144, 218), parent_process="W_boson"),

            ## Old W off-shell pythia background ==> Deprecated ##
              Process("Wmunu", Label("off-shell W #rightarrow #mu#nu"), color=ROOT.kAzure+1, isPythia=True, parent_process="W_preEE"),
              Process("Wmunu_postEE", Label("off-shell W #rightarrow #mu#nu"), color=ROOT.kAzure+1, parent_process="W_postEE"),
              Process("Wmunu1_postEE", Label("W #rightarrow #mu#nu M_{W} 100to200"), color=(255, 241, 0), isPythia=True, parent_process="Wmunu_postEE"),
              Process("Wmunu2_postEE", Label("W #rightarrow #mu#nu M_{W} 200to500"), color=(255, 140, 0), isPythia=True, parent_process="Wmunu_postEE"),
              Process("Wmunu3_postEE", Label("W #rightarrow #mu#nu M_{W} 500to1000"), color=(232, 17, 35), isPythia=True, parent_process="Wmunu_postEE"),
              Process("Wmunu4_postEE", Label("W #rightarrow #mu#nu M_{W} 1000to2000"), color=(236, 0, 140), isPythia=True, parent_process="Wmunu_postEE"),
              Process("Wmunu5_postEE", Label("W #rightarrow #mu#nu M_{W} 2000to3000"), color=(104, 33, 122), isPythia=True, parent_process="Wmunu_postEE"),
              Process("Wmunu6_postEE", Label("W #rightarrow #mu#nu M_{W} 3000to4000"), color=(0, 24, 143), isPythia=True, parent_process="Wmunu_postEE"),
              Process("Wmunu7_postEE", Label("W #rightarrow #mu#nu M_{W} 4000to5000"), color=(0, 188, 242), isPythia=True, parent_process="Wmunu_postEE"),
              Process("Wmunu8_postEE", Label("W #rightarrow #mu#nu M_{W} 5000to6000"), color=(0, 178, 148), isPythia=True, parent_process="Wmunu_postEE"),
              Process("Wmunu9_postEE", Label("W #rightarrow #mu#nu M_{W} 6000"), color=(0, 158, 73), isPythia=True, parent_process="Wmunu_postEE"),
              Process("Wtaunu", Label("off-shell W #rightarrow #tau#nu"), color=ROOT.kAzure+3, isPythia=True, parent_process="W_preEE"),
              Process("Wtaunu_postEE", Label("off-shell W #rightarrow #tau#nu"), color=ROOT.kAzure+3, isPythia=True, parent_process="W_postEE"),
            #######################################################
            
            # W off-shell madgraph
            # For W splitting
            Process("Wlnu_full", Label("off-shell W #rightarrow l#nu"), color=ROOT.kAzure+1, isWoffshell=True, parent_process="W_boson"),
            Process("Wlnu", Label("off-shell W #rightarrow l#nu"), color=ROOT.kAzure+1, isWoffshell=True, parent_process="Wlnu_full"),
            Process("Wlnu_postEE", Label("off-shell W #rightarrow l#nu"), color=ROOT.kAzure+1, isWoffshell=True, parent_process="Wlnu_full"),
            # Old - original
            #Process("Wlnu", Label("off-shell W #rightarrow l#nu"), color=ROOT.kAzure+1, isWoffshell=True, parent_process="W_preEE"),
            Process("Wlnu1", Label("W #rightarrow l#nu M_{W} 120to200"), color=(255, 241, 0), isWoffshell=True, parent_process="Wlnu"),
            Process("Wlnu2", Label("W #rightarrow l#nu M_{W} 200to400"), color=(255, 140, 0), isWoffshell=True, parent_process="Wlnu"),
            Process("Wlnu3", Label("W #rightarrow l#nu M_{W} 400to800"), color=(232, 17, 35), isWoffshell=True, parent_process="Wlnu"),
            Process("Wlnu4", Label("W #rightarrow l#nu M_{W} 800to1500"), color=(236, 0, 140), isWoffshell=True, parent_process="Wlnu"),
            Process("Wlnu5", Label("W #rightarrow l#nu M_{W} 1500to2500"), color=(104, 33, 122), isWoffshell=True, parent_process="Wlnu"),
            Process("Wlnu6", Label("W #rightarrow l#nu M_{W} 2500to4000"), color=(0, 24, 143), isWoffshell=True, parent_process="Wlnu"),
            Process("Wlnu7", Label("W #rightarrow l#nu M_{W} 4000to6000"), color=(0, 188, 242), isWoffshell=True, parent_process="Wlnu"),
            Process("Wlnu8", Label("W #rightarrow l#nu M_{W} 6000"), color=(0, 178, 148), isWoffshell=True, parent_process="Wlnu"),
            #Process("Wlnu_postEE", Label("off-shell W #rightarrow l#nu"), color=ROOT.kAzure+1, isWoffshell=True, parent_process="W_postEE"),

            # W on-shell
            # For W splitting
            Process("Wonshell_full", Label("onshell W #rightarrow l#nu"), color=ROOT.kAzure+10, parent_process="W_boson", isWjets=True),
            Process("Wonshell", Label("onshell W #rightarrow l#nu"), color=ROOT.kAzure+10, parent_process="Wonshell_full", isWjets=True),
            Process("Wonshell_postEE", Label("onshell W #rightarrow l#nu"), color=ROOT.kAzure+10, parent_process="Wonshell_full", isWjets=True),
            # Old - original
            #Process("Wonshell", Label("onshell W #rightarrow l#nu"), color=ROOT.kAzure+10, parent_process="W_preEE", isWjets=True),
            #Process("Wonshell_postEE", Label("onshell W #rightarrow l#nu"), color=ROOT.kAzure+10, parent_process="W_postEE", isWjets=True),
            # W+4j
            Process("W+4j", Label("W #rightarrow l#nu + jets"), color=ROOT.kAzure+10, parent_process="W_preEE", isWjets=True),
            Process("W+4j_postEE", Label("W #rightarrow l#nu + jets"), color=ROOT.kAzure+10, parent_process="W_postEE", isWjets=True),

            # W boosted --> HT-binned LO
            Process("Wboost", Label("boosted W #rightarrow l#nu"), color=(206, 30, 30), isHTbin=True, parent_process="W_preEE"),
            Process("Wboost0", Label("W #rightarrow l#nu HT 40to100"), color=(255, 140, 0), isHTbin=True, parent_process="Wboost"),
            Process("Wboost1", Label("W #rightarrow l#nu HT 100to400"), color=(232, 17, 35), isHTbin=True, parent_process="Wboost"),
            Process("Wboost2", Label("W #rightarrow l#nu HT 400to800"), color=(236, 0, 140), isHTbin=True, parent_process="Wboost"),
            Process("Wboost3", Label("W #rightarrow l#nu HT 800to1500"), color=(104, 33, 122), isHTbin=True, parent_process="Wboost"),
            Process("Wboost4", Label("W #rightarrow l#nu HT 1500to2500"), color=(0, 24, 143), isHTbin=True, parent_process="Wboost"),
            Process("Wboost5", Label("W #rightarrow l#nu HT 2500"), color=(0, 188, 242), isHTbin=True, parent_process="Wboost"),
            Process("Wboost_postEE", Label("boosted W #rightarrow l#nu"), color=(206, 30, 30), isHTbin=True, parent_process="W_postEE"),
            # W boosted --> ptLNu-binned NLO
            # For W splitting
            Process("W_ptW_full", Label("boosted W #rightarrow l#nu"), color=(255, 165, 0), isWboost=True, parent_process="W_boson"),
            Process("W_ptW", Label("boosted W #rightarrow l#nu"), color=(206, 30, 30), isWboost=True, parent_process="W_ptW_full"),
            Process("W_ptW_postEE", Label("boosted W #rightarrow l#nu"), color=(206, 30, 30), isWboost=True, parent_process="W_ptW_full"),
            # Old - original
            #Process("W_ptW", Label("boosted W #rightarrow l#nu"), color=(206, 30, 30), isWboost=True, parent_process="W_preEE"),
            Process("W_ptW1", Label("W #rightarrow l#nu p_{T}^{l#nu} 40to100"), color=(255, 140, 0), isWboost=True, parent_process="W_ptW"),
            Process("W_ptW2", Label("W #rightarrow l#nu p_{T}^{l#nu} 100to200"), color=(232, 17, 35), isWboost=True, parent_process="W_ptW"),
            Process("W_ptW3", Label("W #rightarrow l#nu p_{T}^{l#nu} 200to400"), color=(236, 0, 140), isWboost=True, parent_process="W_ptW"),
            Process("W_ptW4", Label("W #rightarrow l#nu p_{T}^{l#nu} 400to600"), color=(104, 33, 122), isWboost=True, parent_process="W_ptW"),
            Process("W_ptW5", Label("W #rightarrow l#nu p_{T}^{l#nu} 600"), color=(0, 24, 143), isWboost=True, parent_process="W_ptW"),
            #Process("W_ptW_postEE", Label("boosted W #rightarrow l#nu"), color=(206, 30, 30), isWboost=True, parent_process="W_postEE"),

            ## Top ##
            Process("Top", Label("Top"), color=(189, 31, 1), parent_process="background"),
            Process("Top_preEE", Label("Top"), color=(189, 31, 1), parent_process="Top"),
            Process("Top_postEE", Label("Top"), color=(189, 31, 1), parent_process="Top"),
            Process("TTbar", Label("t#bar{t}"), color=(255,255,0), parent_process="Top_preEE"),
            Process("TTbar_postEE", Label("t#bar{t}"), color=(255,255,0), parent_process="Top_postEE"),
            Process("ST", Label("single t"), color=(255,255,0), parent_process="Top_preEE"),
            Process("ST_postEE", Label("single t"), color=(255,255,0), parent_process="Top_postEE"),

            ## Z boson ##
            Process("Z_boson", Label("Z/#gamma* #rightarrow ll"), color=(169, 107, 89), parent_process="background"),
            Process("Z_boson_preEE", Label("Z/#gamma* #rightarrow ll"), color=(169, 107, 89), parent_process="Z_boson"),
            Process("Z_boson_postEE", Label("Z/#gamma* #rightarrow ll"), color=(169, 107, 89), parent_process="Z_boson"),
            Process("Zmumu", Label("Z/#gamma* #rightarrow #mu#mu"), color=(206, 30, 30), parent_process="Z_boson_preEE"),
            Process("Zmumu_postEE", Label("Z/#gamma* #rightarrow #mu#mu"), color=(206, 30, 30), parent_process="Z_boson_postEE"),
            Process("Ztautau", Label("Z/#gamma* #rightarrow #tau#tau"), color=(208, 196, 31), parent_process="Z_boson_preEE"),
            Process("Ztautau_postEE", Label("Z/#gamma* #rightarrow #tau#tau"), color=(208, 196, 31), parent_process="Z_boson_postEE"),
            Process("Znunu", Label("Z/#gamma* #rightarrow #nu#nu"), color=(255, 128, 0), parent_process="Z_boson_preEE"),
            Process("Znunu_postEE", Label("Z/#gamma* #rightarrow #nu#nu"), color=(255, 128, 0), parent_process="Z_boson_postEE"),

            ## Di-Boson ##
            Process("DiBoson", Label("DiBoson"), color=(131, 45, 182), parent_process="background"),
            Process("DiBoson_preEE", Label("DiBoson"), color=(131, 45, 182), parent_process="DiBoson"),
            Process("DiBoson_postEE", Label("DiBoson"), color=(131, 45, 182), parent_process="DiBoson"),
            Process("WW", Label("WW"), color=(36, 147, 25), parent_process="DiBoson_preEE"),
            Process("WW_postEE", Label("WW"), color=(36, 147, 25), parent_process="DiBoson_postEE"),
            Process("WZ", Label("WZ"), color=(36, 147, 25), parent_process="DiBoson_preEE"),
            Process("WZ_postEE", Label("WZ"), color=(36, 147, 25), parent_process="DiBoson_postEE"),
            Process("ZZ", Label("ZZ"), color=(36, 147, 25), parent_process="DiBoson_preEE"),
            Process("ZZ_postEE", Label("ZZ"), color=(36, 147, 25), parent_process="DiBoson_postEE"),
            Process("Wgamma", Label("W#gamma"), color=(14, 75, 7), parent_process="DiBoson_preEE"),
            Process("Wgamma_postEE", Label("W#gamma"), color=(14, 75, 7), parent_process="DiBoson_postEE"),

            ## QCD ##
            Process("QCD", Label("QCD"), color=(255, 169, 14), parent_process="background"),
            Process("QCD_preEE", Label("QCD"), color=(255, 169, 14), parent_process="QCD"),
            Process("QCD_postEE", Label("QCD"), color=(255, 169, 14), parent_process="QCD"),
            Process("QCD_Pt", Label("QCD"), color=(0, 0, 153), parent_process="QCD_preEE"),
            Process("QCD_Pt_postEE", Label("QCD"), color=(0, 0, 153), parent_process="QCD_postEE"),


            ### DATA ###
            Process("PromptData2022", Label("Data"), color=(0, 0, 0), isData=True),
            Process("PromptData2022_preEE", Label("Data"), color=(0, 0, 0), isData=True, parent_process="PromptData2022"),
            Process("PromptData2022_postEE", Label("Data"), color=(0, 0, 0), isData=True, parent_process="PromptData2022"),
            Process("ReRecoData2022", Label("Data"), color=(0, 0, 0), isData=True),
            Process("ReRecoData2022_preEE", Label("Data"), color=(0, 0, 0), isData=True, parent_process="ReRecoData2022"),
            Process("ReRecoData2022_postEE", Label("Data"), color=(0, 0, 0), isData=True, parent_process="ReRecoData2022"),

            # JetMET
            Process("JetMET_Data2022", Label("Data"), color=(0, 0, 0), isData=True),
            Process("JetMET2022_postEE", Label("Data"), color=(0, 0, 0), isData=True, parent_process="JetMET_Data2022"),


        ]

        process_group_names = {

            "2022ReReco_preEE": [
                "Wprime2000_preEE",
                "Wprime3600_preEE",
                "Wprime5600_preEE",
                "W_preEE",
                "Top_preEE",
                "DiBoson_preEE",
                "QCD_preEE",
                "Z_boson_preEE",
                "ReRecoData2022_preEE",
            ],
            "2022ReReco_postEE": [
                "Wprime2000_postEE",
                "Wprime3600_postEE",
                "Wprime5600_postEE",
                "W_postEE",
                "Top_postEE",
                "DiBoson_postEE",
                "QCD_postEE",
                "Z_boson_postEE",
                "ReRecoData2022_postEE",
            ],

            "2022ReReco": [
                "Wprime2000",
                "Wprime3600",
                "Wprime5600",
                "W_boson",
                "Top",
                "DiBoson",
                "QCD",
                "Z_boson",
                "ReRecoData2022",
            ],

            ## For W' SSM limits ##
            "SSMlimits2022": [
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
                "ReRecoData2022",
            ],

            ## For W' variable coupling limits ##
            "CouplingLimits2022": [
                "Wprime400_kR0.01",
                "Wprime400_kR0.1",
                "Wprime400",
                "Wprime400_kR2",
                "Wprime400_kR3",
                "Wprime400_kR5",
                "Wprime600_kR0.01",
                "Wprime600_kR0.1",
                "Wprime600",
                "Wprime600_kR2",
                "Wprime600_kR3",
                "Wprime600_kR5",
                "Wprime1000_kR0.01",
                "Wprime1000_kR0.1",
                "Wprime1000",
                "Wprime1000_kR2",
                "Wprime1000_kR3",
                "Wprime1000_kR5",
                "Wprime1600_kR0.01",
                "Wprime1600_kR0.1",
                "Wprime1600",
                "Wprime1600_kR2",
                "Wprime1600_kR3",
                "Wprime1600_kR5",
                "Wprime2000_kR0.01",
                "Wprime2000_kR0.1",
                "Wprime2000",
                "Wprime2000_kR2",
                "Wprime2000_kR3",
                "Wprime2000_kR5",
                "Wprime2600_kR0.01",
                "Wprime2600_kR0.1",
                "Wprime2600",
                "Wprime2600_kR2",
                "Wprime2600_kR3",
                "Wprime2600_kR5",
                "Wprime3000_kR0.01",
                "Wprime3000_kR0.1",
                "Wprime3000",
                "Wprime3000_kR2",
                "Wprime3000_kR3",
                "Wprime3000_kR5",
                "Wprime3600_kR0.01",
                "Wprime3600_kR0.1",
                "Wprime3600",
                "Wprime3600_kR2",
                "Wprime3600_kR3",
                "Wprime3600_kR5",
                "Wprime4000_kR0.01",
                "Wprime4000_kR0.1",
                "Wprime4000",
                "Wprime4000_kR2",
                "Wprime4000_kR3",
                "Wprime4000_kR5",
                "Wprime4600_kR0.01",
                "Wprime4600_kR0.1",
                "Wprime4600",
                "Wprime4600_kR2",
                "Wprime4600_kR3",
                "Wprime4600_kR5",
                "Wprime5000_kR0.01",
                "Wprime5000_kR0.1",
                "Wprime5000",
                "Wprime5000_kR2",
                "Wprime5000_kR3",
                "Wprime5000_kR5",
                "Wprime5600_kR0.01",
                "Wprime5600_kR0.1",
                "Wprime5600",
                "Wprime5600_kR2",
                "Wprime5600_kR3",
                "Wprime5600_kR5",
                "Wprime6000_kR0.01",
                "Wprime6000_kR0.1",
                "Wprime6000",
                "Wprime6000_kR2",
                "Wprime6000_kR3",
                "Wprime6000_kR5",
                "Wprime6600_kR0.01",
                "Wprime6600_kR0.1",
                "Wprime6600",
                "Wprime6600_kR2",
                "Wprime6600_kR3",
                "Wprime6600_kR5",
                "W_boson",
                "Top",
                "DiBoson",
                "QCD",
                "Z_boson",
                "ReRecoData2022",
            ],            
            
            ## For Systematic contribution plot ##
            "SystPlot": [
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
                "background",
                "ReRecoData2022",
            ],

            
            ########## CHECKS W SAMPLES ##########
            "Woffshell_pythia": [
                "Wmunu1_postEE",
                "Wmunu2_postEE",
                "Wmunu3_postEE",
                "Wmunu4_postEE",
                "Wmunu5_postEE",
                "Wmunu6_postEE",
                "Wmunu7_postEE",
                "Wmunu8_postEE",
                "Wmunu9_postEE",
            ],

            "Wbkg_pythia": [
                "Wmunu_postEE",
                "Wtaunu_postEE",
                "Wonshell_postEE",
            ],

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

            "W_boosted_HT-binned": [
                "Wboost0",
                "Wboost1",
                "Wboost2",
                "Wboost3",
                "Wboost4",
                "Wboost5",
            ],

            "Wbkg_all_HTboost": [
                "Wonshell",
                "Wlnu",
                "Wboost",
            ],

            "Wboosted_ptW": [
                "W_ptW1",
                "W_ptW2",
                "W_ptW3",
                "W_ptW4",
                "W_ptW5",
            ],

            "Wbkg_all_ptW": [
                "Wonshell",
                "Wlnu",
                "W_ptW",
            ],
            
            "Wbkg_LOvsNLO_stitching": [
                "Wonshell",
                "Wlnu",
            ],
                
            ######################################

            # For check
            "2022ReReco_Wsplit": [
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
                "ReRecoData2022",
            ],
            
            "2022ReReco_postEE_Wsplit": [
                "Wprime2000_postEE",
                "Wprime3600_postEE",
                "Wprime5600_postEE",
                "W_postEE",
                "Wboost_postEE",
                "Top_postEE",
                "DiBoson_postEE",
                "QCD_postEE",
                "Z_boson_postEE",
                "ReRecoData2022_postEE",
            ],

            "promptVSrereco": [
                "PromptData2022_postEE",
                "ReRecoData2022_postEE",
            ],

            "inclusiveVShtbinned": [
                "Wonshell_postEE",
                "Wboost_postEE",
                "W+4j_postEE",
            ],

            ## Check PU/MET weights
            "checkPUweights": [
                "Zmumu_postEE",
                "Ztautau_postEE",
                "Znunu_postEE",
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
                dataset="/WprimetoMuNu_M-200_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime200"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                #xs=1106.4,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime200_postEE",
                dataset="/WprimetoMuNu_M-200_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime200"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                #xs=1106.4,
                xs=0.001,
                tags=["postEE"]),

            Dataset("Wprime400",
                dataset="/WprimetoMuNu_M-400_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime400"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                #xs=115.91,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime400_postEE",
                dataset="/WprimetoMuNu_M-400_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime400"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                #xs=115.91,
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime600",
                dataset="/WprimetoMuNu_M-600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                #xs=28.204,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime600_postEE",
                dataset="/WprimetoMuNu_M-600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                #xs=28.204,
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime1000",
                dataset="/WprimetoMuNu_M-1000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                #xs=4.1127,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime1000_postEE",
                dataset="/WprimetoMuNu_M-1000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                #xs=4.1127,
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime1600",
                dataset="/WprimetoMuNu_M-1600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                #xs=0.55518,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime1600_postEE",
                dataset="/WprimetoMuNu_M-1600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                #xs=0.55518,
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime2000",
                dataset="/WprimetoMuNu_M-2000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                #xs=0.18979,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime2000_postEE",
                dataset="/WprimetoMuNu_M-2000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                #xs=0.18979,
                xs=0.001,
                tags=["postEE"]),
          
            Dataset("Wprime2600",
                dataset="/WprimetoMuNu_M-2600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                #xs=0.04641,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime2600_postEE",
                dataset="/WprimetoMuNu_M-2600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                #xs=0.04641,
                xs=0.001,
                tags=["postEE"]),

            Dataset("Wprime3000",
                dataset="/WprimetoMuNu_M-3000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                #xs=0.01988,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime3000_postEE",
                dataset="/WprimetoMuNu_M-3000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                #xs=0.01988,
                xs=0.001,
                tags=["postEE"]),

            Dataset("Wprime3600",
                dataset="/WprimetoMuNu_M-3600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                #xs=0.006262,),
                xs=0.001,), # For datacards

            Dataset("Wprime3600_postEE",
                dataset="/WprimetoMuNu_M-3600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                #xs=0.006262,
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime4000",
                dataset="/WprimetoMuNu_M-4000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                #xs=0.003148,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime4000_postEE",
                dataset="/WprimetoMuNu_M-4000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                #xs=0.003148,
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime4600",
                dataset="/WprimetoMuNu_M-4600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                #xs=0.001289,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime4600_postEE",
                dataset="/WprimetoMuNu_M-4600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                #xs=0.001289,
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime5000",
                dataset="/WprimetoMuNu_M-5000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                #xs=0.000779,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime5000_postEE",
                dataset="/WprimetoMuNu_M-5000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                #xs=0.000779,
                xs=0.001,
                tags=["postEE"]),

            Dataset("Wprime5600",
                dataset="/WprimetoMuNu_M-5600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                #xs=0.000411,),
                xs=0.001,), # For datacards

            Dataset("Wprime5600_postEE",
                dataset="/WprimetoMuNu_M-5600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                #xs=0.000411,
                xs=0.001,
                tags=["postEE"]),

            Dataset("Wprime6000",
                dataset="/WprimetoMuNu_M-6000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                #xs=0.000284,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime6000_postEE",
                dataset="/WprimetoMuNu_M-6000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6000"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                #xs=0.000284,
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime6600",
                dataset="/WprimetoMuNu_M-6600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                #xs=0.000174,), # From AN-21-096, all of them (NNLO)
                xs=0.001,), # For datacards

            Dataset("Wprime6600_postEE",
                dataset="/WprimetoMuNu_M-6600_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6600"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                #xs=0.000174,
                xs=0.001,
                tags=["postEE"]),

            ## Variable coupling signals

            Dataset("Wprime400_kR0.01",
                dataset="/WprimetoMuNu_M-400_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime400_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime400_kR0.01_postEE",
                dataset="/WprimetoMuNu_M-400_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime400_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime400_kR0.1",
                dataset="/WprimetoMuNu_M-400_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime400_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime400_kR0.1_postEE",
                dataset="/WprimetoMuNu_M-400_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime400_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime400_kR2",
                dataset="/WprimetoMuNu_M-400_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime400_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime400_kR2_postEE",
                dataset="/WprimetoMuNu_M-400_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime400_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime400_kR3",
                dataset="/WprimetoMuNu_M-400_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime400_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime400_kR3_postEE",
                dataset="/WprimetoMuNu_M-400_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime400_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime400_kR5",
                dataset="/WprimetoMuNu_M-400_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime400_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime400_kR5_postEE",
                dataset="/WprimetoMuNu_M-400_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime400_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),


            Dataset("Wprime600_kR0.01",
                dataset="/WprimetoMuNu_M-600_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime600_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime600_kR0.01_postEE",
                dataset="/WprimetoMuNu_M-600_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime600_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime600_kR0.1",
                dataset="/WprimetoMuNu_M-600_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime600_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime600_kR0.1_postEE",
                dataset="/WprimetoMuNu_M-600_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime600_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime600_kR2",
                dataset="/WprimeToMuNu_M-600_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime600_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                    xs=0.001,), # Hayq ue usar la del 23, la del 22 no existe

            Dataset("Wprime600_kR2_postEE",
                dataset="/WprimetoMuNu_M-600_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime600_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime600_kR3",
                dataset="/WprimetoMuNu_M-600_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime600_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime600_kR3_postEE",
                dataset="/WprimetoMuNu_M-600_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime600_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime600_kR5",
                dataset="/WprimetoMuNu_M-600_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime600_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime600_kR5_postEE",
                dataset="/WprimetoMuNu_M-600_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime600_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),


            Dataset("Wprime1000_kR0.01",
                dataset="/WprimetoMuNu_M-1000_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1000_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime1000_kR0.01_postEE",
                dataset="/WprimetoMuNu_M-1000_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1000_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime1000_kR0.1",
                dataset="/WprimetoMuNu_M-1000_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1000_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime1000_kR0.1_postEE",
                dataset="/WprimetoMuNu_M-1000_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1000_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime1000_kR2",
                dataset="/WprimetoMuNu_M-1000_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1000_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime1000_kR2_postEE",
                dataset="/WprimetoMuNu_M-1000_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1000_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime1000_kR3",
                dataset="/WprimetoMuNu_M-1000_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1000_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime1000_kR3_postEE",
                dataset="/WprimetoMuNu_M-1000_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1000_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime1000_kR5",
                dataset="/WprimetoMuNu_M-1000_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1000_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime1000_kR5_postEE",
                dataset="/WprimetoMuNu_M-1000_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1000_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),


            Dataset("Wprime1600_kR0.01",
                dataset="/WprimetoMuNu_M-1600_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1600_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime1600_kR0.01_postEE",
                dataset="/WprimetoMuNu_M-1600_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1600_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime1600_kR0.1",
                dataset="/WprimetoMuNu_M-1600_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1600_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime1600_kR0.1_postEE",
                dataset="/WprimetoMuNu_M-1600_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1600_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime1600_kR2",
                dataset="/WprimetoMuNu_M-1600_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1600_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime1600_kR2_postEE",
                dataset="/WprimetoMuNu_M-1600_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1600_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime1600_kR3",
                dataset="/WprimetoMuNu_M-1600_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1600_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime1600_kR3_postEE",
                dataset="/WprimetoMuNu_M-1600_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1600_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime1600_kR5",
                dataset="/WprimetoMuNu_M-1600_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1600_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime1600_kR5_postEE",
                dataset="/WprimetoMuNu_M-1600_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime1600_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            

            Dataset("Wprime2000_kR0.01",
                dataset="/WprimetoMuNu_M-2000_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime2000_kR0.01_postEE",
                dataset="/WprimetoMuNu_M-2000_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime2000_kR0.1",
                dataset="/WprimetoMuNu_M-2000_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime2000_kR0.1_postEE",
                dataset="/WprimetoMuNu_M-2000_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime2000_kR2",
                dataset="/WprimetoMuNu_M-2000_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime2000_kR2_postEE",
                dataset="/WprimetoMuNu_M-2000_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime2000_kR3",
                dataset="/WprimetoMuNu_M-2000_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime2000_kR3_postEE",
                dataset="/WprimetoMuNu_M-2000_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime2000_kR5",
                dataset="/WprimetoMuNu_M-2000_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime2000_kR5_postEE",
                dataset="/WprimetoMuNu_M-2000_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2000_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),


            Dataset("Wprime2600_kR0.01",
                dataset="/WprimetoMuNu_M-2600_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2600_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime2600_kR0.01_postEE",
                dataset="/WprimetoMuNu_M-2600_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2600_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime2600_kR0.1",
                dataset="/WprimetoMuNu_M-2600_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2600_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime2600_kR0.1_postEE",
                dataset="/WprimetoMuNu_M-2600_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2600_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime2600_kR2",
                dataset="/WprimetoMuNu_M-2600_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2600_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime2600_kR2_postEE",
                dataset="/WprimetoMuNu_M-2600_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2600_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime2600_kR3",
                dataset="/WprimetoMuNu_M-2600_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2600_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime2600_kR3_postEE",
                dataset="/WprimetoMuNu_M-2600_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2600_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime2600_kR5",
                dataset="/WprimetoMuNu_M-2600_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2600_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime2600_kR5_postEE",
                dataset="/WprimetoMuNu_M-2600_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime2600_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),


            Dataset("Wprime3000_kR0.01",
                dataset="/WprimetoMuNu_M-3000_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3000_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime3000_kR0.01_postEE",
                dataset="/WprimetoMuNu_M-3000_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3000_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime3000_kR0.1",
                dataset="/WprimetoMuNu_M-3000_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3000_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime3000_kR0.1_postEE",
                dataset="/WprimetoMuNu_M-3000_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3000_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime3000_kR2",
                dataset="/WprimetoMuNu_M-3000_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3000_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime3000_kR2_postEE",
                dataset="/WprimetoMuNu_M-3000_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3000_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime3000_kR3",
                dataset="/WprimetoMuNu_M-3000_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3000_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime3000_kR3_postEE",
                dataset="/WprimetoMuNu_M-3000_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3000_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime3000_kR5",
                dataset="/WprimetoMuNu_M-3000_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3000_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime3000_kR5_postEE",
                dataset="/WprimetoMuNu_M-3000_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3000_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            

            Dataset("Wprime3600_kR0.01",
                dataset="/WprimetoMuNu_M-3600_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime3600_kR0.01_postEE",
                dataset="/WprimetoMuNu_M-3600_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime3600_kR0.1",
                dataset="/WprimetoMuNu_M-3600_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime3600_kR0.1_postEE",
                dataset="/WprimetoMuNu_M-3600_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime3600_kR2",
                dataset="/WprimetoMuNu_M-3600_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime3600_kR2_postEE",
                dataset="/WprimetoMuNu_M-3600_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime3600_kR3",
                dataset="/WprimetoMuNu_M-3600_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime3600_kR3_postEE",
                dataset="/WprimetoMuNu_M-3600_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime3600_kR5",
                dataset="/WprimetoMuNu_M-3600_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime3600_kR5_postEE",
                dataset="/WprimetoMuNu_M-3600_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime3600_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),


            Dataset("Wprime4000_kR0.01",
                dataset="/WprimetoMuNu_M-4000_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4000_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime4000_kR0.01_postEE",
                dataset="/WprimetoMuNu_M-4000_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4000_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime4000_kR0.1",
                dataset="/WprimetoMuNu_M-4000_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4000_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime4000_kR0.1_postEE",
                dataset="/WprimetoMuNu_M-4000_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4000_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime4000_kR2",
                dataset="/WprimetoMuNu_M-4000_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4000_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime4000_kR2_postEE",
                dataset="/WprimetoMuNu_M-4000_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4000_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime4000_kR3",
                dataset="/WprimetoMuNu_M-4000_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4000_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime4000_kR3_postEE",
                dataset="/WprimetoMuNu_M-4000_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4000_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime4000_kR5",
                dataset="/WprimetoMuNu_M-4000_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4000_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime4000_kR5_postEE",
                dataset="/WprimetoMuNu_M-4000_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4000_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            

            Dataset("Wprime4600_kR0.01",
                dataset="/WprimetoMuNu_M-4600_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4600_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime4600_kR0.01_postEE",
                dataset="/WprimetoMuNu_M-4600_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4600_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime4600_kR0.1",
                dataset="/WprimetoMuNu_M-4600_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4600_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime4600_kR0.1_postEE",
                dataset="/WprimetoMuNu_M-4600_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4600_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime4600_kR2",
                dataset="/WprimetoMuNu_M-4600_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4600_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime4600_kR2_postEE",
                dataset="/WprimetoMuNu_M-4600_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4600_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime4600_kR3",
                dataset="/WprimetoMuNu_M-4600_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4600_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime4600_kR3_postEE",
                dataset="/WprimetoMuNu_M-4600_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4600_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime4600_kR5",
                dataset="/WprimetoMuNu_M-4600_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4600_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime4600_kR5_postEE",
                dataset="/WprimetoMuNu_M-4600_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime4600_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            

            Dataset("Wprime5000_kR0.01",
                dataset="/WprimetoMuNu_M-5000_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5000_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime5000_kR0.01_postEE",
                dataset="/WprimetoMuNu_M-5000_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5000_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime5000_kR0.1",
                dataset="/WprimetoMuNu_M-5000_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5000_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime5000_kR0.1_postEE",
                dataset="/WprimetoMuNu_M-5000_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5000_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime5000_kR2",
                dataset="/WprimetoMuNu_M-5000_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5000_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime5000_kR2_postEE",
                dataset="/WprimetoMuNu_M-5000_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5000_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime5000_kR3",
                dataset="/WprimetoMuNu_M-5000_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5000_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime5000_kR3_postEE",
                dataset="/WprimetoMuNu_M-5000_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5000_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime5000_kR5",
                dataset="/WprimetoMuNu_M-5000_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5000_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime5000_kR5_postEE",
                dataset="/WprimetoMuNu_M-5000_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5000_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            

            Dataset("Wprime5600_kR0.01",
                dataset="/WprimetoMuNu_M-5600_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime5600_kR0.01_postEE",
                dataset="/WprimetoMuNu_M-5600_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime5600_kR0.1",
                dataset="/WprimetoMuNu_M-5600_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime5600_kR0.1_postEE",
                dataset="/WprimetoMuNu_M-5600_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime5600_kR2",
                dataset="/WprimetoMuNu_M-5600_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime5600_kR2_postEE",
                dataset="/WprimetoMuNu_M-5600_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime5600_kR3",
                dataset="/WprimetoMuNu_M-5600_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime5600_kR3_postEE",
                dataset="/WprimetoMuNu_M-5600_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime5600_kR5",
                dataset="/WprimetoMuNu_M-5600_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime5600_kR5_postEE",
                dataset="/WprimetoMuNu_M-5600_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime5600_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),

            
            Dataset("Wprime6000_kR0.01",
                dataset="/WprimetoMuNu_M-6000_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6000_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime6000_kR0.01_postEE",
                dataset="/WprimetoMuNu_M-6000_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6000_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime6000_kR0.1",
                dataset="/WprimetoMuNu_M-6000_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6000_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime6000_kR0.1_postEE",
                dataset="/WprimetoMuNu_M-6000_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6000_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime6000_kR2",
                dataset="/WprimetoMuNu_M-6000_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6000_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime6000_kR2_postEE",
                dataset="/WprimetoMuNu_M-6000_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6000_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime6000_kR3",
                dataset="/WprimetoMuNu_M-6000_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6000_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime6000_kR3_postEE",
                dataset="/WprimetoMuNu_M-6000_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6000_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime6000_kR5",
                dataset="/WprimetoMuNu_M-6000_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6000_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime6000_kR5_postEE",
                dataset="/WprimetoMuNu_M-6000_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6000_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            
       
            Dataset("Wprime6600_kR0.01",
                dataset="/WprimetoMuNu_M-6600_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6600_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime6600_kR0.01_postEE",
                dataset="/WprimetoMuNu_M-6600_kR-0p01_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6600_kR0.01"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
            
            Dataset("Wprime6600_kR0.1",
                dataset="/WprimetoMuNu_M-6600_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6600_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime6600_kR0.1_postEE",
                dataset="/WprimetoMuNu_M-6600_kR-0p1_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6600_kR0.1"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime6600_kR2",
                dataset="/WprimetoMuNu_M-6600_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6600_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime6600_kR2_postEE",
                dataset="/WprimetoMuNu_M-6600_kR-2p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6600_kR2"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime6600_kR3",
                dataset="/WprimetoMuNu_M-6600_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6600_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime6600_kR3_postEE",
                dataset="/WprimetoMuNu_M-6600_kR-3p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6600_kR3"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),
     
            Dataset("Wprime6600_kR5",
                dataset="/WprimetoMuNu_M-6600_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6600_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001,), # For datacards

            Dataset("Wprime6600_kR5_postEE",
                dataset="/WprimetoMuNu_M-6600_kR-5p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime6600_kR5"),
                #prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001,
                tags=["postEE"]),     

            

            ### W off-shell ###

            ## WtoMuNu pythia ==> No longer used

            Dataset("Wmunu100to200",
                dataset="/WtoMuNu_M-100to200_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=175.1*1.1328,), # From GenXSecAnalyzer by J. Lee, all of them (LO) x k-factor for Run3 pythia

            Dataset("Wmunu100to200_postEE",
                dataset="/WtoMuNu_M-100to200_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu1_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=175.1*1.1328,
                tags=["postEE"]),

            Dataset("Wmunu200to500",
                dataset="/WtoMuNu_M-200to500_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=7.423*1.1510,),

            Dataset("Wmunu200to500_postEE",
                dataset="/WtoMuNu_M-200to500_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu2_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=7.423*1.1510,
                tags=["postEE"]),

            Dataset("Wmunu500to1000",
                dataset="/WtoMuNu_M-500to1000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=0.254*1.1411,),

            Dataset("Wmunu500to1000_postEE",
                dataset="/WtoMuNu_M-500to1000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu3_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=0.254*1.1411,
                tags=["postEE"]),

            Dataset("Wmunu1000to2000",
                dataset="/WtoMuNu_M-1000to2000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=0.01586*1.1248,),

            Dataset("Wmunu1000to2000_postEE",
                dataset="/WtoMuNu_M-1000to2000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu4_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=0.01586*1.1248,
                tags=["postEE"]),

            Dataset("Wmunu2000to3000",
                dataset="/WtoMuNu_M-2000to3000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=0.0004680*1.2036,),

            Dataset("Wmunu2000to3000_postEE",
                dataset="/WtoMuNu_M-2000to3000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu5_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=0.0004680*1.2036,
                tags=["postEE"]),

            Dataset("Wmunu3000to4000",
                dataset="/WtoMuNu_M-3000to4000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=0.00003197*1.3780,),

            Dataset("Wmunu3000to4000_postEE",
                dataset="/WtoMuNu_M-3000to4000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu6_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=0.00003197*1.3780,
                tags=["postEE"]),

            Dataset("Wmunu4000to5000",
                dataset="/WtoMuNu_M-4000to5000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=0.000002953*1.7551,),

            Dataset("Wmunu4000to5000_postEE",
                dataset="/WtoMuNu_M-4000to5000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu7_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=0.000002953*1.7551,
                tags=["postEE"]),

            Dataset("Wmunu5000to6000",
                dataset="/WtoMuNu_M-5000to6000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=0.0000004031*2.2358,),

            Dataset("Wmunu5000to6000_postEE",
                dataset="/WtoMuNu_M-5000to6000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu8_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=0.0000004031*2.2358,
                tags=["postEE"]),

            Dataset("Wmunu6000",
                dataset="/WtoMuNu_M-6000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=0.0000001049*3.3275,),

            Dataset("Wmunu6000_postEE",
                dataset="/WtoMuNu_M-6000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu9_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=0.0000001049*3.3275,
                tags=["postEE"]),

            ## WtoTauNu pythia ==> No longer used 

            Dataset("Wtaunu100to200",
                dataset="/WtoTauNu_M-100to200_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=174.7*1.1009,), # From GenXSecAnalyzer by J. Lee, all of them (LO) x k-factor for Run3 pythia

            Dataset("Wtaunu100to200_postEE",
                dataset="/WtoTauNu_M-100to200_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=174.7*1.1009,
                tags=["postEE"]),

            Dataset("Wtaunu200to500",
                dataset="/WtoTauNu_M-200to500_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=7.485*1.0941,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu200to500_postEE",
                dataset="/WtoTauNu_M-200to500_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=7.485*1.0941,
                tags=["postEE"]),

            Dataset("Wtaunu500to1000",
                dataset="/WtoTauNu_M-500to1000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=0.2479*1.1109,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu500to1000_postEE",
                dataset="/WtoTauNu_M-500to1000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=0.2479*1.1109,
                tags=["postEE"]),

            Dataset("Wtaunu1000to2000",
                dataset="/WtoTauNu_M-1000to2000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=0.01584*1.0729,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu1000to2000_postEE",
                dataset="/WtoTauNu_M-1000to2000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=0.01584*1.0729,
                tags=["postEE"]),

            Dataset("Wtaunu2000to3000",
                dataset="/WtoTauNu_M-2000to3000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=0.000482*1.1327,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu2000to3000_postEE",
                dataset="/WtoTauNu_M-2000to3000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=0.000482*1.1327,
                tags=["postEE"]),

            Dataset("Wtaunu3000to4000",
                dataset="/WtoTauNu_M-3000to4000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=0.0000311*1.3933,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu3000to4000_postEE",
                dataset="/WtoTauNu_M-3000to4000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=0.0000311*1.3933,
                tags=["postEE"]),

            Dataset("Wtaunu4000to5000",
                dataset="/WtoTauNu_M-4000to5000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=0.00000297*1.7382,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu4000to5000_postEE",
                dataset="/WtoTauNu_M-4000to5000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=0.00000297*1.7382,
                tags=["postEE"]),

            Dataset("Wtaunu5000to6000",
                dataset="/WtoTauNu_M-5000to6000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=0.000000409*2.2178,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu5000to6000_postEE",
                dataset="/WtoTauNu_M-5000to6000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=0.000000409*2.2178,
                tags=["postEE"]),

            Dataset("Wtaunu6000",
                dataset="/WtoTauNu_M-6000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=0.000000101*3.5260,), # From XSGenAnalyzer by J. Lee, all of them (LO)

            Dataset("Wtaunu6000_postEE",
                dataset="/WtoTauNu_M-6000_TuneCP5_13p6TeV_pythia8-tauola/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wtaunu_postEE"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=0.000000101*3.5260,
                tags=["postEE"]),

            ## W off-shell madgraph

            Dataset("Wlnu120to200",
                dataset="/WtoLNu-4Jets_MLNu-120to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu1"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="preEE",
                xs=167.1,), # From Jeongeun --> GenXSecAnalyzer (LO) // NOTE: Final additive + mixed k-factors updated in October2024 in plotting

            Dataset("Wlnu120to200_postEE",
                dataset="/WtoLNu-4Jets_MLNu-120to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                #merging={"preselection":3}, # Descomenta para el proximo reprocess!!!
                runPeriod="postEE",
                xs=167.1, 
                tags=["postEE"]),

            Dataset("Wlnu200to400",
                dataset="/WtoLNu-4Jets_MLNu-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu2"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=20.43,), 

            Dataset("Wlnu200to400_postEE",
                dataset="/WtoLNu-4Jets_MLNu-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=20.43, 
                tags=["postEE"]),

            Dataset("Wlnu400to800",
                dataset="/WtoLNu-4Jets_MLNu-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu3"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=1.596,), 

            Dataset("Wlnu400to800_postEE",
                dataset="/WtoLNu-4Jets_MLNu-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=1.596,
                tags=["postEE"]),

            Dataset("Wlnu800to1500",
                dataset="/WtoLNu-4Jets_MLNu-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu4"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.1095,),

            Dataset("Wlnu800to1500_postEE",
                dataset="/WtoLNu-4Jets_MLNu-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.1095,
                tags=["postEE"]),

            Dataset("Wlnu1500to2500",
                dataset="/WtoLNu-4Jets_MLNu-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu5"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.006377,), 

            Dataset("Wlnu1500to2500_postEE",
                dataset="/WtoLNu-4Jets_MLNu-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.006377,
                tags=["postEE"]),

            Dataset("Wlnu2500to4000",
                dataset="/WtoLNu-4Jets_MLNu-2500to4000_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu6"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.0003464,),

            Dataset("Wlnu2500to4000_postEE",
                dataset="/WtoLNu-4Jets_MLNu-2500to4000_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.0003464,
                tags=["postEE"]),

            Dataset("Wlnu4000to6000",
                dataset="/WtoLNu-4Jets_MLNu-4000to6000_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu7"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.00001074,), 

            Dataset("Wlnu4000to6000_postEE",
                dataset="/WtoLNu-4Jets_MLNu-4000to6000_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.00001074,
                tags=["postEE"]),

            Dataset("Wlnu6000",
                dataset="/WtoLNu-4Jets_MLNu-6000_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu8"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.0000004198,), 

            Dataset("Wlnu6000_postEE",
                dataset="/WtoLNu-4Jets_MLNu-6000_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Wlnu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.0000004198,
                tags=["postEE"]),

        
            ### W + jets inclusive (NLO) ###

            Dataset("Wjets",
                dataset="/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wonshell"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=67710.0,), # From SMP-22-017: Theoretical xs at NNNLO(QCD)xNLO(EWK) is 62390 pb ==> k-fact (at plotting) = 0.9214 (0.9290 / 0.9119)

            Dataset("Wjets_postEE",
                dataset="/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wonshell_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=67710.0,
                tags=["postEE"]),

            ## W + 4jets inclusive (LO) ##

            Dataset("Wjets_4j",
                dataset="/WtoLNu-4Jets_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("W+4j"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="preEE",
                xs=55390,), # From SMP-22-017: Theoretical xs at NNNLO(QCD)xNLO(EWK) is 62390 pb ==> k-fact = 1.126

            Dataset("Wjets_4j_postEE",
                dataset="/WtoLNu-4Jets_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6_ext1-v2/"
                    "NANOAODSIM",
                process=self.processes.get("W+4j_postEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                xs=55390,
                merging={"preselection":2},
                tags=["postEE"]),

            
            ## W boosted --> HT-binned ##

            Dataset("Wlnu_HT-40to100",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-40to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost0"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preEE",
                xs=4265,), # From GenXSecAnalyzer (LO)

            Dataset("Wlnu_HT-40to100_postEE",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-40to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postEE",
                xs=4265, # inclusive k-factor from LO to NNLO
                tags=["postEE"]),

            Dataset("Wlnu_HT-100to400",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost1"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preEE",
                xs=1636,),

            Dataset("Wlnu_HT-100to400_postEE",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-100to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postEE",
                xs=1636,
                tags=["postEE"]),

            Dataset("Wlnu_HT-400to800",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost2"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=59.70,),

            Dataset("Wlnu_HT-400to800_postEE",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=59.70,
                tags=["postEE"]),

            Dataset("Wlnu_HT-800to1500",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost3"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=6.211,),

            Dataset("Wlnu_HT-800to1500_postEE",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=6.211,
                tags=["postEE"]),

            Dataset("Wlnu_HT-1500to2500",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost4"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.4500,),

            Dataset("Wlnu_HT-1500to2500_postEE",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.4500,
                tags=["postEE"]),

            Dataset("Wlnu_HT-2500",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost5"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.03080,),

            Dataset("Wlnu_HT-2500_postEE",
                dataset="/WtoLNu-4Jets_MLNu-0to120_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wboost_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.03080,
                tags=["postEE"]),

            ### W boosted --> ptLNu-binned ###

            Dataset("Wlnu_ptW-40to100_1J",
                dataset="/WtoLNu-2Jets_PTLNu-40to100_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW1"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preEE",
                xs=4379,), # From GenXSecAnalyzer (NLO) // NNLO k-factor from inclusive W+2j sample at plotting

            Dataset("Wlnu_ptW-40to100_1J_postEE",
                dataset="/WtoLNu-2Jets_PTLNu-40to100_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postEE",
                xs=4379,
                tags=["postEE"]),
            
            Dataset("Wlnu_ptW-40to100_2J",
                dataset="/WtoLNu-2Jets_PTLNu-40to100_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW1"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preEE",
                xs=1604,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-40to100_2J_postEE",
                dataset="/WtoLNu-2Jets_PTLNu-40to100_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postEE",
                xs=1604,
                tags=["postEE"]),
            
            Dataset("Wlnu_ptW-100to200_1J",
                dataset="/WtoLNu-2Jets_PTLNu-100to200_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW2"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preEE",
                xs=367.5,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-100to200_1J_postEE",
                dataset="/WtoLNu-2Jets_PTLNu-100to200_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postEE",
                xs=367.5,
                tags=["postEE"]),
            
            Dataset("Wlnu_ptW-100to200_2J",
                dataset="/WtoLNu-2Jets_PTLNu-100to200_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW2"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preEE",
                xs=420.7,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-100to200_2J_postEE",
                dataset="/WtoLNu-2Jets_PTLNu-100to200_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postEE",
                xs=420.7,
                tags=["postEE"]),
                    
            Dataset("Wlnu_ptW-200to400_1J",
                dataset="/WtoLNu-2Jets_PTLNu-200to400_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW3"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="preEE",
                xs=25.63,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-200to400_1J_postEE",
                dataset="/WtoLNu-2Jets_PTLNu-200to400_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="postEE",
                xs=25.63,
                tags=["postEE"]),
            
            Dataset("Wlnu_ptW-200to400_2J",
                dataset="/WtoLNu-2Jets_PTLNu-200to400_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW3"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="preEE",
                xs=54.60,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-200to400_2J_postEE",
                dataset="/WtoLNu-2Jets_PTLNu-200to400_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v1/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="postEE",
                xs=54.60,
                tags=["postEE"]),
                                    
            Dataset("Wlnu_ptW-400to600_1J",
                dataset="/WtoLNu-2Jets_PTLNu-400to600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW4"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.873,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-400to600_1J_postEE",
                dataset="/WtoLNu-2Jets_PTLNu-400to600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v1/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.873,
                tags=["postEE"]),
            
            Dataset("Wlnu_ptW-400to600_2J",
                dataset="/WtoLNu-2Jets_PTLNu-400to600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW4"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=3.124,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-400to600_2J_postEE",
                dataset="/WtoLNu-2Jets_PTLNu-400to600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v1/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=3.124,
                tags=["postEE"]),
                                                
            Dataset("Wlnu_ptW-600_1J",
                dataset="/WtoLNu-2Jets_PTLNu-600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW5"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.1025,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-600_1J_postEE",
                dataset="/WtoLNu-2Jets_PTLNu-600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v1/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.1025,
                tags=["postEE"]),
            
            Dataset("Wlnu_ptW-600_2J",
                dataset="/WtoLNu-2Jets_PTLNu-600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW5"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.5262,), # From GenXSecAnalyzer (NLO)

            Dataset("Wlnu_ptW-600_2J_postEE",
                dataset="/WtoLNu-2Jets_PTLNu-600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v1/"
                    "NANOAODSIM",
                process=self.processes.get("W_ptW_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.5262,
                tags=["postEE"]),
            
            
            ### Top ###

            # TTbar

            Dataset("TT_2l2nu",
                dataset="/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preEE",
                xs=96.9,), # From TOP-22-012

            Dataset("TT_2l2nu_postEE",
                dataset="/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postEE",
                xs=96.9,
                tags=["postEE"]),

            Dataset("TT_lnu2q",
                dataset="/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="preEE",
                xs=404.0,), # From TOP-22-012

            Dataset("TT_lnu2q_postEE",
                dataset="/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":5},
                runPeriod="postEE",
                xs=404.0,
                tags=["postEE"]),

            # Single Top

            Dataset("ST_tW-lnu2q",
                dataset="/TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=19.31,), # From https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopNNLORef x BR

            Dataset("ST_tW-lnu2q_postEE",
                dataset="/TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=19.31,
                tags=["postEE"]),

            Dataset("ST_tW-2l2nu",
                dataset="/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=4.663,),

            Dataset("ST_tW-2l2nu_postEE",
                dataset="/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=4.663,
                tags=["postEE"]),

            # The 4q samples have a very low impact, so no longer used
            Dataset("ST_tW-4q",
                dataset="/TWminusto4Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=19.98,),

            Dataset("ST_tW-4q_postEE",
                dataset="/TWminusto4Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=19.98,
                tags=["postEE"]),

            Dataset("ST_tbarW-lnu2q",
                dataset="/TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=19.31,), 

            Dataset("ST_tbarW-lnu2q_postEE",
                dataset="/TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=19.31,
                tags=["postEE"]),

            Dataset("ST_tbarW-2l2nu",
                dataset="/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=4.663,), 

            Dataset("ST_tbarW-2l2nu_postEE",
                dataset="/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=4.663,
                tags=["postEE"]),

            # The 4q samples have a very low impact, so no longer used
            Dataset("ST_tbarW-4q",
                dataset="/TbarWplusto4Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=19.98,),

            Dataset("ST_tbarW-4q_postEE",
                dataset="/TbarWplusto4Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=19.98,
                tags=["postEE"]),

            Dataset("ST_s-top",
                dataset="/TBbartoLplusNuBbar-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=3.623,),

            Dataset("ST_s-top_postEE",
                dataset="/TBbartoLplusNuBbar-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=3.623,
                tags=["postEE"]),

            Dataset("ST_s-tbar",
                dataset="/TbarBtoLminusNuB-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=3.623,),

            Dataset("ST_s-tbar_postEE",
                dataset="/TbarBtoLminusNuB-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=3.623,
                tags=["postEE"]),

            Dataset("ST_t-top",
                dataset="/TBbarQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=145.0,),

            Dataset("ST_t-top_postEE",
                dataset="/TBbarQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=145.0,
                tags=["postEE"]),

            Dataset("ST_t-tbar",
                dataset="/TbarBQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=87.2,),

            Dataset("ST_t-tbar_postEE",
                dataset="/TbarBQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=87.2,
                tags=["postEE"]),

            ### Drell-Yan ###

            # ZtoMuMu

            Dataset("Zmumu_M-50to120",
                dataset="/DYto2Mu_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=2219.0,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-50to120_postEE",
                dataset="/DYto2Mu_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=2219.0,
                tags=["postEE"]),

            Dataset("Zmumu_M-120to200",
                dataset="/DYto2Mu_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=21.65,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-120to200_postEE",
                dataset="/DYto2Mu_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=21.65,
                tags=["postEE"]),

            Dataset("Zmumu_M-200to400",
                dataset="/DYto2Mu_MLL-200to400_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=3.058,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-200to400_postEE",
                dataset="/DYto2Mu_MLL-200to400_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=3.058,
                tags=["postEE"]),

            Dataset("Zmumu_M-400to800",
                dataset="/DYto2Mu_MLL-400to800_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.2691,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-400to800_postEE",
                dataset="/DYto2Mu_MLL-400to800_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.2691,
                tags=["postEE"]),

            Dataset("Zmumu_M-800to1500",
                dataset="/DYto2Mu_MLL-800to1500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.01915,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-800to1500_postEE",
                dataset="/DYto2Mu_MLL-800to1500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.01915,
                tags=["postEE"]),

            Dataset("Zmumu_M-1500to2500",
                dataset="/DYto2Mu_MLL-1500to2500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001111,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-1500to2500_postEE",
                dataset="/DYto2Mu_MLL-1500to2500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001111,
                tags=["postEE"]),

            Dataset("Zmumu_M-2500to4000",
                dataset="/DYto2Mu_MLL-2500to4000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.00005949,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-2500to4000_postEE",
                dataset="/DYto2Mu_MLL-2500to4000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.00005949,
                tags=["postEE"]),

            Dataset("Zmumu_M-4000to6000",
                dataset="/DYto2Mu_MLL-4000to6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.000001558,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-4000to6000_postEE",
                dataset="/DYto2Mu_MLL-4000to6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.000001558,
                tags=["postEE"]),

            Dataset("Zmumu_M-6000",
                dataset="/DYto2Mu_MLL-6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.00000003519,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-6000_postEE",
                dataset="/DYto2Mu_MLL-6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.00000003519,
                tags=["postEE"]),

            # ZtoTauTau

            Dataset("Ztautau_M-50to120",
                dataset="/DYto2Tau_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=2219.0,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-50to120_postEE",
                dataset="/DYto2Tau_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=2219.0,
                tags=["postEE"]),

            Dataset("Ztautau_M-120to200",
                dataset="/DYto2Tau_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=21.65,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-120to200_postEE",
                dataset="/DYto2Tau_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=21.65,
                tags=["postEE"]),

            Dataset("Ztautau_M-200to400",
                dataset="/DYto2Tau_MLL-200to400_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=3.058,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-200to400_postEE",
                dataset="/DYto2Tau_MLL-200to400_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=3.058,
                tags=["postEE"]),

            Dataset("Ztautau_M-400to800",
                dataset="/DYto2Tau_MLL-400to800_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.2691,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-400to800_postEE",
                dataset="/DYto2Tau_MLL-400to800_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.2691,
                tags=["postEE"]),

            Dataset("Ztautau_M-800to1500",
                dataset="/DYto2Tau_MLL-800to1500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.01915,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-800to1500_postEE",
                dataset="/DYto2Tau_MLL-800to1500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.01915,
                tags=["postEE"]),

            Dataset("Ztautau_M-1500to2500",
                dataset="/DYto2Tau_MLL-1500to2500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.001111,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-1500to2500_postEE",
                dataset="/DYto2Tau_MLL-1500to2500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.001111,
                tags=["postEE"]),

            Dataset("Ztautau_M-2500to4000",
                dataset="/DYto2Tau_MLL-2500to4000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.00005949,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-2500to4000_postEE",
                dataset="/DYto2Tau_MLL-2500to4000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.00005949,
                tags=["postEE"]),

            Dataset("Ztautau_M-4000to6000",
                dataset="/DYto2Tau_MLL-4000to6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.000001558,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-4000to6000_postEE",
                dataset="/DYto2Tau_MLL-4000to6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.000001558,
                tags=["postEE"]),

            Dataset("Ztautau_M-6000",
                dataset="/DYto2Tau_MLL-6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.00000003519,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-6000_postEE",
                dataset="/DYto2Tau_MLL-6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.00000003519,
                tags=["postEE"]),

            # ZtoNuNu

            Dataset("Znunu_HT-100to200",
                dataset="/Zto2Nu-4Jets_HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=273.5,), # From GenXSecAnalyzer (NLO)

            Dataset("Znunu_HT-100to200_postEE",
                dataset="/Zto2Nu-4Jets_HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=273.5,
                tags=["postEE"]),

            Dataset("Znunu_HT-200to400",
                dataset="/Zto2Nu-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=76.09,), # From GenXSecAnalyzer (NLO)

            Dataset("Znunu_HT-200to400_postEE",
                dataset="/Zto2Nu-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=76.09,
                tags=["postEE"]),

            Dataset("Znunu_HT-400to800",
                dataset="/Zto2Nu-4Jets_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=13.19,), # From GenXSecAnalyzer (NLO)

            Dataset("Znunu_HT-400to800_postEE",
                dataset="/Zto2Nu-4Jets_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=13.19,
                tags=["postEE"]),

            Dataset("Znunu_HT-800to1500",
                dataset="/Zto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=1.364,), # From GenXSecAnalyzer (NLO)

            Dataset("Znunu_HT-800to1500_postEE",
                dataset="/Zto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=1.364,
                tags=["postEE"]),

            Dataset("Znunu_HT-1500to2500",
                dataset="/Zto2Nu-4Jets_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.09843,), # From GenXSecAnalyzer (NLO)

            Dataset("Znunu_HT-1500to2500_postEE",
                dataset="/Zto2Nu-4Jets_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.09843,
                tags=["postEE"]),

            Dataset("Znunu_HT-2500",
                dataset="/Zto2Nu-4Jets_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.006699,), # From GenXSecAnalyzer (NLO)

            Dataset("Znunu_HT-2500_postEE",
                dataset="/Zto2Nu-4Jets_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Znunu_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.006699,
                tags=["postEE"]),


            ### DiBoson ###

            Dataset("WW_2l2nu",
                dataset="/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WW"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=12.98,), # From 13 TeV value with 4% expected increase with MCFM x BR

            Dataset("WW_2l2nu_postEE",
                dataset="/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WW_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=12.98,
                tags=["postEE"]),

            Dataset("WW_lnu2q",
                dataset="/WWtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WW"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=53.73,),

            Dataset("WW_lnu2q_postEE",
                dataset="/WWtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WW_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=53.73,
                tags=["postEE"]),

            # The 4q samples have a very low impact, so no longer used
            Dataset("WW_4q",
                dataset="/WWto4Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WW"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=55.59,),

            Dataset("WW_4q_postEE",
                dataset="/WWto4Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WW_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=55.59,
                tags=["postEE"]),

            Dataset("WZ_2l2q",
                dataset="/WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=3.661,), # From MATRIX (SMP-22-017 at NNLO) x BR

            Dataset("WZ_2l2q_postEE",
                dataset="/WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=3.661,
                tags=["postEE"]),

            Dataset("WZ_3lnu",
                dataset="/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=1.769,),  

            Dataset("WZ_3lnu_postEE",
                dataset="/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=1.769,
                tags=["postEE"]),

            Dataset("WZ_lnu2q",
                dataset="/WZtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=12.39,),  

            Dataset("WZ_lnu2q_postEE",
                dataset="/WZtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=12.39,
                tags=["postEE"]),

            Dataset("ZZ",
                dataset="/ZZ_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ZZ"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=16.7,), # From MATRIX (SMP-22-017 at NNLO)

            Dataset("ZZ_postEE",
                dataset="/ZZ_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ZZ_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=16.7,
                tags=["postEE"]),

            ## Wgamma

            Dataset("Wg_pT-10to100",
                dataset="/WGtoLNuG-1Jets_PTG-10to100_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="preEE",
                xs=668.6,), 

            Dataset("Wg_pT-10to100_postEE",
                dataset="/WGtoLNuG-1Jets_PTG-10to100_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":2},
                runPeriod="postEE",
                xs=668.6,
                tags=["postEE"]),

            Dataset("Wg_pT-100to200",
                dataset="/WGtoLNuG-1Jets_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=2.224,), 

            Dataset("Wg_pT-100to200_postEE",
                dataset="/WGtoLNuG-1Jets_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=2.224,
                tags=["postEE"]),

            Dataset("Wg_pT-200to400",
                dataset="/WGtoLNuG-1Jets_PTG-200to400_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.2914,), 

            Dataset("Wg_pT-200to400_postEE",
                dataset="/WGtoLNuG-1Jets_PTG-200to400_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.2914,
                tags=["postEE"]),

            Dataset("Wg_pT-400to600",
                dataset="/WGtoLNuG-1Jets_PTG-400to600_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.02232,), 

            Dataset("Wg_pT-400to600_postEE",
                dataset="/WGtoLNuG-1Jets_PTG-400to600_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.02232,
                tags=["postEE"]),

            Dataset("Wg_pT-600",
                dataset="/WGtoLNuG-1Jets_PTG-600_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=0.004910,), 

            Dataset("Wg_pT-600_postEE",
                dataset="/WGtoLNuG-1Jets_PTG-600_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Wgamma_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=0.004910,
                tags=["postEE"]),


            ### QCD ###

            Dataset("QCD_Pt-120to170",
                dataset="/QCD_PT-120to170_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=23150,), # From GenXSecAnalyzer

            Dataset("QCD_Pt-120to170_postEE",
                dataset="/QCD_PT-120to170_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=23150,
                tags=["postEE"]),

            Dataset("QCD_Pt-170to300",
                dataset="/QCD_PT-170to300_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=7760,), # From GenXSecAnalyzer

            Dataset("QCD_Pt-170to300_postEE",
                dataset="/QCD_PT-170to300_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=7760,
                tags=["postEE"]),

            Dataset("QCD_Pt-300to470",
                dataset="/QCD_PT-300to470_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=698.9,), # From GenXSecAnalyzer

            Dataset("QCD_Pt-300to470_postEE",
                dataset="/QCD_PT-300to470_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=698.9,
                tags=["postEE"]),

            Dataset("QCD_Pt-470to600",
                dataset="/QCD_PT-470to600_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=67.79,), # From GenXSecAnalyzer

            Dataset("QCD_Pt-470to600_postEE",
                dataset="/QCD_PT-470to600_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=67.79,
                tags=["postEE"]),

            Dataset("QCD_Pt-600to800",
                dataset="/QCD_PT-600to800_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=21.24,), # From GenXSecAnalyzer

            Dataset("QCD_Pt-600to800_postEE",
                dataset="/QCD_PT-600to800_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=21.24,
                tags=["postEE"]),

            Dataset("QCD_Pt-800to1000",
                dataset="/QCD_PT-800to1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=3.891,), # From GenXSecAnalyzer

            Dataset("QCD_Pt-800to1000_postEE",
                dataset="/QCD_PT-800to1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=3.891,
                tags=["postEE"]),

            Dataset("QCD_Pt-1000",
                dataset="/QCD_PT-1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                xs=1.320,), # From GenXSecAnalyzer

            Dataset("QCD_Pt-1000_postEE",
                dataset="/QCD_PT-1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("QCD_Pt_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                xs=1.320,
                tags=["postEE"]),

 
            ### DATA ###

            # ReReco CDE + PromptReco FG

            Dataset("ReReco_2022_C_SingleMuon",
                dataset="/SingleMuon/Run2022C-22Sep2023-v1/NANOAOD",
                process=self.processes.get("ReRecoData2022_preEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                runEra="C",
                ),

            Dataset("ReReco_2022_C_Muon",
                dataset="/Muon/Run2022C-22Sep2023-v1/NANOAOD",
                process=self.processes.get("ReRecoData2022_preEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                runEra="C",
                ),

            Dataset("ReReco_2022_D",
                dataset="/Muon/Run2022D-22Sep2023-v1/NANOAOD",
                process=self.processes.get("ReRecoData2022_preEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preEE",
                runEra="D",
                ),

            Dataset("ReReco_2022_E",
                dataset="/Muon/Run2022E-22Sep2023-v1/NANOAOD",
                process=self.processes.get("ReRecoData2022_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                runEra="E",
                tags=["postEE"]),

            Dataset("ReReco_2022_F",
                dataset="/Muon/Run2022F-22Sep2023-v2/NANOAOD",
                process=self.processes.get("ReRecoData2022_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                merging={"preselection":3},
                runPeriod="postEE",
                runEra="F",
                tags=["postEE"]),

            Dataset("ReReco_2022_G",
                dataset="/Muon/Run2022G-22Sep2023-v1/NANOAOD",
                process=self.processes.get("ReRecoData2022_postEE"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postEE",
                runEra="G",
                tags=["postEE"]),


            # JetMET Datasets

            Dataset("JetMET2022_F",
                dataset="/JetMET/Run2022F-PromptNanoAODv11_v1-v2/NANOAOD",
                process=self.processes.get("JetMET2022_postEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                runEra="F",
                tags=["JetMET"]),

            Dataset("JetMET2022_G",
                dataset="/Muon/Run2022G-PromptNanoAODv11_v1-v2/NANOAOD",
                process=self.processes.get("JetMET2022_postEE"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                runPeriod="postEE",
                runEra="G",
                tags=["JetMET"]),



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

            #Feature("genJet_HT_peak", "genHT", binning=(200, 0, 400),
            #    x_title=Label("GenJet HT"),
            #    units="GeV"),

            #Feature("genJet_HT_tail", "genHT", binning=(200, 0, 4000),
            #    x_title=Label("GenJet HT"),
            #    units="GeV"),

            # LHE distributions

            Feature("lhe_Wmass_peak", "lhe_Wmass", binning=(200, 0, 400),
                x_title=Label("LHE m_{W}"),
                units="GeV"),

            Feature("lhe_Wmass_tail", "lhe_Wmass", binning=(200, 0, 7000),
                x_title=Label("LHE m_{W}"),
                units="GeV"),

            Feature("lhe_Wpt_peak", "lhe_Wpt", binning=(200, 0, 120),
                x_title=Label("LHE W p_{T}"),
                units="GeV"),

            Feature("lhe_Wpt_tail", "lhe_Wpt", binning=(200, 0, 2000),
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

        ### For PDF plots ###
        mTforPDF = [
            Feature("mT", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*TypeICorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - TypeICorrMET_phi)) )",
                binning=(80, 80, 8000),
                x_title=Label("m_{T}"),
                units="GeV"),
        ]

        ### For ScaleMap Region Population ###
        etas = [-2.4, -2.1, -1.2, 0, 1.2, 2.1, 2.4]
        phis_deg = [-180, -60, 60, 180]
        phis = [-math.pi, -math.pi/3.0, math.pi/3.0, math.pi]
        axis = []
        selections = []

        for i in range(len(etas)-1):
            for j in range(len(phis)-1):
                axis.append(str(etas[i])+" < #eta < "+str(etas[i+1]) + " , " + str(phis_deg[j])+" < #phi < "+str(phis_deg[j+1]))
                selections.append( "(Muon_eta.at(goodMuIdx) > " + str(etas[i]) + " && Muon_eta.at(goodMuIdx) <= " + str(etas[i+1]) + " && Muon_phi.at(goodMuIdx) > " + str(phis[j]) + " && Muon_phi.at(goodMuIdx) <= " + str(phis[j+1]) + ")" )
                
        mT_regions = []
        
        for x,sel in enumerate(selections):
            mT_regions.append( Feature("mT_%s" %x, "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*TypeICorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - TypeICorrMET_phi)) )", 
            binning=(70, 80, 7000),
            selection=sel,
            x_title=Label("m_{T}  " + axis[x]),
            units="GeV"), )

            
        #### mT for limit extraction ####
        binningResolution = [400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3300, 3600, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000]
        lastBinMerged = [400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3300, 3600, 4000, 9000]
        binningErrorPt = [400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1700, 2000, 2400, 3000, 3600, 5000, 6000, 7000, 9000]
        
        mT_limit = [

            # Type-I + TuneP
            #Feature("mT", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{CorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{CorrMET_phi}})) )",
            #    binning=(69, 120, 7000),
            #    systematics=["CMS_scale_met_2022"],
            #    x_title=Label("m_{T}"),
            #    units="GeV"),

            # ONLY Type-I
            Feature("mT", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{TypeICorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{TypeICorrMET_phi}})) )",
                binning=(66, 400, 7000),
                systematics=["CMS_scale_met_2022"],
                x_title=Label("m_{T}"),
                units="GeV"),
            
            Feature("mT_binRes", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{TypeICorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{TypeICorrMET_phi}})) )",
                binning=binningResolution,
                systematics=["CMS_scale_met_2022"],
                x_title=Label("m_{T}"),
                units="GeV"),
            
            Feature("mT_lastBinMerge", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{TypeICorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{TypeICorrMET_phi}})) )",
                binning=lastBinMerged,
                systematics=["CMS_scale_met_2022"],
                x_title=Label("m_{T}"),
                units="GeV"),

            Feature("mT_pTerror", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{TypeICorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{TypeICorrMET_phi}})) )",
                binning=binningErrorPt,
                systematics=["CMS_scale_met_2022"],
                x_title=Label("m_{T}"),
                units="GeV"),

            ## mT with QCD cleaning (MET-mu cut) ##

            Feature("mT_reference", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{TypeICorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{TypeICorrMET_phi}})) )",
                binning=binningErrorPt,
                systematics=["CMS_scale_met_2022"],
                selection="METnoMu_pt > 250 ? dPhi_METnoMu > 0.4 : 1",
                x_title=Label("m_{T}"),
                units="GeV"),
                                    
            Feature("mT_tight", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{TypeICorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{TypeICorrMET_phi}})) )",
                binning=binningErrorPt,
                systematics=["CMS_scale_met_2022"],
                selection="METnoMu_pt > 150 ? dPhi_METnoMu > 0.2 : 1",
                x_title=Label("m_{T}"),
                units="GeV"),

            Feature("mT_tight2", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*TypeICorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - TypeICorrMET_phi)) )",
                binning=(86, 400, 9000),
                selection="METnoMu_pt > 150 ? dPhi_METnoMu > 0.2 : 1",
                x_title=Label("m_{T}"),
                units="GeV"),
            
            ## mTs for convenor checks ##
            
            Feature("mT_200_eta2.0", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{TypeICorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{TypeICorrMET_phi}})) )",
                binning=(68, 200, 7000),
                selection="fabs(Muon_eta.at(goodMuIdx)) < 2.0",
                systematics=["CMS_scale_met_2022"],
                x_title=Label("m_{T}"),
                units="GeV"),
                        
            Feature("mT_300_eta2.0", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{TypeICorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{TypeICorrMET_phi}})) )",
                binning=(67, 300, 7000),
                selection="fabs(Muon_eta.at(goodMuIdx)) < 2.0",
                systematics=["CMS_scale_met_2022"],
                x_title=Label("m_{T}"),
                units="GeV"),
                        
            Feature("mT_400_eta2.0", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{TypeICorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{TypeICorrMET_phi}})) )",
                binning=(66, 400, 7000),
                selection="fabs(Muon_eta.at(goodMuIdx)) < 2.0",
                systematics=["CMS_scale_met_2022"],
                x_title=Label("m_{T}"),
                units="GeV"),
            
            # mT for Goodness of Fit
            Feature("mT_GoF_200", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{TypeICorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{TypeICorrMET_phi}})) )",
                binning=(18, 200, 2000),
                systematics=["CMS_scale_met_2022"],
                x_title=Label("m_{T}"),
                units="GeV"),

            Feature("mT_GoF_300", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{TypeICorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{TypeICorrMET_phi}})) )",
                binning=(17, 300, 2000),
                systematics=["CMS_scale_met_2022"],
                x_title=Label("m_{T}"),
                units="GeV"),
            
            Feature("mT_GoF_400", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{TypeICorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{TypeICorrMET_phi}})) )",
                binning=(16, 400, 2000),
                systematics=["CMS_scale_met_2022"],
                x_title=Label("m_{T}"),
                units="GeV"),
            
            # mT for Goodness of Fit --> |eta| < 2.0
            Feature("mT_GoF_200_eta2.0", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{TypeICorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{TypeICorrMET_phi}})) )",
                binning=(18, 200, 2000),
                selection="fabs(Muon_eta.at(goodMuIdx)) < 2.0",
                systematics=["CMS_scale_met_2022"],
                x_title=Label("m_{T}"),
                units="GeV"),

            Feature("mT_GoF_300_eta2.0", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{TypeICorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{TypeICorrMET_phi}})) )",
                binning=(17, 300, 2000),
                selection="fabs(Muon_eta.at(goodMuIdx)) < 2.0",
                systematics=["CMS_scale_met_2022"],
                x_title=Label("m_{T}"),
                units="GeV"),
            
            Feature("mT_GoF_400_eta2.0", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*{{TypeICorrMET_pt}}*(1 - cos(Muon_phi.at(goodMuIdx) - {{TypeICorrMET_phi}})) )",
                binning=(16, 400, 2000),
                selection="fabs(Muon_eta.at(goodMuIdx)) < 2.0",
                systematics=["CMS_scale_met_2022"],
                x_title=Label("m_{T}"),
                units="GeV"),
            
            
            ## Weights for systematics ##
            Feature("puWeight", "puWeight", binning=(20, 0, 2),
                systematics=["CMS_pileup"],
                x_title=Label("puWeight")),

            Feature("mu_recoSF_weight", "mu_recoSF_weight", binning=(20, 0, 2),
                systematics=["CMS_eff_m_reco_2022"],
                x_title=Label("mu_recoSF_weight")),
            
            Feature("mu_idSF_weight", "mu_idSF_weight", binning=(20, 0, 2),
                systematics=["CMS_eff_m_id_2022"],
                x_title=Label("mu_idSF_weight")),
            
            Feature("mu_isoSF_weight", "mu_isoSF_weight", binning=(20, 0, 2),
                systematics=["CMS_eff_m_iso_2022"],
                x_title=Label("mu_isoSF_weight")),
            
            Feature("mu_hltSF_weight", "mu_hltSF_weight", binning=(20, 0, 2),
                systematics=["CMS_eff_m_trigger_2022"],
                x_title=Label("mu_hltSF_weight")),

            Feature("btag_weight", "btag_weight", binning=(20, 0, 2),
                systematics=["CMS_eff_b_2022"],
                x_title=Label("btag_weight")),

            Feature("Wkfact", "Wkfact", binning=(20, 0, 2),
                systematics=["CMS_EXO24021_W_kfactor"],
                x_title=Label("W k-factor")),

            Feature("PDFweight_total", "PDFweight_total", binning=(20, 0, 2),
                systematics=["pdf_qqbar"],
                x_title=Label("PDF uncertainty")),
            
            Feature("muonScale", "muonScale", binning=(20, 0, 2),
                systematics=["CMS_scale_m_2022"],
                x_title=Label("Muon p_{T} scale")),

            ## Features for non-weight systematics ##
            # Type-I + TuneP
            #Feature("CorrMET_pt", "CorrMET_pt", binning=(50, 35, 4000),
            #    systematics=["CMS_scale_met_2022"],
            #    x_title=Label("p_{T}^{miss}"),
            #    units="GeV"),

            #Feature("CorrMET_phi", "CorrMET_phi", binning=(50, -math.pi, math.pi),
            #    systematics=["CMS_scale_met_2022"],
            #    x_title=Label("p_{T}^{miss} #phi"),
            #    units="rad"),

            # ONLY Type-I
            Feature("TypeICorrMET_pt", "TypeICorrMET_pt", binning=(50, 35, 4000),
                systematics=["CMS_scale_met_2022"],
                x_title=Label("p_{T}^{miss}"),
                units="GeV"),

            Feature("TypeICorrMET_phi", "TypeICorrMET_phi", binning=(50, -math.pi, math.pi),
                systematics=["CMS_scale_met_2022"],
                x_title=Label("p_{T}^{miss} #phi"),
                units="rad"),            

        ]

        #### QCD checks: MET no muon ####
        
        MET_noMuon = [

            Feature("METnoMu_pt", "METnoMu_pt", binning=(40, 0, 2000),
                x_title=Label("p_{T}^{miss} - #mu"),
                units="GeV"),

            Feature("METnoMu_phi", "METnoMu_phi", binning=(40, -math.pi, math.pi),
                x_title=Label("p_{T}^{miss} - #mu #phi "),
                units="rad"),

            Feature("dPhi_METnoMu", "dPhi_METnoMu", binning=(40, 0, math.pi),
                x_title=Label("#Delta#phi(p_{T}^{#mu}, p_{T}^{miss} - #mu)"),
                ),
            
            Feature("muon_eta", "Muon_eta.at(goodMuIdx)", binning=(40, -2.4, 2.4),
                x_title=Label("#mu #eta")),

            Feature("muon_phi", "Muon_phi.at(goodMuIdx)", binning=(40, -math.pi, math.pi),
                x_title=Label("#mu #phi"),
                units="rad"),

            Feature("muon_pt", "Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)", binning=(50, 50, 3000),
                x_title=Label("p_{T}^{#mu}"),
                units="GeV"),
            
        ]

        QCD_reduction = [
            
            Feature("mT_orig", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*TypeICorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - TypeICorrMET_phi)) )",
                binning=(86, 400, 9000),
                x_title=Label("m_{T}"),
                units="GeV"),
                        
            Feature("mT_reference", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*TypeICorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - TypeICorrMET_phi)) )",
                binning=(86, 400, 9000),
                selection="METnoMu_pt > 250 ? dPhi_METnoMu > 0.4 : 1",
                x_title=Label("m_{T}"),
                units="GeV"),
                                    
            Feature("mT_loose", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*TypeICorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - TypeICorrMET_phi)) )",
                binning=(86, 400, 9000),
                selection="METnoMu_pt > 500 ? dPhi_METnoMu > 0.4 : 1",
                x_title=Label("m_{T}"),
                units="GeV"),
                                    
            Feature("mT_tight", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*TypeICorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - TypeICorrMET_phi)) )",
                binning=(86, 400, 9000),
                selection="METnoMu_pt > 150 ? dPhi_METnoMu > 0.4 : 1",
                x_title=Label("m_{T}"),
                units="GeV"),
                                    
            Feature("mT_tightDphi", "sqrt( 2*Muon_tunepRelPt.at(goodMuIdx)*Muon_pt.at(goodMuIdx)*TypeICorrMET_pt*(1 - cos(Muon_phi.at(goodMuIdx) - TypeICorrMET_phi)) )",
                binning=(86, 400, 9000),
                selection="METnoMu_pt > 250 ? dPhi_METnoMu > 0.2 : 1",
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

        weights.preselection  = ["genWeight", "puWeight", "mu_idSF_weight", "mu_isoSF_weight", "mu_hltSF_weight", "mu_recoSF_weight", "btag_weight", "Wkfact", "PDFweight_total", "muonScale"]
        
        ### For PDF plots ###
        #weights.preselection  = ["genWeight", "puWeight", "PDFweight"]

        return weights

    def add_systematics(self):
        systematics = [
            Systematic("CMS_pileup", ""),
            Systematic("CMS_eff_m_reco_2022", ""),
            Systematic("CMS_eff_m_id_2022", ""),
            Systematic("CMS_eff_m_iso_2022", ""),
            Systematic("CMS_eff_m_trigger_2022", ""),
            Systematic("CMS_scale_m_2022", ""),
            Systematic("CMS_eff_b_2022", ""),
            Systematic("CMS_EXO24021_W_kfactor", ""),
            Systematic("pdf_qqbar", ""),

            # Type-I + TuneP
            #Systematic("CMS_scale_met_2022",""),
            # ONLY Type-I
            Systematic("CMS_scale_met_2022","", Up="_JESTotalUp", Down="_JESTotalDown"),
        ]

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


config = Config("base", year=2022, ecm=13.6, lumi_pb=34652)
