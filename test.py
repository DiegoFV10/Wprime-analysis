
import ROOT



df = ROOT.RDataFrame("Events","root://eoscms-ns-ip563.cern.ch:1098///store/mc/Run3Summer22EENanoAODv11/WprimetoMuNu_M-2000_kR-1p0_LO_TuneCP5_13p6TeV_madgraph-pythia8/NANOAODSIM/126X_mcRun3_2022_realistic_postEE_v1-v1/40000/2d52e1b2-fe8e-459e-9590-f0944659ec80.root")

print(df.GetColumnNames())
