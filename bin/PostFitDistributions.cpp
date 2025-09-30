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


TGraphAsymmErrors* SystRatioPlot(const TH1F* bkgHisto, std::vector<float> binCenters){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  TGraphAsymmErrors* bkgSyst = new TGraphAsymmErrors(bkgHisto);
        
  for (size_t i = 0; i < binCenters.size(); i++){

    double x = binCenters.at(i);
    bkgSyst->SetPoint(i, x, 1.0);

    double nominal = bkgHisto->GetBinContent(i+1);
    double errUp   = bkgHisto->GetBinErrorUp(i+1)/nominal;
    double errLow  = bkgHisto->GetBinErrorLow(i+1)/nominal;

    bkgSyst->SetPointEYhigh(i, errUp);
    bkgSyst->SetPointEYlow(i, errLow);
    
  } // Loop over histogram bins 
  
  return bkgSyst;
  
}


TH1F* RebinHisto(const TH1F* original, const TH1D* referenceBinning, const TString& newname) {

    const int nbins = referenceBinning->GetNbinsX();
    std::vector<double> newBins(nbins + 1);
    for (int i = 0; i <= nbins; i++) {
        newBins[i] = referenceBinning->GetBinLowEdge(i + 1);
    }

    TH1F* rebinned = new TH1F(newname, original->GetTitle(), nbins, &newBins[0]);

    for (int i = 1; i <= nbins; i++) {
        rebinned->SetBinContent(i, original->GetBinContent(i));
        rebinned->SetBinError(i, original->GetBinError(i));
    }

    return rebinned;
}



void PostFitPlot(string postfitFile, bool bkgOnlyFit, string dataFile, string year, bool savePlots = false){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  TFile *f1 = TFile::Open(postfitFile.c_str());
  TFile *f2 = TFile::Open(dataFile.c_str());

  TString fitType;
  if (bkgOnlyFit)
    fitType = "shapes_fit_b";
  else
    fitType = "shapes_fit_s";
  
  TString postfit_name = fitType + "/muon_channel/";
  TH1F* W_boson_old    = (TH1F*) f1->Get(postfit_name + "W_boson");           
  TH1F* Top_old        = (TH1F*) f1->Get(postfit_name + "Top");
  TH1F* Z_boson_old    = (TH1F*) f1->Get(postfit_name + "Z_boson");
  TH1F* DiBoson_old    = (TH1F*) f1->Get(postfit_name + "DiBoson");
  TH1F* QCD_old        = (TH1F*) f1->Get(postfit_name + "QCD");
  TH1F* background_old = (TH1F*) f1->Get(postfit_name + "total_background");
  
  TString data_name;
  if (year == "2022")
    data_name = "histograms/ReRecoData2022";
  else if (year == "2023")
    data_name = "histograms/PromptData2023";
  TH1D* Data       = (TH1D*) f2->Get(data_name);

  const int nBins = Data->GetNbinsX();
  float Xmin = Data->GetXaxis()->GetXmin();
  float Xmax = Data->GetXaxis()->GetXmax();

  std::vector<float> binCenters;
  std::vector<float> binWidths;
  for (int i = 0; i < nBins; i++) {
    binCenters.push_back(Data->GetXaxis()->GetBinCenter(i+1));
    binWidths.push_back(Data->GetXaxis()->GetBinWidth(i+1));
  }

  // Rebin postfit histos to original binning
  TH1F* W_boson    = RebinHisto(W_boson_old, Data, "W_boson_new");
  TH1F* Top        = RebinHisto(Top_old, Data, "Top_new");
  TH1F* Z_boson    = RebinHisto(Z_boson_old, Data, "Z_boson_new");
  TH1F* DiBoson    = RebinHisto(DiBoson_old, Data, "DiBoson_new");
  TH1F* QCD        = RebinHisto(QCD_old, Data, "QCD_new");
  TH1F* background = RebinHisto(background_old, Data, "background_new");

  /// Draw mT distribution with same style ///

  TCanvas* mT = new TCanvas("mT_postfit","",602,676);
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
  bkg->GetXaxis()->SetTitle(Data->GetXaxis()->GetTitle());
  bkg->GetYaxis()->SetTitle(Data->GetYaxis()->GetTitle());
  float xLabelSize = bkg->GetXaxis()->GetLabelSize();
  float xTitleSize = bkg->GetXaxis()->GetTitleSize();
  bkg->GetXaxis()->SetLabelSize(0);
  bkg->GetXaxis()->SetTitleSize(0);
  bkg->SetMinimum(ylow);
  bkg->SetMaximum(yup);
  bkg->GetXaxis()->SetRangeUser(Xmin, Xmax);
  bkg->Draw("hist");

  // Obtain full systematic band
  TGraphAsymmErrors* systBand = SystRatioPlot(background, binCenters);

  // Graph for syst band in stack
  TGraphAsymmErrors* systGraph = new TGraphAsymmErrors();
  systGraph->SetName("systBandGraph");
  systGraph->SetFillColor(kGray+2);
  systGraph->SetFillStyle(3002);
  systGraph->SetLineWidth(1);
  systGraph->SetLineColor(kGray+2);

  for (size_t i = 0; i < binCenters.size(); i++) {
    double x = binCenters.at(i);
    double xErr = binWidths.at(i) / 2.0;

    double y = background->GetBinContent(i+1);
    double yErrUp = systBand->GetErrorYhigh(i) * y;
    double yErrDown = systBand->GetErrorYlow(i) * y;

    systGraph->SetPoint(i, x, y);
    systGraph->SetPointError(i, xErr, xErr, yErrDown, yErrUp);
  }
  systGraph->Draw("2 SAME");

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
  ydown_up = 4.0;
  auto frame = down->DrawFrame(Xmin, ydown_low, Xmax, ydown_up);
  frame->GetYaxis()->SetTitle("Data / MC");
  frame->GetYaxis()->SetTitleSize(bkg->GetYaxis()->GetTitleSize()*2.0);
  frame->GetYaxis()->SetTitleOffset(0.6);
  frame->GetYaxis()->CenterTitle(true);
  frame->GetYaxis()->SetLabelSize(bkg->GetYaxis()->GetLabelSize()*1.9);
  frame->GetYaxis()->SetNdivisions(304);
  frame->GetXaxis()->SetTitle(Data->GetXaxis()->GetTitle());
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
  leg->AddEntry(Z_boson, "Z/#gamma* #rightarrow ll", "f");
  leg->AddEntry(QCD, "QCD", "f");
  leg->AddEntry(Top, "Top", "f");
  leg->AddEntry(DiBoson, "DiBoson", "f");
  leg->AddEntry(systBand, "Stat. + Syst.", "f");
  leg->AddEntry(Data, "Data", "lp");
  leg->AddEntry("", "", "");
  leg->AddEntry("", "", "");
  leg->Draw();

  string lumi;
  if (year == "2022")
    lumi = "34.7";
  else if (year == "2023")
    lumi = "27.2";
  TString title_left = "#bf{CMS} #it{Work in progress}";
  TLatex* preliminary_left = new TLatex(0.12,0.89, title_left);
  preliminary_left->SetNDC();
  preliminary_left->SetTextFont(42);
  preliminary_left->SetTextSize(0.045);
  preliminary_left->Draw();
  
  TString title_right = year +", "+ lumi +" fb^{-1}  (13.6 TeV)";
  TLatex* preliminary_right = new TLatex(0.56,0.89, title_right);
  preliminary_right->SetNDC();
  preliminary_right->SetTextFont(42);
  preliminary_right->SetTextSize(0.045);
  preliminary_right->Draw();

  /// Save plots ///
  string fitTypeName;
  if (bkgOnlyFit)
    fitTypeName = "_B-only";
  else
    fitTypeName = "_S+B";
  if (savePlots){
    mT->SaveAs(("plots/PostFitPlots/mT_"+ year + fitTypeName + "_NjetsGT0_PostFit.png").c_str());
    mT->SaveAs(("plots/PostFitPlots/mT_"+ year + fitTypeName + "_NjetsGT0_PostFit.pdf").c_str());
  }
  
}// End of main


void PostFitDistributions(){

  //PostFitPlot("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/checks/GoF/fullCuts/fitDiagnostics_muon22.root", true, "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SSMlimit_fullCuts/root/mT__pg_SSMlimits2022.root", "2022", true);
  PostFitPlot("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/checks/GoF/fullCuts/fitDiagnostics_NjetsGT0_muon22.root", true, "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/feedback22Jul_mT_pT_MET-v3/root/mT_jets__pg_SSMlimits2022.root", "2022", true);

  //PostFitPlot("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/checks/GoF/fullCuts/fitDiagnostics_muon23.root", false, "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/SSMlimit_fullCuts-v2/root/mT__pg_SSMlimits2023.root", "2023", true);

}


