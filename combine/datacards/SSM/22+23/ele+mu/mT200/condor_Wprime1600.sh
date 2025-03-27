#!/bin/sh
ulimit -s unlimited
set -e
cd /afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/nanoaod_base_analysis/data/cmssw/CMSSW_13_0_13/src
export SCRAM_ARCH=el9_amd64_gcc11
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
cd /afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/datacards/SSM/22+23/ele+mu/mT200

if [ $1 -eq 0 ]; then
  combine datacard_elemu_Wprime1600.txt --tries 15 -t 100 -i 10000 --noDefaultPrior=0 --rMax 3.4 -M MarkovChainMC -s -1 -n .Test
fi

