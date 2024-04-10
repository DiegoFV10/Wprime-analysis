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


void compare(string MCfile, string hist, string label, string name){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  TFile *f1 =  TFile::Open((MCfile + hist).c_str());

  TH1D* histA = (TH1D*) f1->Get("histograms/Wonshell_postEE");
  TH1D* histB = (TH1D*) f1->Get("histograms/Wboost_postEE");
  TH1D* histC = (TH1D*) f1->Get("histograms/W+4j_postEE");

  // Compute MC ratio of W+2j vs HT-binned
  TH1D* rateA = (TH1D*)histA->Clone("rateA");
  rateA->Divide(histB);

  // Compute MC ratio of W+4j vs HT-binned
  TH1D* rateB = (TH1D*)histC->Clone("rateB");
  rateB->Divide(histB);

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
  float xlow = 100;
  float xup = 1000;
  float ylow = 1E0;
  float yup = histA->GetMaximum()*5;
  if(histB->GetMaximum() > histA->GetMaximum())
    yup = histB->GetMaximum()*5;

  up->cd();
  up->SetLogy();
  histB->GetXaxis()->SetTitle((label+"  [GeV]").c_str());
  histB->SetMinimum(ylow);
  histB->SetMaximum(yup);
  histB->SetLineColor(2);
  histB->SetLineWidth(2);
  histB->GetXaxis()->SetRangeUser(xlow, xup);
  histB->Draw("hist");
  histA->SetLineColor(1);
  histA->SetLineWidth(2);
  histA->Draw("same");
  //histC->SetLineColor(4);
  //histC->SetLineWidth(2);
  //histC->Draw("same");

  // Draw ratio plot (lower panel)
  down ->cd();
  auto frame = down->DrawFrame(xlow, 0.25, xup, 1.75);
  frame->GetYaxis()->SetTitle("inclusive / HT-binned");
  frame->GetYaxis()->SetTitleSize(histA->GetYaxis()->GetTitleSize()*2.0);
  frame->GetYaxis()->SetTitleOffset(0.6);
  frame->GetYaxis()->CenterTitle(true);
  frame->GetYaxis()->SetLabelSize(histA->GetYaxis()->GetLabelSize()*1.9);
  frame->GetYaxis()->SetNdivisions(304);
  frame->GetXaxis()->SetTitle((label+"  [GeV]").c_str());
  frame->GetXaxis()->SetTickLength(histA->GetYaxis()->GetTickLength()*1.8);
  frame->GetXaxis()->SetTitleSize(histA->GetXaxis()->GetTitleSize()*2.4);
  frame->GetXaxis()->SetTitleOffset(1.2);
  frame->GetXaxis()->SetLabelSize(histA->GetXaxis()->GetLabelSize()*1.9);

  rateA->SetMarkerStyle(20);
  rateA->SetMarkerColor(1);
  rateA->SetLineColor(1);
  rateA->SetMarkerSize(0.8);
  rateA->Draw("AP SAME");

  //rateB->SetMarkerStyle(20);
  //rateB->SetMarkerColor(4);
  //rateB->SetLineColor(4);
  //rateB->SetMarkerSize(0.8);
  //rateB->Draw("AP SAME");

  TLine* lmid = new TLine(xlow, 1.0, xup, 1.0);
  lmid->SetLineStyle(3);
  lmid->Draw("SAME");
  TLine* lbot = new TLine(xlow, 0.5, xup, 0.5);
  lbot->SetLineStyle(3);
  lbot->Draw("SAME");
  TLine* ltop = new TLine(xlow, 1.5, xup, 1.5);
  ltop->SetLineStyle(3);
  ltop->Draw("SAME");

  // Set legend and title
  up->cd();
  TLegend * leg = new TLegend(0.65, 0.65, 0.9, 0.8);
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetTextSize(0.034);
  leg->AddEntry(histA, "W+2j amc@nlo", "apel");
  leg->AddEntry(histB, "W+4j HT-binned", "apel");
  //leg->AddEntry(histC, "W+4j inclsuive", "apel");
  leg->Draw();

  TString title = "#bf{CMS} #it{Simulation}                                    2022 postEE (13.6 TeV)";
  TLatex* preliminary = new TLatex(0.12,0.89, title);
  preliminary->SetNDC();
  preliminary->SetTextFont(42);
  preliminary->SetTextSize(0.045);
  preliminary->Draw();


  /// Save Plot ///
  //c_rate->SaveAs(("plots/MCvsMC/"+ name +"_inclusiveVSbinned_postEE_All.png").c_str());

  /// Save k-factors ///
  for(int i = 0; i < rateA->GetNbinsX(); i++){
    if(histA->GetBinLowEdge(histA->GetBin(i+1)) >= 100 && histA->GetBinLowEdge(histA->GetBin(i+1)) <= 1000 )
      cout << "HT: " << histA->GetBinLowEdge(histA->GetBin(i+1)) << " k-factor: " << rateA->GetBinContent(i+1) << " +- " << rateA->GetBinError(i+1) << endl;
  }

  

}// End of main 

void MCtoMCcomparison(){

  compare("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/Wboost_comparison_postEE_LOtoNNLO/root/","lhe_HT_tail__pg_inclusiveVShtbinned.root","lhe HT","lhe_HT");
  //compare("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/Wboost_comparison_postEE_All/root/","genJet_HT_tail__pg_inclusiveVShtbinned.root","GenJet HT","genJet_HT");
  
  //compare("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/Wboost_comparison_postEE_All/root/","lhe_Wpt__pg_inclusiveVShtbinned.root","lhe W p_{T}","lhe_Wpt");
  //compare("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/Wboost_comparison_postEE_All/root/","lhe_muonPt__pg_inclusiveVShtbinned.root","lhe #mu p_{T}","lhe_muonPt");
  //compare("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/Wboost_comparison_postEE_All/root/","lhe_nuPt__pg_inclusiveVShtbinned.root","lhe #nu p_{T}","lhe_nuPt");
  //compare("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/Wboost_comparison_postEE_All/root/","lhe_mT__pg_inclusiveVShtbinned.root","lhe m_{T}","lhe_mT");
  
}


