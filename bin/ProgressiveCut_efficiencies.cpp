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


void DrawEfficiencies(std::map<std::string, TH1D*> hist, std::map<std::string, TEfficiency*> effs, std::vector<std::string> eff_order, std::string histName, bool save = true) {

    // Define the ratio canvas
    TCanvas* c_rate = new TCanvas("effs","",602,676);
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

    TLegend* legend = new TLegend(0.56, 0.57, 0.88, 0.81);
    legend->SetBorderSize(0);
    legend->SetFillStyle(0);
    legend->SetTextSize(0.033);

    int colorIndex = 0;
    bool first = true;
    std::vector<Color_t> colors = {kBlack, kP10Green, kP10Orange};
    
    // Draw upper panel
    bool logY = true;
    float xlow, xup;
    if (histName == "ReRecoData2022") {
      xlow = 400;
      xup = 2000;
    }
    else {
      xlow = hist["ref"]->GetXaxis()->GetXmin();
      xup = hist["ref"]->GetXaxis()->GetXmax();
    }
    float ylow;
    if (histName == "ReRecoData2022")
      ylow = 2E-1;
    else
      ylow = 2E-6;
    float hmax = 1.0;
    if (logY)
      hmax = 10;
    float yup = hist["ref"]->GetMaximum()*hmax;
    
    up->cd();
    if (logY)
      up->SetLogy();
    hist["ref"]->GetXaxis()->SetTitle("m_{T}  [GeV]");
    hist["ref"]->SetMinimum(ylow);
    hist["ref"]->SetMaximum(yup);
    hist["ref"]->SetLineColor(kAzure);
    hist["ref"]->SetFillColor(kAzure+1);
    hist["ref"]->SetFillStyle(3002);
    hist["ref"]->SetLineWidth(2);
    if (histName == "ReRecoData2022")
      hist["ref"]->GetXaxis()->SetRangeUser(400, 2000);
    else
      hist["ref"]->GetXaxis()->SetRangeUser(xlow, xup);
    hist["ref"]->Draw("hist");

    // Draw ratio plot (lower panel)
    down ->cd();
    float ydown_low, ydown_up;
    ydown_low = 0.0;
    ydown_up = 1.25;
      
    auto frame = down->DrawFrame(xlow, ydown_low, xup, ydown_up);
    frame->GetYaxis()->SetTitle("Cuts / Reference");
    frame->GetYaxis()->SetTitleSize(hist["ref"]->GetYaxis()->GetTitleSize()*2.0);
    frame->GetYaxis()->SetTitleOffset(0.6);
    frame->GetYaxis()->CenterTitle(true);
    frame->GetYaxis()->SetLabelSize(hist["ref"]->GetYaxis()->GetLabelSize()*1.9);
    frame->GetYaxis()->SetNdivisions(304);
    frame->GetXaxis()->SetTitle(hist["ref"]->GetXaxis()->GetTitle());
    frame->GetXaxis()->SetTickLength(hist["ref"]->GetYaxis()->GetTickLength()*1.8);
    frame->GetXaxis()->SetTitleSize(hist["ref"]->GetXaxis()->GetTitleSize()*2.4);
    frame->GetXaxis()->SetTitleOffset(1.2);
    frame->GetXaxis()->SetLabelSize(hist["ref"]->GetXaxis()->GetLabelSize()*1.9);
    
    for (const auto& name : eff_order) {
      if (name == "ref")
	continue;

      up->cd();
      hist[name]->SetLineColor(colors.at(colorIndex));
      hist[name]->SetMarkerColor(colors.at(colorIndex));
      hist[name]->SetMarkerStyle(20 + colorIndex);
      hist[name]->SetLineWidth(2);
      //      if (histName == "ReRecoData2022")
	hist[name]->Draw("same");
	//      else
	//	hist[name]->Draw("hist same");

      // Draw ratio plot (lower panel)
      down ->cd();
      TEfficiency* gr = effs[name];
      gr->SetLineColor(colors.at(colorIndex));
      gr->SetMarkerColor(colors.at(colorIndex));
      gr->SetMarkerStyle(20 + colorIndex);
      gr->Draw("P SAME");


      /*
      if (first) {
	gr->Draw("AP");
	gPad->Update();
	    
	TGraphAsymmErrors* painted = gr->GetPaintedGraph();
	if (painted){
	  painted->SetMaximum(1.2);
	  painted->SetMinimum(0.5);
	  if (histName == "ReRecoData2022") {
	    painted->GetXaxis()->SetRangeUser(400, 2000);
	  }
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
      */

      TString legName;
      if (name == "etaCut")
	legName = "|#eta| < 2.0";
      else if (name == "etaHPcut")
	legName = "|#eta| < 2.0 + HP";
      else if (name == "etaHPmetNoMuCut")
	legName = "|#eta| < 2.0 + HP + MET-#mu";
      legend->AddEntry(gr, legName, "apel");

      TLine* lmid = new TLine(xlow, 1.0, xup, 1.0);
      lmid->SetLineStyle(3);
      lmid->Draw("SAME");
      TLine* lbot = new TLine(xlow, 1.0-(1.0-ydown_low)/2.0, xup, 1.0-(1.0-ydown_low)/2.0);
      lbot->SetLineStyle(3);
      lbot->Draw("SAME");
      TLine* ltop = new TLine(xlow, 1.0+(1.0-ydown_low)/2.0, xup, 1.0+(1.0-ydown_low)/2.0);
      ltop->SetLineStyle(3);
      ltop->Draw("SAME");
      
      colorIndex++;
      if (colorIndex == 5 || colorIndex == 10) colorIndex++;
    }
    
    // Set legend and title
    up->cd();
    legend->AddEntry(hist["ref"], "Reference", "f");
    legend->Draw();
    
    TString title;
    if (histName == "ReRecoData2022")
      title = "#bf{CMS} #it{Private Work}                                       2022, 34.7 fb^{-1} (13.6 TeV)";
    else
      title = "#bf{CMS} #it{Simulation}                                                       2022 (13.6 TeV)";
    TLatex* preliminary = new TLatex(0.12,0.89, title);
    preliminary->SetNDC();
    preliminary->SetTextFont(42);
    preliminary->SetTextSize(0.04);
    preliminary->Draw("same");

    TString hist_string = histName;
    if (histName == "ReRecoData2022")
      hist_string = "2022 Data";
    TPaveLabel *label = new TPaveLabel(0.20,0.70,0.40,0.79, hist_string, "NDC");
    label->SetBorderSize(0);
    label->SetFillColor(0);
    label->SetFillStyle(0);
    label->SetTextSize(0.45);
    label->Draw();

    c_rate->Update();
    if (save)
      c_rate->SaveAs(("plots/HighPurity/ProgressiveCuts_effs_"+ histName +".png").c_str());
}


void efficiencies(std::string files, std::string histName){
    
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
	hist[name] = dynamic_cast<TH1D*>(data[name]->Get(("histograms/" + histName).c_str())->Clone());

	// Rebin QCD
	if (histName == "QCD")
	  hist[name] = (TH1D*) hist[name]->Rebin(4);
	
	if (hist[name]) {
	  //hist[name]->Draw();
	  std::cout << "Works!" << std::endl;
	} else {
	  std::cerr << "Histogram " << histName << " not found in file " << filePath << std::endl;
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
    {"ref", 0},
    {"etaCut", 1},
    {"etaHPcut", 2},
    {"etaHPmetNoMuCut", 3}
  };

  std::sort(histnames.begin(), histnames.end(), [&priority](const std::string& a, const std::string& b) {
    return priority[a] < priority[b];
  });

  h_ref = hist["ref"];

  for (const auto& name : histnames) {
    if (name == "ref")
      continue;
    
    effs[name] = new TEfficiency(*hist[name], *h_ref);
  }

  
  DrawEfficiencies(hist, effs, histnames, histName, true);
  

} // End of main

void ProgressiveCut_efficiencies(){

  //efficiencies("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/progressiveCuts_EXO17Jun/root/", "ReRecoData2022");
  efficiencies("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/progressiveCuts_EXO17Jun/root/", "QCD");
  //efficiencies("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/progressiveCuts_EXO17Jun/root/", "W_boson");
  //efficiencies("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/progressiveCuts_EXO17Jun/root/", "Top");
  //efficiencies("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/progressiveCuts_EXO17Jun/root/", "Z_boson");
  //efficiencies("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/progressiveCuts_EXO17Jun/root/", "DiBoson");
  //efficiencies("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/progressiveCuts_EXO17Jun/root/", "Wprime2000");
  //efficiencies("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/progressiveCuts_EXO17Jun/root/", "Wprime3600");
  //efficiencies("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/progressiveCuts_EXO17Jun/root/", "Wprime5600");
  
}
