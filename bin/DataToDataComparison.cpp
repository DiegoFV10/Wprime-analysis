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


void compare(std::string dataA_files, std::string name_dataA, std::string dataB_files, std::string name_dataB, int scaling){

  /// Scaling meaning:          ///
  /// 0 --> No scale            ///
  /// 1 --> Scale by Luminosity ///
  /// 2 --> Sacle by nEvents    ///
  
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  std::map<std::string, TFile*> dataA;
  std::map<std::string, TFile*> dataB;

  std::map<std::string, TH1D*> histA;
  std::map<std::string, TH1D*> histB;
  std::map<std::string, TH1D*> rates;

  std::vector<std::string> histnames;

  std::map<std::string, TCanvas*> c_rate;
  
  // Load the histograms for data A
  for (const auto &fileA : fs::directory_iterator(dataA_files)){
    std::string fileApath = fileA.path().string();
    //std::cout << fileApath << std::endl;
    size_t loc1 = fileApath.find("root");
    size_t loc2 = fileApath.find("__pg");

    if (loc1 != std::string::npos && loc2 != std::string::npos && loc2 > loc1) {
      std::string name = fileApath.substr(loc1+5, loc2 - (loc1+5));
      histnames.push_back(name);
      //std::cout << name << std::endl;

      // Patch necessary to avoid ROOT from deleting the histos when closing the file
      TDirectory *current_dir = gDirectory;
      dataA[name] = TFile::Open(fileApath.c_str());
      current_dir->cd();
      
      if (dataA[name] && !dataA[name]->IsZombie()) {
	histA[name] = dynamic_cast<TH1D*>(dataA[name]->Get(("histograms/" + name_dataA).c_str())->Clone());
	//histA[name] = (TH1D*) dataA[name]->Get(("histograms/" + name_dataA).c_str());
	if (histA[name]) {
	  //histA[name]->Draw();
	  std::cout << "Works!" << std::endl;
	} else {
	  std::cerr << "Histogram " << name_dataA << " not found in file " << fileApath << std::endl;
	}
	dataA[name]->Close();
      } else {
	std::cerr << "Failed to open file " << fileApath << std::endl;
      }
    } else {
      std::cerr << "Filename does not match expected format: " << fileApath << std::endl;
    }
    
  }
  
  // Load the histograms for data B
  int i = 0;
  for (const auto &fileB : fs::directory_iterator(dataB_files)){
    std::string fileBpath = fileB.path().string();
    //std::cout << fileBpath << std::endl;
    size_t loc1 = fileBpath.find("root");
    size_t loc2 = fileBpath.find("__pg");

    if (loc1 != std::string::npos && loc2 != std::string::npos && loc2 > loc1) {
      std::string name = fileBpath.substr(loc1+5, loc2 - (loc1+5));
      if(name != histnames.at(i)){
	std::cout << "ERROR! Histos from files A and B don't match" << std::endl;
	break;
      }

      // Patch necessary to avoid ROOT from deleting the histos when closing the file
      TDirectory *current_dir = gDirectory;
      dataB[name] = TFile::Open(fileBpath.c_str());
      current_dir->cd();
      
      if (dataB[name] && !dataB[name]->IsZombie()) {
	histB[name] = dynamic_cast<TH1D*>(dataB[name]->Get(("histograms/" + name_dataB).c_str())->Clone());
	if (histB[name]) {
	  //histB[name]->Draw();
	  std::cout << "Works!" << std::endl;
	} else {
	  std::cerr << "Histogram " << name_dataB << " not found in file " << fileBpath << std::endl;
	}
	dataB[name]->Close();
      } else {
	std::cerr << "Failed to open file " << fileBpath << std::endl;
      }
    } else {
      std::cerr << "Filename does not match expected format: " << fileBpath << std::endl;
    }
    i++;
    
  }
  
  // Create the rate for the different variables, draw the canvas and save
  
  TString title = "#bf{CMS} #it{Private Work}             2022 + 2023, 34.7 + 27.1 fb^{-1} (13.6 TeV)";
  TLatex* preliminary = new TLatex(0.12,0.89, title);
  preliminary->SetNDC();
  preliminary->SetTextFont(42);
  preliminary->SetTextSize(0.042);
  
  for (size_t var = 0; var < histnames.size(); var++){
    std::cout << histnames.at(var) <<  std::endl;

    // Apply scaling to histos if specified
    if (scaling == 1){
      histA[histnames.at(var)]->Scale(27.1);
      histB[histnames.at(var)]->Scale(34.7);
    } else if (scaling == 2){
      histA[histnames.at(var)]->Scale(1.0/histA[histnames.at(var)]->Integral());
      histB[histnames.at(var)]->Scale(1.0/histB[histnames.at(var)]->Integral());
    }

    // Compute the data-to-data ratio
    rates[histnames.at(var)] = (TH1D*) histA[histnames.at(var)]->Clone();
    rates[histnames.at(var)]->Divide(histB[histnames.at(var)]);

    // Define the ratio canvas
    c_rate[histnames.at(var)] = new TCanvas(histnames.at(var).c_str(),"",602,676);
    c_rate[histnames.at(var)]->cd();
    c_rate[histnames.at(var)]->Draw();

    TPad* up = new TPad("","",0.0,0.36,1.0,1.0);
    TPad* down = new TPad("","",0.0,0.0,1.0,0.36);
    up->SetTopMargin(0.13);
    up->SetBottomMargin(0.0);
    up->Draw("SAME");
    down->SetTopMargin(0.0);
    down->SetBottomMargin(0.35);
    down->Draw("SAME");

    // Draw upper panel
    float xlow = histA[histnames.at(var)]->GetXaxis()->GetXmin();
    float xup = histA[histnames.at(var)]->GetXaxis()->GetXmax();
    float ylow = 1E0;
    if (scaling == 2)
      ylow = 1E-8;
    float yup = histA[histnames.at(var)]->GetMaximum()*5;
    if(histB[histnames.at(var)]->GetMaximum() > histA[histnames.at(var)]->GetMaximum())
      yup = histB[histnames.at(var)]->GetMaximum()*5;

    up->cd();
    up->SetLogy();
    histB[histnames.at(var)]->GetXaxis()->SetTitle(histB[histnames.at(var)]->GetXaxis()->GetTitle());
    histB[histnames.at(var)]->SetMinimum(ylow);
    histB[histnames.at(var)]->SetMaximum(yup);
    histB[histnames.at(var)]->SetLineColor(2);
    histB[histnames.at(var)]->SetMarkerColor(2);
    histB[histnames.at(var)]->SetLineWidth(2);
    histB[histnames.at(var)]->GetXaxis()->SetRangeUser(xlow, xup);
    histB[histnames.at(var)]->Draw("hist");
    histA[histnames.at(var)]->SetLineColor(1);
    histA[histnames.at(var)]->SetLineWidth(2);
    histA[histnames.at(var)]->Draw("same");

    // Draw ratio plot (lower panel)
    down ->cd();
    auto frame = down->DrawFrame(xlow, 0.25, xup, 1.75);
    frame->GetYaxis()->SetTitle("2022 / 2023");
    frame->GetYaxis()->SetTitleSize(histA[histnames.at(var)]->GetYaxis()->GetTitleSize()*2.0);
    frame->GetYaxis()->SetTitleOffset(0.6);
    frame->GetYaxis()->CenterTitle(true);
    frame->GetYaxis()->SetLabelSize(histA[histnames.at(var)]->GetYaxis()->GetLabelSize()*1.9);
    frame->GetYaxis()->SetNdivisions(304);
    frame->GetXaxis()->SetTitle(histA[histnames.at(var)]->GetXaxis()->GetTitle());
    frame->GetXaxis()->SetTickLength(histA[histnames.at(var)]->GetYaxis()->GetTickLength()*1.8);
    frame->GetXaxis()->SetTitleSize(histA[histnames.at(var)]->GetXaxis()->GetTitleSize()*2.4);
    frame->GetXaxis()->SetTitleOffset(1.2);
    frame->GetXaxis()->SetLabelSize(histA[histnames.at(var)]->GetXaxis()->GetLabelSize()*1.9);

    rates[histnames.at(var)]->SetMarkerStyle(20);
    rates[histnames.at(var)]->SetMarkerColor(1);
    rates[histnames.at(var)]->SetLineColor(1);
    rates[histnames.at(var)]->SetMarkerSize(0.8);
    rates[histnames.at(var)]->Draw("AP SAME");

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
    leg->AddEntry(histA[histnames.at(var)], "2022 data", "apel");
    leg->AddEntry(histB[histnames.at(var)], "2023 data", "apel");
    leg->Draw();

    preliminary->Draw();

    /// Save Plots ///
    //c_rate[histnames.at(var)]->SaveAs(("plots/DataToData/22vs23/kinselection/"+ histnames.at(var) +"_scaledLumi.png").c_str());
    
  }


}// End of main 

void DataToDataComparison(){

  /// 2022 vs 2023 at preselection ///
  //compare("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/Inaugural_preselection_2022/root", "ReRecoData2022","/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/2023preliminary/root/", "PromptData2023", 2);

    /// 2022 vs 2023 at kinselection ///
  compare("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/Inaugural_kinselection_2022/root", "ReRecoData2022","/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/2023preliminary_kinselection/root/", "PromptData2023", 2);

}


