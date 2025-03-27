#include "TMath.h"
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <math.h>
#include <time.h>
#include "TFile.h"
#include "TChain.h"
#include "TTree.h"
#include "TBranch.h"
#include "TH1.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TLorentzVector.h"
#include "RooGlobalFunc.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include <vector>
#include <assert.h>
#include <TMVA/Reader.h>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <cassert>
#include <sstream>
#include <string>
#include "TFileCollection.h"
#include "THashList.h"
#include "TBenchmark.h"


void computePopulation(TString filePath, TString fileSuffix){

  std::vector<double> occupancies;
  std::vector<double> relOcc;
  double totalOcc = 0;
  
  std::vector<TFile*> files;
  for (int i = 0; i < 18; i++) {
    TString fileName = filePath + i + fileSuffix;
    files.push_back(TFile::Open(fileName, "READ"));
    if (!files.back()) {
      std::cerr << "Error opening file: " << fileName << std::endl;
      return;
    }
    TH1D* bkg = (TH1D*)files[i]->Get("histograms/background");
    double occupancy = bkg->GetEntries();
    occupancies.push_back(occupancy);
    totalOcc += occupancy;

  }
  cout << "Showing occupancies for " << filePath << endl;
  for (int i = 0; i < 18; i++) {
    relOcc.push_back(occupancies.at(i)/totalOcc);
    cout << "Region " << i << " --> Occupancy: " << relOcc.at(i) << endl;
  }
  cout << "Total Occupancy " << totalOcc << endl;
 

}// End of main 

void ScaleMapRegionPopulation(){

  computePopulation("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/ScaleMapRegions_preEE/root/mT_", "__pg_2022ReReco.root");
  computePopulation("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/ScaleMapRegions_postEE/root/mT_", "__pg_2022ReReco.root");
  computePopulation("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/ScaleMapRegions_preBPix-v2/root/mT_", "__pg_2023_full.root");
  computePopulation("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/ScaleMapRegions_postBPix/root/mT_", "__pg_2023_full.root");
  
}


