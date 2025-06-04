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


void cumulative(string original, string year, string runPeriod=""){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  TFile *f1 =  TFile::Open(original.c_str());
  // Original histos
  /*
  TH1D* Wprime2000_orig     = (TH1D*) f1->Get("histograms/Wprime2000");
  TH1D* Wprime3600_orig     = (TH1D*) f1->Get("histograms/Wprime3600");
  TH1D* Wprime5600_orig     = (TH1D*) f1->Get("histograms/Wprime5600");
  */
  TH1D* W_boson_orig        = (TH1D*) f1->Get("histograms/W_boson");           
  TH1D* Top_orig            = (TH1D*) f1->Get("histograms/Top");
  TH1D* Z_boson_orig        = (TH1D*) f1->Get("histograms/Z_boson");
  TH1D* DiBoson_orig        = (TH1D*) f1->Get("histograms/DiBoson");
  TH1D* QCD_orig            = (TH1D*) f1->Get("histograms/QCD");
  TString data_name;
  if (year == "2022")
    data_name = "histograms/ReRecoData2022";
  else if (year == "2023")
    data_name = "histograms/PromptData2023";
  TH1D* Data_orig           = (TH1D*) f1->Get(data_name);
  TH1D* background_orig     = (TH1D*) f1->Get("histograms/background");

  const int nBins  = W_boson_orig->GetNbinsX();
  float Xmin = W_boson_orig->GetXaxis()->GetXmin();
  float Xmax = W_boson_orig->GetXaxis()->GetXmax();

  // New cumulative histos
  /*
  TH1D* Wprime2000     = new TH1D("", "", nBins, Xmin, Xmax);
  TH1D* Wprime3600     = new TH1D("", "", nBins, Xmin, Xmax);
  TH1D* Wprime5600     = new TH1D("", "", nBins, Xmin, Xmax);
  */
  TH1D* W_boson        = new TH1D("", "", nBins, Xmin, Xmax);
  TH1D* Top            = new TH1D("", "", nBins, Xmin, Xmax);
  TH1D* Z_boson        = new TH1D("", "", nBins, Xmin, Xmax);
  TH1D* DiBoson        = new TH1D("", "", nBins, Xmin, Xmax);
  TH1D* QCD            = new TH1D("", "", nBins, Xmin, Xmax);
  TH1D* Data           = new TH1D("", "", nBins, Xmin, Xmax);
  TH1D* background     = new TH1D("", "", nBins, Xmin, Xmax);

  // Vectors with bin contents
  Float_t Wp2000_new[nBins], Wp3600_new[nBins], Wp5600_new[nBins], W_new[nBins], Top_new[nBins];
  Float_t Z_new[nBins], VV_new[nBins], QCD_new[nBins], Data_new[nBins], bkg_new[nBins];

  // Fill cumulative histos from the original ones
  for (int i = 0; i < nBins; i++){

    Wp2000_new[i] = 0;
    Wp3600_new[i] = 0;
    Wp5600_new[i] = 0;
    W_new[i]      = 0;
    Top_new[i]    = 0;
    Z_new[i]      = 0;
    VV_new[i]     = 0;
    QCD_new[i]    = 0;
    Data_new[i]   = 0;
    bkg_new[i]    = 0;

    for (int j = i; j < nBins; j++){
      /*
      Wp2000_new[i] += Wprime2000_orig->GetBinContent(j+1);
      Wp3600_new[i] += Wprime3600_orig->GetBinContent(j+1);
      Wp5600_new[i] += Wprime5600_orig->GetBinContent(j+1);
      */
      W_new[i]      += W_boson_orig->GetBinContent(j+1);
      Top_new[i]    += Top_orig->GetBinContent(j+1);
      Z_new[i]      += Z_boson_orig->GetBinContent(j+1);
      VV_new[i]     += DiBoson_orig->GetBinContent(j+1);
      QCD_new[i]    += QCD_orig->GetBinContent(j+1);
      Data_new[i]   += Data_orig->GetBinContent(j+1);
      bkg_new[i]    += background_orig->GetBinContent(j+1);

    } // Loop over original bins to be added
    /*
    Wprime2000    ->SetBinContent(i+1, Wp2000_new[i]);
    Wprime3600    ->SetBinContent(i+1, Wp3600_new[i]);
    Wprime5600    ->SetBinContent(i+1, Wp5600_new[i]);
    */
    W_boson       ->SetBinContent(i+1, W_new[i]);
    Top           ->SetBinContent(i+1, Top_new[i]);
    Z_boson       ->SetBinContent(i+1, Z_new[i]);
    DiBoson       ->SetBinContent(i+1, VV_new[i]);
    QCD           ->SetBinContent(i+1, QCD_new[i]);
    Data          ->SetBinContent(i+1, Data_new[i]);
    background    ->SetBinContent(i+1, bkg_new[i]);

    //// PRINT EVT. NUMBERS ////
    if(i == 6)
      cout << "mT > 1 TeV ==> # Obs. " << Data_new[i] << " / # Exp. " << bkg_new[i] << endl;
    if(i == 16)
      cout << "mT > 2 TeV ==> # Obs. " << Data_new[i] << " / # Exp. " << bkg_new[i] << endl;
    if(i == 26)
      cout << "mT > 3 TeV ==> # Obs. " << Data_new[i] << " / # Exp. " << bkg_new[i] << endl;   
    ////////////////////////////

  } // Loop over cumulative bins


  /// Draw cumulative plot with same style ///

  TCanvas* mT = new TCanvas("mT_cumulative","",602,676);
  mT->cd();
  mT->Draw();

  TPad* up = new TPad("","",0.0,0.36,1.0,1.0);
  TPad* down = new TPad("","",0.0,0.0,1.0,0.36);
  up->SetTopMargin(0.13);
  up->SetBottomMargin(0.0);
  up->Draw("SAME");
  down->SetTopMargin(0.0);
  down->SetBottomMargin(0.35);
  down->Draw("SAME");

  /// Draw upper panel with cumulative distribution
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
  bkg->GetXaxis()->SetTitle(W_boson_orig->GetXaxis()->GetTitle());
  bkg->GetYaxis()->SetTitle(W_boson_orig->GetYaxis()->GetTitle());
  bkg->SetMinimum(ylow);
  bkg->SetMaximum(yup);
  bkg->GetXaxis()->SetRangeUser(Xmin, Xmax);
  bkg->Draw("hist");

  // Draw Wprime signals
  /*
  Wprime2000->SetLineColor(Wprime2000_orig->GetLineColor());
  Wprime2000->Draw("same hist");
  Wprime3600->SetLineColor(Wprime3600_orig->GetLineColor());
  Wprime3600->Draw("same hist");
  Wprime5600->SetLineColor(Wprime5600_orig->GetLineColor());
  Wprime5600->Draw("same hist");
  */

  // Draw Data
  Data->SetMarkerStyle(Data_orig->GetMarkerStyle());
  Data->SetMarkerColor(Data_orig->GetMarkerColor());
  Data->SetMarkerSize(Data_orig->GetMarkerSize());
  Data->SetLineColor(Data_orig->GetLineColor());
  Data->SetBinErrorOption(Data_orig->GetBinErrorOption());
  Data->Draw("same PEZ");


  /// Draw lower panel with Data/MC ratio

  // Compute data to MC ratio
  TH1D* rate = (TH1D*)Data->Clone("rate");
  rate->Divide(background);
  for (int i = 0; i < nBins; i++){
    rate->SetBinError(i+1, Data->GetBinError(i+1)/background->GetBinContent(i+1) );
  }

  down ->cd();
  //  auto frame = down->DrawFrame(Xmin, 0.25, Xmax, 1.75);
  auto frame = down->DrawFrame(Xmin, 0.25, Xmax, 6.75);
  frame->GetYaxis()->SetTitle("Data / MC");
  frame->GetYaxis()->SetTitleSize(bkg->GetYaxis()->GetTitleSize()*2.0);
  frame->GetYaxis()->SetTitleOffset(0.6);
  frame->GetYaxis()->CenterTitle(true);
  frame->GetYaxis()->SetLabelSize(bkg->GetYaxis()->GetLabelSize()*1.9);
  frame->GetYaxis()->SetNdivisions(304);
  frame->GetXaxis()->SetTitle(W_boson_orig->GetXaxis()->GetTitle());
  frame->GetXaxis()->SetTickLength(bkg->GetYaxis()->GetTickLength()*1.8);
  frame->GetXaxis()->SetTitleSize(bkg->GetXaxis()->GetTitleSize()*2.4);
  frame->GetXaxis()->SetTitleOffset(1.2);
  frame->GetXaxis()->SetLabelSize(bkg->GetXaxis()->GetLabelSize()*1.9);

  rate->SetMarkerStyle(20);
  rate->SetMarkerColor(1);
  rate->SetLineColor(1);
  rate->SetMarkerSize(0.7);
  rate->Draw("SAME PEZ");


  TLine* lmid = new TLine(Xmin, 1.0, Xmax, 1.0);
  lmid->SetLineStyle(3);
  lmid->Draw("SAME");
  //  TLine* lbot = new TLine(Xmin, 0.5, Xmax, 0.5);
  TLine* lbot = new TLine(Xmin, 4.0, Xmax, 4.0);
  lbot->SetLineStyle(3);
  lbot->Draw("SAME");
  //  TLine* ltop = new TLine(Xmin, 1.5, Xmax, 1.5);
  TLine* ltop = new TLine(Xmin, 6.0, Xmax, 6.0);
  ltop->SetLineStyle(3);
  ltop->Draw("SAME");

  // Set legend and title
  up->cd();
  TLegend * leg = new TLegend(0.38, 0.64, 0.87, 0.87);
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetNColumns(3);
  /*
  leg->AddEntry(Wprime2000, "W' M_{W'} = 2.0 TeV", "l");
  leg->AddEntry(Wprime3600, "W' M_{W'} = 3.6 TeV", "l");
  leg->AddEntry(Wprime5600, "W' M_{W'} = 5.6 TeV", "l");
  */
  leg->AddEntry(W_boson, "W-boson", "f");
  leg->AddEntry(Top, "Top", "f");
  leg->AddEntry(Z_boson, "Z/#gamma* #rightarrow ll", "f");
  leg->AddEntry(DiBoson, "DiBoson", "f");
  leg->AddEntry(QCD, "QCD", "f");
  leg->AddEntry(Data, "Data", "lp");
  leg->Draw();

  string lumi;
  if (year == "2022"){
    if (runPeriod == "preEE")
      lumi = "8.1";
    else if (runPeriod == "postEE")
      lumi = "27.0";
    else if (runPeriod == "E")
      lumi = "5.8";
    else
      lumi = "34.7";
  }
  else if (year == "2023")
    lumi = "27.2";
  TString title = "#bf{CMS} #it{Private Work}                       "+ year + runPeriod + ", "+ lumi +" fb^{-1}  (13.6 TeV)";
  TLatex* preliminary = new TLatex(0.12,0.89, title);
  preliminary->SetNDC();
  preliminary->SetTextFont(42);
  preliminary->SetTextSize(0.045);
  preliminary->Draw();


  /// Save Plot ///
  //mT->SaveAs(("plots/cumulative/mT_cumulative_"+ year + runPeriod + ".png").c_str());

}// End of main 

void cumulativePlot(){

  //cumulative("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/Inaugural_kinselection_2022/root/mT__pg_2022ReReco.root", "2022");
  //cumulative("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/preEE_kinselection_allW_HTkfact-LOtoNNLO/root/mT__pg_2022ReReco_preEE.root", "2022", "_preEE");
  //cumulative("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/postEE_kinselection_allW_HTkfact-LOtoNNLO/root/mT__pg_2022ReReco_postEE.root", "2022", "_postEE");  
  //cumulative("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SSMlimit_mT400_Unblind_ext-NoSignal/root/mT_9TeV__pg_SSMlimits2022.root", "2022");
  //cumulative("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/mT_kinSel_preEE/root/mT_9TeV__pg_SSMlimits2022.root", "2022", "preEE");
  //cumulative("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/mT_kinSel_postEE/root/mT_9TeV__pg_SSMlimits2022.root", "2022", "postEE");
  //cumulative("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/mT_kinSel_eraE/root/mT_9TeV__pg_SSMlimits2022.root", "2022", "E");

  cumulative("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/SSMlimit_mT400_Unblind_NoSignal/root/mT__pg_SSMlimits2023.root", "2023");

}


