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


void plotChecks(string filename, string selection){
    
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
  Float_t mu_Dxyerr[size_max];      chain.SetBranchAddress("Muon_dxyErr",&mu_Dxyerr);
  Float_t mu_Dz[size_max];          chain.SetBranchAddress("Muon_dz",&mu_Dz);
  Float_t mu_Dxy[size_max];         chain.SetBranchAddress("Muon_dxy",&mu_Dxy);
  Float_t mu_Iso04[size_max];       chain.SetBranchAddress("Muon_pfRelIso04_all",&mu_Iso04);
  UChar_t mu_nStations[size_max];   chain.SetBranchAddress("Muon_nStations",&mu_nStations);

  Float_t MET_pt =                  chain.SetBranchAddress("MET_pt",&MET_pt);
  Float_t MET_phi =                 chain.SetBranchAddress("MET_phi",&MET_phi);
  Float_t PuppiMET_pt =             chain.SetBranchAddress("PuppiMET_pt", &PuppiMET_pt);
  Float_t PuppiMET_phi =            chain.SetBranchAddress("PuppiMET_phi", &PuppiMET_phi);
  Double_t TypeIMET_pt =            chain.SetBranchAddress("TypeICorrMET_pt",&TypeIMET_pt);
  Double_t TypeIMET_phi =           chain.SetBranchAddress("TypeICorrMET_phi",&TypeIMET_phi);

  Int_t nJet =                           chain.SetBranchAddress("nJet",&nJet);
  Float_t jet_pt[size_max];              chain.SetBranchAddress("Jet_pt",&jet_pt);
  Float_t jet_mass[size_max];            chain.SetBranchAddress("Jet_mass",&jet_mass);
  Float_t jet_phi[size_max];             chain.SetBranchAddress("Jet_phi",&jet_phi);
  Float_t jet_eta[size_max];             chain.SetBranchAddress("Jet_eta",&jet_eta);
  UChar_t jet_jetId[size_max];           chain.SetBranchAddress("Jet_jetId",&jet_jetId);
  Float_t jet_deepBTag[size_max];        chain.SetBranchAddress("Jet_btagDeepFlavB",&jet_deepBTag);
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
  Int_t elIdx =                     chain.SetBranchAddress("goodElIdx",&elIdx);

  Double_t mT =                     chain.SetBranchAddress("mT",&mT);

  UChar_t nVertices =               chain.SetBranchAddress("PV_npvsGood", &nVertices);

  /// Define histograms to plot ///
  TH1F* elePt     = new TH1F("elePt", "", 20, 0, 2000);
  TH1F* eleEta    = new TH1F("eleEta", "", 20, -2.5, 2.5);
  TH1F* elePhi    = new TH1F("elePhi", "", 20, -3.2, 3.2);
  TH1I* nVert     = new TH1I("nVertices", "", 80, 0, 80);
  TH1F* muonPt    = new TH1F("muonPt", "", 18, 200, 2000);
  TH1F* muonPt2   = new TH1F("muonPt2", "", 18, 200, 2000);
  TH1F* muPtOverMET = new TH1F("muPtOverMET", "", 9, 0.4, 1.5);
  TH1F* dPhiMuMET = new TH1F("dPhiMuMET", "", 8, 2.4, 3.2);
  TH1F* muonEta   = new TH1F("muonEta", "", 20, -2.5, 2.5);
  TH1F* muonPhi   = new TH1F("muonPhi", "", 20, -3.2, 3.2);
  TH1I* numberMuon = new TH1I("numberMuon", "", 12, 0, 12);
  TH1I* muonCharge = new TH1I("muonCharge", "", 3, -1, 2);
  TH1I* muonHP    = new TH1I("muonHP", "", 2, 0, 2);
  TH1I* muonIndex = new TH1I("muonIndex", "", 4, 0, 4);
  TH1F* MET       = new TH1F("MET", "", 20, 200, 2000);
  TH1F* METphi    = new TH1F("METphi", "", 20, -3.2, 3.2);
  TH1F* jetEta    = new TH1F("jetEta", "", 20, -2.5, 2.5);
  TH1F* jetPhi    = new TH1F("jetPhi", "", 20, -3.2, 3.2);

  TH2F* eleEtaPhi = new TH2F("eleEtaPhi", "", 20, -2.5, 2.5, 20, -3.2, 3.2);
  TH2F* jetEtaPhi = new TH2F("jetEtaPhi", "", 20, -2.5, 2.5, 20, -3.2, 3.2);
  TH2F* muonEtaJetEta = new TH2F("muonEtaJetEta", "", 20, -2.5, 2.5, 20, -3.2, 3.2);
  TH2F* muonEtaEleEta = new TH2F("muonEtaEleEta", "", 20, -2.5, 2.5, 20, -3.2, 3.2);
  
  int counter = 0;
  
  for(int i = 0; i < nentries; i++){

    chain.GetEntry(i);

    //if(i % 100 == 0) 
    //  std::cout << "[Data2022excess_check.cpp] processed : " << i << " entries\r" << std::flush;

    if (el_pt[elIdx] >= 700 && el_pt[elIdx] <= 1000){// && mu_eta[elIdx] >= 0.5 && mu_eta[elIdx] <= 1.25){

      counter ++;
      cout << "Event " << i << " run:lumi:event --> " << run << ":" << luminosityBlock << ":" << event << endl;

      elePt->Fill(el_pt[elIdx]);
      eleEta->Fill(el_eta[elIdx]);
      elePhi->Fill(el_phi[elIdx]);
      nVert->Fill(nVertices);

      eleEtaPhi->Fill(el_eta[elIdx], el_phi[elIdx]);
      
      //cout << "Muon ==> pt: " << mu_pt[elIdx] << "  TuneP: " << mu_TunePRelPt[elIdx] << "  eta: " << mu_eta[elIdx] << "  phi: " << mu_phi[elIdx] << endl;
      //cout << "MET ==> pt: " << CorrMET_pt << "  phi: " << CorrMET_phi << endl;
      //for (int m = 0; m < nMuon; m++){
      //	cout << "Event #" << counter << " --> Run:Lumi:Event " << run << ":" << luminosityBlock << ":" << event << " HighPtId: "<< (int)mu_HighPtId[m] << " LooseId: "<< mu_isLoose[m] << " Muon eta: "<< mu_eta[m] << " Muon phi: "<< mu_phi[m] << " Muon pt: "<< mu_pt[m] << " Muon tuneP: "<< mu_TunePRelPt[m] <<  endl;
      //}
	
      if(selection == "presel") {
	for (int j = 0; j < nJet; j++){
	
	  jetEta->Fill(jet_eta[j]);
	  jetPhi->Fill(jet_phi[j]);

	  jetEtaPhi->Fill(jet_eta[j], jet_phi[j]);
	  muonEtaJetEta->Fill(el_eta[elIdx], jet_eta[j]);

	} // Loop over jets
      } else {
	for (size_t j = 0; j < goodJets_corr->size(); j++){
	
	  jetEta->Fill(jet_eta[goodJets_corr->at(j)]);
	  jetPhi->Fill(jet_phi[goodJets_corr->at(j)]);

	  jetEtaPhi->Fill(jet_eta[goodJets_corr->at(j)], jet_phi[goodJets_corr->at(j)]);
	  muonEtaJetEta->Fill(el_eta[elIdx], jet_eta[goodJets_corr->at(j)]);

	} // Loop over jets
      }
      /// Poner aqui los muones ///
      /*
      muonPt->Fill(mu_pt[muIdx]*mu_TunePRelPt[muIdx]);
      if (mu_eta[muIdx] >= 0.5 && mu_eta[muIdx] <= 1.25) muonPt2->Fill(mu_pt[muIdx]*mu_TunePRelPt[muIdx]);
      muPtOverMET->Fill(mu_pt[muIdx]*mu_TunePRelPt[muIdx]/CorrMET_pt);
      dPhiMuMET->Fill(acos(cos(mu_phi[muIdx] - CorrMET_phi)));
      muonTuneP->Fill(mu_TunePRelPt[muIdx]);
      muonEta->Fill(mu_eta[muIdx]);
      muonPhi->Fill(mu_phi[muIdx]);
      muonPtErr->Fill(mu_ptErr[muIdx]);
      muonIso->Fill(mu_tkRelIso[muIdx]);
      MET->Fill(CorrMET_pt);
      METphi->Fill(CorrMET_phi);
      numberMuon->Fill(nMuon);
      muonCharge->Fill(mu_ch[muIdx]);
      muonHP->Fill(mu_isHP[muIdx]);
      muonIndex->Fill(muIdx);
      */
      
    } // Check problematic events

    //cout << "Event " << i << " run:lumi:event --> " << run << ":" << luminosityBlock << ":" << event << endl;
    
  } // Loop over entries

  cout << "Found " << counter << " events above mT threshold" << endl;

/*
  TCanvas* c1 = new TCanvas();
  c1->cd();
  muonPt->Draw("hist");
  TCanvas* c1p1 = new TCanvas();
  c1p1->cd();
  muonPt2->Draw("hist");
  TCanvas* c1p2 = new TCanvas();
  c1p2->cd();
  muPtOverMET->Draw("hist");
  TCanvas* c1p3 = new TCanvas();
  c1p3->cd();
  dPhiMuMET->Draw("hist");
  //TCanvas* c2 = new TCanvas();
  //c2->cd();
  //muonTuneP->Draw("hist");
  TCanvas* c3 = new TCanvas();
  c3->cd();
  muonEta->GetXaxis()->SetTitle("#mu #eta");
  muonEta->Draw("hist");
  //c3->SaveAs("plots/Data2022excess/muon_eta_mT1000.png");
  TCanvas* c4 = new TCanvas();
  c4->cd();
  muonPhi->GetXaxis()->SetTitle("#mu #phi  (rad)");
  muonPhi->Draw("hist");
*/
  //c4->SaveAs("plots/Data2022excess/muon_phi_mT1000.png");
  //TCanvas* c5 = new TCanvas();
  //c5->cd();
  //MET->Draw("hist");
  //TCanvas* c6 = new TCanvas();
  //c6->cd();
  //METphi->Draw("hist");
  //TCanvas* c7 = new TCanvas();
  //c7->cd();
  //muonPtErr->Draw("hist");
  //TCanvas* c8 = new TCanvas();
  //c8->cd();
  //muonIso->Draw("hist");
  //TCanvas* c9 = new TCanvas();
  //c9->cd();
  //jetEta->Draw("hist");
  //TCanvas* c10 = new TCanvas();
  //c10->cd();
  //jetPhi->Draw("hist");
  //TCanvas* c11 = new TCanvas();
  //c11->cd();
  //numberMuon->Draw("hist");
  //TCanvas* c12 = new TCanvas();
  //c12->cd();
  //eleEta->Draw("hist");
  //TCanvas* c13 = new TCanvas();
  //c13->cd();
  //elePhi->Draw("hist");
  //TCanvas* c14 = new TCanvas();
  //c14->cd();
  //eleHEEP->Draw("hist");
  //TCanvas* c15 = new TCanvas();
  //c15->cd();
  //muonCharge->Draw("hist");
  //TCanvas* c16 = new TCanvas();
  //c16->cd();
  //muonHP->Draw("hist");
  //TCanvas* c17 = new TCanvas();
  //c17->cd();
  //muonIndex->Draw("hist");

  TCanvas* c1 = new TCanvas();
  c1->cd();
  elePt->Draw("hist");
  c1->SaveAs("plots/Data2022excess/electron/ele_pT_pT-700.png");
  TCanvas* c2 = new TCanvas();
  c2->cd();
  eleEta->Draw("hist");
  c2->SaveAs("plots/Data2022excess/electron/ele_eta_pT-700.png");
  TCanvas* c3 = new TCanvas();
  c3->cd();
  elePhi->Draw("hist");
  c3->SaveAs("plots/Data2022excess/electron/ele_phi_pT-700.png");
  TCanvas* c18 = new TCanvas();
  c18->cd();
  nVert->Draw("hist");
  //c18->SaveAs("plots/Data2022excess/electron/nVert_pT-700.root");
  

  TCanvas* c21 = new TCanvas();
  c21->cd();
  eleEtaPhi->GetXaxis()->SetTitle("e #eta");
  eleEtaPhi->GetYaxis()->SetTitle("e #phi  (rad)");
  eleEtaPhi->Draw("COLZ");
  c21->SaveAs("plots/Data2022excess/electron/ele_eta-phi_pT-700.png");
  //TCanvas* c22 = new TCanvas();
  //c22->cd();
  //jetEtaPhi->Draw("COLZ");
  //if (selection == "presel")
  //  c22->SaveAs("plots/Data2022excess/jet_etaVSphi_mT1000_presel.png");
  //else
  //  c22->SaveAs("plots/Data2022excess/jet_etaVSphi_mT1000.png");
  //TCanvas* c23 = new TCanvas();
  //c23->cd();
  //muonEtaJetEta->Draw("COLZ");
  //TCanvas* c24 = new TCanvas();
  //c24->cd();
  //muonEtaEleEta->Draw("COLZ");

  
} // End of main 

void Data2022excess_checkElectrons(){

  plotChecks("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/bin/txt/postEE_excessCheck_electron.txt", "kinsel");

}


