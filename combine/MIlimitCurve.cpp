#include <TGraph.h>
#include <TCanvas.h>
#include <TAxis.h>
#include <TLegend.h>
#include <TStyle.h>
#include <TSystemDirectory.h>
#include <TSystemFile.h>
#include <TList.h>
#include <TSystem.h>
#include <TString.h>
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
#include <regex>
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

using namespace std;

/* Routine for reading the expected limits */
bool readExpectedLimits(const std::string& filename, double& medianLimit, double& low68, double& high68, double& low95, double& high95) {
    std::ifstream infile(filename);

    if (!infile) {
        std::cerr << "Error al abrir el archivo: " << filename << std::endl;
        return false;
    }

    std::string line;

    std::regex medianRegex(R"(median expected limit: r < ([0-9]*\.[0-9]+))");
    std::regex band68Regex(R"(68% expected band : ([0-9]*\.[0-9]+) < r < ([0-9]*\.[0-9]+))");
    std::regex band95Regex(R"(95% expected band : ([0-9]*\.[0-9]+) < r < ([0-9]*\.[0-9]+))");

    while (std::getline(infile, line)) {
        std::smatch match;

        // Find median expected limit
        if (std::regex_search(line, match, medianRegex)) {
            medianLimit = std::stod(match[1]);
        }

        // Fin 68% expected band
        if (std::regex_search(line, match, band68Regex)) {
            low68 = std::stod(match[1]);
            high68 = std::stod(match[2]);
        }

        // Find 95% expected band
        if (std::regex_search(line, match, band95Regex)) {
            low95 = std::stod(match[1]);
            high95 = std::stod(match[2]);
        }
    }

    infile.close();
    return true;
}

/* For reading the observed limit */
bool readObservedLimit(const std::string& fileName, double& observedLimit) {
    std::ifstream infile(fileName);

    if (!infile) {
        std::cerr << "Error al abrir el archivo: " << fileName << std::endl;
        return false;
    }

    std::string line;
    std::regex observedRegex(R"(Limit: r < ([0-9]*\.[0-9]+))");

    while (std::getline(infile, line)) {
        std::smatch match;

        if (std::regex_search(line, match, observedRegex)) {
            observedLimit = std::stod(match[1]);
            break;
        }
    }

    infile.close();
    return true;
}

/* For looking for the correct mTmin file in a given directory */
string findFileForMTmin(const string &prefix, int mTmin, const string &dirName) {
  TSystemDirectory dir(dirName.c_str(), dirName.c_str());
  TList *files = dir.GetListOfFiles();
  if (!files) return "";

  string match;
  TIter next(files);
  TSystemFile *file;
  while ((file = (TSystemFile*)next())) {
    TString fname = file->GetName();
    if (!file->IsDirectory() && fname.EndsWith(".out")) {
      TString expectedPrefix = Form("%s%d", prefix.c_str(), mTmin);
      if (fname.BeginsWith(expectedPrefix)) {
	match = dirName + "/" + string(fname.Data());
	break;
      }
    }
  }
  delete files;
  return match;
}

void plotMIlimit(string output_dir, string model, string year, string channel="", string checkRegion="") {
  
  gStyle->SetOptStat(0);

  string limit_path = output_dir + model +"/"+ year +"/"+ channel +"/"+ checkRegion;

  vector<double> mTmins;
  vector<double> medians, obsVals;
  vector<double> err1Low, err1High, err2Low, err2High;

  for (int mTmin = 400; mTmin <= 3600; mTmin += 100) {
    string fnameExp = findFileForMTmin("mTmin", mTmin, limit_path);
    string fnameObs = findFileForMTmin("UnblindMTmin", mTmin, limit_path);

    if (fnameExp.empty() || fnameObs.empty()) {
      cout << "Missing files for mTmin = " << mTmin << endl;
      continue;
    }

    double median, low1s, high1s, low2s, high2s;
    if (!readExpectedLimits(fnameExp, median, low1s, high1s, low2s, high2s)) continue;

    double obs;
    if (!readObservedLimit(fnameObs, obs)) continue;

    mTmins.push_back(mTmin);
    medians.push_back(median);
    obsVals.push_back(obs);

    err1Low.push_back(median - low1s);
    err1High.push_back(high1s - median);
    err2Low.push_back(median - low2s);
    err2High.push_back(high2s - median);
  }

  int n = mTmins.size();

  // Define graphs for expected & observed curves
  TGraphAsymmErrors *band68 = new TGraphAsymmErrors(n, &mTmins[0], &medians[0], 0, 0, &err1Low[0], &err1High[0]);
  band68->SetFillColor(TColor::GetColor("#607641"));

  TGraphAsymmErrors *band95 = new TGraphAsymmErrors(n, &mTmins[0], &medians[0], 0, 0, &err2Low[0], &err2High[0]);
  band95->SetFillColor(TColor::GetColor("#f5bb54"));

  TGraph *expected_curve = new TGraph(n, &mTmins[0], &medians[0]);
  expected_curve->SetLineStyle(7);
  expected_curve->SetLineColor(1);
  expected_curve->SetLineWidth(3);

  TGraph *observed_curve = new TGraph(n, &mTmins[0], &obsVals[0]);
  observed_curve->SetLineColor(kBlack);
  observed_curve->SetLineStyle(1);      
  observed_curve->SetLineWidth(2); 

  // Create the canvas
  TCanvas *MIcanvas = new TCanvas("MIcanvas", "", 800, 600);
  MIcanvas->cd();
  MIcanvas->Draw();
  MIcanvas->SetLogy();

  float xlow = 400;
  float xup = 3600;
  float ylow = 5.0E-3;
  float yup = 1.0E3;

  // Draw the different curves
  band95->GetXaxis()->SetTitle("m_{T}^{min} (GeV)");
  band95->GetXaxis()->SetTitleOffset(1.2);
  band95->GetXaxis()->SetRangeUser(xlow, xup);
  band95->GetYaxis()->SetTitle("#sigma #times #it{B} #times #it{A} #times #epsilon  (fb)");
  band95->SetMinimum(ylow);
  band95->SetMaximum(yup);
  band95->SetTitle("");
  band95->Draw("A3");
  band68->Draw("3 SAME");
  expected_curve->Draw("L SAME");
  observed_curve->Draw("L SAME");

  // Legend and cosmetics
  TLegend *leg = new TLegend(0.62, 0.67, 0.9, 0.85);
  leg->AddEntry(observed_curve, "Observed", "l");
  leg->AddEntry(expected_curve, "Expected", "l");
  leg->AddEntry(band68, "#pm 1 s.d.", "f");
  leg->AddEntry(band95, "#pm 2 s.d.", "f");
  leg->SetBorderSize(0);
  leg->Draw();

  TString channel_label;
  if(channel == "muon")
    channel_label = "#bf{#mu + p_{T}^{miss}}";
  else if(channel == "ele+mu")
    channel_label = "#bf{e/#mu + p_{T}^{miss}}";
  else
    channel_label = "#bf{#mu + p_{T}^{miss}}";

  TLatex* ch = new TLatex(0.22, 0.72, channel_label);
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
  MIcanvas->SaveAs(("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/plots/" + model +"/"+ year +"/MIlimit_"+ channel +"_"+ year +"_"+ checkRegion + ".png").c_str());

}


void MIlimitCurve(){

  //plotMIlimit("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/outputs/", "MI", "2022", "muon", "fullCuts");
  //plotMIlimit("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/outputs/", "MI", "2023", "muon", "fullCuts");
  plotMIlimit("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/outputs/", "MI", "22+23", "muon", "fullCuts");
  
}
