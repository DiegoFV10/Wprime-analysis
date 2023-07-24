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
        ]
        return ObjectCollection(categories)

    def add_processes(self):

        processes = [
            Process("Wprime", Label("W' #rightarrow #mu#nu"), color=ROOT.kAzure+1, isDY=True),
            Process("Wmunu", Label("W #rightarrow #mu#nu"), color=ROOT.kAzure+1, isDY=True),
        ]

        process_group_names = {}

        return ObjectCollection(processes), process_group_names


    def prefix_datasets(self, datasets, prefix):

        for dataset in datasets:
            dataset.prefix = prefix + '//'


    def add_datasets(self):
        datasets = [
            Dataset("Wprime2000",
                dataset="/WprimetoMuNu_M-2000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wprime2000_postEE",
                dataset="/WprimetoMuNu_M-2000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wprime"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),



            Dataset("Wmunu100to200",
                dataset="/WtoMuNu_M-100to200_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu100to200_postEE",
                dataset="/WtoMuNu_M-100to200_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu200to500",
                dataset="/WtoMuNu_M-200to500_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu200to500_postEE",
                dataset="/WtoMuNu_M-200to500_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu500to1000",
                dataset="/WtoMuNu_M-500to1000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu500to1000_postEE",
                dataset="/WtoMuNu_M-500to1000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu1000to2000",
                dataset="/WtoMuNu_M-1000to2000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu1000to2000_postEE",
                dataset="/WtoMuNu_M-1000to2000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu2000to3000",
                dataset="/WtoMuNu_M-2000to3000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu2000to3000_postEE",
                dataset="/WtoMuNu_M-2000to3000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu3000to4000",
                dataset="/WtoMuNu_M-3000to4000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu3000to4000_postEE",
                dataset="/WtoMuNu_M-3000to4000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu4000to5000",
                dataset="/WtoMuNu_M-4000to5000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu4000to5000_postEE",
                dataset="/WtoMuNu_M-4000to5000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu5000to6000",
                dataset="/WtoMuNu_M-5000to6000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                #prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu5000to6000_postEE",
                dataset="/WtoMuNu_M-5000to6000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu6000",
                dataset="/WtoMuNu_M-6000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1/"
                    "NANOAODSIM ",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),

            Dataset("Wmunu6000_postEE",
                dataset="/WtoMuNu_M-6000_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/"
                    "NANOAODSIM",
                process=self.processes.get("Wmunu"),
                prefix="eoscms-ns-ip563.cern.ch:1098//",
                xs=1.0,),





            #Dataset("Wprime2000_18",
            #    dataset="/WprimeToMuNu_M_2000_TuneCP5_13TeV_pythia8/"
            #        "RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/"
            #        "NANOAODSIM",
            #    process=self.processes.get("Wprime"),
            #    #prefix="eoscms-ns-ip563.cern.ch:1098//",
            #    xs=1.0,),

            #Dataset("Wmunu2000_18",
            #    dataset="/WToMuNu_M-2000_TuneCP5_13TeV-pythia8/"
            #        "RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/"
            #        "NANOAODSIM ",
            #    process=self.processes.get("Wmunu"),
            #    #prefix="eoscms-ns-ip563.cern.ch:1098//",
            #    xs=1.0,),
        ]
        return ObjectCollection(datasets)

    def add_features(self):
 
        features = []

        return ObjectCollection(features)

    def add_versions(self):
        versions = {}
        return versions

    def add_weights(self):
        weights = DotDict()
        weights.default = "1"

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


config = Config("base", year=2022, ecm=13.6, lumi_pb=34298)
