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
#include <TCanvas.h>
#include <TPad.h>
#include <TLegend.h>
#include <TLine.h>

void DrawNormalizedRatio(TH1* h1, TH1* h2, string cname = "c_ratio", string label="", bool savePlots=false) {
  gStyle->SetOptStat(0);
  
  if (!h1 || !h2) {
    std::cerr << "Error: histograms not valid!" << std::endl;
    return;
  }

  // Clonar para no modificar los originales
  TH1* h1_norm = (TH1*)h1->Clone("h1_norm");
  TH1* h2_norm = (TH1*)h2->Clone("h2_norm");

  // Normalización a área 1
  if (h1_norm->Integral() != 0) h1_norm->Scale(1.0 / h1_norm->Integral());
  if (h2_norm->Integral() != 0) h2_norm->Scale(1.0 / h2_norm->Integral());

  // Crear canvas con dos pads
  TCanvas* c = new TCanvas(cname.c_str(), cname.c_str(), 602,676);
  c->cd();
  c->Draw();
  
  TPad* up = new TPad("","",0.0,0.36,1.0,1.0);
  TPad* down = new TPad("","",0.0,0.0,1.0,0.36);
  up->SetTopMargin(0.13);
  up->SetBottomMargin(0.0);
  up->Draw("SAME");
  down->SetTopMargin(0.0);
  down->SetBottomMargin(0.35);
  down->Draw("SAME");

  // ----- Parte superior -----
  float xlow = h1->GetXaxis()->GetXmin();
  float xup = h1->GetXaxis()->GetXmax();
  
  up->cd();
  h1->SetLineColor(1);
  h1->SetLineWidth(2);
  h1->GetYaxis()->SetTitle("Events");
  h2->SetLineColor(2);
  h2->SetLineWidth(2);

  h1->Draw("HIST");
  h2->Draw("HIST SAME");

  TLegend* leg = new TLegend(0.55,0.7,0.88,0.88);
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetTextSize(0.034);
  leg->AddEntry(h1, "500 GeV #leq p_{T}^{#mu} < 700 GeV", "l");
  leg->AddEntry(h2, "700 GeV #leq p_{T}^{#mu} #leq 1000 GeV", "l");
  leg->Draw("SAME");

  // ----- Parte inferior (ratio) -----
  down->cd();
  TH1F* ratio = (TH1F*)h2_norm->Clone("ratio");
  ratio->Divide(h1_norm);

  auto frame = down->DrawFrame(xlow, 0.0, xup, 2.0);
  frame->GetYaxis()->SetTitle("high / ref.");
  frame->GetYaxis()->SetTitleSize(h1_norm->GetYaxis()->GetTitleSize()*2.0);
  frame->GetYaxis()->SetTitleOffset(0.6);
  frame->GetYaxis()->CenterTitle(true);
  frame->GetYaxis()->SetLabelSize(h1_norm->GetYaxis()->GetLabelSize()*1.9);
  frame->GetYaxis()->SetNdivisions(304);
  frame->GetXaxis()->SetTitle(label.c_str());
  frame->GetXaxis()->SetTickLength(h1_norm->GetYaxis()->GetTickLength()*1.8);
  frame->GetXaxis()->SetTitleSize(h1_norm->GetXaxis()->GetTitleSize()*2.4);
  frame->GetXaxis()->SetTitleOffset(1.2);
  frame->GetXaxis()->SetLabelSize(h1_norm->GetXaxis()->GetLabelSize()*1.9);

  ratio->SetLineColor(1);
  ratio->SetLineWidth(2);
  ratio->SetFillStyle(0);
  ratio->Draw("HIST SAME");

  TLine* lmid = new TLine(xlow, 1.0, xup, 1.0);
  lmid->SetLineStyle(3);
  lmid->Draw("SAME");
  TLine* lbot = new TLine(xlow, 0.5, xup, 0.5);
  lbot->SetLineStyle(3);
  lbot->Draw("SAME");
  TLine* ltop = new TLine(xlow, 1.5, xup, 1.5);
  ltop->SetLineStyle(3);
  ltop->Draw("SAME");

  c->cd();
  c->Update();

  if(savePlots)
    c->SaveAs(("plots/Data2022excess/lastPlotsPreApp/"+ cname +"_2022.png").c_str());
  
}



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
  
  const int size_max = 300;
  const int size_max2 = 1000;

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

  UChar_t nVertices =               chain.SetBranchAddress("PV_npvsGood", &nVertices);
  Float_t PV_z =                    chain.SetBranchAddress("PV_z", &PV_z);

  /// Define histograms to plot ///
  TH1F* muonPt_ref    = new TH1F("muonPt_ref", "", 12, 500, 800);
  TH1F* muonPt_high   = new TH1F("muonPt_high", "", 20, 700, 1100);
  //TH1F* muonTuneP = new TH1F("muonTuneP", "", 50, 0, 20);
  TH1F* muonEta_ref   = new TH1F("muonEta_ref", "", 25, -2.5, 2.5);
  TH1F* muonEta_high   = new TH1F("muonEta_high", "", 25, -2.5, 2.5);
  TH1F* muonPhi_ref   = new TH1F("muonPhi_ref", "", 32, -3.2, 3.2);
  TH1F* muonPhi_high   = new TH1F("muonPhi_high", "", 32, -3.2, 3.2);
  TH1I* muonNstat_ref = new TH1I("muonNstat_ref", "", 5, 0, 5);
  TH1I* muonNstat_high = new TH1I("muonNstat_high", "", 5, 0, 5);
  TH1F* hPV_z_ref     = new TH1F("hPV_z_ref", "", 20, -10, 10);
  TH1F* hPV_z_high     = new TH1F("hPV_z_high", "", 20, -10, 10);

  //TH2F* muonEtaPhi = new TH2F("muonEtaPhi", "", 20, -2.5, 2.5, 20, -3.2, 3.2);
 
  int counter_ref = 0;
  int counter_high = 0;
  
  for(int i = 0; i < nentries; i++){

    chain.GetEntry(i);

    double mT = sqrt( 2*mu_TunePRelPt[muIdx]*mu_pt[muIdx]*CorrMET_pt*(1.0 - cos(mu_phi[muIdx] - CorrMET_phi)) );

    // Events with pT in range [500, 700)
    if (mu_pt[muIdx]*mu_TunePRelPt[muIdx] >= 500 && mu_pt[muIdx]*mu_TunePRelPt[muIdx] < 700) {
      
      counter_ref ++;
      cout << "  run:lumi:event --> " << run << ":" << luminosityBlock << ":" << event << endl;

      muonPt_ref->Fill(mu_pt[muIdx]*mu_TunePRelPt[muIdx]);
      //muonTuneP->Fill(mu_TunePRelPt[muIdx]);
      muonEta_ref->Fill(mu_eta[muIdx]);
      muonPhi_ref->Fill(mu_phi[muIdx]);      
      muonNstat_ref->Fill(mu_nStations[muIdx]);
      hPV_z_ref->Fill(PV_z);

      //muonEtaPhi->Fill(mu_eta[muIdx], mu_phi[muIdx]); 
    }
    
    // Events with pT in range [700, 1000]
    if (mu_pt[muIdx]*mu_TunePRelPt[muIdx] >= 700 && mu_pt[muIdx]*mu_TunePRelPt[muIdx] <= 1000) {
      
      counter_high ++;
      cout << "  run:lumi:event --> " << run << ":" << luminosityBlock << ":" << event << endl;

      muonPt_high->Fill(mu_pt[muIdx]*mu_TunePRelPt[muIdx]);
      muonEta_high->Fill(mu_eta[muIdx]);
      muonPhi_high->Fill(mu_phi[muIdx]);      
      muonNstat_high->Fill(mu_nStations[muIdx]);
      hPV_z_high->Fill(PV_z);
      
    }
    
  } // Loop over entries

  cout << "Found " << counter_ref << " events between 500 <= pT < 700" << endl;
  cout << "Found " << counter_high << " events between 700 <= pT <= 1000" << endl;

  /*
  TCanvas* c1 = new TCanvas();
  c1->cd();
  muonPt_ref->GetXaxis()->SetTitle("#mu p_{T} (500 #leq p_{T}^{#mu} < 700) [GeV]");
  muonPt_ref->Draw("hist");
  //c1->SaveAs("plots/Data2022excess/muon_pT_pT-700_jets.png");
  TCanvas* c2 = new TCanvas();
  c2->cd();
  muonEta_ref->GetXaxis()->SetTitle("#mu #eta (500 #leq p_{T}^{#mu} < 700)");
  muonEta_ref->Draw("hist");
  //c2->SaveAs("plots/Data2022excess/muon_eta_pT-700_jets.png");
  TCanvas* c3 = new TCanvas();
  c3->cd();
  muonPhi_ref->GetXaxis()->SetTitle("#mu #phi (500 #leq p_{T}^{#mu} < 700) [rad]");
  muonPhi_ref->Draw("hist");
  //c3->SaveAs("plots/Data2022excess/muon_phi_pT-700_jets.png");
  TCanvas* c4 = new TCanvas();
  c4->cd();
  muonNstat_ref->GetXaxis()->SetTitle("#mu # Stations (500 #leq p_{T}^{#mu} < 700)");
  muonNstat_ref->Draw("hist");
  TCanvas* c5 = new TCanvas();
  c5->cd();
  hPV_z_ref->GetXaxis()->SetTitle("PV z (500 #leq p_{T}^{#mu} < 700)");
  hPV_z_ref->Draw("hist");

  TCanvas* c6 = new TCanvas();
  c6->cd();
  muonPt_high->GetXaxis()->SetTitle("#mu p_{T} (700 #leq p_{T}^{#mu} #leq 1000) [GeV]");
  muonPt_high->Draw("hist");
  //c6->SaveAs("plots/Data2022excess/muon_pT_pT-700_jets.png");
  TCanvas* c7 = new TCanvas();
  c7->cd();
  muonEta_high->GetXaxis()->SetTitle("#mu #eta (700 #leq p_{T}^{#mu} #leq 1000)");
  muonEta_high->Draw("hist");
  //c7->SaveAs("plots/Data2022excess/muon_eta_pT-700_jets.png");
  TCanvas* c8 = new TCanvas();
  c8->cd();
  muonPhi_high->GetXaxis()->SetTitle("#mu #phi (700 #leq p_{T}^{#mu} #leq 1000) [rad]");
  muonPhi_high->Draw("hist");
  //c8->SaveAs("plots/Data2022excess/muon_phi_pT-700_jets.png");
  TCanvas* c9 = new TCanvas();
  c9->cd();
  muonNstat_high->GetXaxis()->SetTitle("#mu # Stations (700 #leq p_{T}^{#mu} #leq 1000)");
  muonNstat_high->Draw("hist");
  TCanvas* c10 = new TCanvas();
  c10->cd();
  hPV_z_high->GetXaxis()->SetTitle("PV z (700 #leq p_{T}^{#mu} #leq 1000)");
  hPV_z_high->Draw("hist");
  */
  /*
  TCanvas* c_mupT = new TCanvas();
  c_mupT->cd();
  muonPt_ref->GetXaxis()->SetTitle("#mu p_{T} [GeV]");
  muonPt_ref->SetLineColor(1);
  muonPt_ref->Draw("hist");
  muonPt_high->SetLineColor(2);
  muonPt_high->Draw("hist same");
  //c_mupT->SaveAs("plots/Data2022excess/muon_pT_pT-700_jets.png");
  TCanvas* c_muEta = new TCanvas();
  c_muEta->cd();
  muonEta_ref->GetXaxis()->SetTitle("#mu #eta");
  muonEta_ref->SetLineColor(1);
  muonEta_ref->Draw("hist");
  muonEta_high->SetLineColor(2);
  muonEta_high->Draw("hist same");
  //c_muEta->SaveAs("plots/Data2022excess/muon_eta_pT-700_jets.png");
  TCanvas* c_muPhi = new TCanvas();
  c_muPhi->cd();
  muonPhi_ref->GetXaxis()->SetTitle("#mu #phi [rad]");
  muonPhi_ref->SetLineColor(1);
  muonPhi_ref->Draw("hist");
  muonPhi_high->SetLineColor(2);
  muonPhi_high->Draw("hist same");
  //c_muPhi->SaveAs("plots/Data2022excess/muon_phi_pT-700_jets.png");
  TCanvas* c_muStat = new TCanvas();
  c_muStat->cd();
  muonNstat_ref->GetXaxis()->SetTitle("#mu # Stations");
  muonNstat_ref->SetLineColor(1);
  muonNstat_ref->Draw("hist");
  muonNstat_high->SetLineColor(2);
  muonNstat_high->Draw("hist same");
  //c_muStat->SaveAs();
  TCanvas* c_PVz = new TCanvas();
  c_PVz->cd();
  hPV_z_ref->GetXaxis()->SetTitle("PV z");
  hPV_z_ref->SetLineColor(1);
  hPV_z_ref->Draw("hist");
  hPV_z_high->SetLineColor(2);
  hPV_z_high->Draw("hist same");
  //c_muPVz->SaveAs();
  */

  DrawNormalizedRatio(muonEta_ref, muonEta_high, "c_muEta", "#mu #eta", true);
  DrawNormalizedRatio(muonPhi_ref, muonPhi_high, "c_muPhi", "#mu #phi", true);
  DrawNormalizedRatio(muonNstat_ref, muonNstat_high, "c_muStat", "#mu # Stations", true);
  DrawNormalizedRatio(hPV_z_ref, hPV_z_high, "c_PVz", "PV z", true);
  
} // End of main 

void Data2022excess_check_Approval(){

  plotChecks("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/bin/txt/lastChecksPreApp2022.txt", "kinsel");
  //plotChecks("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/bin/txt/lastChecksPreApp2023.txt", "kinsel");

}


