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

/* Routine to read limits from the output of a datacard for a given mass */
bool readLimits(const std::string& filename, double& expected, double& low68, double& up68, double& low95, double& up95) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error opening the file " << filename << std::endl;
        return false;
    }
    file >> expected >> low68 >> up68 >> low95 >> up95;
    file.close();
    return true;
}

void plotLimits(string output_dir, string model, string year){

  string limit_path = output_dir + model +"/"+ year;
  string xsec_fileName = "/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/SSMCrossSections.txt";

  /* Part I: Read the theoretical cross sections */

  // Read and store the values in vectors
  std::vector<double> masses;
  std::vector<double> xsecs;
  std::vector<double> xsecs_relErr;

  std::ifstream xsec_file(xsec_fileName);
  if (!xsec_file.is_open()) {
    std::cerr << "Error openning the cross section file" << std::endl;
    return;
  }

  double mass, xsec, xsec_relErr;
  while (xsec_file >> mass >> xsec >> xsec_relErr) {
    masses.push_back(mass);
    xsecs.push_back(xsec);
    xsecs_relErr.push_back(xsec_relErr);
  }
  xsec_file.close();

  std::vector<double> xsecs_err;
  for (size_t i = 0; i < masses.size(); ++i) {
    xsecs_err.push_back(xsecs[i]*xsecs_relErr[i]);
  }
  
  /* Part II: Read the limits for different mass signals and plot the bands */

  // Read and store the limits in vectors
  std::vector<double> masses_limits;
  std::vector<double> expected_limits;
  std::vector<double> low68_limits, up68_limits;
  std::vector<double> low95_limits, up95_limits;
    
  for (const auto& entry : fs::directory_iterator(limit_path)) {
    std::string limit_file = entry.path().filename().string();
    if (limit_file.find("Wprime") != std::string::npos) {
      // Read mass value from the file name
      std::string mass_str = limit_file.substr(6, limit_file.find("_results") - 6);
      double mass_val = std::stod(mass_str);
      masses_limits.push_back(mass_val);

      // Read limits from each file
      double expected, low68, up68, low95, up95;
      if (readLimits(entry.path().string(), expected, low68, up68, low95, up95)) {
	expected_limits.push_back(expected);
	low68_limits.push_back(low68);
	up68_limits.push_back(up68);
	low95_limits.push_back(low95);
	up95_limits.push_back(up95);
      }
    }
  }

  std::vector<double> errYlow68, errYup68, errYlow95, errYup95;
  for (size_t i = 0; i < masses_limits.size(); ++i) {
    errYlow68.push_back(expected_limits[i] - low68_limits[i]);
    errYup68.push_back(up68_limits[i] - expected_limits[i]);
    errYlow95.push_back(expected_limits[i] - low95_limits[i]);
    errYup95.push_back(up95_limits[i] - expected_limits[i]);
  }


  /* Part III: Draw the theoretical curve & expected limits  */

  // Create the canvas
  TCanvas *SSMcanvas = new TCanvas("SSMcanvas", "", 800, 600);
  SSMcanvas->cd();
  SSMcanvas->Draw();
  SSMcanvas->SetLogy();
  
  float xlow = 400;
  float xup = 6600;
  float ylow = 0.01;
  float yup = 2.2E5;
  
  // Draw the limit curve with the uncertainty bands
  TGraph* expected_curve = new TGraph(masses_limits.size(), &masses_limits[0], &expected_limits[0]);
  
  TGraphAsymmErrors* band68 = new TGraphAsymmErrors(masses_limits.size(), &masses_limits[0], &expected_limits[0], 0, 0, &errYlow68[0], &errYup68[0]);
  TGraphAsymmErrors* band95 = new TGraphAsymmErrors(masses_limits.size(), &masses_limits[0], &expected_limits[0], 0, 0, &errYlow95[0], &errYup95[0]);

  band95->GetXaxis()->SetTitle("M_{W'} (GeV)");
  band95->GetXaxis()->SetTitleOffset(1.2);
  band95->GetXaxis()->SetRangeUser(xlow, xup);
  band95->GetYaxis()->SetTitle("#sigma #times #it{B}  (fb)");
  band95->SetMinimum(ylow);
  band95->SetMaximum(yup);
  band95->SetTitle("");
  band95->SetFillColor(TColor::GetColor("#f5bb54"));
  band95->Draw("A3");
  band68->SetFillColor(TColor::GetColor("#607641"));
  band68->Draw("3 SAME");

  expected_curve->SetLineStyle(7);
  expected_curve->SetLineColor(1);
  expected_curve->SetLineWidth(3);
  expected_curve->Draw("L SAME");
  
  // Draw the theoretical curve with the PDF + alpha_s uncert. band
  TGraph *xsec_curve = new TGraph(masses.size(), &masses[0], &xsecs[0]);
  TGraphErrors *xsec_errorBand = new TGraphErrors(masses.size(), &masses[0], &xsecs[0], 0, &xsecs_err[0]);

  xsec_errorBand->SetFillColor(29);
  xsec_errorBand->Draw("3 SAME");
  xsec_curve->SetLineColor(kBlue);
  xsec_curve->SetLineWidth(2);
  xsec_curve->SetFillColor(29);
  xsec_curve->Draw("C SAME");
  
  // Legends and cosmetics
  TLegend* leg1 = new TLegend(0.60, 0.80, 0.88, 0.87);
  leg1->AddEntry(xsec_curve, "#sigma SSM W' NNLO", "fl");
  leg1->SetBorderSize(0);
  leg1->Draw();

  TLegend* leg2 = new TLegend(0.60, 0.60, 0.88, 0.75);
  leg2->AddEntry(expected_curve, "Expected", "l");
  leg2->AddEntry(band68, "#pm 1 s.d.", "f");
  leg2->AddEntry(band95, "#pm 2 s.d.", "f");
  leg2->SetBorderSize(0);
  leg2->Draw();

  TString channel;
  channel = "#bf{#mu + p_{T}^{miss}}";

  TLatex* ch = new TLatex(0.22, 0.72, channel);
  ch->SetNDC();
  ch->SetTextFont(42);
  ch->SetTextSize(0.038);
  ch->Draw();

  TString title1;
  TString title2;
  if (year == "2022"){
    title1 = "#splitline{#bf{CMS}}{#it{Work in progress}}";
    title2 = "2022, 34.7 fb^{-1} (13.6 TeV)";
  }
  else if (year == "2023"){
    title1 = "#splitline{#bf{CMS}}{#it{Work in progress}}";
    title2 = "2023, 27.2 fb^{-1} (13.6 TeV)";
  }
  else if (year == "22+23"){
    title1 = "#splitline{#bf{CMS}}{#it{Work in progress}}";
    title2 = "2022 + 2023, 61.9 fb^{-1} (13.6 TeV)";
  }
  float comb_prelim = 0;
  if(year == "22+23") comb_prelim = 0.09;
  
  TLatex* preliminary1 = new TLatex(0.17, 0.83, title1);
  preliminary1->SetNDC();
  preliminary1->SetTextFont(42);
  preliminary1->SetTextSize(0.04);
  preliminary1->Draw();
  TLatex* preliminary2 = new TLatex(0.60 - comb_prelim, 0.92, title2);
  preliminary2->SetNDC();
  preliminary2->SetTextFont(42);
  preliminary2->SetTextSize(0.04);
  preliminary2->Draw();

  // Save limit plot
  string plotName = "SSMlimit_muon_";
  //SSMcanvas->SaveAs(("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/plots/" + model +"/"+ year +"/"+ plotName + year + ".png").c_str());
  
}

void limitCurve(){

  plotLimits("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/outputs/", "SSM", "2022");
  plotLimits("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/outputs/", "SSM", "2023");
  plotLimits("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/outputs/", "SSM", "22+23");
  
}
