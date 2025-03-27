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


void PDFproducer68CL(TString filePath, TString fileSuffix){

  int nVariations = 103;

  std::vector<TString> histNames = {"W_boson", "Top", "Z_boson", "DiBoson"};

  // Store in a vector the ROOT files with the PDF variations
  std::vector<TFile*> files;
  for (int i = 0; i < nVariations; i++) {
    TString fileName = filePath + i + fileSuffix;
    files.push_back(TFile::Open(fileName, "READ"));
    if (!files.back()) {
      std::cerr << "Error opening file: " << fileName << std::endl;
      return;
    }
  }
  
  // Output hist with full PDF uncertainty
  std::vector<TH1D*> outputHists;

  for (const auto& histName : histNames) {
    // Nominal histogram (variation 0)
    TH1D* nominalHist = (TH1D*)files[0]->Get("histograms/" + histName);
    
    // Histograms with alpha_s variations (Up -> 102, Down -> 101)
    TH1D* alphasUpHist = (TH1D*)files[102]->Get("histograms/" + histName);
    TH1D* alphasDownHist = (TH1D*)files[101]->Get("histograms/" + histName);

    // Output histogram
    TH1D* outputHist = (TH1D*)nominalHist->Clone(histName + "_PDFError");
    outputHist->Reset();

    int nBins = nominalHist->GetNbinsX();

    for (int bin = 1; bin <= nBins; bin++) {
      
      double nominalValue = nominalHist->GetBinContent(bin);
      std::vector<double> variations;
      
      for (int i = 1; i < nVariations - 2; ++i) {
	TH1D* variationHist = (TH1D*)files[i]->Get("histograms/" + histName);
	variations.push_back(variationHist->GetBinContent(bin));
      }
      // Sort the PDF variations
      std::sort(variations.begin(), variations.end());
      
      // Compute the total PDF error from eq. 24 in https://arxiv.org/pdf/1510.03865v1 (difference between quantile 84 & 16 over 2)
      double value16 = variations[15];
      double value84 = variations[83];

      double pdfError = (value84 - value16) / 2.0;

      // Compute alpha_s error
      double alphasUpValue = alphasUpHist->GetBinContent(bin);
      double alphasDownValue = alphasDownHist->GetBinContent(bin);
      double alphasError = (alphasUpValue - alphasDownValue) / 2.0;

      // Combine PDF + alpha_s errors
      double pdfAlphasError = std::sqrt(pdfError*pdfError + alphasError*alphasError);
      
      outputHist->SetBinContent(bin, pdfAlphasError / nominalValue); // Relative error
      
    } // Loop over histogram bins

    outputHists.push_back(outputHist);
    
  } // Loop over different backgorund processes

  // Save output histogram in new ROOT file
  TString outDir = "/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/nanoaod_base_analysis/data/cmssw/CMSSW_13_0_13/src/Wprime/Modules/PDF/";
  TFile* outputFile = TFile::Open(outDir + "PDFErrors.root", "RECREATE");
  for (auto& hist : outputHists) {
    hist->Write();
  }

  outputFile->Close();
  for (auto& file : files) {
    file->Close();
  }

}



void PDFproducerSumOfSquares(TString filePath, TString fileSuffix){

  int nVariations = 103;

  std::vector<TString> histNames = {"W_boson", "Top", "Z_boson", "DiBoson"};

  // Store in a vector the ROOT files with the PDF variations
  std::vector<TFile*> files;
  for (int i = 0; i < nVariations; i++) {
    TString fileName = filePath + i + fileSuffix;
    files.push_back(TFile::Open(fileName, "READ"));
    if (!files.back()) {
      std::cerr << "Error opening file: " << fileName << std::endl;
      return;
    }
  }
  
  // Output hist with full PDF uncertainty
  std::vector<TH1D*> outputHists;

  for (const auto& histName : histNames) {
    // Nominal histogram (variation 0)
    TH1D* nominalHist = (TH1D*)files[0]->Get("histograms/" + histName);
    
    // Histograms with alpha_s variations (Up -> 102, Down -> 101)
    TH1D* alphasUpHist = (TH1D*)files[102]->Get("histograms/" + histName);
    TH1D* alphasDownHist = (TH1D*)files[101]->Get("histograms/" + histName);

    // Output histogram
    TH1D* outputHist = (TH1D*)nominalHist->Clone(histName + "_PDFError");
    outputHist->Reset();

    int nBins = nominalHist->GetNbinsX();

    for (int bin = 1; bin <= nBins; bin++) {
      
      double nominalValue = nominalHist->GetBinContent(bin);
      double pdfError = 0.0;

      // Compute total PDF error from eq.20 in https://arxiv.org/pdf/1510.03865v1 (sum of squared differences)
      for (int i = 1; i < nVariations - 2; i++) {
	
	TH1D* variationHist = (TH1D*)files[i]->Get("histograms/" + histName);

	double variationValue = variationHist->GetBinContent(bin);
	double diff = variationValue - nominalValue;
	pdfError += diff * diff;
	
      } // Loop over 100 PDF variations

      pdfError = std::sqrt(pdfError);

      // Compute alpha_s error
      double alphasUpValue = alphasUpHist->GetBinContent(bin);
      double alphasDownValue = alphasDownHist->GetBinContent(bin);
      double alphasError = (alphasUpValue - alphasDownValue) / 2.0;

      // Combine PDF + alpha_s errors
      double pdfAlphasError = std::sqrt(pdfError*pdfError + alphasError*alphasError);
      
      outputHist->SetBinContent(bin, pdfAlphasError / nominalValue); // Relative error
      
    } // Loop over histogram bins

    outputHists.push_back(outputHist);
    
  } // Loop over different backgorund processes

  // Save output histogram in new ROOT file
  TString outDir = "/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/nanoaod_base_analysis/data/cmssw/CMSSW_13_0_13/src/Wprime/Modules/PDF/";
  TFile* outputFile = TFile::Open(outDir + "PDFErrors.root", "RECREATE");
  for (auto& hist : outputHists) {
    hist->Write();
  }

  outputFile->Close();
  for (auto& file : files) {
    file->Close();
  }

}


void PDFcalculatorFromMt(){

  /// For PDF variations using eq.20 in https://arxiv.org/pdf/1510.03865v1 (sum of squared differences) ///
  //PDFproducerSumOfSquares("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/zzzz_PDFreweight_", "/root/mT__pg_2022ReReco.root");

  /// For PDF variations using eq.24 in https://arxiv.org/pdf/1510.03865v1 (68% CL interval) ///
  PDFproducer68CL("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/zzzz_PDFreweight_", "/root/mT__pg_2022ReReco.root");
  
}


