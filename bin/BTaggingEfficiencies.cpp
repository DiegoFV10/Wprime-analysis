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


void computeEff(string histFile, string year, string period){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  string pg;
  if(year == "2022")
    pg = "__noweights__pg_2022ReReco.root";
  else if(year == "2023")
    pg = "__noweights__pg_2023_full.root";

  TFile *b      =  TFile::Open((histFile + "Jet_pt_b" + pg).c_str());
  TFile *b_btag =  TFile::Open((histFile + "Jet_pt_b_btag" + pg).c_str());
  TFile *c      =  TFile::Open((histFile + "Jet_pt_c" + pg).c_str());
  TFile *c_btag =  TFile::Open((histFile + "Jet_pt_c_btag" + pg).c_str());
  TFile *uds      =  TFile::Open((histFile + "Jet_pt_uds" + pg).c_str());
  TFile *uds_btag =  TFile::Open((histFile + "Jet_pt_uds_btag" + pg).c_str());  

  std::map<std::string, TH1*> b_hist;
  std::map<std::string, TH1*> b_btag_hist;
  std::map<std::string, TH1*> c_hist;
  std::map<std::string, TH1*> c_btag_hist;
  std::map<std::string, TH1*> uds_hist;
  std::map<std::string, TH1*> uds_btag_hist;

  std::map<std::string, TGraphAsymmErrors*> b_eff;
  std::map<std::string, TGraphAsymmErrors*> c_eff;
  std::map<std::string, TGraphAsymmErrors*> uds_eff;

  std::vector<std::string> backgrounds = {"Wprime2000", "W_boson", "Top", "Z_boson", "DiBoson", "QCD", "background"};
  
  for(auto & elem: backgrounds){
    std::string bkg = elem;
    b_hist[bkg]      = (TH1D*) b->Get(("histograms/" + bkg).c_str());
    b_btag_hist[bkg] = (TH1D*) b_btag->Get(("histograms/" + bkg).c_str());
    c_hist[bkg]      = (TH1D*) c->Get(("histograms/" + bkg).c_str());
    c_btag_hist[bkg] = (TH1D*) c_btag->Get(("histograms/" + bkg).c_str());
    uds_hist[bkg]      = (TH1D*) uds->Get(("histograms/" + bkg).c_str());
    uds_btag_hist[bkg] = (TH1D*) uds_btag->Get(("histograms/" + bkg).c_str());    

    b_eff[bkg] = new TGraphAsymmErrors(b_btag_hist[bkg], b_hist[bkg]);
    c_eff[bkg] = new TGraphAsymmErrors(c_btag_hist[bkg], c_hist[bkg]);
    uds_eff[bkg] = new TGraphAsymmErrors(uds_btag_hist[bkg], uds_hist[bkg]);

    TString title = "#bf{CMS} #it{Simulation}                                       2022 preEE (13.6 TeV)";
    TLatex* preliminary = new TLatex(0.12,0.91, title);
    preliminary->SetNDC();
    preliminary->SetTextFont(42);
    preliminary->SetTextSize(0.039);
    
    TCanvas* c_b = new TCanvas(("b_" + bkg).c_str(),"",600,500);
    c_b->cd();
    c_b->Draw();
    b_eff[bkg]->SetTitle(("b-eff. " + bkg).c_str());
    b_eff[bkg]->GetXaxis()->SetTitle("Jet p_{T} [GeV]");
    b_eff[bkg]->GetXaxis()->SetTitleOffset(1.2);
    b_eff[bkg]->GetXaxis()->SetRangeUser(0, 1000);
    b_eff[bkg]->GetYaxis()->SetTitle("Efficiency");
    b_eff[bkg]->GetYaxis()->SetTitleOffset(1.3);
    b_eff[bkg]->SetLineWidth(2);
    b_eff[bkg]->Draw("AP");
    preliminary->Draw();

    TCanvas* c_c = new TCanvas(("c_" + bkg).c_str(),"",600,500);
    c_c->cd();
    c_c->Draw();
    c_eff[bkg]->SetTitle(("c-eff. " + bkg).c_str());
    c_eff[bkg]->GetXaxis()->SetTitle("Jet p_{T} [GeV]");
    c_eff[bkg]->GetXaxis()->SetTitleOffset(1.2);
    c_eff[bkg]->GetXaxis()->SetRangeUser(0, 1000);
    c_eff[bkg]->GetYaxis()->SetTitle("Efficiency");
    c_eff[bkg]->GetYaxis()->SetTitleOffset(1.3);
    c_eff[bkg]->SetLineWidth(2);
    c_eff[bkg]->Draw("AP");
    preliminary->Draw();
    
    TCanvas* c_uds = new TCanvas(("uds_" + bkg).c_str(),"",600,500);
    c_uds->cd();
    c_uds->Draw();
    uds_eff[bkg]->SetTitle(("light-eff. " + bkg).c_str());
    uds_eff[bkg]->GetXaxis()->SetTitle("Jet p_{T} [GeV]");
    uds_eff[bkg]->GetXaxis()->SetTitleOffset(1.2);
    uds_eff[bkg]->GetXaxis()->SetRangeUser(0, 1000);
    uds_eff[bkg]->GetYaxis()->SetTitle("Efficiency");
    uds_eff[bkg]->GetYaxis()->SetTitleOffset(1.3);
    uds_eff[bkg]->SetLineWidth(2);
    uds_eff[bkg]->Draw("AP");
    preliminary->Draw();

    /// Save plots ///
    c_b->SaveAs(("plots/BTagEff/"+ bkg +"_b-eff_"+ year + period +".png").c_str());
    c_c->SaveAs(("plots/BTagEff/"+ bkg +"_c-eff_"+ year + period +".png").c_str());
    c_uds->SaveAs(("plots/BTagEff/"+ bkg +"_light-eff_"+ year + period +".png").c_str());

    //if(bkg == "background"){
    //  c_b->SaveAs(("plots/BTagEff/"+ bkg +"_b-eff_"+ year + period +".root").c_str());
    //  c_c->SaveAs(("plots/BTagEff/"+ bkg +"_c-eff_"+ year + period +".root").c_str());
    //  c_uds->SaveAs(("plots/BTagEff/"+ bkg +"_light-eff_"+ year + period +".root").c_str());
    //}

    /// Output efficiencies ///
    if(bkg == "background"){
      std::vector<int> bins = {40, 60, 85, 120, 170, 250, 450, 800};
      cout << "\n Efficiencies for run period " << year << period << endl;
      for (size_t i = 0; i < bins.size(); i++){
	cout << "\t b-eff for pT " << bins.at(i) << " GeV : " << b_eff[bkg]->Eval(bins.at(i)) << endl;
	cout << "\t c-eff for pT " << bins.at(i) << " GeV : " << c_eff[bkg]->Eval(bins.at(i)) << endl;
	cout << "\t light-eff for pT " << bins.at(i) << " GeV : " << uds_eff[bkg]->Eval(bins.at(i)) << "\n" << endl;
      }
    }

  } // Loop over different MC backgrounds

  

}// End of main 

void BTaggingEfficiencies(){

  computeEff("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/BTagHist_2022preEE_v2_NoNorm/root/", "2022", "preEE");
  //computeEff("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/BTagHist_2022postEE_v2_NoNorm/root/", "2022", "postEE");
  
  //computeEff("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/BTagHist_2023preBPix_v2_NoNorm/root/", "2023", "preBPix");
  //computeEff("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/BTagHist_2023postBPix_v2_NoNorm/root/", "2023", "postBPix");
  
}


