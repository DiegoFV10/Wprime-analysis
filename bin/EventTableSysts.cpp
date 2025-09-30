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
#include <map>


void SystPlot(string systFile, string year){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  TFile *f1 =  TFile::Open(systFile.c_str());

  std::vector<string> systList;
  if (year == "2022")
    systList = {"CMS_pileup", "CMS_eff_m_reco_2022", "CMS_eff_m_id_2022", "CMS_eff_m_iso_2022", "CMS_eff_m_trigger_2022", "CMS_scale_m_2022", "CMS_scale_met_2022", "CMS_eff_b_2022", "CMS_EXO24021_W_kfactor", "pdf_qqbar"};
  else if (year == "2023")
    systList = {"CMS_pileup", "CMS_eff_m_reco_2023", "CMS_eff_m_id_2023", "CMS_eff_m_iso_2023", "CMS_eff_m_trigger_2023", "CMS_scale_m_2023", "CMS_scale_met_2023", "CMS_eff_b_2023", "CMS_EXO24021_W_kfactor", "pdf_qqbar"};
  std::vector<string> systDirs = {"_Up", "_Down"};

  std::map<string, TH1D*> bkgVars;
  TH1D* bkgNominal = (TH1D*) f1->Get("histograms/background");
  // For evt tables
  std::map<string, TH1D*> W2000Vars;
  std::map<string, TH1D*> W3600Vars;
  std::map<string, TH1D*> W5600Vars;
  std::map<string, TH1D*> WbosonVars;
  std::map<string, TH1D*> TopVars;
  std::map<string, TH1D*> ZbosonVars;
  std::map<string, TH1D*> DiBosonVars;
  std::map<string, TH1D*> QCDVars;
  TH1D* W2000Nominal   = (TH1D*) f1->Get("histograms/Wprime2000");
  TH1D* W3600Nominal   = (TH1D*) f1->Get("histograms/Wprime3600");
  TH1D* W5600Nominal   = (TH1D*) f1->Get("histograms/Wprime5600");
  TH1D* WbosonNominal  = (TH1D*) f1->Get("histograms/W_boson");
  TH1D* TopNominal     = (TH1D*) f1->Get("histograms/Top");
  TH1D* ZbosonNominal  = (TH1D*) f1->Get("histograms/Z_boson");
  TH1D* DiBosonNominal = (TH1D*) f1->Get("histograms/DiBoson");
  TH1D* QCDNominal     = (TH1D*) f1->Get("histograms/QCD");
  TH1D* Data22Nominal  = (TH1D*) f1->Get("histograms/ReRecoData2022");
  /////////
  int nBins = bkgNominal->GetNbinsX();
  TGraphAsymmErrors* bkgSyst = new TGraphAsymmErrors(nBins);

  // For evt tables
  TGraphAsymmErrors* W2000Syst   = new TGraphAsymmErrors(nBins);
  TGraphAsymmErrors* W3600Syst   = new TGraphAsymmErrors(nBins);
  TGraphAsymmErrors* W5600Syst   = new TGraphAsymmErrors(nBins);
  TGraphAsymmErrors* WbosonSyst  = new TGraphAsymmErrors(nBins);
  TGraphAsymmErrors* TopSyst     = new TGraphAsymmErrors(nBins);
  TGraphAsymmErrors* ZbosonSyst  = new TGraphAsymmErrors(nBins);
  TGraphAsymmErrors* DiBosonSyst = new TGraphAsymmErrors(nBins);
  TGraphAsymmErrors* QCDSyst     = new TGraphAsymmErrors(nBins);
  
  Double_t W2000_IntegralFull = 0, W2000_Integral1000 = 0, W2000_Integral2000 = 0;
  Double_t W3600_IntegralFull = 0, W3600_Integral1000 = 0, W3600_Integral2000 = 0;
  Double_t W5600_IntegralFull = 0, W5600_Integral1000 = 0, W5600_Integral2000 = 0;
  Double_t Wboson_IntegralFull = 0, Wboson_Integral1000 = 0, Wboson_Integral2000 = 0;
  Double_t Top_IntegralFull = 0, Top_Integral1000 = 0, Top_Integral2000 = 0;
  Double_t Zboson_IntegralFull = 0, Zboson_Integral1000 = 0, Zboson_Integral2000 = 0;
  Double_t DiBoson_IntegralFull = 0, DiBoson_Integral1000 = 0, DiBoson_Integral2000 = 0;
  Double_t QCD_IntegralFull = 0, QCD_Integral1000 = 0, QCD_Integral2000 = 0;
  Double_t Data22_IntegralFull = 0, Data22_Integral1000 = 0;
  
  for (int i = 0; i < nBins; i++){
    W2000_IntegralFull   += W2000Nominal->GetBinContent(i+1);
    W3600_IntegralFull   += W3600Nominal->GetBinContent(i+1);
    W5600_IntegralFull   += W5600Nominal->GetBinContent(i+1);
    Wboson_IntegralFull  += WbosonNominal->GetBinContent(i+1);
    Top_IntegralFull     += TopNominal->GetBinContent(i+1);
    Zboson_IntegralFull  += ZbosonNominal->GetBinContent(i+1);
    DiBoson_IntegralFull += DiBosonNominal->GetBinContent(i+1);
    QCD_IntegralFull     += QCDNominal->GetBinContent(i+1);
  } // Loop over histogram bins
  for (int i = 6; i < nBins; i++){
    W2000_Integral1000   += W2000Nominal->GetBinContent(i+1);
    W3600_Integral1000   += W3600Nominal->GetBinContent(i+1);
    W5600_Integral1000   += W5600Nominal->GetBinContent(i+1);
    Wboson_Integral1000  += WbosonNominal->GetBinContent(i+1);
    Top_Integral1000     += TopNominal->GetBinContent(i+1);
    Zboson_Integral1000  += ZbosonNominal->GetBinContent(i+1);
    DiBoson_Integral1000 += DiBosonNominal->GetBinContent(i+1);
    QCD_Integral1000     += QCDNominal->GetBinContent(i+1);
  } // Loop over histogram bins
  for (int i = 16; i < nBins; i++){
    W2000_Integral2000   += W2000Nominal->GetBinContent(i+1);
    W3600_Integral2000   += W3600Nominal->GetBinContent(i+1);
    W5600_Integral2000   += W5600Nominal->GetBinContent(i+1);
    Wboson_Integral2000  += WbosonNominal->GetBinContent(i+1);
    Top_Integral2000     += TopNominal->GetBinContent(i+1);
    Zboson_Integral2000  += ZbosonNominal->GetBinContent(i+1);
    DiBoson_Integral2000 += DiBosonNominal->GetBinContent(i+1);
    QCD_Integral2000     += QCDNominal->GetBinContent(i+1);
  } // Loop over histogram bins
  Data22_IntegralFull = Data22Nominal->Integral(1,16);
  Data22_Integral1000 = Data22Nominal->Integral(7,16);

  cout <<"# Wprime2000 ==> Full: "<< W2000_IntegralFull <<" | mT > 1 TeV: "<< W2000_Integral1000 <<" | mT > 2 TeV: "<< W2000_Integral2000 << endl;
  cout <<"# Wprime3600 ==> Full: "<< W3600_IntegralFull <<" | mT > 1 TeV: "<< W3600_Integral1000 <<" | mT > 2 TeV: "<< W3600_Integral2000 << endl;
  cout <<"# Wprime5600 ==> Full: "<< W5600_IntegralFull <<" | mT > 1 TeV: "<< W5600_Integral1000 <<" | mT > 2 TeV: "<< W5600_Integral2000 << endl;
  cout <<"# Wboson     ==> Full: "<< Wboson_IntegralFull <<" | mT > 1 TeV: "<< Wboson_Integral1000 <<" | mT > 2 TeV: "<< Wboson_Integral2000 << endl;
  cout <<"# Top        ==> Full: "<< Top_IntegralFull <<" | mT > 1 TeV: "<< Top_Integral1000 <<" | mT > 2 TeV: "<< Top_Integral2000 << endl;
  cout <<"# Zboson     ==> Full: "<< Zboson_IntegralFull <<" | mT > 1 TeV: "<< Zboson_Integral1000 <<" | mT > 2 TeV: "<< Zboson_Integral2000 << endl;
  cout <<"# DiBoson    ==> Full: "<< DiBoson_IntegralFull <<" | mT > 1 TeV: "<< DiBoson_Integral1000 <<" | mT > 2 TeV: "<< DiBoson_Integral2000 << endl;
  cout <<"# QCD        ==> Full: "<< QCD_IntegralFull <<" | mT > 1 TeV: "<< QCD_Integral1000 <<" | mT > 2 TeV: "<< QCD_Integral2000 << endl;
  cout <<"# Data 2022  ==> Full: "<< Data22_IntegralFull <<" | mT > 1 TeV: "<< Data22_Integral1000 << endl;
  /////////
  
  for (const auto &syst : systList) {
    for (const auto &dir : systDirs) {
      
      //      bkgVars[syst+dir] = (TH1D*) f1->Get(("histograms/background_" + syst + dir).c_str());
      // For evt tables
      W2000Vars[syst+dir]   = (TH1D*) f1->Get(("histograms/Wprime2000_" + syst + dir).c_str());
      W3600Vars[syst+dir]   = (TH1D*) f1->Get(("histograms/Wprime3600_" + syst + dir).c_str());
      W5600Vars[syst+dir]   = (TH1D*) f1->Get(("histograms/Wprime5600_" + syst + dir).c_str());
      WbosonVars[syst+dir]  = (TH1D*) f1->Get(("histograms/W_boson_" + syst + dir).c_str());
      TopVars[syst+dir]     = (TH1D*) f1->Get(("histograms/Top_" + syst + dir).c_str());
      ZbosonVars[syst+dir]  = (TH1D*) f1->Get(("histograms/Z_boson_" + syst + dir).c_str());
      DiBosonVars[syst+dir] = (TH1D*) f1->Get(("histograms/DiBoson_" + syst + dir).c_str());
      QCDVars[syst+dir]     = (TH1D*) f1->Get(("histograms/QCD_" + syst + dir).c_str());
      ///////////     

    } // Loop over Up/Down variations
  } // Loop over systematics
        
  for (int i = 0; i < nBins; i++){

    double x = bkgNominal->GetXaxis()->GetBinCenter(i+1);
    bkgSyst->SetPoint(i, x, 1.0);

    // For evt tables (same for bkg)
    double systUpTotW2000 = 0;
    double systDownTotW2000 = 0;
    double nominalW2000 = W2000Nominal->GetBinContent(i+1);
    double systUpTotW3600 = 0;
    double systDownTotW3600 = 0;
    double nominalW3600 = W3600Nominal->GetBinContent(i+1);
    double systUpTotW5600 = 0;
    double systDownTotW5600 = 0;
    double nominalW5600 = W5600Nominal->GetBinContent(i+1);
    double systUpTotWboson = 0;
    double systDownTotWboson = 0;
    double nominalWboson = WbosonNominal->GetBinContent(i+1);
    double systUpTotTop = 0;
    double systDownTotTop = 0;
    double nominalTop = TopNominal->GetBinContent(i+1);
    double systUpTotZboson = 0;
    double systDownTotZboson = 0;
    double nominalZboson = ZbosonNominal->GetBinContent(i+1);
    double systUpTotDiBoson = 0;
    double systDownTotDiBoson = 0;
    double nominalDiBoson = DiBosonNominal->GetBinContent(i+1);
    double systUpTotQCD = 0;
    double systDownTotQCD = 0;
    double nominalQCD = QCDNominal->GetBinContent(i+1);

    W2000Syst->SetPoint(i, x, nominalW2000); // Poner 1.0 para el plot en vez del valor nominal
    W3600Syst->SetPoint(i, x, nominalW3600);
    W5600Syst->SetPoint(i, x, nominalW5600);
    WbosonSyst->SetPoint(i, x, nominalWboson);
    TopSyst->SetPoint(i, x, nominalTop);
    ZbosonSyst->SetPoint(i, x, nominalZboson);
    DiBosonSyst->SetPoint(i, x, nominalDiBoson);
    QCDSyst->SetPoint(i, x, nominalQCD);
    
    for (const auto &syst : systList) {

      // For evt tables (same for bkg)
      double systUpW2000 = W2000Vars[syst+"_Up"]->GetBinContent(i+1);
      double systDownW2000 = W2000Vars[syst+"_Down"]->GetBinContent(i+1);
      double systUpW3600 = W3600Vars[syst+"_Up"]->GetBinContent(i+1);
      double systDownW3600 = W3600Vars[syst+"_Down"]->GetBinContent(i+1);
      double systUpW5600 = W5600Vars[syst+"_Up"]->GetBinContent(i+1);
      double systDownW5600 = W5600Vars[syst+"_Down"]->GetBinContent(i+1);
      double systUpWboson = WbosonVars[syst+"_Up"]->GetBinContent(i+1);
      double systDownWboson = WbosonVars[syst+"_Down"]->GetBinContent(i+1);
      double systUpTop = TopVars[syst+"_Up"]->GetBinContent(i+1);
      double systDownTop = TopVars[syst+"_Down"]->GetBinContent(i+1);
      double systUpZboson = ZbosonVars[syst+"_Up"]->GetBinContent(i+1);
      double systDownZboson = ZbosonVars[syst+"_Down"]->GetBinContent(i+1);
      double systUpDiBoson = DiBosonVars[syst+"_Up"]->GetBinContent(i+1);
      double systDownDiBoson = DiBosonVars[syst+"_Down"]->GetBinContent(i+1);
      double systUpQCD = QCDVars[syst+"_Up"]->GetBinContent(i+1);
      double systDownQCD = QCDVars[syst+"_Down"]->GetBinContent(i+1);

      systUpTotW2000 += (systUpW2000-nominalW2000)*(systUpW2000-nominalW2000);
      systDownTotW2000 += (nominalW2000-systDownW2000)*(nominalW2000-systDownW2000);
      systUpTotW3600 += (systUpW3600-nominalW3600)*(systUpW3600-nominalW3600);
      systDownTotW3600 += (nominalW3600-systDownW3600)*(nominalW3600-systDownW3600);
      systUpTotW5600 += (systUpW5600-nominalW5600)*(systUpW5600-nominalW5600);
      systDownTotW5600 += (nominalW5600-systDownW5600)*(nominalW5600-systDownW5600);
      systUpTotWboson += (systUpWboson-nominalWboson)*(systUpWboson-nominalWboson);
      systDownTotWboson += (nominalWboson-systDownWboson)*(nominalWboson-systDownWboson);
      systUpTotTop += (systUpTop-nominalTop)*(systUpTop-nominalTop);
      systDownTotTop += (nominalTop-systDownTop)*(nominalTop-systDownTop);
      systUpTotZboson += (systUpZboson-nominalZboson)*(systUpZboson-nominalZboson);
      systDownTotZboson += (nominalZboson-systDownZboson)*(nominalZboson-systDownZboson);
      systUpTotDiBoson += (systUpDiBoson-nominalDiBoson)*(systUpDiBoson-nominalDiBoson);
      systDownTotDiBoson += (nominalDiBoson-systDownDiBoson)*(nominalDiBoson-systDownDiBoson);
      systUpTotQCD += (systUpQCD-nominalQCD)*(systUpQCD-nominalQCD);
      systDownTotQCD += (nominalQCD-systDownQCD)*(nominalQCD-systDownQCD);
      
    } // Loop over systematics

    // Add normalization systematics (Lumi)
    systUpTotW2000 += (0.014*nominalW2000)*(0.014*nominalW2000);
    systDownTotW2000 += (0.014*nominalW2000)*(0.014*nominalW2000);
    systUpTotW3600 += (0.014*nominalW3600)*(0.014*nominalW3600);
    systDownTotW3600 += (0.014*nominalW3600)*(0.014*nominalW3600);
    systUpTotW5600 += (0.014*nominalW5600)*(0.014*nominalW5600);
    systDownTotW5600 += (0.014*nominalW5600)*(0.014*nominalW5600);
    systUpTotWboson += (0.014*nominalWboson)*(0.014*nominalWboson);
    systDownTotWboson += (0.014*nominalWboson)*(0.014*nominalWboson);
    systUpTotTop += (0.014*nominalTop)*(0.014*nominalTop);
    systDownTotTop += (0.014*nominalTop)*(0.014*nominalTop);
    systUpTotZboson += (0.014*nominalZboson)*(0.014*nominalZboson);
    systDownTotZboson += (0.014*nominalZboson)*(0.014*nominalZboson);
    systUpTotDiBoson += (0.014*nominalDiBoson)*(0.014*nominalDiBoson);
    systDownTotDiBoson += (0.014*nominalDiBoson)*(0.014*nominalDiBoson);
    systUpTotQCD += (0.014*nominalQCD)*(0.014*nominalQCD);
    systDownTotQCD += (0.014*nominalQCD)*(0.014*nominalQCD);
    // Add normalization systematics (xsec)
    systUpTotW2000 += (0.045*nominalW2000)*(0.045*nominalW2000);
    systDownTotW2000 += (0.045*nominalW2000)*(0.045*nominalW2000);
    systUpTotW3600 += (0.099*nominalW3600)*(0.099*nominalW3600);
    systDownTotW3600 += (0.099*nominalW3600)*(0.099*nominalW3600);
    systUpTotW5600 += (0.189*nominalW5600)*(0.189*nominalW5600);
    systDownTotW5600 += (0.189*nominalW5600)*(0.189*nominalW5600);
    systUpTotTop += (0.05*nominalTop)*(0.05*nominalTop);
    systDownTotTop += (0.05*nominalTop)*(0.05*nominalTop);
    systUpTotZboson += (0.02*nominalZboson)*(0.02*nominalZboson);
    systDownTotZboson += (0.02*nominalZboson)*(0.02*nominalZboson);
    systUpTotDiBoson += (0.04*nominalDiBoson)*(0.04*nominalDiBoson);
    systDownTotDiBoson += (0.04*nominalDiBoson)*(0.04*nominalDiBoson);
    systUpTotQCD += (0.5*nominalQCD)*(0.5*nominalQCD);
    systDownTotQCD += (0.5*nominalQCD)*(0.5*nominalQCD);

    systUpTotW2000 = sqrt(systUpTotW2000);
    systDownTotW2000 = sqrt(systDownTotW2000);
    systUpTotW3600 = sqrt(systUpTotW3600);
    systDownTotW3600 = sqrt(systDownTotW3600);
    systUpTotW5600 = sqrt(systUpTotW5600);
    systDownTotW5600 = sqrt(systDownTotW5600);
    systUpTotWboson = sqrt(systUpTotWboson);
    systDownTotWboson = sqrt(systDownTotWboson);
    systUpTotTop = sqrt(systUpTotTop);
    systDownTotTop = sqrt(systDownTotTop);
    systUpTotZboson = sqrt(systUpTotZboson);
    systDownTotZboson = sqrt(systDownTotZboson);
    systUpTotDiBoson = sqrt(systUpTotDiBoson);
    systDownTotDiBoson = sqrt(systDownTotDiBoson);
    systUpTotQCD = sqrt(systUpTotQCD);
    systDownTotQCD = sqrt(systDownTotQCD);

    W2000Syst->SetPointEYhigh(i, systUpTotW2000);
    W2000Syst->SetPointEYlow(i, systDownTotW2000);
    W3600Syst->SetPointEYhigh(i, systUpTotW3600);
    W3600Syst->SetPointEYlow(i, systDownTotW3600);
    W5600Syst->SetPointEYhigh(i, systUpTotW5600);
    W5600Syst->SetPointEYlow(i, systDownTotW5600);
    WbosonSyst->SetPointEYhigh(i, systUpTotWboson);
    WbosonSyst->SetPointEYlow(i, systDownTotWboson);
    TopSyst->SetPointEYhigh(i, systUpTotTop);
    TopSyst->SetPointEYlow(i, systDownTotTop);
    ZbosonSyst->SetPointEYhigh(i, systUpTotZboson);
    ZbosonSyst->SetPointEYlow(i, systDownTotZboson);
    DiBosonSyst->SetPointEYhigh(i, systUpTotDiBoson);
    DiBosonSyst->SetPointEYlow(i, systDownTotDiBoson);
    QCDSyst->SetPointEYhigh(i, systUpTotQCD);
    QCDSyst->SetPointEYlow(i, systDownTotQCD);

    //cout <<"  bin "<<i<<" --> Nom: "<<nominalWboson<<" + "<<systUpTotWboson<<" - "<<systDownTotWboson<< endl;
    
    //////////////
    //bkgSyst->SetPointEYhigh(i, );
    
  } // Loop over histogram bins 

  // For evt. tables
  Double_t W2000_SystFull = 0, W2000_Syst1000 = 0, W2000_Syst2000 = 0;
  Double_t W3600_SystFull = 0, W3600_Syst1000 = 0, W3600_Syst2000 = 0;
  Double_t W5600_SystFull = 0, W5600_Syst1000 = 0, W5600_Syst2000 = 0;
  Double_t Wboson_SystFull = 0, Wboson_Syst1000 = 0, Wboson_Syst2000 = 0;
  Double_t Top_SystFull = 0, Top_Syst1000 = 0, Top_Syst2000 = 0;
  Double_t Zboson_SystFull = 0, Zboson_Syst1000 = 0, Zboson_Syst2000 = 0;
  Double_t DiBoson_SystFull = 0, DiBoson_Syst1000 = 0, DiBoson_Syst2000 = 0;
  Double_t QCD_SystFull = 0, QCD_Syst1000 = 0, QCD_Syst2000 = 0;
  
  for (int i = 0; i < nBins; i++){
    W2000_SystFull += (W2000Syst->GetErrorY(i));
    W3600_SystFull += (W3600Syst->GetErrorY(i));
    W5600_SystFull += (W5600Syst->GetErrorY(i));
    Wboson_SystFull += (WbosonSyst->GetErrorY(i));
    Top_SystFull += (TopSyst->GetErrorY(i));
    Zboson_SystFull += (ZbosonSyst->GetErrorY(i));
    DiBoson_SystFull += (DiBosonSyst->GetErrorY(i));
    QCD_SystFull += (QCDSyst->GetErrorY(i));
  }/*
  W2000_SystFull = sqrt(W2000_SystFull);
  W3600_SystFull = sqrt(W3600_SystFull);
  W5600_SystFull = sqrt(W5600_SystFull);
  Wboson_SystFull = sqrt(Wboson_SystFull);
  Top_SystFull = sqrt(Top_SystFull);
  Zboson_SystFull = sqrt(Zboson_SystFull);
  DiBoson_SystFull = sqrt(DiBoson_SystFull);
  QCD_SystFull = sqrt(QCD_SystFull);
   */
  for (int i = 6; i < nBins; i++){
    W2000_Syst1000 += (W2000Syst->GetErrorY(i));
    W3600_Syst1000 += (W3600Syst->GetErrorY(i));
    W5600_Syst1000 += (W5600Syst->GetErrorY(i));
    Wboson_Syst1000 += (WbosonSyst->GetErrorY(i));
    Top_Syst1000 += (TopSyst->GetErrorY(i));
    Zboson_Syst1000 += (ZbosonSyst->GetErrorY(i));
    DiBoson_Syst1000 += (DiBosonSyst->GetErrorY(i));
    QCD_Syst1000 += (QCDSyst->GetErrorY(i));
  }/*
  W2000_Syst1000 = sqrt(W2000_Syst1000);
  W3600_Syst1000 = sqrt(W3600_Syst1000);
  W5600_Syst1000 = sqrt(W5600_Syst1000);
  Wboson_Syst1000 = sqrt(Wboson_Syst1000);
  Top_Syst1000 = sqrt(Top_Syst1000);
  Zboson_Syst1000 = sqrt(Zboson_Syst1000);
  DiBoson_Syst1000 = sqrt(DiBoson_Syst1000);
  QCD_Syst1000 = sqrt(QCD_Syst1000);
   */
  for (int i = 16; i < nBins; i++){
    W2000_Syst2000 += (W2000Syst->GetErrorY(i));
    W3600_Syst2000 += (W3600Syst->GetErrorY(i));
    W5600_Syst2000 += (W5600Syst->GetErrorY(i));
    Wboson_Syst2000 += (WbosonSyst->GetErrorY(i));
    Top_Syst2000 += (TopSyst->GetErrorY(i));
    Zboson_Syst2000 += (ZbosonSyst->GetErrorY(i));
    DiBoson_Syst2000 += (DiBosonSyst->GetErrorY(i));
    QCD_Syst2000 += (QCDSyst->GetErrorY(i));
  }/*
  W2000_Syst2000 = sqrt(W2000_Syst2000);
  W3600_Syst2000 = sqrt(W3600_Syst2000);
  W5600_Syst2000 = sqrt(W5600_Syst2000);
  Wboson_Syst2000 = sqrt(Wboson_Syst2000);
  Top_Syst2000 = sqrt(Top_Syst2000);
  Zboson_Syst2000 = sqrt(Zboson_Syst2000);
  DiBoson_Syst2000 = sqrt(DiBoson_Syst2000);
  QCD_Syst2000 = sqrt(QCD_Syst2000);
   */
  cout <<"Error Wprime2000 ==> Full: "<< W2000_SystFull <<" | mT > 1 TeV: "<< W2000_Syst1000 <<" | mT > 2 TeV: "<< W2000_Syst2000 << endl;
  cout <<"Error Wprime3600 ==> Full: "<< W3600_SystFull <<" | mT > 1 TeV: "<< W3600_Syst1000 <<" | mT > 2 TeV: "<< W3600_Syst2000 << endl;
  cout <<"Error Wprime5600 ==> Full: "<< W5600_SystFull <<" | mT > 1 TeV: "<< W5600_Syst1000 <<" | mT > 2 TeV: "<< W5600_Syst2000 << endl;
  cout <<"Error Wboson     ==> Full: "<< Wboson_SystFull <<" | mT > 1 TeV: "<< Wboson_Syst1000 <<" | mT > 2 TeV: "<< Wboson_Syst2000 << endl;
  cout <<"Error Top        ==> Full: "<< Top_SystFull <<" | mT > 1 TeV: "<< Top_Syst1000 <<" | mT > 2 TeV: "<< Top_Syst2000 << endl;
  cout <<"Error Zboson     ==> Full: "<< Zboson_SystFull <<" | mT > 1 TeV: "<< Zboson_Syst1000 <<" | mT > 2 TeV: "<< Zboson_Syst2000 << endl;
  cout <<"Error DiBoson    ==> Full: "<< DiBoson_SystFull <<" | mT > 1 TeV: "<< DiBoson_Syst1000 <<" | mT > 2 TeV: "<< DiBoson_Syst2000 << endl;
  cout <<"Error QCD        ==> Full: "<< QCD_SystFull <<" | mT > 1 TeV: "<< QCD_Syst1000 <<" | mT > 2 TeV: "<< QCD_Syst2000 << endl;

  /*
  for (int i = 0; i < nBins; i++){
    cout << "Uncertainties for Wboson" << endl;
    cout << "  bin " << i << " --> value: " << WbosonSyst->GetErrorYhigh(i) << " // Nominal: " << WbosonNominal->GetBinContent(i+1) << endl;
  }
  */
  //WbosonSyst->Draw();
  ////////////////

  
  
}// End of main 

void FinalPlotsWithSysts(){

  //SystPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/SSMlimit_TunePcorr/root/mT__pg_SystPlot.root", "2022");

  // For event tables
  SystPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/mT_progressiveCuts_Systs_EXO17Jun/root/mT_ref__pg_SSMlimits2022.root", "2022");
  SystPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/mT_progressiveCuts_Systs_EXO17Jun/root/mT_etaCut__pg_SSMlimits2022.root", "2022");
  SystPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/mT_progressiveCuts_Systs_EXO17Jun/root/mT_etaHPcut__pg_SSMlimits2022.root", "2022");
  SystPlot("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/mT_progressiveCuts_Systs_EXO17Jun/root/mT_etaHPmetNoMuCut__pg_SSMlimits2022.root", "2022");

}


