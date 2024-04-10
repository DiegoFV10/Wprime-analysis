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


void METtrigger_eff(TString denominator, TString numerator){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  // Set signal mass point
  string signal = "Wprime5600_postEE";

  // Get denominator hist (no trigger)
  TFile *den =  TFile::Open(denominator);
  TH1D* h_NOtrig = (TH1D*) den->Get(("histograms/" + signal).c_str()); 

  // Get numerator hist (MET trigger)
  TFile *num =  TFile::Open(numerator);
  TH1D* h_METtrig = (TH1D*) num->Get(("histograms/" + signal).c_str());
  
  // Draw efficiency
  TGraphAsymmErrors* METeff = new TGraphAsymmErrors(h_METtrig, h_NOtrig);


  TCanvas* c_METprime = new TCanvas("METtrig_eff","",600,500);
  c_METprime->cd();

  METeff->SetMaximum(1.1);
  METeff->SetMarkerStyle(20);
  METeff->SetMarkerSize(0.6);
  METeff->SetMarkerColor(h_METtrig->GetLineColor());
  METeff->GetYaxis()->SetTitle("Efficiency");
  METeff->GetYaxis()->SetTitleOffset(1.3);
  METeff->GetXaxis()->SetTitle("p_{T}^{#mu + MET}  [GeV]");
  METeff->GetXaxis()->SetTitleOffset(1.2);
  METeff->Draw("AP");

  TLegend * leg = new TLegend(0.60, 0.50, 0.85, 0.65);
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetTextSize(0.03);
  leg->AddEntry(METeff, (signal.substr(0,10)).c_str(), "apel");
  leg->Draw();

  TString title = "#bf{CMS} Simulation                                         2022 (13.6 TeV)";
  TLatex* preliminary = new TLatex(0.12,0.92, title);
  preliminary->SetNDC();
  preliminary->SetTextFont(42);
  preliminary->SetTextSize(0.040);
  preliminary->Draw();

  /// Save Plots ///
  c_METprime->SaveAs(("plots/MET_effs/METtrigger_eff_" + signal.substr(0,10) + ".png").c_str());


}// End of main 

void trigger_efficiencies(){

  TString inp_path = "/eos/user/d/diegof/cmt/FeaturePlot/triggerOscar_config/cat_preselection/";
 
  METtrigger_eff(inp_path + "Wprime_NOtrigger/root/METprime__pg_signal_METeff__nodata.root", inp_path + "Wprime_METtriggers/root/METprime__pg_signal_METeff__nodata.root");

}


