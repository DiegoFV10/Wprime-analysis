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
//#include "DataFormats/Math/interface/deltaPhi.h"


void plotChecks(string filename){

  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  string path(filename);
  TFileCollection fc("FileCollection", "FileCollection", path.c_str());

  TString treeName = "Events";
  TChain chain(treeName);
  chain.AddFileInfoList(fc.GetList());

  int nFiles = fc.GetNFiles();
  int nentries = chain.GetEntries();
  cout <<"This chain made of "<<nFiles<<" files, has "<<nentries<<" entries"<< endl;

  /// Read branches ///
  
  const int size_max = 30;
  const int size_max2 = 300;

  UInt_t run =                      chain.SetBranchAddress("run",&run);
  UInt_t luminosityBlock =          chain.SetBranchAddress("luminosityBlock",&luminosityBlock);
  ULong64_t event =                 chain.SetBranchAddress("event",&event);

  Int_t nMuon =                     chain.SetBranchAddress("nMuon",&nMuon);
  Float_t mu_pt[size_max];          chain.SetBranchAddress("Muon_pt",&mu_pt);
  Float_t mu_TunePRelPt[size_max];  chain.SetBranchAddress("Muon_tunepRelPt",&mu_TunePRelPt);
  Float_t mu_ptErr[size_max];       chain.SetBranchAddress("Muon_ptErr",&mu_ptErr);
  Float_t mu_phi[size_max];         chain.SetBranchAddress("Muon_phi",&mu_phi);
  Float_t mu_eta[size_max];         chain.SetBranchAddress("Muon_eta",&mu_eta);
  Float_t mu_tkRelIso[size_max];    chain.SetBranchAddress("Muon_tkRelIso",&mu_tkRelIso);
  Int_t mu_ch[size_max];            chain.SetBranchAddress("Muon_charge",&mu_ch);
  UChar_t mu_HighPtId[size_max];    chain.SetBranchAddress("Muon_highPtId",&mu_HighPtId);
  Bool_t mu_IsGlobal[size_max];     chain.SetBranchAddress("Muon_isGlobal",&mu_IsGlobal);
  Bool_t mu_IsTracker[size_max];    chain.SetBranchAddress("Muon_isTracker",&mu_IsTracker);
  Bool_t mu_isMedium[size_max];     chain.SetBranchAddress("Muon_mediumId",&mu_isMedium);
  Bool_t mu_isLoose[size_max];      chain.SetBranchAddress("Muon_looseId",&mu_isLoose);
  Bool_t mu_isTight[size_max];      chain.SetBranchAddress("Muon_tightId",&mu_isTight);
  Bool_t mu_isHP[size_max];         chain.SetBranchAddress("Muon_highPurity",&mu_isHP);
  Bool_t mu_isPF[size_max];         chain.SetBranchAddress("Muon_isPFcand",&mu_isPF);
  Float_t mu_Dxyerr[size_max];      chain.SetBranchAddress("Muon_dxyErr",&mu_Dxyerr);
  Float_t mu_Dz[size_max];          chain.SetBranchAddress("Muon_dz",&mu_Dz);
  Float_t mu_Dxy[size_max];         chain.SetBranchAddress("Muon_dxy",&mu_Dxy);
  Float_t mu_Iso04[size_max];       chain.SetBranchAddress("Muon_pfRelIso04_all",&mu_Iso04);
  UChar_t mu_nStations[size_max];   chain.SetBranchAddress("Muon_nStations",&mu_nStations);
  Int_t muIdx =                     chain.SetBranchAddress("goodMuIdx",&muIdx);

  Float_t MET_pt =                  chain.SetBranchAddress("MET_pt",&MET_pt);
  Float_t MET_phi =                 chain.SetBranchAddress("MET_phi",&MET_phi);
  Float_t PuppiMET_pt =             chain.SetBranchAddress("PuppiMET_pt", &PuppiMET_pt);
  Float_t PuppiMET_phi =            chain.SetBranchAddress("PuppiMET_phi", &PuppiMET_phi);
  Double_t TypeIMET_pt =            chain.SetBranchAddress("TypeICorrMET_pt",&TypeIMET_pt);
  Double_t TypeIMET_phi =           chain.SetBranchAddress("TypeICorrMET_phi",&TypeIMET_phi);
  Double_t CorrMET_pt =             chain.SetBranchAddress("CorrMET_pt",&CorrMET_pt);
  Double_t CorrMET_phi =            chain.SetBranchAddress("CorrMET_phi",&CorrMET_phi);

  Double_t METnoMu_pt =             chain.SetBranchAddress("METnoMu_pt",&METnoMu_pt);
  Double_t METnoMu_phi =            chain.SetBranchAddress("METnoMu_phi",&METnoMu_phi);


  /// Define histograms to plot ///
  TH1F* muonPt    = new TH1F("muonPt", "", 20, 200, 2000);
  TH1F* muonTuneP = new TH1F("muonTuneP", "", 20, 0, 5);
  TH1F* muonEta   = new TH1F("muonEta", "", 20, -2.5, 2.5);
  TH1F* muonPhi   = new TH1F("muonPhi", "", 20, -3.2, 3.2);
  TH1F* muonPtErr = new TH1F("muonPtErr", "", 20, 0, 600);
  TH1F* muonIso   = new TH1F("muonIso", "", 20, 0, 0.1);
  TH1I* numberMuon = new TH1I("numberMuon", "", 12, 0, 12);
  TH1I* muonCharge = new TH1I("muonCharge", "", 3, -1, 2);
  TH1I* muonHP    = new TH1I("muonHP", "", 2, 0, 2);
  TH1I* muonIndex = new TH1I("muonIndex", "", 4, 0, 4);
  TH1F* MET       = new TH1F("MET", "", 20, 200, 2000);
  TH1F* METphi    = new TH1F("METphi", "", 20, -3.2, 3.2);
  TH1F* jetEta    = new TH1F("jetEta", "", 20, -2.5, 2.5);
  TH1F* jetPhi    = new TH1F("jetPhi", "", 20, -3.2, 3.2);
  TH1F* elePt     = new TH1F("elePt", "", 20, 0, 2000);
  TH1F* eleEta    = new TH1F("eleEta", "", 20, -2.5, 2.5);
  TH1F* elePhi    = new TH1F("elePhi", "", 20, -3.2, 3.2);
  TH1I* eleHEEP   = new TH1I("eleHEEP", "", 2, 0, 2);

  TH2F* muonEtaPhi = new TH2F("muonEtaPhi", "", 20, -2.5, 2.5, 20, -3.2, 3.2);
  TH2F* jetEtaPhi = new TH2F("jetEtaPhi", "", 20, -2.5, 2.5, 20, -3.2, 3.2);
  TH2F* muonEtaJetEta = new TH2F("muonEtaJetEta", "", 20, -2.5, 2.5, 20, -2.5, 2.5);
  TH2F* muonEtaEleEta = new TH2F("muonEtaEleEta", "", 20, -2.5, 2.5, 20, -2.5, 2.5);
  
  int counter = 0;
  
  for(int i = 0; i < nentries; i++){

    chain.GetEntry(i);

    //if(i % 100 == 0) 
    //  std::cout << "[Wboosted_DataChecks.cpp] processed : " << i << " entries\r" << std::flush;

    if (mu_TunePRelPt[muIdx]*mu_pt[muIdx] > 2000){
      counter++;

      cout << "Event " << counter << ":" << endl;
      cout << "  run:lumi:event ==> "<< run << ":" << luminosityBlock << ":" << event << endl;

      cout << "  Muon            --> TuneP pT: " << mu_TunePRelPt[muIdx]*mu_pt[muIdx] << " pT: " << mu_pt[muIdx] << "  phi: " << mu_phi[muIdx] << " eta: " << mu_eta[muIdx] << endl;
      cout << "  Muon            --> isHP: " << mu_isHP[muIdx] << " isPF: " << mu_isPF[muIdx] << endl;
      cout << "  MET (orig)      --> pT: " << MET_pt << " phi: " << MET_phi << endl;
      cout << "  PuppiMET (orig) --> pT: " << PuppiMET_pt << " phi: " << PuppiMET_phi << endl;
      cout << "  PuppiMET (corr) --> pT: " << CorrMET_pt << " phi: " << CorrMET_phi << endl;
      cout << "  MET - muon      --> pT: " << METnoMu_pt << " phi: " << METnoMu_phi << endl;
      
    } // Check problematic events
    
  } // Loop over entries

  cout << "Found " << counter << " events above mT threshold" << endl;

  /*
  TCanvas* c23 = new TCanvas();
  c23->cd();
  muonEtaJetEta->Draw("COLZ");
  TCanvas* c24 = new TCanvas();
  c24->cd();
  muonEtaEleEta->Draw("COLZ");
  */
  
} // End of main 

void Wboosted_DataChecks(){
 
  plotChecks("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/bin/txt/Data2022_WboostedCR.txt");

}


