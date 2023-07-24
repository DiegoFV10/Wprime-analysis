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

void chargeMissID(string filename, string output, int f){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  /* When input is TChain (for pre + postEE periods) */
  
  string path(filename);
  TFileCollection fc("FileCollection", "FileCollection", path.c_str());

  TString treeName = "Events";
  TChain chain(treeName);
  chain.AddFileInfoList(fc.GetList());

  int nFiles = fc.GetNFiles();
  int nentries = chain.GetEntries();
  cout <<"This chain made of "<<nFiles<<" files, has "<<nentries<<" entries"<< endl;
  
  /*************************/

  /* For a Single File input */
  /*
  TFile *f1 =  TFile::Open((filename).c_str());
  TTree *tree = new TTree;
    tree = (TTree*) f1->Get("Events");
  int nentries = tree->GetEntries();
  */

  /* Variable allocation */
  int size_max = 30;
  int size_max2 = 300;
  
  UInt_t nGenP = chain.SetBranchAddress("nGenPart", &nGenP);
  Float_t genP_pt[size_max2];          chain.SetBranchAddress("GenPart_pt", &genP_pt);
  Float_t genP_phi[size_max2];         chain.SetBranchAddress("GenPart_phi", &genP_phi);
  Float_t genP_eta[size_max2];         chain.SetBranchAddress("GenPart_eta", &genP_eta);
  Float_t genP_mass[size_max2];        chain.SetBranchAddress("GenPart_mass", &genP_mass);
  Int_t genP_flavor[size_max2];        chain.SetBranchAddress("GenPart_pdgId", &genP_flavor);
  Int_t genP_momIdx[size_max2];        chain.SetBranchAddress("GenPart_genPartIdxMother", &genP_momIdx);
  std::vector<int> *genP_momIdxPrompt = 0;  chain.SetBranchAddress("GenPart_genPartIdxMotherPrompt", &genP_momIdxPrompt);

  UInt_t nGenJet = chain.SetBranchAddress("nGenJet", &nGenJet);
  Float_t GenJet_pt[size_max2];        chain.SetBranchAddress("GenJet_pt", &GenJet_pt);

  Float_t LHE_HT = chain.SetBranchAddress("LHE_HT", &LHE_HT);
  Float_t LHE_HTin = chain.SetBranchAddress("LHE_HTIncoming", &LHE_HTin);

  UInt_t nLHEPart = chain.SetBranchAddress("nLHEPart", &nLHEPart);
  Float_t LHEPart_M[size_max2];        chain.SetBranchAddress("LHEPart_mass", &LHEPart_M);
  Int_t LHEPart_Id[size_max2];         chain.SetBranchAddress("LHEPart_pdgId", &LHEPart_Id);
  Float_t LHEPart_pt[size_max2];       chain.SetBranchAddress("LHEPart_pt", &LHEPart_pt);
  Float_t LHEPart_eta[size_max2];      chain.SetBranchAddress("LHEPart_eta", &LHEPart_eta);
  Float_t LHEPart_phi[size_max2];      chain.SetBranchAddress("LHEPart_phi", &LHEPart_phi);

  Float_t met_pt = chain.SetBranchAddress("MET_pt",&met_pt);
  Float_t met_phi = chain.SetBranchAddress("MET_phi",&met_phi);
  Float_t PuppiMET_pt = chain.SetBranchAddress("PuppiMET_pt", &PuppiMET_pt);
  Float_t PuppiMET_phi = chain.SetBranchAddress("PuppiMET_phi", &PuppiMET_phi);

  UInt_t nMuon = chain.SetBranchAddress("nMuon",&nMuon);
  Float_t mu_pt[size_max];          chain.SetBranchAddress("Muon_pt",&mu_pt);
  Float_t mu_mass[size_max];        chain.SetBranchAddress("Muon_mass",&mu_mass);
  Float_t mu_phi[size_max];         chain.SetBranchAddress("Muon_phi",&mu_phi);
  Float_t mu_eta[size_max];         chain.SetBranchAddress("Muon_eta",&mu_eta);
  Int_t mu_ch[size_max];            chain.SetBranchAddress("Muon_charge",&mu_ch);
  Bool_t mu_isMedium[size_max];     chain.SetBranchAddress("Muon_mediumId",&mu_isMedium);
  Bool_t mu_isLoose[size_max];      chain.SetBranchAddress("Muon_looseId",&mu_isLoose);
  Bool_t mu_isTight[size_max];      chain.SetBranchAddress("Muon_tightId",&mu_isTight);
  Float_t mu_Dxyerr[size_max];      chain.SetBranchAddress("Muon_dxyErr",&mu_Dxyerr);
  Float_t mu_Dz[size_max];          chain.SetBranchAddress("Muon_dz",&mu_Dz);
  Float_t mu_Dxy[size_max];         chain.SetBranchAddress("Muon_dxy",&mu_Dxy);
  Float_t mu_ptErr[size_max];       chain.SetBranchAddress("Muon_ptErr",&mu_ptErr);
  Float_t mu_MiniIso[size_max];     chain.SetBranchAddress("Muon_miniPFRelIso_all",&mu_MiniIso);
  Float_t mu_Iso04[size_max];       chain.SetBranchAddress("Muon_pfRelIso04_all",&mu_Iso04);
  Float_t mu_tkRelIso[size_max];    chain.SetBranchAddress("Muon_tkRelIso",&mu_tkRelIso);
  UChar_t mu_isHigh[size_max];      chain.SetBranchAddress("Muon_highPtId",&mu_isHigh);
  Bool_t mu_IsGlobal[size_max];     chain.SetBranchAddress("Muon_isGlobal",&mu_IsGlobal);
  Bool_t mu_IsTracker[size_max];    chain.SetBranchAddress("Muon_isTracker",&mu_IsTracker);
  Int_t mu_nStations[size_max];     chain.SetBranchAddress("Muon_nStations",&mu_nStations);
  Int_t mu_nTkLayers[size_max];     chain.SetBranchAddress("Muon_nTrackerLayers",&mu_nTkLayers);
  UChar_t mu_genFlav[size_max];     chain.SetBranchAddress("Muon_genPartFlav",&mu_genFlav);
  Int_t mu_genIdx[size_max];        chain.SetBranchAddress("Muon_genPartIdx",&mu_genIdx);
  Float_t mu_TunePRelPt[size_max];  chain.SetBranchAddress("Muon_tunepRelPt",&mu_TunePRelPt);

  UInt_t nJet = chain.SetBranchAddress("nJet",&nJet);
  Float_t jet_pt[size_max];        chain.SetBranchAddress("Jet_pt",&jet_pt);
  Float_t jet_mass[size_max];      chain.SetBranchAddress("Jet_mass",&jet_mass);
  Float_t jet_phi[size_max];       chain.SetBranchAddress("Jet_phi",&jet_phi);
  Float_t jet_eta[size_max];       chain.SetBranchAddress("Jet_eta",&jet_eta);
  Int_t jet_hadronFlav[size_max];  chain.SetBranchAddress("Jet_hadronFlavour",&jet_hadronFlav);
  Float_t jet_deepBTag[size_max];  chain.SetBranchAddress("Jet_btagDeepFlavB",&jet_deepBTag); 
  Int_t Jet_partonFlav[size_max];  chain.SetBranchAddress("Jet_partonFlavour",&Jet_partonFlav);
  Int_t Jet_genJetIdx[size_max];   chain.SetBranchAddress("Jet_genJetIdx",&Jet_genJetIdx);

  UInt_t nElectron = chain.SetBranchAddress("nElectron",&nElectron);
  Float_t el_pt[size_max];                         chain.SetBranchAddress("Electron_pt",&el_pt);
  Float_t el_mass[size_max];                       chain.SetBranchAddress("Electron_mass",&el_mass);
  Float_t el_phi[size_max];                        chain.SetBranchAddress("Electron_phi",&el_phi);
  Float_t el_eta[size_max];                        chain.SetBranchAddress("Electron_eta",&el_eta);
  Int_t el_ch[size_max];                           chain.SetBranchAddress("Electron_charge",&el_ch);
  Int_t el_cutBased[size_max];                     chain.SetBranchAddress("Electron_cutBased",&el_cutBased);
  Float_t Electron_pfRelIso03_all[size_max];       chain.SetBranchAddress("Electron_pfRelIso03_all",&Electron_pfRelIso03_all);
  Float_t Electron_miniPFRelIso_all[size_max];     chain.SetBranchAddress("Electron_miniPFRelIso_all",&Electron_miniPFRelIso_all);
  Float_t el_Dxy[size_max];                        chain.SetBranchAddress("Electron_dxy",&el_Dxy);

  Bool_t HLT_Mu50 = chain.SetBranchAddress("HLT_Mu50", &HLT_Mu50);


  /* Histogram Definition */
  float bin_edges[10] = {50,100,175,300,500,800,1200,1600,2000,3000};

  TH1D* muPlusMatch = new TH1D("MuonPlus_matched", "", 9, bin_edges);              // + Muon matched (12,0,1800)
  TH1D* muPlusMatch_miss = new TH1D("MuonPlus_matched_misID", "", 9, bin_edges);   // + Muon matched but gen charge != reco charge
  TH1D* muMinusMatch = new TH1D("MuonMinus_matched", "", 9, bin_edges);            // - Muon matched
  TH1D* muMinusMatch_miss = new TH1D("MuonMinus_matched_misID", "", 9, bin_edges); // - Muon matched but gen charge != reco charge

  TH1D* muPmatch_eta = new TH1D("MuonPlus_matched_eta", "", 20, -2.4, 2.4);            // Eta
  TH1D* muPmatch_miss_eta = new TH1D("MuonPlus_matched_misID_eta", "", 20, -2.4, 2.4);  
  TH1D* muNmatch_eta = new TH1D("MuonMinus_matched_eta", "", 20, -2.4, 2.4);             
  TH1D* muNmatch_miss_eta = new TH1D("MuonMinus_matched_misID_eta", "", 20, -2.4, 2.4);
  
  TH1D* muPmatch_barrel = new TH1D("MuonPlus_matched_barrel", "", 9, bin_edges);            // pT in barrel
  TH1D* muPmatch_miss_barrel = new TH1D("MuonPlus_matched_misID_barrel", "", 9, bin_edges);
  TH1D* muNmatch_barrel = new TH1D("MuonMinus_matched_barrel", "", 9, bin_edges);             
  TH1D* muNmatch_miss_barrel = new TH1D("MuonMinus_matched_misID_barrel", "", 9, bin_edges); 

  TH1D* muPmatch_endcap = new TH1D("MuonPlus_matched_endcap", "", 9, bin_edges);            // pT in endcap
  TH1D* muPmatch_miss_endcap = new TH1D("MuonPlus_matched_misID_endcap", "", 9, bin_edges);
  TH1D* muNmatch_endcap = new TH1D("MuonMinus_matched_endcap", "", 9, bin_edges);             
  TH1D* muNmatch_miss_endcap = new TH1D("MuonMinus_matched_misID_endcap", "", 9, bin_edges);

  float iso_edges[10] = {0,0.0005,0.002,0.005,0.008,0.015,0.05,0.1,0.4,1.0};
  TH1D* muPmatch_iso = new TH1D("MuonPlus_matched_iso", "", 9, iso_edges);            // Rel Tk Iso
  TH1D* muPmatch_miss_iso = new TH1D("MuonPlus_matched_misID_iso", "", 9, iso_edges);  
  TH1D* muNmatch_iso = new TH1D("MuonMinus_matched_iso", "", 9, iso_edges);             
  TH1D* muNmatch_miss_iso = new TH1D("MuonMinus_matched_misID_iso", "", 9, iso_edges);

  TH1I* muPmatch_nStat = new TH1I("MuonPlus_matched_nStations", "", 5, 0, 5);            // nStations
  TH1I* muPmatch_miss_nStat = new TH1I("MuonPlus_matched_misID_nStations", "", 5, 0, 5);  
  TH1I* muNmatch_nStat = new TH1I("MuonMinus_matched_nStations", "", 5, 0, 5);             
  TH1I* muNmatch_miss_nStat = new TH1I("MuonMinus_matched_misID_nStations", "", 5, 0, 5);



  if(f!=0)
    nentries=f; 

  for(int i = 0; i < nentries; i++){

    chain.GetEntry(i);

    if(i % 100 == 0) 
      std::cout << "[Lep_tagger.cpp] processed : " << i << " entries\r" << std::flush;

    if(nMuon == 0) continue;

    /* // Method A: Use gen info & avoid double reco match
    int counter_recoGen = 0;
    std::vector<int> gen_indices = {}; // QUITAR!!
    for(int iMu = 0; iMu < nMuon; iMu++){
      if(fabs(mu_eta[iMu]) < 2.4){
	int genMatch_idx = 0;

	for(int iGen = 0; iGen < nGenP; iGen++){
	  if(fabs(genP_flavor[iGen]) == 13 && fabs(genP_eta[iGen]) < 2.4){
	    if(deltaR(mu_eta[iMu], mu_phi[iMu], genP_eta[iGen], genP_phi[iGen]) < 0.1 && genP_momIdxPrompt->at(iGen) != -1){ //&& fabs(mu_pt[iMu] - genP_pt[iGen])/genP_pt[iGen] < 0.7){
	      if(fabs(genP_flavor[genP_momIdxPrompt->at(iGen)]) == 24){
		genMatch_idx = iGen;
	      }
	    } // Matching
	  }
	} // Loop over gen particles
        if(genMatch_idx != 0) {counter_recoGen++;
	  gen_indices.push_back(iMu);
	}
      }
    } // Loop over reco muons

    //if(counter_recoGen > 1){
    //  cout <<"Event "<<i<<" with "<<counter_recoGen<<" reco-gen matches." << endl;
    //  for(int k = 0; k < counter_recoGen; k++){
    //	if(mu_isLoose[gen_indices.at(k)]){
    //	cout <<"\tReco Muon #"<<k<<" ==> eta: "<<mu_eta[gen_indices.at(k)]<<" phi: "<<mu_phi[gen_indices.at(k)]<<" pt: "<<mu_pt[gen_indices.at(k)]<<" charge: "<<mu_ch[gen_indices.at(k)]<<" gen match: "<<mu_genIdx[gen_indices.at(k)]<<" # match stats: "<<mu_nStations[gen_indices.at(k)]<<" # of tk layers: "<<mu_nTkLayers[gen_indices.at(k)]<<" isLoose: "<<mu_isLoose[gen_indices.at(k)]<<" isHigh: "<<(int)mu_isHigh[gen_indices.at(k)]<<" dz: "<<mu_Dz[gen_indices.at(k)]<< endl;
    //	}
	  //<<" pt gen: "<<genP_pt[mu_genIdx[gen_indices.at(k)]]<<" eta gen: "<<genP_eta[mu_genIdx[gen_indices.at(k)]]<<" phi gen: "<<genP_phi[mu_genIdx[gen_indices.at(k)]]<<" gen charge: "<<genP_flavor[mu_genIdx[gen_indices.at(k)]]/(-13.0)<< endl;
    //  }
    //} // Checks
    
     //QUITAR!!
    //if(counter_recoGen > 1) continue;


    for(int iMu = 0; iMu < nMuon; iMu++){
      //counter_recoGen = 0;
      //std::vector<int> gen_indices = {};
      if(fabs(mu_eta[iMu]) < 2.4 && (int)mu_isHigh[iMu] != 0){ // New muon requirements
	int genMatch_idx = 0;
	bool muPmatch = false;
	bool muNmatch = false;
	bool muPmiss = false;
	bool muNmiss = false;

	for(int iGen = 0; iGen < nGenP; iGen++){
	  if(fabs(genP_flavor[iGen]) == 13 && fabs(genP_eta[iGen]) < 2.4){
	    if(deltaR(mu_eta[iMu], mu_phi[iMu], genP_eta[iGen], genP_phi[iGen]) < 0.1 && genP_momIdxPrompt->at(iGen) != -1){ //&& fabs(mu_pt[iMu] - genP_pt[iGen])/genP_pt[iGen] < 0.7){
	      if(fabs(genP_flavor[genP_momIdxPrompt->at(iGen)]) == 24){
		//counter_recoGen++;
		//gen_indices.push_back(iGen);

		if(genP_flavor[iGen] == -13){
		  genMatch_idx = iGen;
		  muPmatch = true;
		  if(mu_ch[iMu]*genP_flavor[iGen] > 0) muPmiss = true;
		} else {
		  genMatch_idx = iGen;
		  muNmatch = true;
		  if(mu_ch[iMu]*genP_flavor[iGen] > 0) muNmiss = true;
		}
	      }
	    } // Matching
	  }
	} // Loop over gen particles
	if(muPmatch){
	  muPlusMatch->Fill(genP_pt[genMatch_idx]);
	  muPmatch_eta->Fill(genP_eta[genMatch_idx]);
	  if(fabs(genP_eta[genMatch_idx]) < 1.2) muPmatch_barrel->Fill(genP_pt[genMatch_idx]);
	  else muPmatch_endcap->Fill(genP_pt[genMatch_idx]);
	}
	if(muPmiss){
	  muPlusMatch_miss->Fill(genP_pt[genMatch_idx]);
	  muPmatch_miss_eta->Fill(genP_eta[genMatch_idx]);
	  if(fabs(genP_eta[genMatch_idx]) < 1.2) muPmatch_miss_barrel->Fill(genP_pt[genMatch_idx]);
	  else muPmatch_miss_endcap->Fill(genP_pt[genMatch_idx]);
	  /// Debugging ///
	  if(genP_pt[genMatch_idx] < 100){
	    cout <<"Event "<<i<<" with "<<counter_recoGen<<" reco-gen matches." << endl;
	    cout <<"\tGenPart pt: "<<genP_pt[genMatch_idx]<<" eta: "<<genP_eta[genMatch_idx]<<" phi: "<<genP_phi[genMatch_idx]<<" flavor: "<<genP_flavor[genMatch_idx]<<" mom: "<<genP_flavor[genP_momIdx[genMatch_idx]]<<" final mom: "<<genP_flavor[genP_momIdxPrompt->at(genMatch_idx)]<<" genP idx: "<<genMatch_idx << endl;
	    cout <<"\tReco Muon pt: "<<mu_pt[iMu]<<" eta: "<<mu_eta[iMu]<<" phi: "<<mu_phi[iMu]<<" charge: "<<mu_ch[iMu]<<" gen match: "<<mu_genIdx[iMu]<<" # match stats: "<<mu_nStations[iMu]<<" # of tk layers: "<<mu_nTkLayers[iMu]<<" isLoose: "<<mu_isLoose[iMu]<<" isHigh: "<<(int)mu_isHigh[iMu]<<" dz: "<<mu_Dz[iMu]<< endl;
	    if(mu_genIdx[iMu]!=-1) cout <<"\tMatched GenPart pt: "<<genP_pt[mu_genIdx[iMu]]<<" eta: "<<genP_eta[mu_genIdx[iMu]]<<" phi: "<<genP_phi[mu_genIdx[iMu]]<<" flavor: "<<genP_flavor[mu_genIdx[iMu]]<<" mom: "<<genP_flavor[genP_momIdx[mu_genIdx[iMu]]]<<" final mom: "<<genP_flavor[genP_momIdxPrompt->at(mu_genIdx[iMu])] << endl;
	  }
	  /////////////////
	}
	if(muNmatch){
	  muMinusMatch->Fill(genP_pt[genMatch_idx]);
	  muNmatch_eta->Fill(genP_eta[genMatch_idx]);
	  if(fabs(genP_eta[genMatch_idx]) < 1.2) muNmatch_barrel->Fill(genP_pt[genMatch_idx]);
	  else muNmatch_endcap->Fill(genP_pt[genMatch_idx]);
	}
	if(muNmiss){
	  muMinusMatch_miss->Fill(genP_pt[genMatch_idx]);
	  muNmatch_miss_eta->Fill(genP_eta[genMatch_idx]);
	  if(fabs(genP_eta[genMatch_idx]) < 1.2) muNmatch_miss_barrel->Fill(genP_pt[genMatch_idx]);
	  else muNmatch_miss_endcap->Fill(genP_pt[genMatch_idx]);
	  /// Debugging ///
	  if(genP_pt[genMatch_idx] < 100){
	    cout <<"Event "<<i<<" with "<<counter_recoGen<<" reco-gen matches." << endl;
	    cout <<"\tGenPart pt: "<<genP_pt[genMatch_idx]<<" eta: "<<genP_eta[genMatch_idx]<<" phi: "<<genP_phi[genMatch_idx]<<" flavor: "<<genP_flavor[genMatch_idx]<<" mom: "<<genP_flavor[genP_momIdx[genMatch_idx]]<<" final mom: "<<genP_flavor[genP_momIdxPrompt->at(genMatch_idx)]<<" genP idx: "<<genMatch_idx << endl;
	    cout <<"\tReco Muon pt: "<<mu_pt[iMu]<<" eta: "<<mu_eta[iMu]<<" phi: "<<mu_phi[iMu]<<" charge: "<<mu_ch[iMu]<<" gen match: "<<mu_genIdx[iMu]<<" # match stats: "<<mu_nStations[iMu]<<" # of tk layers: "<<mu_nTkLayers[iMu]<<" isLoose: "<<mu_isLoose[iMu]<<" isHigh: "<<(int)mu_isHigh[iMu]<<" dz: "<<mu_Dz[iMu]<< endl;
	    if(mu_genIdx[iMu]!=-1) cout <<"\tMatched GenPart pt: "<<genP_pt[mu_genIdx[iMu]]<<" eta: "<<genP_eta[mu_genIdx[iMu]]<<" phi: "<<genP_phi[mu_genIdx[iMu]]<<" flavor: "<<genP_flavor[mu_genIdx[iMu]]<<" mom: "<<genP_flavor[genP_momIdx[mu_genIdx[iMu]]]<<" final mom: "<<genP_flavor[genP_momIdxPrompt->at(mu_genIdx[iMu])] << endl;
	  }
	  /////////////////
	}
      }
      /// Debugging ///
      //if(counter_recoGen > 1){
	//cout <<"Event "<<i<<" with "<<counter_recoGen<<" reco-gen matches." << endl;
	//cout <<"\tReco Muon ==> eta: "<<mu_eta[iMu]<<" phi: "<<mu_phi[iMu]<<" pt: "<<mu_pt[iMu] << endl;
	//for(int k = 0; k < counter_recoGen; k++){
	  //cout <<"\tGen Muon #"<<k<<" ==> eta: "<<genP_eta[gen_indices.at(k)]<<" phi: "<<genP_phi[gen_indices.at(k)]<<" pt: "<<genP_pt[gen_indices.at(k)] <<" mother: "<<genP_flavor[genP_momIdx[gen_indices.at(k)]]<<" genp idx: "<<gen_indices.at(k)<< endl;
	//}
	//cout <<"\t  Matched index:"<<genMatch_idx<<endl;
      //} // Checks
      /////////////////
    } // Loop over reco Muons
    */// QUITAR!!
     


    /* // Method B: Use reco-gen matching already in NanoAOD
    //int counter_recoGen = 0;
    //std::vector<int> gen_indices = {};

    for(int iMu = 0; iMu < nMuon; iMu++){
      if(fabs(mu_eta[iMu]) < 2.4){
	bool muPmatch = false;
	bool muNmatch = false;
	bool muPmiss = false;
	bool muNmiss = false;

	if(mu_genIdx[iMu] != -1 && genP_momIdxPrompt->at(mu_genIdx[iMu]) != -1){
	  if(fabs(genP_flavor[genP_momIdxPrompt->at(mu_genIdx[iMu])]) == 24){
	    //counter_recoGen++;
	    //gen_indices.push_back(iMu);
	    if(genP_flavor[mu_genIdx[iMu]] == -13){
	      muPmatch = true;
	      if(mu_ch[iMu]*genP_flavor[mu_genIdx[iMu]] > 0) muPmiss = true;
	    } else {
	      muNmatch = true;
	      if(mu_ch[iMu]*genP_flavor[mu_genIdx[iMu]] > 0) muNmiss = true;
	    }

	  }
	} // Matching
	if(muPmatch) muPlusMatch->Fill(genP_pt[mu_genIdx[iMu]]);
	if(muPmiss)  muPlusMatch_miss->Fill(genP_pt[mu_genIdx[iMu]]);
	if(muNmatch) muMinusMatch->Fill(genP_pt[mu_genIdx[iMu]]);
	if(muNmiss)  muMinusMatch_miss->Fill(genP_pt[mu_genIdx[iMu]]);
      }
    } // Loop over reco Muons
    /// Debugging ///
    //if(counter_recoGen > 1){
      //cout <<"Event "<<i<<" with "<<counter_recoGen<<" reco-gen matches." << endl;
      //for(int k = 0; k < counter_recoGen; k++){
	//cout <<"\tReco Muon #"<<k<<" ==> eta: "<<mu_eta[gen_indices.at(k)]<<" phi: "<<mu_phi[gen_indices.at(k)]<<" pt: "<<mu_pt[gen_indices.at(k)]<<" charge: "<<mu_ch[gen_indices.at(k)]<<" gen match: "<<mu_genIdx[gen_indices.at(k)]<<" pt gen: "<<genP_pt[mu_genIdx[gen_indices.at(k)]]<<" eta gen: "<<genP_eta[mu_genIdx[gen_indices.at(k)]]<<" phi gen: "<<genP_phi[mu_genIdx[gen_indices.at(k)]]<<" gen charge: "<<genP_flavor[mu_genIdx[gen_indices.at(k)]]/(-13.0)<< endl;
      //}
    //}
    /////////////////
    */
    

    // Method C: Match reco-gen using minimum deltaR criterium
    std::vector<int> muIndices = {};
    std::vector<int> genIndices = {};
    for(int iMu = 0; iMu < nMuon; iMu++){
      if(fabs(mu_eta[iMu]) < 2.4 && (int)mu_isHigh[iMu] != 0){
	double mindR = 999.0;
	int minMuIdx = -1;
	int minGenIdx = -1;

	for(int iGen = 0; iGen < nGenP; iGen++){
	  if(fabs(genP_flavor[iGen]) == 13 && deltaR(mu_eta[iMu], mu_phi[iMu], genP_eta[iGen], genP_phi[iGen]) < 0.1){

	    if(deltaR(mu_eta[iMu], mu_phi[iMu], genP_eta[iGen], genP_phi[iGen]) <= mindR){
	      mindR = deltaR(mu_eta[iMu], mu_phi[iMu], genP_eta[iGen], genP_phi[iGen]);
	      minMuIdx = iMu;
	      minGenIdx = iGen;
	    }

	  } // Require gen Muon + deltaR < 0.1
	} // Loop over gen particles
	if(minMuIdx != -1){
	  muIndices.push_back(minMuIdx);
	  genIndices.push_back(minGenIdx);
	}

      } // Muon acceptance + ID requirements
    } // Loop over reco Muons

    for(size_t k = 0; k < muIndices.size(); k++){
      if(genP_momIdxPrompt->at(genIndices.at(k)) != -1){
	if(fabs(genP_flavor[genP_momIdxPrompt->at(genIndices.at(k))]) == 24){

	  if(genP_flavor[genIndices.at(k)] == -13){
	    muPlusMatch->Fill(genP_pt[genIndices.at(k)]);
	    muPmatch_eta->Fill(genP_eta[genIndices.at(k)]);
	    muPmatch_iso->Fill(mu_tkRelIso[muIndices.at(k)]);
	    if(fabs(genP_eta[genIndices.at(k)]) < 1.2) muPmatch_barrel->Fill(genP_pt[genIndices.at(k)]);
	    else muPmatch_endcap->Fill(genP_pt[genIndices.at(k)]);
	    if(genP_pt[genIndices.at(k)] >= 2000 && genP_pt[genIndices.at(k)] <= 3000) muPmatch_nStat->Fill(mu_nStations[muIndices.at(k)]);

	    if(mu_ch[muIndices.at(k)]*genP_flavor[genIndices.at(k)] > 0){
	      muPlusMatch_miss->Fill(genP_pt[genIndices.at(k)]);
	      muPmatch_miss_eta->Fill(genP_eta[genIndices.at(k)]);
	      muPmatch_miss_iso->Fill(mu_tkRelIso[muIndices.at(k)]);
	      if(fabs(genP_eta[genIndices.at(k)]) < 1.2) muPmatch_miss_barrel->Fill(genP_pt[genIndices.at(k)]);
	      else muPmatch_miss_endcap->Fill(genP_pt[genIndices.at(k)]);
	      if(genP_pt[genIndices.at(k)] >= 2000 && genP_pt[genIndices.at(k)] <= 3000) muPmatch_miss_nStat->Fill(mu_nStations[muIndices.at(k)]);
	      /*/// Debugging ///
	      if(genP_pt[genIndices.at(k)] < 10000){
		cout <<"Event "<<i<<" with "<<muIndices.size()<<" reco-gen matches." << endl;
		cout <<"\tGenPart pt: "<<genP_pt[genIndices.at(k)]<<" eta: "<<genP_eta[genIndices.at(k)]<<" phi: "<<genP_phi[genIndices.at(k)]<<" flavor: "<<genP_flavor[genIndices.at(k)]<<" mom: "<<genP_flavor[genP_momIdx[genIndices.at(k)]]<<" final mom: "<<genP_flavor[genP_momIdxPrompt->at(genIndices.at(k))]<<" genP idx: "<<genIndices.at(k) << endl;
		cout <<"\tReco Muon pt: "<<mu_pt[muIndices.at(k)]<<" eta: "<<mu_eta[muIndices.at(k)]<<" phi: "<<mu_phi[muIndices.at(k)]<<" charge: "<<mu_ch[muIndices.at(k)]<<" gen match: "<<mu_genIdx[muIndices.at(k)]<<" # match stats: "<<mu_nStations[muIndices.at(k)]<<" # of tk layers: "<<mu_nTkLayers[muIndices.at(k)]<<" isLoose: "<<mu_isLoose[muIndices.at(k)]<<" isHigh: "<<(int)mu_isHigh[muIndices.at(k)]<<" dz: "<<mu_Dz[muIndices.at(k)]<< endl;
		if(mu_genIdx[muIndices.at(k)]!=-1) cout <<"\tMatched GenPart pt: "<<genP_pt[mu_genIdx[muIndices.at(k)]]<<" eta: "<<genP_eta[mu_genIdx[muIndices.at(k)]]<<" phi: "<<genP_phi[mu_genIdx[muIndices.at(k)]]<<" flavor: "<<genP_flavor[mu_genIdx[muIndices.at(k)]]<<" mom: "<<genP_flavor[genP_momIdx[mu_genIdx[muIndices.at(k)]]]<<" final mom: "<<genP_flavor[genP_momIdxPrompt->at(mu_genIdx[muIndices.at(k)])] << endl;
	      }
	      /////////////////*/
	    } // Positive miss match
	  } // Positive match
	  else {
	    muMinusMatch->Fill(genP_pt[genIndices.at(k)]);
	    muNmatch_eta->Fill(genP_eta[genIndices.at(k)]);
	    muNmatch_iso->Fill(mu_tkRelIso[muIndices.at(k)]);
	    if(fabs(genP_eta[genIndices.at(k)]) < 1.2) muNmatch_barrel->Fill(genP_pt[genIndices.at(k)]);
	    else muNmatch_endcap->Fill(genP_pt[genIndices.at(k)]);
	    if(genP_pt[genIndices.at(k)] >= 2000 && genP_pt[genIndices.at(k)] <= 3000) muNmatch_nStat->Fill(mu_nStations[muIndices.at(k)]);

	    if(mu_ch[muIndices.at(k)]*genP_flavor[genIndices.at(k)] > 0){
	      muMinusMatch_miss->Fill(genP_pt[genIndices.at(k)]);
	      muNmatch_miss_eta->Fill(genP_eta[genIndices.at(k)]);
	      muNmatch_miss_iso->Fill(mu_tkRelIso[muIndices.at(k)]);
	      if(fabs(genP_eta[genIndices.at(k)]) < 1.2) muNmatch_miss_barrel->Fill(genP_pt[genIndices.at(k)]);
	      else muNmatch_miss_endcap->Fill(genP_pt[genIndices.at(k)]);
	      if(genP_pt[genIndices.at(k)] >= 2000 && genP_pt[genIndices.at(k)] <= 3000) muNmatch_miss_nStat->Fill(mu_nStations[muIndices.at(k)]);
	      /*/// Debugging ///
	      if(genP_pt[genIndices.at(k)] < 10000){
		cout <<"Event "<<i<<" with "<<muIndices.size()<<" reco-gen matches." << endl;
		cout <<"\tGenPart pt: "<<genP_pt[genIndices.at(k)]<<" eta: "<<genP_eta[genIndices.at(k)]<<" phi: "<<genP_phi[genIndices.at(k)]<<" flavor: "<<genP_flavor[genIndices.at(k)]<<" mom: "<<genP_flavor[genP_momIdx[genIndices.at(k)]]<<" final mom: "<<genP_flavor[genP_momIdxPrompt->at(genIndices.at(k))]<<" genP idx: "<<genIndices.at(k) << endl;
		cout <<"\tReco Muon pt: "<<mu_pt[muIndices.at(k)]<<" eta: "<<mu_eta[muIndices.at(k)]<<" phi: "<<mu_phi[muIndices.at(k)]<<" charge: "<<mu_ch[muIndices.at(k)]<<" gen match: "<<mu_genIdx[muIndices.at(k)]<<" # match stats: "<<mu_nStations[muIndices.at(k)]<<" # of tk layers: "<<mu_nTkLayers[muIndices.at(k)]<<" isLoose: "<<mu_isLoose[muIndices.at(k)]<<" isHigh: "<<(int)mu_isHigh[muIndices.at(k)]<<" dz: "<<mu_Dz[muIndices.at(k)]<< endl;
		if(mu_genIdx[muIndices.at(k)]!=-1) cout <<"\tMatched GenPart pt: "<<genP_pt[mu_genIdx[muIndices.at(k)]]<<" eta: "<<genP_eta[mu_genIdx[muIndices.at(k)]]<<" phi: "<<genP_phi[mu_genIdx[muIndices.at(k)]]<<" flavor: "<<genP_flavor[mu_genIdx[muIndices.at(k)]]<<" mom: "<<genP_flavor[genP_momIdx[mu_genIdx[muIndices.at(k)]]]<<" final mom: "<<genP_flavor[genP_momIdxPrompt->at(mu_genIdx[muIndices.at(k)])] << endl;
	      }
	      /////////////////*/
	    } // Negative miss match
	  } // Negative match

	} // Require the muon to be prompt
      }
    } // Loop over good reco-gen matches





  }// Loop over entries

  std::cout << std::endl;
  
  TCanvas* c0 = new TCanvas();
  c0->cd();
  muPlusMatch->SetTitle("+ Muon Matched p_{T}");
  muPlusMatch->GetXaxis()->SetTitle("#mu p_{T}  [GeV]");
  muPlusMatch->Draw();
  c0->SaveAs("plots/charge_misID/MuPlus_match_Wmunu-preEE_pT.png");
  TCanvas* c2 = new TCanvas();
  c2->cd();
  muPlusMatch_miss->SetTitle("+ Muon mis-identified p_{T}");
  muPlusMatch_miss->GetXaxis()->SetTitle("#mu p_{T}  [GeV]");
  muPlusMatch_miss->Draw();
  c2->SaveAs("plots/charge_misID/MuPlus_matchMissID_Wmunu-preEE_pT.png");
  TCanvas* c3 = new TCanvas();
  c3->cd();
  muMinusMatch->SetTitle("- Muon Matched p_{T}");
  muMinusMatch->GetXaxis()->SetTitle("#mu p_{T}  [GeV]");
  muMinusMatch->Draw();
  c3->SaveAs("plots/charge_misID/MuMinus_match_Wmunu-preEE_pT.png");
  TCanvas* c4 = new TCanvas();
  c4->cd();
  muMinusMatch_miss->SetTitle("- Muon mis-identified p_{T}");
  muMinusMatch_miss->GetXaxis()->SetTitle("#mu p_{T}  [GeV]");
  muMinusMatch_miss->Draw();
  c4->SaveAs("plots/charge_misID/MuMinus_matchMissID_Wmunu-preEE_pT.png");

  TCanvas* c5 = new TCanvas();
  c5->cd();
  muPmatch_eta->SetTitle("+ Muon Matched #eta");
  muPmatch_eta->GetXaxis()->SetTitle("#mu #eta");
  muPmatch_eta->Draw();
  c5->SaveAs("plots/charge_misID/MuPlus_match_Wmunu-preEE_eta.png");
  TCanvas* c6 = new TCanvas();
  c6->cd();
  muPmatch_miss_eta->SetTitle("+ Muon mis-identified #eta");
  muPmatch_miss_eta->GetXaxis()->SetTitle("#mu #eta");
  muPmatch_miss_eta->Draw();
  c6->SaveAs("plots/charge_misID/MuPlus_matchMissID_Wmunu-preEE_eta.png");
  TCanvas* c7 = new TCanvas();
  c7->cd();
  muNmatch_eta->SetTitle("- Muon Matched #eta");
  muNmatch_eta->GetXaxis()->SetTitle("#mu #eta");
  muNmatch_eta->Draw();
  c7->SaveAs("plots/charge_misID/MuMinus_match_Wmunu-preEE_eta.png");
  TCanvas* c8 = new TCanvas();
  c8->cd();
  muNmatch_miss_eta->SetTitle("- Muon mis-identified #eta");
  muNmatch_miss_eta->GetXaxis()->SetTitle("#mu #eta");
  muNmatch_miss_eta->Draw();
  c8->SaveAs("plots/charge_misID/MuMinus_matchMissID_Wmunu-preEE_eta.png");
  
  
  TGraphAsymmErrors* missIDplus = new TGraphAsymmErrors(muPlusMatch_miss, muPlusMatch);
  TGraphAsymmErrors* missIDminus = new TGraphAsymmErrors(muMinusMatch_miss, muMinusMatch);

  TGraphAsymmErrors* missIDplus_eta = new TGraphAsymmErrors(muPmatch_miss_eta, muPmatch_eta);
  TGraphAsymmErrors* missIDminus_eta = new TGraphAsymmErrors(muNmatch_miss_eta, muNmatch_eta);

  TGraphAsymmErrors* missIDplus_barrel = new TGraphAsymmErrors(muPmatch_miss_barrel, muPmatch_barrel);
  TGraphAsymmErrors* missIDminus_barrel = new TGraphAsymmErrors(muNmatch_miss_barrel, muNmatch_barrel);

  TGraphAsymmErrors* missIDplus_endcap = new TGraphAsymmErrors(muPmatch_miss_endcap, muPmatch_endcap);
  TGraphAsymmErrors* missIDminus_endcap = new TGraphAsymmErrors(muNmatch_miss_endcap, muNmatch_endcap);

  TGraphAsymmErrors* missIDplus_iso = new TGraphAsymmErrors(muPmatch_miss_iso, muPmatch_iso);
  TGraphAsymmErrors* missIDminus_iso = new TGraphAsymmErrors(muNmatch_miss_iso, muNmatch_iso);

  TGraphAsymmErrors* missIDplus_nStat = new TGraphAsymmErrors(muPmatch_miss_nStat, muPmatch_nStat);
  TGraphAsymmErrors* missIDminus_nStat = new TGraphAsymmErrors(muNmatch_miss_nStat, muNmatch_nStat);

  cout <<"# of + match: "<<muPlusMatch->GetEntries()<< endl;
  cout <<"# of + match miss-ID: "<<muPlusMatch_miss->GetEntries()<< endl;
  cout <<"# of - match: "<<muMinusMatch->GetEntries()<< endl;
  cout <<"# of - match miss-ID: "<<muMinusMatch_miss->GetEntries()<< endl;

  
  TCanvas* c_pT = new TCanvas("Charge_missID","",600,500);
  c_pT->cd();
  c_pT->SetLogy();

  missIDplus->SetMaximum(1.0);
  missIDplus->SetMinimum(1E-5);
  missIDplus->SetMarkerStyle(20);
  missIDplus->SetMarkerColor(1);
  missIDplus->SetLineColor(1);
  missIDplus->GetYaxis()->SetTitle("Charge mis-ID rate");
  missIDplus->GetYaxis()->SetTitleOffset(1.3);
  missIDplus->GetXaxis()->SetRangeUser(0, 3000);
  missIDplus->GetXaxis()->SetTitle("#mu p_{T}  [GeV]");
  missIDplus->GetXaxis()->SetTitleOffset(1.2);
  missIDplus->Draw("AP");

  missIDminus->SetMarkerStyle(20);
  missIDminus->SetMarkerColor(2);
  missIDminus->SetLineColor(2);
  missIDminus->Draw("P same");

  TLegend * leg = new TLegend(0.65, 0.75, 0.9, 0.9);
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetTextSize(0.03);
  leg->AddEntry(missIDplus, "Positive muons", "apel");
  leg->AddEntry(missIDminus, "Negative muons", "apel");
  leg->Draw();

  TString title = "#bf{CMS} Simulation                                         2022 (13.6 TeV)";
  TLatex* preliminary = new TLatex(0.12,0.92, title);
  preliminary->SetNDC();
  preliminary->SetTextFont(42);
  preliminary->SetTextSize(0.040);
  preliminary->Draw();


  TCanvas* c_eta = new TCanvas("Charge_missID_eta","",600,500);
  c_eta->cd();
  c_eta->SetLogy();

  missIDplus_eta->SetMaximum(1.0);
  missIDplus_eta->SetMinimum(1E-4);
  missIDplus_eta->SetMarkerStyle(20);
  missIDplus_eta->SetMarkerColor(1);
  missIDplus_eta->SetLineColor(1);
  missIDplus_eta->GetYaxis()->SetTitle("Charge mis-ID rate");
  missIDplus_eta->GetYaxis()->SetTitleOffset(1.3);
  missIDplus_eta->GetXaxis()->SetRangeUser(-2.4, 2.4);
  missIDplus_eta->GetXaxis()->SetTitle("#mu #eta");
  missIDplus_eta->GetXaxis()->SetTitleOffset(1.2);
  missIDplus_eta->Draw("AP");

  missIDminus_eta->SetMarkerStyle(20);
  missIDminus_eta->SetMarkerColor(2);
  missIDminus_eta->SetLineColor(2);
  missIDminus_eta->Draw("P same");

  TLegend * leg_eta = new TLegend(0.65, 0.75, 0.9, 0.9);
  leg_eta->SetFillStyle(0);
  leg_eta->SetBorderSize(0);
  leg_eta->SetTextSize(0.03);
  leg_eta->AddEntry(missIDplus_eta, "Positive muons", "apel");
  leg_eta->AddEntry(missIDminus_eta, "Negative muons", "apel");
  leg_eta->Draw();

  preliminary->Draw();


  TCanvas* c_barrel = new TCanvas("Charge_missID_barrel","",600,500);
  c_barrel->cd();
  c_barrel->SetLogy();

  missIDplus_barrel->SetMaximum(1.0);
  missIDplus_barrel->SetMinimum(1E-5);
  missIDplus_barrel->SetMarkerStyle(20);
  missIDplus_barrel->SetMarkerColor(1);
  missIDplus_barrel->SetLineColor(1);
  missIDplus_barrel->GetYaxis()->SetTitle("Charge mis-ID rate");
  missIDplus_barrel->GetYaxis()->SetTitleOffset(1.3);
  missIDplus_barrel->GetXaxis()->SetRangeUser(0, 3000);
  missIDplus_barrel->GetXaxis()->SetTitle("#mu p_{T}  [GeV]");
  missIDplus_barrel->GetXaxis()->SetTitleOffset(1.2);
  missIDplus_barrel->Draw("AP");

  missIDminus_barrel->SetMarkerStyle(20);
  missIDminus_barrel->SetMarkerColor(2);
  missIDminus_barrel->SetLineColor(2);
  missIDminus_barrel->Draw("P same");

  TLegend * leg_barrel = new TLegend(0.65, 0.75, 0.9, 0.9);
  leg_barrel->SetFillStyle(0);
  leg_barrel->SetBorderSize(0);
  leg_barrel->SetTextSize(0.03);
  leg_barrel->AddEntry(missIDplus_barrel, "Positive muons", "apel");
  leg_barrel->AddEntry(missIDminus_barrel, "Negative muons", "apel");
  leg_barrel->Draw();

  preliminary->Draw();


  TCanvas* c_endcap = new TCanvas("Charge_missID_endcap","",600,500);
  c_endcap->cd();
  c_endcap->SetLogy();

  missIDplus_endcap->SetMaximum(1.0);
  missIDplus_endcap->SetMinimum(1E-5);
  missIDplus_endcap->SetMarkerStyle(20);
  missIDplus_endcap->SetMarkerColor(1);
  missIDplus_endcap->SetLineColor(1);
  missIDplus_endcap->GetYaxis()->SetTitle("Charge mis-ID rate");
  missIDplus_endcap->GetYaxis()->SetTitleOffset(1.3);
  missIDplus_endcap->GetXaxis()->SetRangeUser(0, 3000);
  missIDplus_endcap->GetXaxis()->SetTitle("#mu p_{T}  [GeV]");
  missIDplus_endcap->GetXaxis()->SetTitleOffset(1.2);
  missIDplus_endcap->Draw("AP");

  missIDminus_endcap->SetMarkerStyle(20);
  missIDminus_endcap->SetMarkerColor(2);
  missIDminus_endcap->SetLineColor(2);
  missIDminus_endcap->Draw("P same");

  TLegend * leg_endcap = new TLegend(0.65, 0.75, 0.9, 0.9);
  leg_endcap->SetFillStyle(0);
  leg_endcap->SetBorderSize(0);
  leg_endcap->SetTextSize(0.03);
  leg_endcap->AddEntry(missIDplus_endcap, "Positive muons", "apel");
  leg_endcap->AddEntry(missIDminus_endcap, "Negative muons", "apel");
  leg_endcap->Draw();

  preliminary->Draw();


  TCanvas* c_iso = new TCanvas("Charge_missID_iso","",600,500);
  c_iso->cd();
  c_iso->SetLogy();
  c_iso->SetLogx();

  missIDplus_iso->SetMaximum(1.0);
  missIDplus_iso->SetMinimum(1E-5);
  missIDplus_iso->SetMarkerStyle(20);
  missIDplus_iso->SetMarkerColor(1);
  missIDplus_iso->SetLineColor(1);
  missIDplus_iso->GetYaxis()->SetTitle("Charge mis-ID rate");
  missIDplus_iso->GetYaxis()->SetTitleOffset(1.3);
  missIDplus_iso->GetXaxis()->SetRangeUser(1E-4, 1);
  missIDplus_iso->GetXaxis()->SetTitle("#mu relative tracker isolation");
  missIDplus_iso->GetXaxis()->SetTitleOffset(1.2);
  missIDplus_iso->Draw("AP");

  missIDminus_iso->SetMarkerStyle(20);
  missIDminus_iso->SetMarkerColor(2);
  missIDminus_iso->SetLineColor(2);
  missIDminus_iso->Draw("P same");

  TLegend * leg_iso = new TLegend(0.65, 0.75, 0.9, 0.9);
  leg_iso->SetFillStyle(0);
  leg_iso->SetBorderSize(0);
  leg_iso->SetTextSize(0.03);
  leg_iso->AddEntry(missIDplus_iso, "Positive muons", "apel");
  leg_iso->AddEntry(missIDminus_iso, "Negative muons", "apel");
  leg_iso->Draw();

  preliminary->Draw();


  TCanvas* c_nStat = new TCanvas("Charge_missID_nStations","",600,500);
  c_nStat->cd();
  c_nStat->SetLogy();

  missIDplus_nStat->SetMaximum(1.0);
  missIDplus_nStat->SetMinimum(1E-5);
  missIDplus_nStat->SetMarkerStyle(20);
  missIDplus_nStat->SetMarkerColor(1);
  missIDplus_nStat->SetLineColor(1);
  missIDplus_nStat->GetYaxis()->SetTitle("Charge mis-ID rate");
  missIDplus_nStat->GetYaxis()->SetTitleOffset(1.3);
  missIDplus_nStat->GetXaxis()->SetRangeUser(1, 5);
  missIDplus_nStat->GetXaxis()->SetTitle("#mu # of matched stations");
  missIDplus_nStat->GetXaxis()->SetTitleOffset(1.2);
  missIDplus_nStat->Draw("AP");

  missIDminus_nStat->SetMarkerStyle(20);
  missIDminus_nStat->SetMarkerColor(2);
  missIDminus_nStat->SetLineColor(2);
  missIDminus_nStat->Draw("P same");

  TLegend * leg_nStat = new TLegend(0.65, 0.75, 0.9, 0.9);
  leg_nStat->SetFillStyle(0);
  leg_nStat->SetBorderSize(0);
  leg_nStat->SetTextSize(0.03);
  leg_nStat->AddEntry(missIDplus_nStat, "Positive muons", "apel");
  leg_nStat->AddEntry(missIDminus_nStat, "Negative muons", "apel");
  leg_nStat->Draw();

  preliminary->Draw();

  /// Save Plots ///
  //c_pT->SaveAs("plots/charge_misID/ChargeMisID_Wmunu-All_pT.png");
  //c_eta->SaveAs("plots/charge_misID/ChargeMisID_Wmunu-All_eta.png");
  //c_barrel->SaveAs("plots/charge_misID/ChargeMisID_Wmunu-All_pT-barrel.png");
  //c_endcap->SaveAs("plots/charge_misID/ChargeMisID_Wmunu-All_pT-endcap.png");
  //c_iso->SaveAs("plots/charge_misID/ChargeMisID_Wmunu-All_TkRelIso.png");
  //c_nStat->SaveAs("plots/charge_misID/ChargeMisID_Wmunu-All_nStations.png");
  



}// End of main 

void charge_misId(){
 
  //chargeMissID("/eos/user/d/diegof/cmt/PreprocessRDF/Wprime_chargeMissID_config/Wmunu2000to3000_postEE/cat_base/chargeMissID_good/data_1.root","ok.root",10000);
  //chargeMissID("/eos/user/d/diegof/cmt/PreprocessRDF/Wprime_chargeMissID_config/Wprime2000_postEE/cat_base/chargeMissID_good/data_0.root","ok.root",0);
  //chargeMissID("/eos/user/d/diegof/cmt/MergeCategorization/Wprime_chargeMissID_config/Wmunu6000_postEE/cat_base/chargeMissID_full/data_0.root","ok.root",100000);

  //chargeMissID("/eos/user/d/diegof/cmt/MergeCategorization/Wprime_chargeMissID_config/Wmunu2000_18/cat_base/chargeMissID_2018/data_0.root","ok.root",10000);

  chargeMissID("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/bin/txt/Wmunu_preEE.txt","ok.root",0);

}


