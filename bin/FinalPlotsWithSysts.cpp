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
#include "TColor.h"
#include <map>
#include "Math/QuantFuncMathCore.h"


TGraphAsymmErrors* StatRatioPlot(string systFile){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  TFile *f1 =  TFile::Open(systFile.c_str());
  TH1D* bkgNominal = (TH1D*) f1->Get("histograms/background");

  int nBins = bkgNominal->GetNbinsX();
  TGraphAsymmErrors* bkgStat = new TGraphAsymmErrors(bkgNominal);
        
  for (int i = 0; i < nBins; i++){

    double x = bkgNominal->GetXaxis()->GetBinCenter(i+1);
    bkgStat->SetPoint(i, x, 1.0);

    double nominal = bkgNominal->GetBinContent(i+1);
    double statErr = bkgNominal->GetBinError(i+1)/nominal;

    bkgStat->SetPointEYhigh(i, statErr);
    bkgStat->SetPointEYlow(i, statErr);
    
  } // Loop over histogram bins 

  f1->Close();
  
  return bkgStat;
  
}


TGraphAsymmErrors* SystRatioPlot(string systFile, string year, string histName, bool statPlusSyst = true){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  TFile *f1 =  TFile::Open(systFile.c_str());

  std::vector<string> systList;
  if (year == "2022")
    systList = {"CMS_pileup", "CMS_eff_m_reco_2022", "CMS_eff_m_id_2022", "CMS_eff_m_iso_2022", "CMS_eff_m_trigger_2022", "CMS_scale_m_2022", "CMS_eff_b_2022", "CMS_EXO24021_W_kfactor", "pdf_qqbar"};
  else if (year == "2023")
    systList = {"CMS_pileup", "CMS_eff_m_reco_2023", "CMS_eff_m_id_2023", "CMS_eff_m_iso_2023", "CMS_eff_m_trigger_2023", "CMS_scale_m_2023", "CMS_eff_b_2023", "CMS_EXO24021_W_kfactor", "pdf_qqbar"};
  if (histName == "mT_" || histName == "MET_" || histName == "mT_Njets-gt-0_" || histName == "MET_0jets_" || histName == "mT_0jets_" || histName == "mT_dPhiJetsMETcut_" || histName == "mT_jets_"){
    if (year == "2022")
      systList.push_back("CMS_scale_met_2022");
    else if (year == "2023")
      systList.push_back("CMS_scale_met_2023");
  }
  
  std::vector<string> systDirs = {"_Up", "_Down"};

  std::map<string, TH1D*> bkgVars;
  TH1D* bkgNominal = (TH1D*) f1->Get("histograms/background");

  int nBins = bkgNominal->GetNbinsX();
  //TGraphAsymmErrors* bkgSyst = new TGraphAsymmErrors(nBins);
  TGraphAsymmErrors* bkgSyst = new TGraphAsymmErrors(bkgNominal);
  
  for (const auto &syst : systList) {
    for (const auto &dir : systDirs) {
      
      bkgVars[syst+dir] = (TH1D*) f1->Get(("histograms/background_" + syst + dir).c_str());

    } // Loop over Up/Down variations
  } // Loop over systematics
        
  for (int i = 0; i < nBins; i++){

    double x = bkgNominal->GetXaxis()->GetBinCenter(i+1);
    bkgSyst->SetPoint(i, x, 1.0);

    double nominal = bkgNominal->GetBinContent(i+1);
    // Stat. Error
    double statErr = bkgNominal->GetBinError(i+1)/nominal;

    double systUpTot = 0;
    double systDownTot = 0;

    double errUpTot = 0;
    double errDownTot = 0;
    
    for (const auto &syst : systList) {

      double systUp   = bkgVars[syst+"_Up"]->GetBinContent(i+1);
      double systDown = bkgVars[syst+"_Down"]->GetBinContent(i+1);

      systUpTot   += (systUp/nominal - 1.0)*(systUp/nominal - 1.0);
      systDownTot += (1.0 - systDown/nominal)*(1.0 - systDown/nominal);
      
    } // Loop over systematics

    // Add normalization systematics (Lumi)
    systUpTot   += 0.014*0.014;
    systDownTot += 0.014*0.014;

    // Add normalization systematics (xsec)
    systUpTot += 0.012*0.012;
    systDownTot += 0.012*0.012;

    systUpTot   = sqrt(systUpTot);
    systDownTot = sqrt(systDownTot);

    // Stat. + Syst.
    if (statPlusSyst){
      errUpTot   = sqrt(statErr*statErr + systUpTot*systUpTot);
      errDownTot = sqrt(statErr*statErr + systDownTot*systDownTot);
    } else {
      errUpTot = systUpTot;
      errDownTot = systDownTot;
    }

    bkgSyst->SetPointEYhigh(i, errUpTot);
    bkgSyst->SetPointEYlow(i, errDownTot);

    cout <<"  bin "<<i<<" --> Nom: "<<nominal<<" + "<<systUpTot<<" - "<<systDownTot<< " => Value: " << (nominal*systUpTot)*(nominal*systUpTot) << endl;
    
  } // Loop over histogram bins 

  f1->Close();
  
  return bkgSyst;
  
}




void FullPlot(string systFile, string histFile, string year, string runPeriod, string histName, bool statPlusSyst = true, bool savePlots = false){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);


  TFile *f1 =  TFile::Open(histFile.c_str());

  TH1D* Wprime2000 = (TH1D*) f1->Get("histograms/Wprime2000");
  TH1D* Wprime3600 = (TH1D*) f1->Get("histograms/Wprime3600");
  TH1D* Wprime5600 = (TH1D*) f1->Get("histograms/Wprime5600");
  TH1D* W_boson    = (TH1D*) f1->Get("histograms/W_boson");           
  TH1D* Top        = (TH1D*) f1->Get("histograms/Top");
  TH1D* Z_boson    = (TH1D*) f1->Get("histograms/Z_boson");
  TH1D* DiBoson    = (TH1D*) f1->Get("histograms/DiBoson");
  TH1D* QCD        = (TH1D*) f1->Get("histograms/QCD");
  TH1D* background = (TH1D*) f1->Get("histograms/background");
  TString data_name;
  if (year == "2022")
    data_name = "histograms/ReRecoData2022";
  else if (year == "2023")
    data_name = "histograms/PromptData2023";
  TH1D* Data       = (TH1D*) f1->Get(data_name);

  const int nBins = W_boson->GetNbinsX();
  float Xmin = W_boson->GetXaxis()->GetXmin();
  float Xmax = W_boson->GetXaxis()->GetXmax();

  /// Draw mT distribution with same style ///

  TCanvas* mT = new TCanvas("mT_syst","",602,676);
  mT->cd();
  mT->Draw();

  TPad* up = new TPad("","",0.0,0.36,1.0,1.0);
  TPad* down = new TPad("","",0.0,0.0,1.0,0.36);
  up->SetTopMargin(0.13);
  up->SetBottomMargin(0.017);
  up->Draw("SAME");
  down->SetTopMargin(0.017);
  down->SetBottomMargin(0.35);
  down->Draw("SAME");

  /// Draw upper panel
  up->cd();
  up->SetLogy();

  // Prepare & Draw background stack
  W_boson->SetLineColor(1);
  W_boson->SetFillColor(kP10Blue);
  Top->SetLineColor(1);
  Top->SetFillColor(kP10Red);
  Z_boson->SetLineColor(1);
  Z_boson->SetFillColor(kP10Brown);
  DiBoson->SetLineColor(1);
  DiBoson->SetFillColor(kP10Violet);
  QCD->SetLineColor(1);
  QCD->SetFillColor(kP10Yellow);
  
  THStack *bkg = new THStack("bkg_stack","");
  bkg->Add(QCD);
  bkg->Add(DiBoson);
  bkg->Add(Z_boson);
  bkg->Add(Top);
  bkg->Add(W_boson);

  float ylow = 0.0011;
  float yup = bkg->GetMaximum()*10;

  bkg->Draw("hist");
  bkg->GetXaxis()->SetTitle(W_boson->GetXaxis()->GetTitle());
  bkg->GetYaxis()->SetTitle(W_boson->GetYaxis()->GetTitle());
  float xLabelSize = bkg->GetXaxis()->GetLabelSize();
  float xTitleSize = bkg->GetXaxis()->GetTitleSize();
  bkg->GetXaxis()->SetLabelSize(0);
  bkg->GetXaxis()->SetTitleSize(0);
  bkg->SetMinimum(ylow);
  bkg->SetMaximum(yup);
  bkg->GetXaxis()->SetRangeUser(Xmin, Xmax);
  bkg->Draw("hist");

  // Obtain full systematic band
  TGraphAsymmErrors* systBand = SystRatioPlot(systFile, year, histName, statPlusSyst);

  // Graph for syst band in stack
  TGraphAsymmErrors* systGraph = new TGraphAsymmErrors();
  systGraph->SetName("systBandGraph");
  systGraph->SetFillColor(kGray+2);
  systGraph->SetFillStyle(3002);
  systGraph->SetLineWidth(1);
  systGraph->SetLineColor(kGray+2);

  for (int i = 0; i < background->GetNbinsX(); i++) {
    double x = background->GetBinCenter(i+1);
    double xErr = background->GetBinWidth(i+1) / 2.0;

    double y = background->GetBinContent(i+1);
    double yErrUp = systBand->GetErrorYhigh(i) * y;
    double yErrDown = systBand->GetErrorYlow(i) * y;

    systGraph->SetPoint(i, x, y);
    systGraph->SetPointError(i, xErr, xErr, yErrDown, yErrUp);
  }
  systGraph->Draw("2 SAME");

  // Draw Wprime signals
  Wprime2000->SetLineColor(Wprime2000->GetLineColor());
  //  Wprime2000->Scale(189.79);
  Wprime2000->Draw("same hist");
  Wprime3600->SetLineColor(Wprime3600->GetLineColor());
  //Wprime3600->Scale(6.262);
  Wprime3600->Draw("same hist");
  Wprime5600->SetLineColor(Wprime5600->GetLineColor());
  //Wprime5600->Scale(0.411);
  Wprime5600->Draw("same hist");

  // Draw Data
  Data->SetMarkerStyle(Data->GetMarkerStyle());
  Data->SetMarkerColor(Data->GetMarkerColor());
  Data->SetMarkerSize(Data->GetMarkerSize());
  Data->SetLineColor(Data->GetLineColor());
  Data->SetBinErrorOption(Data->GetBinErrorOption());
  Data->Draw("same PEZ");
  

  /// Draw lower panel with Data/MC ratio
  
  down ->cd();
  float ydown_low, ydown_up;
  ydown_low = 0.0;
  ydown_up = 2.0; // 2.0
  auto frame = down->DrawFrame(Xmin, ydown_low, Xmax, ydown_up);
  frame->GetYaxis()->SetTitle("Data / MC");
  frame->GetYaxis()->SetTitleSize(bkg->GetYaxis()->GetTitleSize()*2.0);
  frame->GetYaxis()->SetTitleOffset(0.6);
  frame->GetYaxis()->CenterTitle(true);
  frame->GetYaxis()->SetLabelSize(bkg->GetYaxis()->GetLabelSize()*1.9);
  frame->GetYaxis()->SetNdivisions(304);
  frame->GetXaxis()->SetTitle(W_boson->GetXaxis()->GetTitle());
  frame->GetXaxis()->SetTickLength(bkg->GetYaxis()->GetTickLength()*1.8);
  frame->GetXaxis()->SetTitleSize(xTitleSize*2.4);
  frame->GetXaxis()->SetTitleOffset(1.2);
  frame->GetXaxis()->SetLabelSize(xLabelSize*1.9);

  // Draw full systematic band
  systBand->SetFillColor(kGray+2);
  systBand->SetFillStyle(3001); // 3017
  systBand->SetMarkerColor(0);
  systBand->SetLineColor(0);
  systBand->SetMarkerSize(0);
  systBand->Draw("SAME E2");

  // Draw stat band separated from syst
  TGraphAsymmErrors* statBand = StatRatioPlot(systFile);
  if (!statPlusSyst){
    statBand->SetFillColor(kAzure+2);
    statBand->SetFillStyle(3017);
    statBand->SetMarkerColor(0);
    statBand->SetLineColor(0);
    statBand->SetMarkerSize(0);
    statBand->Draw("SAME E2");
  }
    
  // Compute data to MC ratio
  TGraphAsymmErrors* ratio = new TGraphAsymmErrors();
  ratio->SetMarkerStyle(20);
  ratio->SetMarkerSize(0.7);
  ratio->SetLineColor(kBlack);
  ratio->SetMarkerColor(kBlack);

  for (int i = 0; i < Data->GetNbinsX(); i++) {
    double x = Data->GetBinCenter(i+1);
    double xErr = Data->GetBinWidth(i+1) / 2.0;

    double mc = background->GetBinContent(i+1);
    double d = Data->GetBinContent(i+1);

    if (d == 0 || mc == 0) continue;

    double dataMC = d / mc;
    double errUp = Data->GetBinErrorUp(i+1) / mc;
    double errDown = Data->GetBinErrorLow(i+1) / mc;
    
    ratio->SetPoint(i, x, dataMC);
    ratio->SetPointError(i, xErr, xErr, errDown, errUp);
  }
  ratio->Draw("PZ0");
  
  
  TLine* lmid = new TLine(Xmin, 1.0, Xmax, 1.0);
  lmid->SetLineStyle(3);
  lmid->Draw("SAME");
  TLine* lbot = new TLine(Xmin, 1.0-(1.0-ydown_low)/2.0, Xmax, 1.0-(1.0-ydown_low)/2.0);
  lbot->SetLineStyle(3);
  lbot->Draw("SAME");
  TLine* ltop = new TLine(Xmin, 1.0+(ydown_up-1.0)/2.0, Xmax, 1.0+(ydown_up-1.0)/2.0);
  ltop->SetLineStyle(3);
  ltop->Draw("SAME");

  // Set legend and title
  up->cd();
  TLegend *leg = new TLegend(0.34, 0.63, 0.92, 0.86);
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetTextSize(0.033);
  leg->SetNColumns(3);
  leg->AddEntry(W_boson, "W boson", "f");
  leg->AddEntry(DiBoson, "DiBoson", "f");
  leg->AddEntry(Wprime2000, "W' M_{W'} = 2.0 TeV", "l");
  leg->AddEntry(Top, "Top", "f");
  leg->AddEntry(QCD, "QCD", "f");
  leg->AddEntry(Wprime3600, "W' M_{W'} = 3.6 TeV", "l");
  leg->AddEntry(Z_boson, "Z/#gamma* #rightarrow ll", "f");
  leg->AddEntry(Data, "Data", "lp");
  leg->AddEntry(Wprime5600, "W' M_{W'} = 5.6 TeV", "l");
  if (statPlusSyst) {
    leg->AddEntry(systBand, "Stat. + Syst.", "f");
    leg->AddEntry("", "", "");
  } else {
    leg->AddEntry(systBand, "Syst.", "f");
    leg->AddEntry(statBand, "Stat.", "f");
  }
  leg->AddEntry("", "", "");
  leg->Draw();

  string lumi;
  if (year == "2022"){
    if (runPeriod == "preEE")
      lumi = "8.0";
    else if (runPeriod == "postEE")
      lumi = "26.7";
    else
      lumi = "34.7";
  }
  else if (year == "2023")
    lumi = "27.2";
  TString title_left = "#bf{CMS} #it{Work in progress}";
  TLatex* preliminary_left = new TLatex(0.12,0.89, title_left);
  preliminary_left->SetNDC();
  preliminary_left->SetTextFont(42);
  preliminary_left->SetTextSize(0.045);
  preliminary_left->Draw();
  
  TString title_right = year + runPeriod +", "+ lumi +" fb^{-1}  (13.6 TeV)";
  TLatex* preliminary_right = new TLatex(0.56,0.89, title_right);
  preliminary_right->SetNDC();
  preliminary_right->SetTextFont(42);
  preliminary_right->SetTextSize(0.045);
  preliminary_right->Draw();

  /// Save plots ///
  string stat = "";
  if (!statPlusSyst)
    stat = "_StatSplit";
  
  if (savePlots){
    mT->SaveAs(("plots/FinalPlotsSysts/"+ histName + year + runPeriod + "_SystPlot"+ stat +".png").c_str());
    mT->SaveAs(("plots/FinalPlotsSysts/"+ histName + year + runPeriod + "_SystPlot"+ stat +".pdf").c_str());
  }
  
}// End of main


void FinalPlotsWithSysts(){

  //FullPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SystBand_SSMlimit_fullCuts/root/mT__pg_SystPlot.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SSMlimit_fullCuts/root/mT__pg_SSMlimits2022.root", "2022", "", "mT_", true, true);

  //FullPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/SystBand_SSMlimit_fullCuts/root/mT__pg_SystPlot.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/SSMlimit_fullCuts-v2/root/mT__pg_SSMlimits2023.root", "2023", "", "mT_", true, true);

  //FullPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SystBand_SSMlimit_fullCuts_preEE/root/mT__pg_SystPlot.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SSMlimit_fullCuts_preEE/root/mT__pg_SSMlimits2022.root", "2022", "preEE", "mT_", true, false);
  //FullPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SystBand_SSMlimit_fullCuts_postEE/root/mT__pg_SystPlot.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SSMlimit_fullCuts_postEE/root/mT__pg_SSMlimits2022.root", "2022", "postEE", "mT_", true, false);
  
  FullPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SystBand_feedback22Jul_mT_pT_MET-v3/root/mT_jets__pg_SystPlot.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/feedback22Jul_mT_pT_MET-v3/root/mT_jets__pg_SSMlimits2022.root", "2022", "", "mT_jets_", true, true);
  //FullPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SystBand_feedback22Jul_mT_pT_MET/root/muon_pt__pg_SystPlot.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/feedback22Jul_mT_pT_MET/root/muon_pt__pg_SSMlimits2022.root", "2022", "", "muon_pt_", true, true);
  //FullPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SystBand_feedback22Jul_mT_pT_MET/root/MET__pg_SystPlot.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/feedback22Jul_mT_pT_MET/root/MET__pg_SSMlimits2022.root", "2022", "", "MET_", true, true);
  
  //FullPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SystBand_feedback22Jul_mT_pT_MET-v2/root/mT_0jets__pg_SystPlot.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/feedback22Jul_mT_pT_MET-v2/root/mT_0jets__pg_SSMlimits2022.root", "2022", "", "mT_0jets_", true, true);
  //FullPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SystBand_feedback22Jul_mT_pT_MET-v3/root/muon_pt_0jets__pg_SystPlot.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/feedback22Jul_mT_pT_MET-v3/root/muon_pt_0jets__pg_SSMlimits2022.root", "2022", "", "muon_pt_0jets_", true, true);
  //FullPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SystBand_feedback22Jul_mT_pT_MET-v3/root/MET_0jets__pg_SystPlot.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/feedback22Jul_mT_pT_MET-v3/root/MET_0jets__pg_SSMlimits2022.root", "2022", "", "MET_0jets_", true, true);

  //FullPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SystBand_mT_dPhiJetsMETcut/root/mT_dPhiJetMET__pg_SystPlot.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/mT_dPhiJetsMETcut/root/mT_dPhiJetMET__pg_SSMlimits2022.root", "2022", "", "mT_dPhiJetMET_", true, true);
}


