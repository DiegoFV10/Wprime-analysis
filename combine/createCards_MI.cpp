#include <TFile.h>
#include <TH1D.h>
#include <TKey.h>
#include <TDirectory.h>
#include <TString.h>
#include <TList.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <map>
#include <string>

void make_cards_and_roots(TString infile, TString year, TString outDir, TString checkName) {

  double lumi;
  TString dataHist;
  if (year == "2022") {
    lumi = 34.652;
    dataHist = "ReRecoData2022";
  } else if (year == "2023") {
    lumi = 27.101;
    dataHist = "PromptData2023";
  }
  
  // Open original file
  TFile *fin = TFile::Open(infile, "READ");
  if (!fin || fin->IsZombie()) {
    std::cerr << "Error: connot open file " << infile << std::endl;
    return;
  }
  TDirectory *dir = (TDirectory*)fin->Get("histograms");
  if (!dir) {
    std::cerr << "Error: connot find histograms folder." << std::endl;
    return;
  }
  
  // Read Data hist (for bin edges)
  TH1D *hData = (TH1D*)dir->Get(dataHist);
  if (!hData) {
    std::cerr << "Error: cannot find data histogram." << std::endl;
    return;
  }

  int nbins = hData->GetNbinsX();

  // Loop over all mT bins
  for (int ibin = 1; ibin <= nbins; ibin++) {
    int mTmin = (int)hData->GetXaxis()->GetBinLowEdge(ibin);
    int mTnext = (ibin < nbins) ?
      (int)hData->GetXaxis()->GetBinLowEdge(ibin+1) :
      (int)hData->GetXaxis()->GetBinUpEdge(nbins);

    TString outrootname = Form("histograms_mTmin_%d_lumi_%.2f.root", mTmin, lumi);
    TString outFullName = outDir + year + "/muon/" + checkName + "/" + outrootname;
    TFile *fout = new TFile(outFullName, "RECREATE");

    std::vector<TString> processNames;
    processNames.push_back("Signal");
    processNames.push_back("W_boson");
    processNames.push_back("Top");
    processNames.push_back("Z_boson");
    processNames.push_back("DiBoson");
    processNames.push_back("QCD");

    // Run over all histograms from input
    TIter nextkey(dir->GetListOfKeys());
    TKey *key;
    while ((key = (TKey*)nextkey())) {
      TString hname = key->GetName();
      TH1D *hOrig = (TH1D*)dir->Get(hname);
      if (!hOrig) continue;

      // Rename Data histo
      TString newname = (hname == dataHist) ? "data_obs" : hname;
      TH1D *hNew = new TH1D(newname, "", 1, mTmin, mTnext);

      int bin_start = hOrig->GetXaxis()->FindBin(mTmin);
      double integral = hOrig->Integral(bin_start, hOrig->GetNbinsX());
      double err2 = 0.0;
      for (int b = bin_start; b <= hOrig->GetNbinsX(); b++) {
	err2 += std::pow(hOrig->GetBinError(b), 2);
      }

      hNew->SetBinContent(1, integral);
      hNew->SetBinError(1, std::sqrt(err2));
      hNew->Write();
    }

    // Add Signal hist
    TH1D *hSig = new TH1D("Signal", "", 1, mTmin, mTnext);
    hSig->SetBinContent(1, lumi);
    hSig->Write();

    fout->Close();

    /// PART II: Create the datacards ///
    
    // Open root file again for creating the datacards
    TFile *fcheck = TFile::Open(outFullName, "READ");
    double obs = ((TH1D*)fcheck->Get("data_obs"))->GetBinContent(1);

    // Final lists of processes with rates != 0
    std::vector<TString> processes;
    std::vector<double> rates;

    // List of shape systematics
    std::vector<TString> shapes;
    if (year == "2022"){
      shapes = {
	"CMS_pileup_", "CMS_eff_m_reco_2022_", "CMS_eff_m_id_2022_",
	"CMS_eff_m_iso_2022_", "CMS_eff_m_trigger_2022_", "CMS_eff_b_2022_",
	"CMS_scale_met_2022_", "CMS_scale_m_2022_", "CMS_EXO24021_W_kfactor_",
	"pdf_qqbar_"
      };
    } else if (year == "2023"){
      shapes = {
	"CMS_pileup_", "CMS_eff_m_reco_2023_", "CMS_eff_m_id_2023_",
	"CMS_eff_m_iso_2023_", "CMS_eff_m_trigger_2023_", "CMS_eff_b_2023_",
	"CMS_scale_met_2023_", "CMS_scale_m_2023_", "CMS_EXO24021_W_kfactor_",
	"pdf_qqbar_"
      };  
    }
    
    for (auto &p : processNames) {
      TH1D *hNom = (TH1D*)fcheck->Get(p);
      if (!hNom) continue;
      double valNom = hNom->GetBinContent(1);

      bool keep = true;
      if (valNom <= 0.0) {
	keep = false;
      } else {
	// Check all syst. variations
	for (auto &syst : shapes) {
	  TString hUp = p + "_" + syst + "Up";
	  TString hDown = p + "_" + syst + "Down";

	  TH1D *hU = (TH1D*)fcheck->Get(hUp);
	  TH1D *hD = (TH1D*)fcheck->Get(hDown);

	  if ((hU && hU->GetBinContent(1) <= 0.0) ||
	      (hD && hD->GetBinContent(1) <= 0.0)) {
	    keep = false;
	    break;
	  }
	}
      }

      if (keep) {
	processes.push_back(p);
	rates.push_back(valNom);
      }
    }
  
    TString datacardName = outDir + year + "/muon/" + checkName + "/" + Form("datacard_mTmin_%d_lumi_%.2f.txt", mTmin, lumi);
    std::ofstream card(datacardName.Data());

    // Write the datacard
    card << "imax    1 number of bins\n";
    card << "jmax    " << processes.size()-1 << " number of processes minus 1\n";
    card << "kmax    * number of nuisance parameters\n";
    card << "----------------------------------------------------------------------------------------------------------------------------\n";
    card << "shapes * * " << outrootname << " $PROCESS $PROCESS_$SYSTEMATIC\n";
    card << "----------------------------------------------------------------------------------------------------------------------------\n";
    card << "bin          muon_channel\n";
    card << "observation  " << obs << "\n";
    card << "-----------------------------------------------------------------------------------------------------------------------------\n";

    // Processes
    card << "bin                                   ";
    for (size_t i=0; i<processes.size(); i++) card << "muon_channel   ";
    card << "\n";

    card << "process                               ";
    for (auto &p : processes) card << p << "         ";
    card << "\n";

    card << "process                               ";
    for (size_t i=0; i<processes.size(); i++) card << i << "              ";
    card << "\n";

    card << "rate                                  ";
    for (auto &r : rates) card << r << "         ";
    card << "\n";

    card << "-----------------------------------------------------------------------------------------------------------------------------\n";

    // Log-normal systematics
    std::map<std::string, std::map<std::string, std::string>> lnN_map;
    if (year == "2022"){
      lnN_map = {
	{"cross_section_ttbar", {{"Top", "1.050"}}},
	{"cross_section_Z",     {{"Z_boson", "1.020"}}},
	{"cross_section_VV",    {{"DiBoson", "1.040"}}},
	{"cross_section_QCD",   {{"QCD", "1.50"}}},
	{"lumi_13p6TeV_2022",   {{"Signal", "1.014"}, {"W_boson","1.014"}, {"Top","1.014"},
				 {"Z_boson","1.014"}, {"DiBoson","1.014"}, {"QCD","1.014"}}}
      };
    } else if (year == "2023"){
      lnN_map = {
	{"cross_section_ttbar", {{"Top", "1.050"}}},
	{"cross_section_Z",     {{"Z_boson", "1.020"}}},
	{"cross_section_VV",    {{"DiBoson", "1.040"}}},
	{"cross_section_QCD",   {{"QCD", "1.50"}}},
	{"lumi_13p6TeV_2023",   {{"Signal", "1.013"}, {"W_boson","1.013"}, {"Top","1.013"},
				 {"Z_boson","1.013"}, {"DiBoson","1.013"}, {"QCD","1.013"}}}
      };
    }   
    for (auto &syst : lnN_map) {
      card << syst.first << "   lnN   ";
      for (auto &p : processes) {
	std::string pname = p.Data();
	auto it = syst.second.find(pname);
	if (it != syst.second.end())
	  card << it->second << "    ";
	else
	  card << "-    ";
      }
      card << "\n";
    }

    // Shape systematics (Not considered for Signal for the moment)
    for (auto &s : shapes) {
      card << s << "     shape     ";
      for (size_t i=0; i<processes.size(); i++) {
        if (processes[i] == "Signal")
	  card << "-              ";
        else
	  card << "1              ";
      }
      card << "\n";
    }

    card << "* autoMCStats 10\n";
    card.close();

    fcheck->Close();
    
  } // Loop over all mT bins

  fin->Close();
  std::cout << "Done: Rootfiles and datacards created." << std::endl;
}

void createCards_MI() {

  //make_cards_and_roots("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/MIlimits/root/mT__pg_SSMlimits2022.root", "2022",
  //		       "/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/datacards/MI/", "fullCuts");

    make_cards_and_roots("/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/MIlimits/root/mT__pg_SSMlimits2023.root", "2023",
			 "/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/datacards/MI/", "fullCuts");
}
