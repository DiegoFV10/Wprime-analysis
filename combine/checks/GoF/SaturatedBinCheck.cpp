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
#include "TF1.h"
#include "TAxis.h"
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
#include "TLegend.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TColor.h"
#include "TLine.h"
#include "TLatex.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TGraphAsymmErrors.h"
#include "TKey.h"
#include "THStack.h"
#include "TPaveLabel.h"
#include <filesystem>
namespace fs = std::filesystem;


void GoFMultiChannel(TString postfit, TString dataMu22, TString dataMu23, TString dataEl22, TString dataEl23){

  TFile *fbkg = TFile::Open(postfit);
  
  std::vector<TString> channels = {"muon22", "muon23", "ele22", "ele23"};
  std::vector<TString> data_histnames = {"histograms/ReRecoData2022", "histograms/PromptData2023", "data_obs", "data_obs"};
  std::vector<TString> fileNames = {dataMu22, dataMu23, dataEl22, dataEl23};

  std::vector<TFile*> data_files;
  for (size_t i = 0; i < fileNames.size(); i++) {
    data_files.push_back(TFile::Open(fileNames.at(i), "READ"));
    if (!data_files.back()) {
      std::cerr << "Error opening file: " << fileNames.at(i) << std::endl;
      return;
    }
  }

  float GoF_total = 0.0;
  
  for (size_t ch = 0; ch < channels.size(); ch++) {
    
    cout << "Goodness of Fit for " << channels.at(ch) << " channel" << endl;
    
    TString bkg_histname = "shapes_fit_b/" + channels.at(ch) + "/total_background";

    TH1F* bkg_postfit = (TH1F*) fbkg->Get(bkg_histname);
    TH1F* data_hist   = (TH1F*) data_files.at(ch)->Get(data_histnames.at(ch));
    
    float GoF_channel = 0.0;
    std::vector<float> GoF_vect;
    std::vector<float> mT_vect;
    std::vector<float> binwidth;
    
    for (int bin = 0; bin < data_hist->GetNbinsX(); bin++){
      float GoF;
    
      float n_postfit = bkg_postfit->GetBinContent(bin+1);
      float n_data = data_hist->GetBinContent(bin+1);
      
      if(n_data > 0)
	GoF = 2*( (n_postfit - n_data) - n_data*log(n_postfit/n_data) );
      else
	GoF = 0;
      
      GoF_channel += GoF;
      GoF_vect.push_back(GoF);
      mT_vect.push_back(data_hist->GetXaxis()->GetBinCenter(bin+1));
      binwidth.push_back((data_hist->GetXaxis()->GetBinUpEdge(bin+1) - data_hist->GetXaxis()->GetBinLowEdge(bin+1))/2.0);
      cout << "  mT: [" << data_hist->GetXaxis()->GetBinLowEdge(bin+1) << ", " << data_hist->GetXaxis()->GetBinUpEdge(bin+1) << ") --> " << GoF << endl;

    } // Loop over histogram bins

    GoF_total += GoF_channel;
    cout << "Full channel " << channels.at(ch) << " --> " << GoF_channel << "\n" << endl;

    TGraphErrors* GoFbinned = new TGraphErrors(mT_vect.size(), &mT_vect[0], &GoF_vect[0], &binwidth[0], 0);

    TCanvas* c = new TCanvas("GoFbinBybin","",600,500);
    GoFbinned->SetMinimum(0.0);
    GoFbinned->SetMarkerStyle(20);
    GoFbinned->SetFillColor(kAzure+1);
    GoFbinned->GetYaxis()->SetTitle("GoF score");
    GoFbinned->GetYaxis()->SetTitleOffset(1.3);
    GoFbinned->GetXaxis()->SetRangeUser(200, 2000);
    GoFbinned->GetXaxis()->SetTitle("m_{T}  [GeV]");
    GoFbinned->GetXaxis()->SetTitleOffset(1.2);
    GoFbinned->SetTitle("GoF bin-by-bin" + channels.at(ch));
    GoFbinned->Draw("ABX");

    c->SaveAs("GoF_binned_" + channels.at(ch) + ".png");
    
  } // Loop over channels

  cout << "Total for all channels --> " << GoF_total << endl;

}




void GoFSingleChannel(string postfit, string data, string channel, string year){

  TFile *f1 = TFile::Open(postfit.c_str());
  TFile *f2 = TFile::Open(data.c_str());

  string bkg_histname;
  string data_histname;
  if(channel == "muon"){
    bkg_histname = "shapes_fit_b/muon_channel/total_background";
    if(year == "2022")
      data_histname = "histograms/ReRecoData2022";
    else if(year == "2023")
      data_histname = "histograms/PromptData2023";
  }
  else if (channel == "electron"){
    bkg_histname = "shapes_fit_b/channel/total_background";
    data_histname = "data_obs";
  }
  TH1F* bkg_postfit = (TH1F*) f1->Get(bkg_histname.c_str());
  TH1D* data_hist   = (TH1D*) f2->Get(data_histname.c_str());

  float GoF_cumulative = 0;
  std::vector<float> GoF_vect;
  std::vector<float> mT_vect;
  std::vector<float> binwidth;
  
  for(int bin = 0; bin < bkg_postfit->GetNbinsX(); bin++){

    float GoF;
    
    float n_postfit = bkg_postfit->GetBinContent(bin+1);
    float n_data = data_hist->GetBinContent(bin+1);

    if(n_data > 0)
      GoF = 2*( (n_postfit - n_data) - n_data*log(n_postfit/n_data) );
    else
      GoF = 0;
    
    GoF_cumulative += GoF;
    GoF_vect.push_back(GoF);
    mT_vect.push_back(data_hist->GetXaxis()->GetBinCenter(bin+1));
    binwidth.push_back((data_hist->GetXaxis()->GetBinUpEdge(bin+1) - data_hist->GetXaxis()->GetBinLowEdge(bin+1))/2.0);
    cout << "  mT: [" << data_hist->GetXaxis()->GetBinLowEdge(bin+1) << ", " << data_hist->GetXaxis()->GetBinUpEdge(bin+1) << ") --> " << GoF << endl;
   
  }
  cout << "Full Poisson part --> " << GoF_cumulative << endl;

  TGraphErrors* GoFbinned = new TGraphErrors(mT_vect.size(), &mT_vect[0], &GoF_vect[0], &binwidth[0], 0);

  TCanvas* c = new TCanvas("GoFbinBybin","",600,500);
  GoFbinned->SetMinimum(0.0);
  GoFbinned->SetMarkerStyle(20);
  GoFbinned->SetFillColor(kAzure+1);
  GoFbinned->GetYaxis()->SetTitle("GoF score");
  GoFbinned->GetYaxis()->SetTitleOffset(1.3);
  GoFbinned->GetXaxis()->SetRangeUser(400, 7000);
  GoFbinned->GetXaxis()->SetTitle("m_{T}  [GeV]");
  GoFbinned->GetXaxis()->SetTitleOffset(1.2);
  if(year == "2022")
    GoFbinned->SetTitle("GoF bin-by-bin muon 2022");
  else if(year == "2023")
    GoFbinned->SetTitle("GoF bin-by-bin muon 2023");
  GoFbinned->Draw("ABX");

  c->SaveAs(("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/checks/GoF/fullCuts/GoF_binned_" + channel + year + ".png").c_str());
}

void SaturatedBinCheck(){

  //GoFSingleChannel("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/checks/GoF/mT200_eta2.0/fitDiagnostics_BkgFit_muon22.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SSMlimit_PreAppFeedback/root/mT_GoF_200_eta2.0__pg_SSMlimits2022.root", "muon", "2022");
  //GoFSingleChannel("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/checks/GoF/mT200_eta2.0/fitDiagnostics_BkgFit_muon23.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/SSMlimit_PreAppFeedback/root/mT_GoF_200_eta2.0__pg_SSMlimits2023.root", "muon", "2023");
  //GoFSingleChannel("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/checks/fitDiagnostics_electron_2022.root", "/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/checks/histograms_mW_1000_lumi_34.653.root", "electron");
  //GoFSingleChannel("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/checks/GoF/fullCuts/fitDiagnostics_muon22.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SSMlimit_fullCuts/root/mT__pg_SSMlimits2022.root", "muon", "2022");
  GoFSingleChannel("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/checks/GoF/fullCuts/fitDiagnostics_muon23.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/SSMlimit_fullCuts-v2/root/mT__pg_SSMlimits2023.root", "muon", "2023");
  
  //GoFMultiChannel("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/checks/GoF/mT200/fitDiagnostics_BkgFit_combination.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SSMlimit_mT200_PreAppFinal/root/mT_GoF__pg_SSMlimits2022.root", "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/SSMlimit_mT200_PreAppFinal/root/mT_GoF__pg_SSMlimits2023.root", "histograms_mW_2000_lumi_34.653.root", "histograms_mW_2000_lumi_27.862.root");
  
}
