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
#include <regex>
#include <filesystem>
#include <map>
namespace fs = std::filesystem;


void DrawEfficiencies(std::map<std::string, TEfficiency*> effs, std::vector<std::string> eff_order, std::string Wmass, bool save = true) {
    TCanvas* c = new TCanvas("signalEffs", "", 600, 500);
    c->cd();

    TLegend* legend = new TLegend(0.64, 0.60, 0.92, 0.85);
    legend->SetBorderSize(0);
    legend->SetFillStyle(0);
    legend->SetTextSize(0.03);

    int colorIndex = 1;
    bool first = true;

    for (const auto& name : eff_order) {
      if (name == "Ref")
	continue;
      TEfficiency* gr = effs[name];
      gr->SetLineColor(colorIndex);
      gr->SetMarkerColor(colorIndex);
      gr->SetMarkerStyle(20 + colorIndex);

      if (first) {
	gr->Draw("AP");
	gPad->Update();
	    
	TGraphAsymmErrors* painted = gr->GetPaintedGraph();
	if (painted){
	  painted->SetMaximum(1.03);
	  painted->SetMinimum(0.97);
	  painted->GetYaxis()->SetTitle("Efficiency");
	  painted->GetYaxis()->SetTitleOffset(1.3);
	  painted->GetXaxis()->SetTitle("m_{T}  [GeV]");
	  painted->GetXaxis()->SetTitleOffset(1.2);
	} else {
	  std::cerr << "Warning: Could not get PaintedGraph for TEfficiency." << std::endl;
	}
	first = false;
      } else {
	gr->Draw("P SAME");  // Draw on same canvas
      }

      legend->AddEntry(gr, name.c_str(), "apel");

      colorIndex++;
      if (colorIndex == 5 || colorIndex == 10) colorIndex++;
    }

    legend->Draw();
    
    TString title = "#bf{CMS} #it{Simulation}                                             2023 (13.6 TeV)";
    TLatex* preliminary = new TLatex(0.12,0.91, title);
    preliminary->SetNDC();
    preliminary->SetTextFont(42);
    preliminary->SetTextSize(0.04);
    preliminary->Draw("same");

    TPaveLabel *label = new TPaveLabel(0.17,0.70,0.37,0.79, Wmass.c_str(), "NDC");
    label->SetBorderSize(0);
    label->SetFillColor(0);
    label->SetFillStyle(0);
    label->SetTextSize(0.37);
    label->Draw();

    c->Update();
    if (save)
      c->SaveAs(("plots/AbsIso/Isolation_effs_"+ Wmass +".png").c_str());
}


void absIso_eff(std::string files, std::string Wmass){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  std::map<std::string, TFile*> data;
  std::map<std::string, TH1D*> hist;
  TH1D* h_ref;
  std::map<std::string, TEfficiency*> effs;
  std::vector<std::string> histnames;


  /// Reading all files ///
  
  for (const auto &file : fs::directory_iterator(files)){
    std::string filePath = file.path().string();
    //std::cout << filePath << std::endl;
    
    size_t loc1 = filePath.find("mT");
    size_t loc2 = filePath.find("__pg");

    if (loc1 != std::string::npos && loc2 != std::string::npos && loc2 > loc1) {
      std::string name = filePath.substr(loc1+3, loc2 - (loc1+3));
      histnames.push_back(name);
      //std::cout << name << std::endl;

      // Patch necessary to avoid ROOT from deleting the histos when closing the file
      TDirectory *current_dir = gDirectory;
      data[name] = TFile::Open(filePath.c_str());
      current_dir->cd();
      
      if (data[name] && !data[name]->IsZombie()) {
	hist[name] = dynamic_cast<TH1D*>(data[name]->Get(("histograms/" + Wmass).c_str())->Clone());
	if (hist[name]) {
	  //hist[name]->Draw();
	  std::cout << "Works!" << std::endl;
	} else {
	  std::cerr << "Histogram " << Wmass << " not found in file " << filePath << std::endl;
	}
	data[name]->Close();
      } else {
	std::cerr << "Failed to open file " << filePath << std::endl;
      }
    } else {
      std::cerr << "Filename does not match expected format: " << filePath << std::endl;
    }

  } // Loop over all files
  
  // Compute efficiencies for the different WPs, draw the canvas and save

  std::map<std::string, int> priority = {
    {"Ref", 0},
    {"RelIso", 1},
    {"Iso100", 2},
    {"Iso50", 3},
    {"Iso20", 4},
    {"Iso10", 5}
  };

  std::sort(histnames.begin(), histnames.end(), [&priority](const std::string& a, const std::string& b) {
    return priority[a] < priority[b];
  });

  h_ref = hist["Ref"];

  for (const auto& name : histnames) {
    if (name == "Ref")
      continue;
    
    effs[name] = new TEfficiency(*hist[name], *h_ref);
  }

  
  DrawEfficiencies(effs, histnames, Wmass, false);
  

} // End of main

void absIso_efficiencies(){

  /// Absolute Isolation Effs ///
  //absIso_eff("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/ChecksAbsIso-v5/root/", "Wprime2000");
  //absIso_eff("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/ChecksAbsIso-v5/root/", "Wprime3600");
  //absIso_eff("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/ChecksAbsIso-v5/root/", "Wprime5600");

  /// High-Purity Effs ///
  absIso_eff("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/W-boosted-CR_HP+Iso/root/", "QCD");
}
