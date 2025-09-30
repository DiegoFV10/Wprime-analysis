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


void compare(string MCfile22, string MCfile23, string label, string name, string bkgComponent){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  TFile *f22 =  TFile::Open(MCfile22.c_str());
  TFile *f23 =  TFile::Open(MCfile23.c_str());
  
  TH1D* hist22 = (TH1D*) f22->Get(("histograms/" + bkgComponent).c_str());
  TH1D* hist23 = (TH1D*) f23->Get(("histograms/" + bkgComponent).c_str());

  //  hist22->Scale(1.0 / hist22->Integral());
  //  hist23->Scale(1.0 / hist23->Integral());

  hist22->Scale(27.2);
  hist23->Scale(34.7);

  // Compute MC ratio of 22 vs 23
  TH1D* rateA = (TH1D*) hist22->Clone("rateA");
  rateA->Divide(hist23);

  // Define ratio canvas
  TCanvas* c_rate = new TCanvas("MCvsMC","",602,676);
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
  float xlow = hist22->GetXaxis()->GetXmin();
  float xup = hist22->GetXaxis()->GetXmax();
  float ylow = 2E-2;
  float yup = hist22->GetMaximum()*5;
  if(hist23->GetMaximum() > hist22->GetMaximum())
    yup = hist23->GetMaximum()*5;

  up->cd();
  up->SetLogy();
  // Create error band for hist23
  TH1D* hist23_err = (TH1D*) hist23->Clone("hist23_err");
  hist23_err->SetFillColorAlpha(kRed, 0.1);
  hist23_err->SetFillStyle(3002);
  hist23_err->SetLineWidth(0);
  hist23_err->SetMarkerSize(0);
  hist23->GetXaxis()->SetTitle((label+"  [GeV]").c_str());
  hist23->SetMinimum(ylow);
  hist23->SetMaximum(yup);
  hist23->SetLineColor(2);
  hist23->SetLineWidth(2);
  hist23->SetFillStyle(0);
  hist23->GetXaxis()->SetRangeUser(xlow, xup);
  hist23->Draw("HIST SAME");
  hist23_err->Draw("E2 SAME");  // error band
  hist23->Draw("HIST SAME");
  
  // Create error band for hist22
  TH1D* hist22_err = (TH1D*) hist22->Clone("hist22_err");
  hist22_err->SetFillColorAlpha(kAzure+1, 0.35);
  hist22_err->SetFillStyle(3001);
  hist22_err->SetLineWidth(0);
  hist22_err->SetMarkerSize(0);
  hist22_err->Draw("E2 SAME");  // error band
  hist22->SetLineColor(kBlue);
  hist22->SetLineWidth(2);
  hist22->SetFillStyle(0);
  hist22->Draw("HIST SAME");

  // Draw ratio plot (lower panel)
  down ->cd();
  auto frame = down->DrawFrame(xlow, 0.0, xup, 2.0);
  //auto frame = down->DrawFrame(xlow, 0.8, xup, 1.2);
  frame->GetYaxis()->SetTitle("2022 / 2023");
  frame->GetYaxis()->SetTitleSize(hist22->GetYaxis()->GetTitleSize()*2.0);
  frame->GetYaxis()->SetTitleOffset(0.6);
  frame->GetYaxis()->CenterTitle(true);
  frame->GetYaxis()->SetLabelSize(hist22->GetYaxis()->GetLabelSize()*1.9);
  frame->GetYaxis()->SetNdivisions(304);
  frame->GetXaxis()->SetTitle((label+"  [GeV]").c_str());
  frame->GetXaxis()->SetTickLength(hist22->GetYaxis()->GetTickLength()*1.8);
  frame->GetXaxis()->SetTitleSize(hist22->GetXaxis()->GetTitleSize()*2.4);
  frame->GetXaxis()->SetTitleOffset(1.2);
  frame->GetXaxis()->SetLabelSize(hist22->GetXaxis()->GetLabelSize()*1.9);

  // Ratio error band (2022 / 2023)
  TH1D* ratioErr = (TH1D*) hist22->Clone("ratioErr");
  for (int i = 1; i <= ratioErr->GetNbinsX(); ++i) {
    double A = hist22->GetBinContent(i);
    double B = hist23->GetBinContent(i);
    double eA = hist22->GetBinError(i);
    double eB = hist23->GetBinError(i);

    if (B != 0) {
      double ratio = A / B;
      double error = ratio * sqrt((eA / A)*(eA / A) + (eB / B)*(eB / B));
      ratioErr->SetBinContent(i, ratio);
      ratioErr->SetBinError(i, error);
      //cout <<" bin "<<i << " 22: " << A << "+-" << eA << " 23: "<< B <<"+-"<< eB << " ratio: " << ratio <<"+-"<< error << endl;      
    } else {
      ratioErr->SetBinContent(i, 0);
      ratioErr->SetBinError(i, 0);
    }
  }
  ratioErr->SetFillColorAlpha(kGray+2, 0.35);
  ratioErr->SetFillStyle(3001);
  ratioErr->SetLineWidth(0);
  ratioErr->SetMarkerSize(0);
  ratioErr->Draw("E2 SAME");
  rateA->SetLineColor(1);
  rateA->SetFillStyle(0);
  rateA->Draw("HIST SAME");

  TLine* lmid = new TLine(xlow, 1.0, xup, 1.0);
  lmid->SetLineStyle(3);
  lmid->Draw("SAME");
  TLine* lbot = new TLine(xlow, 0.5, xup, 0.5);
  //TLine* lbot = new TLine(xlow, 0.9, xup, 0.9);
  lbot->SetLineStyle(3);
  lbot->Draw("SAME");
  TLine* ltop = new TLine(xlow, 1.5, xup, 1.5);
  //TLine* ltop = new TLine(xlow, 1.1, xup, 1.1);
  ltop->SetLineStyle(3);
  ltop->Draw("SAME");

  up->cd();
  TLegend * leg = new TLegend(0.55, 0.65, 0.8, 0.8); // (0.65. 0.65, 0.9, 0.8)
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetTextSize(0.034);
  leg->AddEntry(hist22, "MC 2022", "apel");
  leg->AddEntry(hist23, "MC 2023", "apel");
  leg->Draw("SAME");

  TString title = "#bf{CMS} #it{Simulation}                                                      (13.6 TeV)";
  TLatex* preliminary = new TLatex(0.12,0.89, title);
  preliminary->SetNDC();
  preliminary->SetTextFont(42);
  preliminary->SetTextSize(0.045);
  preliminary->Draw("SAME");

  /// Save Plot ///
  c_rate->SaveAs(("plots/MCvsMC/"+ name +"_22vs23_"+ bkgComponent +".png").c_str());

}// End of main 

void MCtoMCcomparison(){

  compare("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SSMlimit_fullCuts/root/mT__pg_SSMlimits2022.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/SSMlimit_fullCuts-v2/root/mT__pg_SSMlimits2023.root", "m_{T}", "mT", "background");
}


