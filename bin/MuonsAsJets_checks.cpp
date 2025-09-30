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
#include "DataFormats/Math/interface/deltaPhi.h"

float deltaR(float eta1, float phi1, float eta2, float phi2){
  float deta = eta1 - eta2;
  float dphi = deltaPhi(phi1, phi2);

  return sqrt(deta*deta + dphi*dphi);
}

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
  Float_t mu_MVAID[size_max];       chain.SetBranchAddress("Muon_mvaMuID",&mu_MVAID);
  Float_t mu_promptMVA[size_max];   chain.SetBranchAddress("Muon_mvaTTH",&mu_promptMVA);
  Bool_t mu_isHP[size_max];         chain.SetBranchAddress("Muon_highPurity",&mu_isHP);
  Bool_t mu_isPF[size_max];         chain.SetBranchAddress("Muon_isPFcand",&mu_isPF);
  Float_t mu_Dxyerr[size_max];      chain.SetBranchAddress("Muon_dxyErr",&mu_Dxyerr);
  Float_t mu_Dz[size_max];          chain.SetBranchAddress("Muon_dz",&mu_Dz);
  Float_t mu_Dxy[size_max];         chain.SetBranchAddress("Muon_dxy",&mu_Dxy);
  Float_t mu_Iso04[size_max];       chain.SetBranchAddress("Muon_pfRelIso04_all",&mu_Iso04);
  UChar_t mu_nStations[size_max];   chain.SetBranchAddress("Muon_nStations",&mu_nStations);
  UChar_t mu_nTkLayers[size_max];   chain.SetBranchAddress("Muon_nTrackerLayers",&mu_nTkLayers);
  Float_t mu_segComp[size_max];     chain.SetBranchAddress("Muon_segmentComp",&mu_segComp);
  Int_t muIdx =                     chain.SetBranchAddress("goodMuIdx",&muIdx);

  Float_t MET_pt =                  chain.SetBranchAddress("MET_pt",&MET_pt);
  Float_t MET_phi =                 chain.SetBranchAddress("MET_phi",&MET_phi);
  Float_t PuppiMET_pt =             chain.SetBranchAddress("PuppiMET_pt", &PuppiMET_pt);
  Float_t PuppiMET_phi =            chain.SetBranchAddress("PuppiMET_phi", &PuppiMET_phi);
  Double_t TypeIMET_pt =            chain.SetBranchAddress("TypeICorrMET_pt",&TypeIMET_pt);
  Double_t TypeIMET_phi =           chain.SetBranchAddress("TypeICorrMET_phi",&TypeIMET_phi);
  Double_t CorrMET_pt =             chain.SetBranchAddress("CorrMET_pt",&CorrMET_pt);
  Double_t CorrMET_phi =            chain.SetBranchAddress("CorrMET_phi",&CorrMET_phi);

  Int_t nJet =                           chain.SetBranchAddress("nJet",&nJet);
  Float_t jet_pt[size_max];              chain.SetBranchAddress("Jet_pt",&jet_pt);
  Float_t jet_mass[size_max];            chain.SetBranchAddress("Jet_mass",&jet_mass);
  Float_t jet_phi[size_max];             chain.SetBranchAddress("Jet_phi",&jet_phi);
  Float_t jet_eta[size_max];             chain.SetBranchAddress("Jet_eta",&jet_eta);
  UChar_t jet_jetId[size_max];           chain.SetBranchAddress("Jet_jetId",&jet_jetId);
  Float_t jet_deepBTag[size_max];        chain.SetBranchAddress("Jet_btagDeepFlavB",&jet_deepBTag);
  UChar_t jet_nConstituents[size_max];   chain.SetBranchAddress("Jet_nConstituents",&jet_nConstituents);
  std::vector<float> *CorrJet_pt = 0;    chain.SetBranchAddress("CorrJet_pt",&CorrJet_pt);
  std::vector<float> *CorrJet_mass = 0;  chain.SetBranchAddress("CorrJet_mass",&CorrJet_mass);
  std::vector<int> *goodJets = 0;        chain.SetBranchAddress("goodJets",&goodJets);
  std::vector<int> *goodJets_corr = 0;   chain.SetBranchAddress("goodJets_corr",&goodJets_corr);

  Int_t nElectron =                 chain.SetBranchAddress("nElectron",&nElectron);
  Float_t el_pt[size_max];          chain.SetBranchAddress("Electron_pt",&el_pt);
  Float_t el_mass[size_max];        chain.SetBranchAddress("Electron_mass",&el_mass);
  Float_t el_phi[size_max];         chain.SetBranchAddress("Electron_phi",&el_phi);
  Float_t el_eta[size_max];         chain.SetBranchAddress("Electron_eta",&el_eta);
  Int_t el_ch[size_max];            chain.SetBranchAddress("Electron_charge",&el_ch);
  Bool_t el_HEEP[size_max];         chain.SetBranchAddress("Electron_cutBased_HEEP",&el_HEEP);
  UChar_t el_cutBased[size_max];    chain.SetBranchAddress("Electron_cutBased",&el_cutBased);
  
  Int_t nPhoton =                   chain.SetBranchAddress("nPhoton",&nPhoton);
  Float_t photon_pt[size_max];      chain.SetBranchAddress("Photon_pt",&photon_pt);


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
    //  std::cout << "[MuonsAsJets_checks.cpp] processed : " << i << " entries\r" << std::flush;
    if(goodJets_corr->size() > 0){
    
      if (CorrJet_pt->at(goodJets_corr->at(0)) > 600.0){
	counter++;

	float dR = deltaR(mu_eta[muIdx], mu_phi[muIdx], jet_eta[goodJets_corr->at(0)], jet_phi[goodJets_corr->at(0)]);
	float mT = sqrt( 2*mu_TunePRelPt[muIdx]*mu_pt[muIdx]*CorrMET_pt*(1.0 - cos(mu_phi[muIdx] - CorrMET_phi)) );
      
	cout << "Event " << counter << ":" << " ==> run:lumi:evt " << run << ":" << luminosityBlock << ":" << event << endl;

	cout << "DeltaR(mu,jet): " << dR << endl;
	cout << "Jets ==> nJets: " << goodJets_corr->size() << " | pT: " << CorrJet_pt->at(goodJets_corr->at(0)) << " | pT uncorr: " << jet_pt[goodJets->at(0)] << " | eta: " << jet_eta[goodJets_corr->at(0)] << " | phi: " << jet_phi[goodJets_corr->at(0)] << " | # constituents: " << (int)jet_nConstituents[goodJets->at(0)] << endl;
	if(goodJets_corr->size() > 1){
	  for(size_t j = 1; j < goodJets_corr->size(); j++)
	    cout << "  jet " << j << " pT: " << CorrJet_pt->at(goodJets_corr->at(j)) << " | eta: " << jet_eta[goodJets_corr->at(j)] << " | phi: " << jet_phi[goodJets_corr->at(j)] << endl;
	}	
	cout << "Muon ==> pT: " << mu_pt[muIdx] << " | TunePrel pT: " << mu_TunePRelPt[muIdx] << " | eta: " << mu_eta[muIdx] << " | phi: " << mu_phi[muIdx] << " | isPF: " << mu_isPF[muIdx] << endl;
	cout << "  ... more Muon ==> MVA ID: " << mu_MVAID[muIdx] << " | promptMVA: " << mu_promptMVA[muIdx] << " | tight ID: " << mu_isTight[muIdx] << " | SegmentComp: " << mu_segComp[muIdx] << " | HP: " << mu_isHP[muIdx] << " | nTkLayers: " << (int)mu_nTkLayers[muIdx] << endl;
	cout << "MET: " << CorrMET_pt << " MET_phi: " << CorrMET_phi << " | mT: " << mT << endl;
	if(nElectron > 0)
	  cout << "Electron ==> nEle: " << nElectron << " | leading pT: " << el_pt[0] << " | eta: " << el_eta[0] << " | phi: " << el_phi[0] << " | isHEEP: " << el_HEEP[0] << "\n" << endl;
	else
	  cout << "Electron ==> nEle: " << nElectron << "\n" << endl;
      	//if(nPhoton > 0)
	//  cout << "Photon ==> nPhot: " << nPhoton << " | leading pT: " << photon_pt[0] << "\n" << endl;
	//else
	//  cout << "Photon ==> nPhot: " << nElectron << "\n" << endl;
      
      
      } // Check problematic events
    }
  } // Loop over entries

  cout << "Found " << counter << " leading jets with pT > 600 GeV" << endl;
  
} // End of main 

void MuonsAsJets_checks(){
 
  plotChecks("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/bin/txt/Data2022_kinsel_fullCuts.txt");

}


