#include <TFile.h>
#include <TH1.h>
#include <TDirectory.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iomanip>
#include <map>

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

    // Lista de masas y valores de sistemático extra
    std::vector<int> masses = {400,600,1000,1600,2000,2600,3000,3600,4000,4600,5000,5600,6000,6600};
    std::vector<double> systsPDFas = {1.017, 1.020, 1.026, 1.037, 1.045, 1.059, 1.071, 1.099,
                                    1.124, 1.162, 1.180, 1.189, 1.179, 1.161};

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

    // Bucle sobre masas
    for (size_t i = 0; i < masses.size(); i++) {
        int m = masses[i];
        double systPDFas = systsPDFas[i];

        std::string sigName = "Wprime" + std::to_string(m);

        TH1* hSig = (TH1*)histDir->Get(sigName.c_str());
        if (!hSig) {
            std::cout << "Aviso: no encontré histograma " << sigName << std::endl;
            continue;
        }
        double sigRate = hSig->Integral();

        // Crear datacard
        std::string outname = outDir + year + "/muon/" + checkName + "/datacard_" + sigName + ".txt";
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
        card << "CMS_EXO24021_Wprime_PDF+as  lnN       " << systPDFas << "          -              -              -              -              -\n";
        card << "* autoMCStats 10\n";

        card.close();
        std::cout << "Creado " << outname << " con rate=" << sigRate << " y syst=" << systPDFas << std::endl;
    }
}

void createCards_SSM() {
  //makeDatacards(
  //      "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/feedback27Aug_SSMlimits_noZeroJets-v2/root/mT_noZeroJets2022EE__pg_SSMlimits2022.root",
  //     "/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/datacards/SSM/", "2022", "NjetsGT0_only22EE"
  //  );
  //makeDatacards(
  //     "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2022_config/cat_preselection/feedback27Aug_SSMlimits_noZeroJets-v2/root/mT_noZeroJets__pg_SSMlimits2022.root",
  //      "/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/datacards/SSM/", "2022", "NjetsGT0"
  //  );

  makeDatacards(
        "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/feedback27Aug_SSMlimits_noZeroJets/root/mT__pg_SSMlimits2023.root",
        "/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/datacards/SSM/", "2023", "NjetsGT0_only22EE"
    );
  makeDatacards(
        "/eos/user/d/diegof/cmt/FeaturePlot/Wprime_2023_config/cat_preselection/feedback27Aug_SSMlimits_noZeroJets/root/mT_noZeroJets__pg_SSMlimits2023.root",
        "/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/datacards/SSM/", "2023", "NjetsGT0"
    );
}
