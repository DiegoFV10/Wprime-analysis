#include "TMath.h"
#include <stdlib.h>
#include <stdio.h>
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
#include <algorithm>
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <cassert>
#include <sstream>
#include "TFileCollection.h"
#include "THashList.h"
#include "TBenchmark.h"
#include <filesystem>
#include <map>
namespace fs = std::filesystem;


void HPeff(TString numerator, TString denominator, TString histType, int plotType, TString xtitle=""){
  
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  TFile *den =  TFile::Open(denominator);
  TH1D* h_ref = (TH1D*) den->Get("histograms/" + histType);

  TFile *num =  TFile::Open(numerator);
  TH1D* h_HP = (TH1D*) num->Get("histograms/" + histType);

  if (plotType == 8) {
  // Include Underflow and Overflow bins
    int nbins = h_ref->GetNbinsX();
    // Underflow 
    h_ref->SetBinContent(1, h_ref->GetBinContent(1) + h_ref->GetBinContent(0));
    h_ref->SetBinError(1, std::sqrt(std::pow(h_ref->GetBinError(1), 2) + std::pow(h_ref->GetBinError(0), 2)));
    h_HP->SetBinContent(1, h_HP->GetBinContent(1) + h_HP->GetBinContent(0));
    h_HP->SetBinError(1, std::sqrt(std::pow(h_HP->GetBinError(1), 2) + std::pow(h_HP->GetBinError(0), 2)));
    // Overflow 
    h_ref->SetBinContent(nbins, h_ref->GetBinContent(nbins) + h_ref->GetBinContent(nbins+1));
    h_ref->SetBinError(nbins, std::sqrt(std::pow(h_ref->GetBinError(nbins), 2) + std::pow(h_ref->GetBinError(nbins+1), 2)));
    h_HP->SetBinContent(nbins, h_HP->GetBinContent(nbins) + h_HP->GetBinContent(nbins+1));
    h_HP->SetBinError(nbins, std::sqrt(std::pow(h_HP->GetBinError(nbins), 2) + std::pow(h_HP->GetBinError(nbins+1), 2)));
  }
  // Create the rate for the different variables, draw the canvas and save
  
  TString title;
  if (histType == "ReRecoData2022")
    title = "#bf{CMS} #it{Private Work}                              2022 + 2023, 62.5 fb^{-1} (13.6 TeV)";
  else
    title = "#bf{CMS} #it{Simulation}                                                     2022 (13.6 TeV)";
  if (plotType == 10)
    title = "#bf{CMS} #it{Private Work}                                     2022, 34.7 fb^{-1} (13.6 TeV)";
  TLatex* preliminary = new TLatex(0.12,0.89, title);
  preliminary->SetNDC();
  preliminary->SetTextFont(42);
  preliminary->SetTextSize(0.042);

  TString hist_string = histType;
  if (histType == "ReRecoData2022")
    hist_string = "2022+2023 Data";
  if (plotType == 10)
    hist_string = "2022 Data";
  TPaveLabel *label = new TPaveLabel(0.17,0.70,0.45,0.79, hist_string, "NDC");
  label->SetBorderSize(0);
  label->SetFillColor(0);
  label->SetFillStyle(0);
  label->SetTextSize(0.45);

  TString pT_string = "p_{T} > 500 GeV";
  if (plotType == 9)
    pT_string = "1000 < p_{T} < 1500 GeV";
  else if (plotType == 10)
    pT_string = "";
  TPaveLabel *pTlabel = new TPaveLabel(0.17,0.61,0.45,0.70, pT_string, "NDC");
  pTlabel->SetBorderSize(0);
  pTlabel->SetFillColor(0);
  pTlabel->SetFillStyle(0);
  pTlabel->SetTextSize(0.40);

  // Compute the data-to-data ratio
  TH1D* h_ratio = (TH1D*) h_HP->Clone("h_ratio");
  h_ratio->Divide(h_ref);

  // Define the ratio canvas
  TCanvas* c_rate = new TCanvas("HPeff","",602,676);
  c_rate->cd();
  c_rate->Draw();

  TPad* up = new TPad("","",0.0,0.36,1.0,1.0);
  TPad* down = new TPad("","",0.0,0.0,1.0,0.36);
  up->SetTopMargin(0.13);
  up->SetBottomMargin(0.0);
  up->Draw("SAME");
  down->SetTopMargin(0.0);
  down->SetBottomMargin(0.35);
  down->Draw("SAME");

  // Draw upper panel
  bool logY = true;
  float xlow = h_ref->GetXaxis()->GetXmin();
  float xup = h_ref->GetXaxis()->GetXmax();
  float ylow;
  if (histType == "ReRecoData2022")
    ylow = 2E-1;
  else
    ylow = 2E-3;
  float hmax = 1.0;
  if (logY)
    hmax = 10;
  float yup = h_ref->GetMaximum()*hmax;
    
  up->cd();
  if (logY)
    up->SetLogy();
  h_ref->GetXaxis()->SetTitle(h_ref->GetXaxis()->GetTitle());
  h_ref->SetMinimum(ylow);
  h_ref->SetMaximum(yup);
  h_ref->SetLineColor(kAzure);
  h_ref->SetFillColor(kAzure+1);
  h_ref->SetFillStyle(3002);
  h_ref->SetLineWidth(2);
  h_ref->GetXaxis()->SetRangeUser(xlow, xup);
  h_ref->Draw("hist");
  h_HP->SetLineColor(1);
  h_HP->SetLineWidth(2);
  h_HP->Draw("same");

  // Draw ratio plot (lower panel)
  down ->cd();
  float ydown_low, ydown_up;
  if (plotType == 0 || plotType == 9){
    ydown_low = 0.95;
    ydown_up = 1.05;
  } else if (plotType == 1 || plotType == 4 || plotType == 5){
    ydown_low = 0.0;
    ydown_up = 2.0;
  } else if (plotType == 2 || plotType == 3){
    ydown_low = 0.5;
    ydown_up = 1.5;
  } else if (plotType == 6 || plotType == 7){
    ydown_low = 0.75;
    ydown_up = 1.25;
  } else if (plotType == 8 || plotType == 10){
    ydown_low = 0.0;
    ydown_up = 1.25;
  }
  auto frame = down->DrawFrame(xlow, ydown_low, xup, ydown_up);
  if (plotType == 0 || plotType == 8 || plotType == 9 || plotType == 10)
    frame->GetYaxis()->SetTitle("HP / Ref.");
  else if (plotType == 1)
    frame->GetYaxis()->SetTitle("MET-#mu cuts / Ref.");
  else if (plotType == 2 || plotType == 4 || plotType == 6)
    frame->GetYaxis()->SetTitle("AbsIso10 / Ref.");
  else if (plotType == 3 || plotType == 5 || plotType == 7)
    frame->GetYaxis()->SetTitle("AbsIso20 / Ref.");
  frame->GetYaxis()->SetTitleSize(h_ref->GetYaxis()->GetTitleSize()*2.0);
  frame->GetYaxis()->SetTitleOffset(0.6);
  frame->GetYaxis()->CenterTitle(true);
  frame->GetYaxis()->SetLabelSize(h_ref->GetYaxis()->GetLabelSize()*1.9);
  frame->GetYaxis()->SetNdivisions(304);
  frame->GetXaxis()->SetTitle(h_ref->GetXaxis()->GetTitle());
  frame->GetXaxis()->SetTickLength(h_ref->GetYaxis()->GetTickLength()*1.8);
  frame->GetXaxis()->SetTitleSize(h_ref->GetXaxis()->GetTitleSize()*2.4);
  frame->GetXaxis()->SetTitleOffset(1.2);
  frame->GetXaxis()->SetLabelSize(h_ref->GetXaxis()->GetLabelSize()*1.9);

  h_ratio->SetMarkerStyle(20);
  h_ratio->SetMarkerColor(1);
  h_ratio->SetLineColor(1);
  h_ratio->SetMarkerSize(0.8);
  h_ratio->Draw("AP SAME");

  
  TLine* lmid = new TLine(xlow, 1.0, xup, 1.0);
  lmid->SetLineStyle(3);
  lmid->Draw("SAME");
  //TLine* lbot = new TLine(xlow, 0.975, xup, 0.975);
  TLine* lbot = new TLine(xlow, 1.0-(1.0-ydown_low)/2.0, xup, 1.0-(1.0-ydown_low)/2.0);
  lbot->SetLineStyle(3);
  lbot->Draw("SAME");
  //TLine* ltop = new TLine(xlow, 1.025, xup, 1.025);
  TLine* ltop = new TLine(xlow, 1.0+(1.0-ydown_low)/2.0, xup, 1.0+(1.0-ydown_low)/2.0);
  ltop->SetLineStyle(3);
  ltop->Draw("SAME");

  // Set legend and title
  up->cd();
  TLegend * leg = new TLegend(0.65, 0.70, 0.9, 0.85);
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetTextSize(0.034);
  if (plotType == 0 || plotType == 8 || plotType == 9 || plotType == 10)
    leg->AddEntry(h_HP, "With High-Purity", "apel");
  else if (plotType == 1)
    leg->AddEntry(h_HP, "With MET-#mu cuts", "apel");
  else if (plotType == 2 || plotType == 4 || plotType == 6)
    leg->AddEntry(h_HP, "AbsIso < 10 GeV", "apel");
  else if (plotType == 3 || plotType == 5 || plotType == 7)
    leg->AddEntry(h_HP, "AbsIso < 20 GeV", "apel");
  leg->AddEntry(h_ref, "Reference", "f");
  leg->Draw();

  preliminary->Draw();
  label->Draw();
  pTlabel->Draw();

  /// Save Plots ///
  /*
  if (plotType == 0)
    c_rate->SaveAs("plots/HighPurity/HPefficiency_"+ histType +"_WboostCR.png");
  else if (plotType == 1)
    c_rate->SaveAs("plots/HighPurity/METnoMuCutsEfficiency_"+ histType +"_WboostCR.png");
  else if (plotType == 2 || plotType == 4 || plotType == 6)
    c_rate->SaveAs("plots/HighPurity/AbsIso10_efficiency_"+ histType +"_WboostCR.png");
  else if (plotType == 3 || plotType == 5 || plotType == 7)
    c_rate->SaveAs("plots/HighPurity/AbsIso20_efficiency_"+ histType +"_WboostCR.png");
  else if (plotType == 8 || plotType == 9)
    c_rate->SaveAs("plots/HighPurity/HPeff_vs_"+ xtitle + "_"+ histType +"_WboostCR.png");
  else if (plotType == 10)
    c_rate->SaveAs("plots/HighPurity/HPeff_"+ histType +"_SR.png");
  */
}// End of main 

void HighPurity_efficiencies(){

  // W-boosted CR
  TString inp_Wboost0 = "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/W-boosted-CR_HP+Iso-v3/root/";
  TString inp_Wboost1 = "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/WboostCR_22+23data-v3/root/";
  //TString inp_Wboost1 = "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/WboostCR_22+23data-pT1000/root/";
  TString inp_Wboost2 = "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/WboostCR_WboostedMC_genRatio/root/";
  TString inp_Wboost3 = "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/WboostCR_QCD-MC_genRatio_pT500/root/";
  // W' analysis
  TString inp_Wprime = "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/HighPurity_Wprime2/root/";
  // W' Signal Region
  TString inp_SR = "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/HighPurity_mT_DataOnly_EXO17Jun-v2/root/";
  // SR for mT progressive cuts
  TString inp_Progressive = "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/mT_progressiveCuts_EXO17Jun/root/";
  
  /*// For High-Purity
  HPeff(inp_Wboost + "muon_pt_HP__pg_Wboosted_CR.root", inp_Wboost + "muon_pt__pg_Wboosted_CR.root", "ReRecoData2022", 0);
  HPeff(inp_Wboost + "muon_pt_HP__pg_Wboosted_CR.root", inp_Wboost + "muon_pt__pg_Wboosted_CR.root", "QCD", 0);
  HPeff(inp_Wboost + "muon_pt_HP__pg_Wboosted_CR.root", inp_Wboost + "muon_pt__pg_Wboosted_CR.root", "W_ptW_full", 0);
  HPeff(inp_Wprime + "mT_HP__pg_2022ReReco.root", inp_Wprime + "mT__pg_2022ReReco.root", "Wprime2000", 0);
  HPeff(inp_Wprime + "mT_HP__pg_2022ReReco.root", inp_Wprime + "mT__pg_2022ReReco.root", "Wprime3600", 0);
  HPeff(inp_Wprime + "mT_HP__pg_2022ReReco.root", inp_Wprime + "mT__pg_2022ReReco.root", "Wprime5600", 0);
  
  // For MET-mu
  HPeff(inp_Wboost + "muon_pt_METnoMuCut__pg_Wboosted_CR.root", inp_Wboost + "muon_pt__pg_Wboosted_CR.root", "ReRecoData2022", 1);
  
  // For Isolation
  HPeff(inp_Wboost + "muon_pt_absIso10__pg_Wboosted_CR.root", inp_Wboost + "muon_pt__pg_Wboosted_CR.root", "ReRecoData2022", 2);
  HPeff(inp_Wboost + "muon_pt_absIso20__pg_Wboosted_CR.root", inp_Wboost + "muon_pt__pg_Wboosted_CR.root", "ReRecoData2022", 3);
  HPeff(inp_Wboost + "muon_pt_absIso10__pg_Wboosted_CR.root", inp_Wboost + "muon_pt__pg_Wboosted_CR.root", "QCD", 4);
  HPeff(inp_Wboost + "muon_pt_absIso20__pg_Wboosted_CR.root", inp_Wboost + "muon_pt__pg_Wboosted_CR.root", "QCD", 5);
  HPeff(inp_Wboost + "muon_pt_absIso10__pg_Wboosted_CR.root", inp_Wboost + "muon_pt__pg_Wboosted_CR.root", "W_ptW_full", 6);
  HPeff(inp_Wboost + "muon_pt_absIso20__pg_Wboosted_CR.root", inp_Wboost + "muon_pt__pg_Wboosted_CR.root", "W_ptW_full", 7);
  HPeff(inp_Wboost + "muon_pt_absIso10__pg_Wboosted_CR.root", inp_Wboost + "muon_pt__pg_Wboosted_CR.root", "Wprime3600", 6);
  HPeff(inp_Wboost + "muon_pt_absIso20__pg_Wboosted_CR.root", inp_Wboost + "muon_pt__pg_Wboosted_CR.root", "Wprime3600", 7);
  */
  // For High-Purity effs. VS muon attributes
  //HPeff(inp_Wboost1 + "segmentComp_HP__pg_Wboosted_CR.root", inp_Wboost1 + "segmentComp__pg_Wboosted_CR.root", "ReRecoData2022", 8, "SegmentComp");
  //HPeff(inp_Wboost1 + "TightId_HP__pg_Wboosted_CR.root", inp_Wboost1 + "TightId__pg_Wboosted_CR.root", "ReRecoData2022", 8, "TightID");
  //HPeff(inp_Wboost1 + "nTkLayers_HP__pg_Wboosted_CR.root", inp_Wboost1 + "nTkLayers__pg_Wboosted_CR.root", "ReRecoData2022", 8, "nTkLayers");
  //HPeff(inp_Wboost1 + "mvaMuonId_HP__pg_Wboosted_CR.root", inp_Wboost1 + "mvaMuonId__pg_Wboosted_CR.root", "ReRecoData2022", 8, "MuonMVAId");
  //HPeff(inp_Wboost1 + "promptMvaId_HP__pg_Wboosted_CR.root", inp_Wboost1 + "promptMvaId__pg_Wboosted_CR.root", "ReRecoData2022", 8, "PromptMVAId");
  //HPeff(inp_Wboost2 + "muon_pTgen_over_pTreco_HP__pg_Wboosted_CR.root", inp_Wboost2 + "muon_pTgen_over_pTreco__pg_Wboosted_CR.root", "W_ptW_full", 9, "pTgen-over-pTreco");
  //HPeff(inp_Wboost3 + "muon_pTgen_over_pTreco_HP__pg_Wboosted_CR.root", inp_Wboost3 + "muon_pTgen_over_pTreco__pg_Wboosted_CR.root", "QCD", 9, "pTgen-over-pTreco");

  // For High-Purity effs in SR
  //HPeff(inp_SR + "mT_HP__pg_2022ReReco.root", inp_SR + "mT__pg_2022ReReco.root", "ReRecoData2022", 10, "m_{T}");

  // Progressive mT cuts from convenors
  HPeff(inp_Progressive + "mT_etaCut__pg_2022ReReco.root", inp_Progressive + "mT_ref__pg_2022ReReco.root", "ReRecoData2022", 10, "m_{T}");
  
}
