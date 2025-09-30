#include <TFile.h>
#include <TH1.h>
#include <TKey.h>
#include <TDirectory.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iomanip>

void makeDatacards(const char* infile, std::string outDir, std::string year, std::string checkName) {
    // Abrimos el ROOT file
    TFile *f = TFile::Open(infile);
    if (!f || f->IsZombie()) {
        std::cerr << "Error: no se pudo abrir el fichero " << infile << std::endl;
        return;
    }

    // Carpeta con histogramas
    TDirectory *histDir = (TDirectory*)f->Get("histograms");
    if (!histDir) {
        std::cerr << "No se encontró la carpeta 'histograms'." << std::endl;
        return;
    }

    // Lista de masas y couplings
    std::vector<int> masses = {400,600,1000,1600,2000,2600,3000,3600,4000,4600,5000,5600,6000,6600};
    std::vector<double> couplings = {0.01,0.1,1,2,3,5};

    // Backgrounds fijos
    std::vector<std::string> bkgs = {"W_boson","Top","Z_boson","DiBoson","QCD"};

    // Integral de datos
    TString data_name;
    if (year == "2022")
      data_name = "ReRecoData2022";
    else if (year == "2023")
      data_name = "PromptData2023";
    TH1* hData = (TH1*)histDir->Get(data_name);
    double obs = (hData) ? hData->Integral() : 0;

    std::cout << "Eventos observados: " << obs << std::endl;

    // Integrales de backgrounds
    std::map<std::string,double> bkgRates;
    for (auto &b : bkgs) {
        TH1* h = (TH1*)histDir->Get(b.c_str());
        if (h) bkgRates[b] = h->Integral();
        else bkgRates[b] = 0;
    }

    // Bucle sobre masas y couplings
    for (auto m : masses) {
        for (auto c : couplings) {
            std::string sigName;
            if (c == 1) sigName = "Wprime" + std::to_string(m);
            else {
                std::ostringstream cc;
                cc << std::fixed << std::setprecision(2) << c; // formatear 0.01 etc
                std::string cstr = cc.str();
                // quitar ceros a la derecha
                cstr.erase(cstr.find_last_not_of('0') + 1, std::string::npos);
                if (cstr.back() == '.') cstr.pop_back();
                sigName = "Wprime" + std::to_string(m) + "_kR" + cstr;
            }

            TH1* hSig = (TH1*)histDir->Get(sigName.c_str());
            if (!hSig) {
                std::cout << "Aviso: no encontré histograma " << sigName << std::endl;
                continue;
            }
            double sigRate = hSig->Integral();

            // Crear datacard
	    std::string outname = outDir + year + "/muon/" + checkName + "/datacard_" + sigName + ".txt";
            //std::string outname = outDir + "datacard_" + sigName + ".txt";
            std::ofstream card(outname);

            card << "imax    1 number of bins\n";
            card << "jmax    5 number of processes minus 1\n";
            card << "kmax    * number of nuisance parameters\n";
            card << "----------------------------------------------------------------------------------------------------------------------------\n";
	    card << "shapes data_obs * " << infile << " histograms/" << data_name << "\n";
            card << "shapes * * " << infile << " histograms/$PROCESS histograms/$PROCESS_$SYSTEMATIC\n";
            card << "----------------------------------------------------------------------------------------------------------------------------\n";
            card << "bin          muon_channel\n";
            card << "observation  " << obs << "\n";
            card << "-----------------------------------------------------------------------------------------------------------------------------\n";
            card << "bin                                   muon_channel         muon_channel   muon_channel   muon_channel   muon_channel   muon_channel\n";
            card << "process                               " << sigName << "     W_boson        Top            Z_boson        DiBoson        QCD\n";
            card << "process                               0                    1              2              3              4              5\n";
            card << "rate                                  " << sigRate << "     "
                 << bkgRates["W_boson"] << "  "
                 << bkgRates["Top"]     << "  "
                 << bkgRates["Z_boson"] << "  "
                 << bkgRates["DiBoson"] << "  "
                 << bkgRates["QCD"] << "\n";
            card << "-----------------------------------------------------------------------------------------------------------------------------\n";
            card << "cross_section_ttbar         lnN       -                    -              1.050          -              -              -\n";
            card << "cross_section_Z             lnN       -                    -              -              1.020          -              -\n";
            card << "cross_section_VV            lnN       -                    -              -              -              1.040          -\n";
            card << "cross_section_QCD           lnN       -                    -              -              -              -              1.50\n";
            card << "lumi_13p6TeV_" << year << "           lnN       1.014                1.014          1.014          1.014          1.014          1.014\n";
            card << "CMS_pileup_                 shape     1                    1              1              1              1              1\n";
            card << "CMS_eff_m_reco_" << year << "_        shape     1                    1              1              1              1              1\n";
            card << "CMS_eff_m_id_" << year << "_          shape     1                    1              1              1              1              1\n";
            card << "CMS_eff_m_iso_" << year << "_         shape     1                    1              1              1              1              1\n";
            card << "CMS_eff_m_trigger_" << year << "_     shape     1                    1              1              1              1              1\n";
            card << "CMS_eff_b_" << year << "_             shape     1                    1              1              1              1              1\n";
            card << "CMS_scale_met_" << year << "_         shape     1                    1              1              1              1              1\n";
            card << "CMS_scale_m_" << year << "_           shape     1                    1              1              1              1              1\n";
            card << "CMS_EXO24021_W_kfactor_     shape     -                    1              -              -              -              -\n";
            card << "pdf_qqbar_                  shape     -                    1              1              1              1              -\n";
            card << "* autoMCStats 10\n";

            card.close();
            std::cout << "Creado " << outname << " con rate=" << sigRate << std::endl;
        }
    }
}


void createCards_coupling(){
  
  //makeDatacards(
  //		"/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/CouplingLimits_finalCuts/root/mT__pg_CouplingLimits2022.root",
  //		"/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/datacards/CouplingLimits/", "2022", "fullCuts"
  //		);

  makeDatacards(
		"/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/CouplingLimits_finalCuts/root/mT__pg_CouplingLimits2023.root",
		"/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/datacards/CouplingLimits/", "2023", "fullCuts"
		);

}
