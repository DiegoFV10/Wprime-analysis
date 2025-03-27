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

void ComputeMisReco(TString filesDir, TString rootname){

  TSystemDirectory dir(filesDir, filesDir);
  TList* files = dir.GetListOfFiles();

  // Initial flat 5% resolution
  float resolution = 0.05;

  if (files) {
    TIter next(files);
    TObject* obj;

    while ((obj = next())) {
      TString subDir = obj->GetName();

      if (subDir.BeginsWith("QCD_Pt")) {
	TString filePath = filesDir + subDir + rootname;
                
	// Open rootfile
	TFile* file = TFile::Open(filePath);

	TTree* tree = (TTree*)file->Get("Events");
	int nEntries = tree->GetEntries();

	int size_max  = 30;
	int size_max2 = 300;
	
	// Define variables
	Float_t Muon_pt[size_max];
	Float_t Muon_tunepRelPt[size_max];
	Float_t Muon_eta[size_max];
	Float_t Muon_phi[size_max];
	Bool_t Muon_isHP[size_max];
	int muIdx;
	Float_t MET_pt;
	Double_t TypeIMET_pt;
	Double_t CorrMET_pt;
	Float_t GenPart_pt[size_max2];
	Float_t GenPart_eta[size_max2];
	Float_t GenPart_phi[size_max2];
	Int_t GenPart_pdgId[size_max2];
	Int_t GenPart_status[size_max2];
	int nGenPart;

	// Read branches
	tree->SetBranchAddress("Muon_pt", &Muon_pt);
	tree->SetBranchAddress("Muon_tunepRelPt", &Muon_tunepRelPt);
	tree->SetBranchAddress("Muon_eta", &Muon_eta);
	tree->SetBranchAddress("Muon_phi", &Muon_phi);
	tree->SetBranchAddress("Muon_highPurity", &Muon_isHP);
	tree->SetBranchAddress("goodMuIdx", &muIdx);

	tree->SetBranchAddress("PuppiMET_pt", &MET_pt);
	tree->SetBranchAddress("TypeICorrMET_pt", &TypeIMET_pt);
	tree->SetBranchAddress("CorrMET_pt", &CorrMET_pt);

	tree->SetBranchAddress("GenPart_pt", &GenPart_pt);
	tree->SetBranchAddress("GenPart_eta", &GenPart_eta);
	tree->SetBranchAddress("GenPart_phi", &GenPart_phi);
	tree->SetBranchAddress("GenPart_pdgId", &GenPart_pdgId);
	tree->SetBranchAddress("GenPart_status", &GenPart_status);
	tree->SetBranchAddress("nGenPart", &nGenPart);

	// Define histograms to plot
	TH1F* muonDeltaPt = new TH1F("muonDeltaPt", "", 40, 0, 2000);
	TH1F* muonRecoPt = new TH1F("muonRecoPt", "", 40, 0, 4000);
	TH1F* muonGenPt = new TH1F("muonGenPt", "", 40, 0, 4000);
	TH2F* muHPvsPt = new TH2F("muHPvsPt", "", 40, 0, 4000, 2, 0, 2);
	TH2F* muHPvsDeltaPt = new TH2F("muHPvsDeltaPt", "", 30, 0, 3000, 2, 0, 2);

	TH1F* TypeIvsCorrMET = new TH1F("TypeIvsCorrMET", "", 100, 0, 200);

	cout << "Reading file " << filePath << " with " << nEntries << " entries" << endl;

	int counter = 0;
	int counter2 = 0;
	
	for (int i = 0; i < nEntries; i++) {
	  tree->GetEntry(i);
	  
	  if(i % 100 == 0)
	    std::cout << "[QCDmisReco.cpp] processed : " << i << " entries\r" << std::flush;

	  for (int iGen = 0; iGen < nGenPart; iGen++){

	    if (abs(GenPart_pdgId[iGen]) == 13 && GenPart_status[iGen] == 1 && deltaR(Muon_eta[muIdx], GenPart_eta[iGen], Muon_phi[muIdx], GenPart_phi[iGen]) < 0.03){
	      float deltaPt = fabs(Muon_pt[muIdx] - GenPart_pt[iGen]);
	      
	      if (deltaPt > 3*resolution*GenPart_pt[iGen]){
		muonDeltaPt->Fill(deltaPt);
		muonRecoPt->Fill(Muon_pt[muIdx]);
		muonGenPt->Fill(GenPart_pt[iGen]);
		muHPvsPt->Fill(Muon_pt[muIdx], Muon_isHP[muIdx]);
		muHPvsDeltaPt->Fill(deltaPt, Muon_isHP[muIdx]);
		counter++;
	      }
	      break;
	    } // Match reco - gen
	    
	  } // Loop over Gen Particles

	  TypeIvsCorrMET->Fill(fabs(TypeIMET_pt - CorrMET_pt));

	} // Loop over entries

	/*
	TCanvas* dPt = new TCanvas();
	dPt->SetLogy();
	muonDeltaPt->Draw("hist");
	//dPt->SaveAs("plots/QCDmisreco/"+subDir+"_misreco.png");

	TCanvas* muPt = new TCanvas();
	muPt->Divide(2,1);
	muPt->cd(1);
	gPad->SetLogy();
	muonRecoPt->Draw("hist");
	muPt->cd(2);
	gPad->SetLogy();
	muonGenPt->Draw("hist");
	//muPt->SaveAs("plots/QCDmisreco/"+subDir+"_reco-gen-pt.png");
	
	TCanvas* HPvsPt = new TCanvas();
	muHPvsPt->Draw("COLZ");
	//HPvsPt->SaveAs("plots/QCDmisreco/"+subDir+"_HPvsPt.png");

	TCanvas* HPvsDeltaPt = new TCanvas();
	muHPvsDeltaPt->Draw("COLZ");
	//HPvsDeltaPt->SaveAs("plots/QCDmisreco/"+subDir+"_HPvsDeltaPt.png");
	*/
	TCanvas* dMET = new TCanvas();
	dMET->SetLogy();
	TypeIvsCorrMET->Draw("hist");
	dMET->SaveAs("plots/QCDmisreco/"+subDir+"_deltaMET.png");
	
	cout << " # of muons with miss-reco pT for file " << filePath << " --> " << counter << endl;
	cout << "    relative for file " << filePath << " --> " << counter/(float)nEntries << endl;

	file->Close();
      }
    }
  }



}


void QCDmisReco(){

  ComputeMisReco("/eos/user/d/diegof/cmt/MergeCategorization/Wprime_2022_config/", "/cat_preselection/QCD_studies/data_0.root");
  //ComputeMisReco("/eos/user/d/diegof/cmt/MergeCategorization/Wprime_2022_config/", "/cat_preselection/METcorrTuneP/data_0.root");
  
}


