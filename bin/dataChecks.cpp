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

float deltaR(float eta1, float eta2, float phi1, float phi2){
  float deta = eta1 - eta2;
  float dphi = deltaPhi(phi1, phi2);

  return sqrt(deta*deta + dphi*dphi);
}

void plotChecks(string filename, string output, int f){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  /* TO CHECK DATA MERGING */
  /*
  string path(filename);
  TFileCollection fc("FileCollection", "FileCollection", path.c_str());

  TString treeName = "Events";
  TChain chain(treeName);
  chain.AddFileInfoList(fc.GetList());

  int nFiles = fc.GetNFiles();
  int nentries = chain.GetEntries();
  cout <<"This chain made of "<<nFiles<<" files, has "<<nentries<<" entries"<< endl;
  */
  /*************************/

  
  TFile *f1 =  TFile::Open((filename).c_str());
  TTree *tree = new TTree;
    tree = (TTree*) f1->Get("Events");
  int nentries = tree->GetEntries();
  
  int size_max = 30;
  int size_max2 = 300;
  
  //Int_t nGenP = tree->SetBranchAddress("nGenPart", &nGenP);
  //Float_t genP_pt[size_max2];          tree->SetBranchAddress("GenPart_pt", &genP_pt);
  //Float_t genP_phi[size_max2];         tree->SetBranchAddress("GenPart_phi", &genP_phi);
  //Float_t genP_eta[size_max2];         tree->SetBranchAddress("GenPart_eta", &genP_eta);
  //Float_t genP_mass[size_max2];        tree->SetBranchAddress("GenPart_mass", &genP_mass);
  //Int_t genP_flavor[size_max2];        tree->SetBranchAddress("GenPart_pdgId", &genP_flavor);
  //Int_t genP_momIdx[size_max2];        tree->SetBranchAddress("GenPart_genPartIdxMother", &genP_momIdx);

  //Int_t nGenJet = tree->SetBranchAddress("nGenJet", &nGenJet);
  //Float_t GenJet_pt[size_max2];        tree->SetBranchAddress("GenJet_pt", &GenJet_pt);

  //Float_t LHE_HT = tree->SetBranchAddress("LHE_HT", &LHE_HT);
  //Float_t LHE_HTin = tree->SetBranchAddress("LHE_HTIncoming", &LHE_HTin);

  //Int_t nLHEPart = tree->SetBranchAddress("nLHEPart", &nLHEPart);
  //Float_t LHEPart_M[size_max2];        tree->SetBranchAddress("LHEPart_mass", &LHEPart_M);
  //Int_t LHEPart_Id[size_max2];         tree->SetBranchAddress("LHEPart_pdgId", &LHEPart_Id);
  //Float_t LHEPart_pt[size_max2];       tree->SetBranchAddress("LHEPart_pt", &LHEPart_pt);
  //Float_t LHEPart_eta[size_max2];      tree->SetBranchAddress("LHEPart_eta", &LHEPart_eta);
  //Float_t LHEPart_phi[size_max2];      tree->SetBranchAddress("LHEPart_phi", &LHEPart_phi);

  Float_t met_pt = tree->SetBranchAddress("MET_pt",&met_pt);
  Float_t met_phi = tree->SetBranchAddress("MET_phi",&met_phi);
  Float_t PuppiMET_pt = tree->SetBranchAddress("PuppiMET_pt", &PuppiMET_pt);
  Float_t PuppiMET_phi = tree->SetBranchAddress("PuppiMET_phi", &PuppiMET_phi);

  Int_t nMuon = tree->SetBranchAddress("nMuon",&nMuon);
  Float_t mu_pt[size_max];          tree->SetBranchAddress("Muon_pt",&mu_pt);
  Float_t mu_mass[size_max];        tree->SetBranchAddress("Muon_mass",&mu_mass);
  Float_t mu_phi[size_max];         tree->SetBranchAddress("Muon_phi",&mu_phi);
  Float_t mu_eta[size_max];         tree->SetBranchAddress("Muon_eta",&mu_eta);
  Int_t mu_ch[size_max];            tree->SetBranchAddress("Muon_charge",&mu_ch);
  Bool_t mu_isMedium[size_max];     tree->SetBranchAddress("Muon_mediumId",&mu_isMedium);
  Bool_t mu_isLoose[size_max];      tree->SetBranchAddress("Muon_looseId",&mu_isLoose);
  Bool_t mu_isTight[size_max];      tree->SetBranchAddress("Muon_tightId",&mu_isTight);
  Float_t mu_Dxyerr[size_max];      tree->SetBranchAddress("Muon_dxyErr",&mu_Dxyerr);
  Float_t mu_Dz[size_max];          tree->SetBranchAddress("Muon_dz",&mu_Dz);
  Float_t mu_Dxy[size_max];         tree->SetBranchAddress("Muon_dxy",&mu_Dxy);
  Float_t mu_ptErr[size_max];       tree->SetBranchAddress("Muon_ptErr",&mu_ptErr);
  Float_t mu_MiniIso[size_max];     tree->SetBranchAddress("Muon_miniPFRelIso_all",&mu_MiniIso);
  Float_t mu_Iso04[size_max];       tree->SetBranchAddress("Muon_pfRelIso04_all",&mu_Iso04);
  Float_t mu_tkRelIso[size_max];    tree->SetBranchAddress("Muon_tkRelIso",&mu_tkRelIso);
  UChar_t mu_isHigh[size_max];      tree->SetBranchAddress("Muon_highPtId",&mu_isHigh);
  Bool_t mu_IsGlobal[size_max];     tree->SetBranchAddress("Muon_isGlobal",&mu_IsGlobal);
  Bool_t mu_IsTracker[size_max];    tree->SetBranchAddress("Muon_isTracker",&mu_IsTracker);
  UChar_t mu_nStations[size_max];     tree->SetBranchAddress("Muon_nStations",&mu_nStations);
  //UChar_t mu_genFlav[size_max];     tree->SetBranchAddress("Muon_genPartFlav",&mu_genFlav);
  //Int_t mu_genIdx[size_max];        tree->SetBranchAddress("Muon_genPartIdx",&mu_genIdx);
  Float_t mu_TunePRelPt[size_max];  tree->SetBranchAddress("Muon_tunepRelPt",&mu_TunePRelPt);

  Int_t nJet = tree->SetBranchAddress("nJet",&nJet);
  Float_t jet_pt[size_max];        tree->SetBranchAddress("Jet_pt",&jet_pt);
  Float_t jet_mass[size_max];      tree->SetBranchAddress("Jet_mass",&jet_mass);
  Float_t jet_phi[size_max];       tree->SetBranchAddress("Jet_phi",&jet_phi);
  Float_t jet_eta[size_max];       tree->SetBranchAddress("Jet_eta",&jet_eta);
  UChar_t jet_jetId[size_max];     tree->SetBranchAddress("Jet_jetId",&jet_jetId);
  //Int_t jet_hadronFlav[size_max];  tree->SetBranchAddress("Jet_hadronFlavour",&jet_hadronFlav);
  Float_t jet_deepBTag[size_max];  tree->SetBranchAddress("Jet_btagDeepFlavB",&jet_deepBTag); 
  //Int_t jet_partonFlav[size_max];  tree->SetBranchAddress("Jet_partonFlavour",&jet_partonFlav);
  //Int_t jet_genJetIdx[size_max];   tree->SetBranchAddress("Jet_genJetIdx",&jet_genJetIdx);

  Int_t nElectron = tree->SetBranchAddress("nElectron",&nElectron);
  Float_t el_pt[size_max];                         tree->SetBranchAddress("Electron_pt",&el_pt);
  Float_t el_mass[size_max];                       tree->SetBranchAddress("Electron_mass",&el_mass);
  Float_t el_phi[size_max];                        tree->SetBranchAddress("Electron_phi",&el_phi);
  Float_t el_eta[size_max];                        tree->SetBranchAddress("Electron_eta",&el_eta);
  Int_t el_ch[size_max];                           tree->SetBranchAddress("Electron_charge",&el_ch);
  Int_t el_cutBased[size_max];                     tree->SetBranchAddress("Electron_cutBased",&el_cutBased);
  Float_t Electron_pfRelIso03_all[size_max];       tree->SetBranchAddress("Electron_pfRelIso03_all",&Electron_pfRelIso03_all);
  Float_t Electron_miniPFRelIso_all[size_max];     tree->SetBranchAddress("Electron_miniPFRelIso_all",&Electron_miniPFRelIso_all);
  Float_t el_Dxy[size_max];                        tree->SetBranchAddress("Electron_dxy",&el_Dxy);

  Int_t muIdx = tree->SetBranchAddress("goodMuIdx",&muIdx);


  TH1F* muonPt = new TH1F("muonPt", "", 20, 200, 700);
  TH1F* muonPhi = new TH1F("muonPhi", "", 10, -M_PI, M_PI);
  TH1F* muonDxy = new TH1F("muonDxy", "", 10, -0.1, 0.1);
  TH1F* muonDz = new TH1F("muonDz", "", 10, -0.1, 0.1);
  TH1I* muonNstat = new TH1I("muonNstat", "", 5, 0, 4);

  TH1F* muon2Pt = new TH1F("muon2Pt", "", 20, 200, 700);
  TH1F* muon2Phi = new TH1F("muon2Phi", "", 10, -M_PI, M_PI);
  TH1F* muon2Dxy = new TH1F("muon2Dxy", "", 10, -0.1, 0.1);
  TH1F* muon2Dz = new TH1F("muon2Dz", "", 10, -0.1, 0.1);
  TH1I* muon2Nstat = new TH1I("muon2Nstat", "", 5, 0, 5);

  
  /*
  TH1F* Mu_TuneP = new TH1F("Muon_TunePpt", "", 100, 0, 200);

  TH1F* NoPass_TunePpt = new TH1F("NoPass_TunePpt", "",50, 0, 200);
  TH1F* NoPass_isHighPt = new TH1F("NoPass_isHighPt", "",3, 0, 3);
  TH1F* NoPass_eta = new TH1F("NoPass_eta", "",50, -4, 4);
  TH1F* NoPass_PtErr = new TH1F("NoPass_PtErr", "",50, 0, 0.5);
  TH1F* NoPass_TkIso = new TH1F("NoPass_TkIso", "",50, 0, 0.4);
  TH1F* NoPass_Dxy = new TH1F("NoPass_Dxy", "",50, -0.05, 0.05);


  TH1F* mu1_TunePpt_True = new TH1F("mu1_TunePpt_true", "",50, 0, 200);
  TH1F* mu1_TunePpt_False = new TH1F("mu1_TunePpt_false", "",50, 0, 200);
  TH1F* mu2_TunePpt_True = new TH1F("mu2_TunePpt_true", "",50, 0, 200);
  TH1F* mu2_TunePpt_False = new TH1F("mu2_TunePpt_false", "",50, 0, 200);

  TH1F* mu1_isHighPt_True = new TH1F("mu1_isHighPt_true", "",3, 0, 3);
  TH1F* mu1_isHighPt_False = new TH1F("mu1_isHighPt_false", "",3, 0, 3);
  TH1F* mu2_isHighPt_True = new TH1F("mu2_isHighPt_true", "",3, 0, 3);
  TH1F* mu2_isHighPt_False = new TH1F("mu2_isHighPt_false", "",3, 0, 3);

  TH1F* mu1_eta_True = new TH1F("mu1_eta_true", "",50, -4, 4);
  TH1F* mu1_eta_False = new TH1F("mu1_eta_false", "",50, -4, 4);
  TH1F* mu2_eta_True = new TH1F("mu2_eta_true", "",50, -4, 4);
  TH1F* mu2_eta_False = new TH1F("mu2_eta_false", "",50, -4, 4);

  TH1F* mu1_PtErr_True = new TH1F("mu1_PtErr_true", "",50, 0, 0.5);
  TH1F* mu1_PtErr_False = new TH1F("mu1_PtErr_false", "",50, 0, 0.5);
  TH1F* mu2_PtErr_True = new TH1F("mu2_PtErr_true", "",50, 0, 0.5);
  TH1F* mu2_PtErr_False = new TH1F("mu2_PtErr_false", "",50, 0, 0.5);

  TH1F* mu1_TkIso_True = new TH1F("mu1_TkIso_true", "",50, 0, 0.4);
  TH1F* mu1_TkIso_False = new TH1F("mu1_TkIso_false", "",50, 0, 0.4);
  TH1F* mu2_TkIso_True = new TH1F("mu2_TkIso_true", "",50, 0, 0.4);
  TH1F* mu2_TkIso_False = new TH1F("mu2_TkIso_false", "",50, 0, 0.4);

  TH1F* mu1_Dxy_True = new TH1F("mu1_Dxy_true", "",50, -0.04, 0.04);
  TH1F* mu1_Dxy_False = new TH1F("mu1_Dxy_false", "",50, -0.04, 0.04);
  TH1F* mu2_Dxy_True = new TH1F("mu2_Dxy_true", "",50, -0.04, 0.04);
  TH1F* mu2_Dxy_False = new TH1F("mu2_Dxy_false", "",50, -0.04, 0.04);

  TH1F* kappa_True = new TH1F("kappa_true", "",50, -20, 20);
  TH1F* kappa_False = new TH1F("kappa_false", "",50, -20, 20);
  */

  if(f!=0)
    nentries=f;
  int counter = 0;
  
  for(int i = 0; i < nentries; i++){

    tree->GetEntry(i);

    if(i % 100 == 0) 
      std::cout << "[dataChecks.cpp] processed : " << i << " entries\r" << std::flush;

    // Define deltaPhi_MuMET
    float deltaPhi_MuMET = fabs(deltaPhi(mu_phi[muIdx], PuppiMET_phi));

    // Define nGoodJets
    int nGoodJets = 0;
    for (int j = 0; j < nJet; j++){
      if(jet_pt[j] > 30.0 && fabs(jet_eta[j]) < 2.5 && jet_jetId[j] != 0 && deltaR(jet_eta[j], mu_eta[muIdx], jet_phi[j], mu_phi[muIdx]) > 0.4){
	nGoodJets ++;
      }
    }

    // Apply kinematic selection
    if (mu_TunePRelPt[muIdx]*mu_pt[muIdx]/PuppiMET_pt <= 0.4 || mu_TunePRelPt[muIdx]*mu_pt[muIdx]/PuppiMET_pt >= 1.5 || deltaPhi_MuMET <= 2.5 || nGoodJets >= 6)
      continue;

    counter ++;

    // Check muons with pt > 200 GeV in far endcaps
    if (fabs(mu_eta[muIdx]) >= 2.1 && mu_TunePRelPt[muIdx]*mu_pt[muIdx] > 200){

      std::cout << "Event "<< i << " ==> Muon pT: "<< mu_pt[muIdx] << " // eta: "<< mu_eta[muIdx] << " // phi: "<< mu_phi[muIdx] << " // nStats: "<<(int) mu_nStations[muIdx] <<" // idx: "<< muIdx << std::endl;

      muonPt->Fill(mu_TunePRelPt[muIdx]*mu_pt[muIdx]);
      muonPhi->Fill(mu_phi[muIdx]);
      muonDxy->Fill(mu_Dxy[muIdx]);
      muonDz->Fill(mu_Dz[muIdx]);
      muonNstat->Fill(mu_nStations[muIdx]);

      int mu2 = 0;
      if(mu2 == muIdx)
	mu2 = muIdx +1;
      std::cout << "   ==> Second muon pT: "<< mu_pt[mu2] << " // eta: "<< mu_eta[mu2] << " // phi: "<< mu_phi[mu2] << " // high-pt: "<< (int)mu_isHigh[mu2] << std::endl;
      
    }



























    
    /********** CHECK HT ***********/
    /*
    float HT = 0;
    for(int j = 0; j<nGenJet; j++){
      HT += GenJet_pt[j];
    }
    bool fillHT = false;
    int idx = 0;
    for(int k = 0; k < nGenP; k++){
      if(genP_flavor[k] == 23 && genP_mass[k] < 120) fillHT = true;

      /// PrintOut ///
      cout <<"GenP #"<< k <<" ==> ID: "<<genP_flavor[k]<<" Pt: "<<genP_pt[k]<<" Eta: "<<genP_eta[k]<<" Phi: "<<genP_phi[k]<< endl;
    }
    for(int m = 0; m < nLHEPart; m++){
      cout <<"LHEP #"<< m <<" ==> ID: "<<LHEPart_Id[m]<<" Pt: "<<LHEPart_pt[m]<<" Eta: "<<LHEPart_eta[m]<<" Phi: "<<LHEPart_phi[m]<< endl;
    }

    if(fillHT) HThisto->Fill(LHE_HT);
    
    mZhisto->Fill(Z_invM);

    float ptZ = sqrt((mu_TunePRelPt[mu1_index]*mu_pt[mu1_index])*(mu_TunePRelPt[mu1_index]*mu_pt[mu1_index])+(mu_TunePRelPt[mu2_index]*mu_pt[mu2_index])*(mu_TunePRelPt[mu2_index]*mu_pt[mu2_index])+2*(mu_TunePRelPt[mu1_index]*mu_pt[mu1_index])*(mu_TunePRelPt[mu2_index]*mu_pt[mu2_index])*(cos(mu_phi[mu1_index])*cos(mu_phi[mu2_index])+sin(mu_phi[mu1_index])*sin(mu_phi[mu2_index])));
    ptZhisto->Fill(ptZ);

    float etaZ = asinh( (mu_TunePRelPt[mu1_index]*mu_pt[mu1_index]*sinh(mu_eta[mu1_index]) + mu_TunePRelPt[mu2_index]*mu_pt[mu2_index]*sinh(mu_eta[mu2_index]) )/ptZ );
    ptZvsEtaZ->Fill(etaZ, ptZ);
    */
    /*******************************/

    /****** CHECK DiMuon MASS ******/
    /*
    int momId1 = 0, momId2 = 0;
    float gen_mZ = 99999;

    if(mu_genIdx[mu1_index] > -1 && mu_genIdx[mu2_index] > -1){
      gen_mZ = sqrt( 2*(genP_pt[mu_genIdx[mu1_index]])*(genP_pt[mu_genIdx[mu2_index]])*(cosh(genP_eta[mu_genIdx[mu1_index]]-genP_eta[mu_genIdx[mu2_index]])-cos(deltaPhi(genP_phi[mu_genIdx[mu1_index]],genP_phi[mu_genIdx[mu2_index]]))));
      if(gen_mZ < 800){
	momId1 = genP_flavor[genP_momIdx[mu_genIdx[mu1_index]]];
	momId2 = genP_flavor[genP_momIdx[mu_genIdx[mu2_index]]];
	counter++;
	//cout <<"Event with diMuon invM = "<<gen_mZ<<", selected muon pair coming from ==> Mu1: "<<momId1<<" | Mu2: "<<momId2<< endl;
      }
    }    
    */
    /*******************************/ 

    /****** CHECK DY FILTER WORKS PROPERLY ******/
    // OPTION 1: Check if selected Muons come from Z. Check if they come from taus coming from Z
    /*
    int momId1 = 0, momId2 = 0;
    int grandmaId1 = 0, grandmaId2 = 0;

    if(mu_genIdx[mu1_index] > -1 && mu_genIdx[mu2_index] > -1){
      if(genP_momIdxPrompt->at(mu_genIdx[mu1_index]) > -1 && genP_momIdxPrompt->at(mu_genIdx[mu2_index]) > -1){
	momId1 = genP_flavor[genP_momIdxPrompt->at(mu_genIdx[mu1_index])];
	momId2 = genP_flavor[genP_momIdxPrompt->at(mu_genIdx[mu2_index])];
      }
    }
    if(abs(momId1) == 23 || abs(momId2) == 23)
      cout <<"Estamos jodidos"<< endl;

    if(abs(momId1) == 15 && abs(momId2) == 15){
      if(genP_momIdxPrompt->at(genP_momIdxPrompt->at(mu_genIdx[mu1_index])) > -1 && genP_momIdxPrompt->at(genP_momIdxPrompt->at(mu_genIdx[mu2_index])) > -1){
	grandmaId1 = genP_flavor[genP_momIdxPrompt->at(genP_momIdxPrompt->at(mu_genIdx[mu1_index]))];
	grandmaId2 = genP_flavor[genP_momIdxPrompt->at(genP_momIdxPrompt->at(mu_genIdx[mu2_index]))];
      }
    }
    if(abs(grandmaId1) == 23 || abs(grandmaId2) == 23)
      cout <<"TODO FUNCIONA BIEN!!"<< endl;
    */
    /*******************************************/

    /**** CHECK TTbar FILTER WORKS PROPERLY ****/
    // Loop over GenPart, selecting 2 tops and check their invM is below 700 GeV
    /*
    for(unsigned int iGen1 = 0; iGen1 < nGenP; iGen1++){
      if(abs(genP_flavor[iGen1]) != 6) continue;
      for(unsigned int iGen2 = iGen1+1; iGen2 < nGenP; iGen2++){
	if(abs(genP_flavor[iGen2]) != 6) continue;

	if(genP_flavor[iGen1]*genP_flavor[iGen2] != 1){
	  float px_t1 = genP_pt[iGen1]*cos(genP_phi[iGen1]);
	  float py_t1 = genP_pt[iGen1]*sin(genP_phi[iGen1]);
	  float pz_t1 = genP_pt[iGen1]*sinh(genP_eta[iGen1]);
	  float px_t2 = genP_pt[iGen2]*cos(genP_phi[iGen2]);
	  float py_t2 = genP_pt[iGen2]*sin(genP_phi[iGen2]);
	  float pz_t2 = genP_pt[iGen2]*sinh(genP_eta[iGen2]);
	  float px_tt = px_t1 + px_t2;
	  float py_tt = py_t1 + py_t2;
	  float pz_tt = pz_t1 + pz_t2;
	  float E_t1 = sqrt(genP_mass[iGen1]*genP_mass[iGen1] + px_t1*px_t1 + py_t1*py_t1 + pz_t1*pz_t1);
	  float E_t2 = sqrt(genP_mass[iGen2]*genP_mass[iGen2] + px_t2*px_t2 + py_t2*py_t2 + pz_t2*pz_t2);
	  float Mtt = sqrt((E_t1 + E_t2)*(E_t1 + E_t2) - px_tt*px_tt - py_tt*py_tt - pz_tt*pz_tt);

	  if(Mtt > 700.0)
	    cout <<"ESTAMOS JODIDOS ==> Mtt = "<< Mtt << endl;
	}

      } // Loop over GenP 2
    } // Loop over GenP 1
    */
    /*******************************************/




    /******************************************************************
               ALL BELOW ARE JUST OLD CHECKS ==> USELESS NOW 
    *******************************************************************/ 

    /*
    int nZ = nMuon*(nMuon-1)/2;
    bool selected_truth = false;
    bool selected_truth_mu2 = false;
    int MomId1_T = 0, MomId2_T = 0, MomId1_F = 0, MomId2_F = 0;
    */
    //if(mu1_index->at(0) != -1){ //QUIERO MIRAR LOS MUONES QUE VIENEN DE TAU Y ESTOS DE Z
      /*
      // Basic Check Plots
      for(int k = 0; k < nMuon; k++){
	//NoPass_TunePpt->Fill(mu_TunePRelPt[k]*mu_pt[k]); 
	//NoPass_isHighPt->Fill(mu_isHigh[k]);
	//NoPass_eta->Fill(mu_eta[k]);
	//NoPass_PtErr->Fill(mu_ptErr[k]/(mu_TunePRelPt[k]*mu_pt[k]));
	//NoPass_TkIso->Fill(mu_tkRelIso[k]);
	//NoPass_Dxy->Fill(mu_Dxy[k]);
      }
      */
      /*
      for(int j = 0; j < nZ; j++){
	if(mu1_index->at(0) == Z_mu1_idx->at(j)){
	  if(mu2_index->at(0) == Z_mu2_idx->at(j)){
	    selected_truth = Z_truth->at(j);
	  }
	}
      }// Obtaining the Ztruth of the selected muon pair
      */
      /*
      // Obtaining Plots with GenPart matching
      if(selected_truth==false){
	MomId1_F = genP_flavor[genP_momIdxPrompt->at(mu_genIdx[mu1_index->at(0)])];
	MomId2_F = genP_flavor[genP_momIdxPrompt->at(mu_genIdx[mu2_index->at(0)])];
	std::cout << " FOR Z FALSE ==> Flavor of Mu1 Mom: " << MomId1_F << " // Flavor of Mu2 Mom: " << MomId2_F << std::endl;
      }
      */

      /*
      if( (abs(MomId1_F)==1 && abs(MomId2_F)==1) || (abs(MomId1_F)==2 && abs(MomId2_F)==2) || (abs(MomId1_F)==3 && abs(MomId2_F)==3) || (abs(MomId1_F)==4 && abs(MomId2_F)==4) || (abs(MomId1_F)==5 && abs(MomId2_F)==5) || (abs(MomId1_F)==21 && abs(MomId2_F)==21) ){
	for(int iGen = 0; iGen < nGenP; iGen++){
	  if( abs(genP_flavor[iGen])==13 ) //&& abs(genP_flavor[genP_momIdxPrompt->at(iGen)])==23 )
	    std::cout <<"\t GenP index: "<<iGen<<" and Pt: "<<genP_pt[iGen]<<" and flavor: "<<genP_flavor[genP_momIdxPrompt->at(iGen)]<< std::endl;
	} // Loop over GenParticles
      }// If Muons from jets
      */
      /*
      // Obtain some basic plots
      if(selected_truth){

	mu1_TunePpt_True->Fill(mu_TunePRelPt[mu1_index->at(0)]*mu_pt[mu1_index->at(0)]);
	mu2_TunePpt_True->Fill(mu_TunePRelPt[mu2_index->at(0)]*mu_pt[mu2_index->at(0)]);

	mu1_isHighPt_True->Fill(mu_isHigh[mu1_index->at(0)]);
	mu2_isHighPt_True->Fill(mu_isHigh[mu2_index->at(0)]);

	mu1_eta_True->Fill(mu_eta[mu1_index->at(0)]);
	mu2_eta_True->Fill(mu_eta[mu2_index->at(0)]);

	mu1_PtErr_True->Fill(mu_ptErr[mu1_index->at(0)]/(mu_TunePRelPt[mu1_index->at(0)]*mu_pt[mu1_index->at(0)]));
	mu2_PtErr_True->Fill(mu_ptErr[mu2_index->at(0)]/(mu_TunePRelPt[mu2_index->at(0)]*mu_pt[mu2_index->at(0)]));

	mu1_TkIso_True->Fill(mu_tkRelIso[mu1_index->at(0)]);
	mu2_TkIso_True->Fill(mu_tkRelIso[mu2_index->at(0)]);

	mu1_Dxy_True->Fill(mu_Dxy[mu1_index->at(0)]);
	mu2_Dxy_True->Fill(mu_Dxy[mu2_index->at(0)]);

	kappa_True->Fill(1000*mu_ch[mu1_index->at(0)]/(mu_TunePRelPt[mu1_index->at(0)]*mu_pt[mu1_index->at(0)]));
	kappa_True->Fill(1000*mu_ch[mu2_index->at(0)]/(mu_TunePRelPt[mu2_index->at(0)]*mu_pt[mu2_index->at(0)]));

      }else {

	mu1_TunePpt_False->Fill(mu_TunePRelPt[mu1_index->at(0)]*mu_pt[mu1_index->at(0)]);
	mu2_TunePpt_False->Fill(mu_TunePRelPt[mu2_index->at(0)]*mu_pt[mu2_index->at(0)]);

	mu1_isHighPt_False->Fill(mu_isHigh[mu1_index->at(0)]);
	mu2_isHighPt_False->Fill(mu_isHigh[mu2_index->at(0)]);

	mu1_eta_False->Fill(mu_eta[mu1_index->at(0)]);
	mu2_eta_False->Fill(mu_eta[mu2_index->at(0)]);

	mu1_PtErr_False->Fill(mu_ptErr[mu1_index->at(0)]/(mu_TunePRelPt[mu1_index->at(0)]*mu_pt[mu1_index->at(0)]));
	mu2_PtErr_False->Fill(mu_ptErr[mu2_index->at(0)]/(mu_TunePRelPt[mu2_index->at(0)]*mu_pt[mu2_index->at(0)]));

	mu1_TkIso_False->Fill(mu_tkRelIso[mu1_index->at(0)]);
	mu2_TkIso_False->Fill(mu_tkRelIso[mu2_index->at(0)]);

	mu1_Dxy_False->Fill(mu_Dxy[mu1_index->at(0)]);
	mu2_Dxy_False->Fill(mu_Dxy[mu2_index->at(0)]);

	kappa_False->Fill(1000*mu_ch[mu1_index->at(0)]/(mu_TunePRelPt[mu1_index->at(0)]*mu_pt[mu1_index->at(0)]));
	kappa_False->Fill(1000*mu_ch[mu2_index->at(0)]/(mu_TunePRelPt[mu2_index->at(0)]*mu_pt[mu2_index->at(0)]));

      }
      */
    /*
    //Checking events with 2 good muon pairs selected
    if(mu1_index->size()>1){
      for(int j = 0; j < nZ; j++){
	if(mu1_index->at(1) == Z_mu1_idx->at(j)){
	  if(mu2_index->at(1) == Z_mu2_idx->at(j)){
	    selected_truth_mu2 = Z_truth->at(j);
	  }
	}
      }// Obtaining the Ztruth of the selected muon pair
      std::cout<<"Evento con 2 pares buenos seleccionados: "<<i<<std::endl;
      std::cout<<"\tMu1 Pair ==> Index1: "<<mu1_index->at(0)<<" Index2: "<<mu2_index->at(0)<<" Truth: "<<selected_truth<<" || Pt: "<<mu_pt[mu2_index->at(0)]<<" Eta: "<<mu_eta[mu2_index->at(0)]<<std::endl;
      std::cout<<"\tMu2 Pair ==> Index1: "<<mu1_index->at(1)<<" Index2: "<<mu2_index->at(1)<<" Truth: "<<selected_truth_mu2<<" || Pt: "<<mu_pt[mu2_index->at(1)]<<" Eta: "<<mu_eta[mu2_index->at(1)]<<std::endl;
    }
    */
    //}// Check muons when they dont pass selection

    // Check ZtoMuMu sample
    /*
    if(mu_genIdx[mu1_index] != -1 && mu_genIdx[mu2_index] != -1){
      if(genP_momIdx[mu_genIdx[mu1_index]] != -1 && genP_momIdx[mu_genIdx[mu2_index]] != -1){
	MomId1_T = genP_flavor[genP_momIdx[mu_genIdx[mu1_index]]];
	MomId2_T = genP_flavor[genP_momIdx[mu_genIdx[mu2_index]]];
	if( (abs(MomId1_T) != 23 || abs(MomId2_T) != 23) && (abs(MomId1_T) != 13 || abs(MomId2_T) != 13) ){
	  std::cout << "  Flavor of Mu1 Mom: " << MomId1_T << " // Flavor of Mu2 Mom: " << MomId2_T << std::endl;
	}
      }
    }
    */
  }// Loop over entries

  std::cout << std::endl;
  cout<<"Total events: "<<counter<<endl;

  TCanvas* c1 = new TCanvas();
  c1->cd();
  muonPt->Draw("hist");
  TCanvas* c2 = new TCanvas();
  c2->cd();
  muonPhi->Draw("hist");
  TCanvas* c3 = new TCanvas();
  c3->cd();
  muonDxy->Draw("hist");
  TCanvas* c4 = new TCanvas();
  c4->cd();
  muonDz->Draw("hist");
  TCanvas* c5 = new TCanvas();
  c5->cd();
  muonNstat->Draw("hist");

























  
  /*
  TCanvas* mZcanv = new TCanvas();
  mZcanv->cd();
  mZhisto->Draw();
  //mZcanv->Print("png/mZ_M-50to120.png");

  TCanvas* ptZcanv = new TCanvas();
  ptZcanv->cd();
  ptZhisto->Draw();
  //ptZcanv->Print("png/ptZ_M-50to120.png");

  TCanvas* ptZvsEtaZcanv = new TCanvas();
  ptZvsEtaZcanv->cd();
  ptZvsEtaZ->Draw("colz");
  //ptZvsEtaZcanv->Print("png/HTchecks/ptZvsEtaZ_2500toInf.png");
  //ptZvsEtaZcanv->SaveAs("png/HTchecks/ptZvsEtaZ_2500toInf.root");
  */
  /* 
  TCanvas* m1_TunePt = new TCanvas();
  m1_TunePt->cd();
  mu1_TunePpt_True->SetLineColor(kBlue+1);
  mu1_TunePpt_False->SetLineColor(kRed);
  mu1_TunePpt_True->Scale(1/mu1_TunePpt_True->Integral());
  mu1_TunePpt_False->Scale(1/mu1_TunePpt_False->Integral());
  mu1_TunePpt_True->Draw("hist");
  mu1_TunePpt_False->Draw("same hist");
  m1_TunePt->Print("png/mu1_TunePpt_pass.png");
  TCanvas* m2_TunePt = new TCanvas();
  m2_TunePt->cd();
  mu2_TunePpt_True->SetLineColor(kBlue+1);
  mu2_TunePpt_False->SetLineColor(kRed);
  mu2_TunePpt_True->Scale(1/mu2_TunePpt_True->Integral());
  mu2_TunePpt_False->Scale(1/mu2_TunePpt_False->Integral());
  mu2_TunePpt_True->Draw("hist");
  mu2_TunePpt_False->Draw("same hist");
  m2_TunePt->Print("png/mu2_TunePpt_pass.png");

  TCanvas* m1_isHighPt = new TCanvas();
  m1_isHighPt->cd();
  mu1_isHighPt_True->SetLineColor(kBlue+1);
  mu1_isHighPt_False->SetLineColor(kRed);
  mu1_isHighPt_True->Scale(1/mu1_isHighPt_True->Integral());
  mu1_isHighPt_False->Scale(1/mu1_isHighPt_False->Integral());
  mu1_isHighPt_True->Draw("hist");
  mu1_isHighPt_False->Draw("same hist");
  m1_isHighPt->Print("png/mu1_isHighPt_pass.png");
  TCanvas* m2_isHighPt = new TCanvas();
  m2_isHighPt->cd();
  mu2_isHighPt_True->SetLineColor(kBlue+1);
  mu2_isHighPt_False->SetLineColor(kRed);
  mu2_isHighPt_True->Scale(1/mu2_isHighPt_True->Integral());
  mu2_isHighPt_False->Scale(1/mu2_isHighPt_False->Integral());
  mu2_isHighPt_True->Draw("hist");
  mu2_isHighPt_False->Draw("same hist");
  m2_isHighPt->Print("png/mu2_isHighPt_pass.png");

  TCanvas* m1_eta = new TCanvas();
  m1_eta->cd();
  mu1_eta_True->SetLineColor(kBlue+1);
  mu1_eta_False->SetLineColor(kRed);
  mu1_eta_True->Scale(1/mu1_eta_True->Integral());
  mu1_eta_False->Scale(1/mu1_eta_False->Integral());
  mu1_eta_True->Draw("hist");
  mu1_eta_False->Draw("same hist");
  m1_eta->Print("png/mu1_eta_pass.png");
  TCanvas* m2_eta = new TCanvas();
  m2_eta->cd();
  mu2_eta_True->SetLineColor(kBlue+1);
  mu2_eta_False->SetLineColor(kRed);
  mu2_eta_True->Scale(1/mu2_eta_True->Integral());
  mu2_eta_False->Scale(1/mu2_eta_False->Integral());
  mu2_eta_True->Draw("hist");
  mu2_eta_False->Draw("same hist");
  m2_eta->Print("png/mu2_eta_pass.png");

  TCanvas* m1_PtErr = new TCanvas();
  m1_PtErr->cd();
  mu1_PtErr_True->SetLineColor(kBlue+1);
  mu1_PtErr_False->SetLineColor(kRed);
  mu1_PtErr_True->Scale(1/mu1_PtErr_True->Integral());
  mu1_PtErr_False->Scale(1/mu1_PtErr_False->Integral());
  mu1_PtErr_True->Draw("hist");
  mu1_PtErr_False->Draw("same hist");
  m1_PtErr->Print("png/mu1_PtErr_pass.png");
  TCanvas* m2_PtErr = new TCanvas();
  m2_PtErr->cd();
  mu2_PtErr_True->SetLineColor(kBlue+1);
  mu2_PtErr_False->SetLineColor(kRed);
  mu2_PtErr_True->Scale(1/mu2_PtErr_True->Integral());
  mu2_PtErr_False->Scale(1/mu2_PtErr_False->Integral());
  mu2_PtErr_True->Draw("hist");
  mu2_PtErr_False->Draw("same hist");
  m2_PtErr->Print("png/mu2_PtErr_pass.png");

  TCanvas* m1_TkIso = new TCanvas();
  m1_TkIso->cd();
  mu1_TkIso_True->SetLineColor(kBlue+1);
  mu1_TkIso_False->SetLineColor(kRed);
  mu1_TkIso_True->Scale(1/mu1_TkIso_True->Integral());
  mu1_TkIso_False->Scale(1/mu1_TkIso_False->Integral());
  mu1_TkIso_True->Draw("hist");
  mu1_TkIso_False->Draw("same hist");
  m1_TkIso->Print("png/mu1_TkIso_pass.png");
  TCanvas* m2_TkIso = new TCanvas();
  m2_TkIso->cd();
  mu2_TkIso_True->SetLineColor(kBlue+1);
  mu2_TkIso_False->SetLineColor(kRed);
  mu2_TkIso_True->Scale(1/mu2_TkIso_True->Integral());
  mu2_TkIso_False->Scale(1/mu2_TkIso_False->Integral());
  mu2_TkIso_True->Draw("hist");
  mu2_TkIso_False->Draw("same hist");
  m2_TkIso->Print("png/mu2_TkIso_pass.png");

  TCanvas* m1_Dxy = new TCanvas();
  m1_Dxy->cd();
  mu1_Dxy_True->SetLineColor(kBlue+1);
  mu1_Dxy_False->SetLineColor(kRed);
  mu1_Dxy_True->Scale(1/mu1_Dxy_True->Integral());
  mu1_Dxy_False->Scale(1/mu1_Dxy_False->Integral());
  mu1_Dxy_True->Draw("hist");
  mu1_Dxy_False->Draw("same hist");
  m1_Dxy->Print("png/mu1_Dxy_pass.png");
  TCanvas* m2_Dxy = new TCanvas();
  m2_Dxy->cd();
  mu2_Dxy_True->SetLineColor(kBlue+1);
  mu2_Dxy_False->SetLineColor(kRed);
  mu2_Dxy_True->Scale(1/mu2_Dxy_True->Integral());
  mu2_Dxy_False->Scale(1/mu2_Dxy_False->Integral());
  mu2_Dxy_True->Draw("hist");
  mu2_Dxy_False->Draw("same hist");
  m2_Dxy->Print("png/mu2_Dxy_pass.png");
  */
  /*
  TCanvas* kappa = new TCanvas();
  kappa->cd();
  kappa->SetLogy();
  kappa_True->SetLineColor(kBlue+1);
  kappa_True->SetLineWidth(1);
  kappa_True->SetFillColor(kBlue);
  kappa_True->SetFillStyle(3001);
  kappa_False->SetLineColor(kRed+1);
  kappa_False->SetLineWidth(1);
  kappa_False->SetFillColor(kRed);
  kappa_False->SetFillStyle(3001);
  kappa_True->Draw("hist");
  kappa_False->Draw("same hist");
  kappa->Print("png/kappa_pass.png");
  */
  /*
  TCanvas* kappa = new TCanvas();
  kappa->cd();
  kappa->SetLogy();
  kappa_DiMu->SetMinimum(0.1);
  kappa_DiMu->SetLineColor(kBlue+1);
  kappa_DiMu->SetLineWidth(1);
  kappa_DiMu->SetFillColor(kBlue);
  kappa_DiMu->SetFillStyle(3001);
  //kappa_DiMu->Draw("hist");
  //kappa->Print("png/kappa_Zmumu.png");
  */
  /*
  TCanvas* c1 = new TCanvas();
  NoPass_TunePpt->Draw();
  c1->Print("png/NoPass_TunePpt.png");
  TCanvas* c2 = new TCanvas();
  c2->cd();
  NoPass_isHighPt->Draw();
  c2->Print("png/NoPass_isHighPt.png");
  TCanvas* c3 = new TCanvas();
  c3->cd();
  NoPass_eta->Draw();
  c3->Print("png/NoPass_eta.png");
  TCanvas* c4 = new TCanvas();
  c4->cd();
  NoPass_PtErr->Draw();
  c4->Print("png/NoPass_PtErr.png");
  TCanvas* c5 = new TCanvas();
  c5->cd();
  NoPass_TkIso->Draw();
  c5->Print("png/NoPass_TkIso.png");
  TCanvas* c6 = new TCanvas();
  c6->cd();
  NoPass_Dxy->Draw();
  c6->Print("png/NoPass_Dxy.png");
  */

  /* PLOTTING */ 
  /*
  TCanvas* c3 = new TCanvas();
  gStyle->SetOptStat(0);
  gStyle->SetOptTitle(0);
  gStyle->SetHatchesSpacing(0.2);
  gStyle->SetHatchesLineWidth(1.0);

  Top_Mass_True->SetLineColor(kAzure-1);
  Top_Mass_True->SetLineWidth(1);
  Top_Mass_True->SetFillColor(kAzure);
  Top_Mass_True->SetFillStyle(3001);
  Top_Mass_False->SetLineColor(kRed+1);
  Top_Mass_False->SetLineWidth(1);
  Top_Mass_False->SetFillColor(kRed);
  Top_Mass_False->SetFillStyle(3001);
  Top_Mass_JetMatch->SetLineColor(kGreen+2);
  Top_Mass_JetMatch->SetLineWidth(1);
  Top_Mass_JetMatch->SetFillColor(kGreen+1);
  Top_Mass_JetMatch->SetFillStyle(3001);
  Top_Mass_LepMatch->SetLineColor(14);
  Top_Mass_LepMatch->SetLineWidth(1);
  Top_Mass_LepMatch->SetFillColor(15); // (920)
  Top_Mass_LepMatch->SetFillStyle(3001);
  Top_Mass_Comb->SetLineColor(kYellow+1);
  Top_Mass_Comb->SetLineWidth(1);
  Top_Mass_Comb->SetFillColor(5);
  Top_Mass_Comb->SetFillStyle(3001);
 
  float hmax = 1.1*Top_Mass_True->GetMaximum();   
  Top_Mass_True->SetMaximum(hmax);
  Top_Mass_True->SetTitle("");
  Top_Mass_True->GetXaxis()->SetTitle("#lower[-0.15]{m}_{#kern[0.25]{#lower[-0.2]{t}}}  (GeV)");
  Top_Mass_True->GetXaxis()->SetTitleSize(Top_Mass_True->GetXaxis()->GetTitleSize()*1.15);
  Top_Mass_True->GetXaxis()->SetLabelSize(Top_Mass_True->GetXaxis()->GetLabelSize()*1.1);
  Top_Mass_True->GetYaxis()->SetTitle("events / 10 GeV^{-1}");
  Top_Mass_True->GetYaxis()->SetMaxDigits(3);

  Top_Mass_True->Draw("hist");
  Top_Mass_LepMatch->Draw("same hist");
  Top_Mass_False->Draw("same hist");
  Top_Mass_JetMatch->Draw("same hist");
  Top_Mass_Comb->Draw("same hist");
 
  TLegend* leg = new TLegend(0.66,0.58,0.89,0.90);
  leg->SetBorderSize(0);
  leg->SetFillStyle(0);
  leg->SetFillColor(0);
  leg->AddEntry(Top_Mass_True,"True Top","f");
  leg->AddEntry(Top_Mass_False,"False Top","f");
  leg->AddEntry(Top_Mass_JetMatch,"JetMatch Top","f");
  leg->AddEntry(Top_Mass_LepMatch,"LepMatch Top","f");
  leg->AddEntry(Top_Mass_Comb,"Comb Top","f");
  leg->Draw();

  //c3->Print("plots/StdCuts/TopM_El_Resolved_StdCut.pdf");
  //c3->Print("plots/StdCuts/TopM_El_Resolved_StdCut.png");

  Float_t S = Top_Mass_True->Integral();
  Float_t False = Top_Mass_False->Integral();
  Float_t JM = Top_Mass_JetMatch->Integral();
  Float_t LM = Top_Mass_LepMatch->Integral();
  Float_t Comb = Top_Mass_Comb->Integral();
  Float_t B = False + JM + LM + Comb;
  Float_t SIG = sqrt(2*((S+B)*log(1+S/B)-S));
  Float_t Relative = 100*S/(S+B);
  cout<<"Sig.: "<<SIG<<endl;
  cout<<"Rel.: "<<Relative<<" % "<<endl;
  cout<<"# Signal: "<<S<<endl;
  cout<<"# Background: "<<B<<endl;
  */
}// End of main 

void dataChecks(){
 
  plotChecks("/eos/user/d/diegof/cmt/MergeCategorization/Wprime_2022_config/ReReco_2022_C_Muon/cat_preselection/preliminary1/data_0.root","ok.root",0);

}


