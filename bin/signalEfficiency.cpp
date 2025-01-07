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
#include "TEfficiency.h"
#include "TGraphAsymmErrors.h"
#include <filesystem>
namespace fs = std::filesystem;


void computeEff(string dirname, string rootfile, string histName, string year, bool combine = false){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  std::vector<string> masses = {"200", "400", "600", "1000", "1600", "2000", "2600", "3000", "3600", "4000", "4600", "5000", "5600", "6000", "6600"};

  std::vector<float> nSigTotal;
  if(year == "2022")
    nSigTotal = {48524.0, 49269.0, 50000.0, 49269.0, 50000.0, 47815.0, 50000.0, 50000.0, 48541.0, 50000.0, 50000.0, 50000.0, 48526.0, 49265.0, 49265.0};
  else if (year == "2023")
    nSigTotal = {75000.0, 75000.0, 75000.0, 75000.0, 71000.0, 75000.0, 75000.0, 75000.0, 75000.0, 73000.0, 75000.0, 75000.0, 75000.0, 75000.0, 75000.0};

  std::vector<double> eff_values;
  std::vector<double> mass_values;
  std::vector<double> eff_errors;

  std::vector<double> eff_electron = {0.0, 0.448, 0.605, 0.701, 0.742, 0.751, 0.752, 0.742, 0.725, 0.705, 0.671, 0.654, 0.628, 0.616, 0.599};
  
  for(size_t i = 0; i < masses.size(); i++){

    float nSignal;
    float efficiency;
    double error;
    
    string period;
    if(year == "2022")
      period = "_postEE";
    else if (year == "2023")
      period = "_postBPix";

    string fileName_pre  = dirname + "Wprime" + masses.at(i) + rootfile;
    string fileName_post = dirname + "Wprime" + masses.at(i) + period + rootfile;

    TFile *f_pre  =  TFile::Open(fileName_pre.c_str());
    TFile *f_post =  TFile::Open(fileName_post.c_str());
    
    TH1D* hist_pre  = (TH1D*) f_pre->Get(histName.c_str());
    TH1D* hist_post = (TH1D*) f_post->Get(histName.c_str());

    nSignal = hist_pre->GetEntries() + hist_post->GetEntries();
    efficiency = nSignal/nSigTotal.at(i);
    error = efficiency*( sqrt(nSignal)/nSignal + sqrt(nSigTotal.at(i))/nSigTotal.at(i) );

    eff_values.push_back(efficiency);
    mass_values.push_back(std::stod(masses.at(i)));
    eff_errors.push_back(error);
    
    cout <<"Mass: "<<masses.at(i)<<" --> Eff: "<< efficiency << endl;
    
    f_pre->Close();
    f_post->Close();
    
  } // Loop over Wprime mass points

  /// Draw the Efficiency Graph ///
  TGraphErrors *signalEff = new TGraphErrors(mass_values.size(), &mass_values[0], &eff_values[0], 0, &eff_errors[0]);
  TGraphErrors *electronEff = new TGraphErrors(mass_values.size(), &mass_values[0], &eff_electron[0], 0, &eff_errors[0]);
  
  TCanvas *cEff = new TCanvas("cEff", "", 800, 600);
  signalEff->SetTitle("");
  signalEff->GetXaxis()->SetTitle("M_{W'} (GeV)");
  signalEff->GetXaxis()->SetTitleOffset(1.2);
  signalEff->GetXaxis()->SetRangeUser(0, 7000);
  signalEff->GetYaxis()->SetTitle("Acceptance #times Efficiency");
  signalEff->SetMinimum(0);
  signalEff->SetMaximum(1.0);
  signalEff->SetMarkerStyle(20);
  signalEff->SetMarkerSize(0.4);
  signalEff->SetMarkerColor(kBlue); // kAzure+1
  signalEff->SetLineColor(kBlue);
  signalEff->Draw("AP");
  if(combine){
    electronEff->SetMarkerStyle(20);
    electronEff->SetMarkerSize(0.4);
    electronEff->SetMarkerColor(kMagenta+1);
    electronEff->SetLineColor(kMagenta+1);
    electronEff->Draw("P SAME");
  }

  float yleg = 0.80;
  if(combine)
    yleg = 0.75;

  TLegend* leg = new TLegend(0.70, yleg, 0.88, 0.85);
  leg->AddEntry(signalEff, "W' #rightarrow #mu#nu", "lep");
  if(combine)
    leg->AddEntry(electronEff, "W' #rightarrow e#nu", "lep");
  leg->SetBorderSize(0);
  leg->Draw();

  TString title1;
  TString title2;
  title1 = "#splitline{#bf{CMS}}{#it{Work in progress}}";
  title2 = year + " (13.6 TeV)";

  TLatex* preliminary1 = new TLatex(0.13, 0.83, title1);
  preliminary1->SetNDC();
  preliminary1->SetTextFont(42);
  preliminary1->SetTextSize(0.04);
  preliminary1->Draw();
  TLatex* preliminary2 = new TLatex(0.70, 0.92, title2);
  preliminary2->SetNDC();
  preliminary2->SetTextFont(42);
  preliminary2->SetTextSize(0.04);
  preliminary2->Draw();

  // Save plot
  if(combine)
    cEff->SaveAs(("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/bin/plots/SignalEff/SignalEfficiency"+ year +"_EleMu.png").c_str());
  else
    cEff->SaveAs(("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/bin/plots/SignalEff/SignalEfficiency"+ year +".png").c_str());
}

void signalEfficiency(){

  computeEff("/eos/user/d/diegof/cmt/PrePlot/Wprime_2022_config/", "/cat_preselection/kinSelection_NewColors_T1MET/data_0.root", "muon_eta", "2022");
  computeEff("/eos/user/d/diegof/cmt/PrePlot/Wprime_2023_config/", "/cat_preselection/kinSelection_NewColors_T1MET/data_0.root", "muon_eta", "2023");

  // Plot in same canvas muon & electron
  computeEff("/eos/user/d/diegof/cmt/PrePlot/Wprime_2022_config/", "/cat_preselection/kinSelection_NewColors_T1MET/data_0.root", "muon_eta", "2022", true);
}


