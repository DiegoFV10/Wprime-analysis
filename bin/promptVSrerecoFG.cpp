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


void compare(string prompt_file, string prompt_h, string rereco_file, string rereco_h){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  TFile *fprompt =  TFile::Open((prompt_file + prompt_h).c_str());
  TFile *frereco =  TFile::Open((rereco_file + rereco_h).c_str());

  TH1D* promptHist = (TH1D*) fprompt->Get("histograms/PromptData2022_postEE");
  TH1D* rerecoHist = (TH1D*) frereco->Get("histograms/ReRecoData2022_postEE");


  TCanvas* c1 = new TCanvas();
  c1->cd();
  c1->SetLogy();
  if(prompt_h == "muon_pt_mT50__pg_2022Prompt_postEE.root"){
    promptHist->SetTitle("Muon p_{T} Prompt");
    promptHist->GetXaxis()->SetTitle("#mu p_{T}  [GeV]");
    promptHist->SetMinimum(0.1);
    promptHist->Draw();
    c1->SaveAs("plots/promptVSrereco/muon_pT_Prompt.png");
  }
  else if(prompt_h == "MET_pt_mT50__pg_2022Prompt_postEE.root"){
    promptHist->SetTitle("MET Prompt");
    promptHist->GetXaxis()->SetTitle("p_{T}^{miss}  [GeV]");
    promptHist->SetMinimum(0.1);
    promptHist->Draw();
    c1->SaveAs("plots/promptVSrereco/MET_Prompt.png");
  }
  else if(prompt_h == "mT_mT50__pg_2022Prompt_postEE.root"){
    promptHist->SetTitle("m_{T} Prompt");
    promptHist->GetXaxis()->SetTitle("m_{T}  [GeV]");
    promptHist->SetMinimum(0.1);
    promptHist->Draw();
    c1->SaveAs("plots/promptVSrereco/mT_Prompt.png");
  }

  TCanvas* c2 = new TCanvas();
  c2->cd();
  c2->SetLogy();
  if(rereco_h == "muon_pt_mT50__pg_2022ReReco_postEE.root"){
    rerecoHist->SetTitle("Muon p_{T} ReReco");
    rerecoHist->GetXaxis()->SetTitle("#mu p_{T}  [GeV]");
    rerecoHist->SetMinimum(0.1);
    rerecoHist->Draw();
    c2->SaveAs("plots/promptVSrereco/muon_pT_ReReco.png");
  }
  else if(rereco_h == "MET_pt_mT50__pg_2022ReReco_postEE.root"){
    rerecoHist->SetTitle("MET ReReco");
    rerecoHist->GetXaxis()->SetTitle("p_{T}^{miss}  [GeV]");
    rerecoHist->SetMinimum(0.1);
    rerecoHist->Draw();
    c2->SaveAs("plots/promptVSrereco/MET_ReReco.png");
  }
  else if(rereco_h == "mT_mT50__pg_2022ReReco_postEE.root"){
    rerecoHist->SetTitle("m_{T} ReReco");
    rerecoHist->GetXaxis()->SetTitle("m_{T}  [GeV]");
    rerecoHist->SetMinimum(0.1);
    rerecoHist->Draw();
    c2->SaveAs("plots/promptVSrereco/mT_ReReco.png");
  }

  //TGraphAsymmErrors* rate = new TGraphAsymmErrors(promptHist, rerecoHist);
  TH1D* rate = (TH1D*)promptHist->Clone("rate");
  rate->Divide(rerecoHist);

  TCanvas* c_rate = new TCanvas("promptVSrereco","",600,500);
  c_rate->cd();
  //c_rate->SetLogy();

  rate->SetMaximum(1.05);
  rate->SetMinimum(0.95);
  rate->SetMarkerStyle(20);
  rate->SetMarkerColor(1);
  rate->SetLineColor(1);
  rate->GetYaxis()->SetTitle("prompt/rereco");
  rate->GetYaxis()->SetTitleOffset(1.3);
  //rate->GetXaxis()->SetRangeUser(0, 3000);
  rate->GetXaxis()->SetTitle("#mu p_{T}  [GeV]");
  rate->GetXaxis()->SetTitleOffset(1.2);
  rate->Draw("AP");


  TString title = "#bf{CMS} #it{Private Work}                2022, 8.1 + 27.0 fb^{-1} (13.6 TeV)";
  TLatex* preliminary = new TLatex(0.12,0.92, title);
  preliminary->SetNDC();
  preliminary->SetTextFont(42);
  preliminary->SetTextSize(0.040);
  preliminary->Draw();


  /// Save Plots ///
  //c_pT->SaveAs("plots/charge_misID/ChargeMisID_Wmunu-All_pT.png");
  //c_eta->SaveAs("plots/charge_misID/ChargeMisID_Wmunu-All_eta.png");
  //c_barrel->SaveAs("plots/charge_misID/ChargeMisID_Wmunu-All_pT-barrel.png");
  //c_endcap->SaveAs("plots/charge_misID/ChargeMisID_Wmunu-All_pT-endcap.png");
  //c_iso->SaveAs("plots/charge_misID/ChargeMisID_Wmunu-All_TkRelIso.png");
  //c_nStat->SaveAs("plots/charge_misID/ChargeMisID_Wmunu-All_nStations.png");
  



}// End of main 

void promptVSrerecoFG(){

  //compare("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/EXO_preselection_FG/root/","MET_pt_mT50__pg_2022Prompt_postEE.root","/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/Wpythia_preselection_FG/root/","MET_pt_mT50__pg_2022ReReco_postEE.root");
  compare("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/preselection_FG_kfact/root/","muon_pt_mT50__pg_2022Prompt_postEE.root","/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/Wpythia_preselection_FG/root/","muon_pt_mT50__pg_2022ReReco_postEE.root");
  //compare("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/EXO_preselection_FG/root/","mT_mT50__pg_2022Prompt_postEE.root","/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/Wpythia_preselection_FG/root/","mT_mT50__pg_2022ReReco_postEE.root");

}


