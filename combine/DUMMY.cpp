#include <TFile.h>
#include <TTree.h>
#include <TBranch.h>
#include <TSystemDirectory.h>
#include <TList.h>
#include <TSystemFile.h>
#include <iostream>
#include <vector>

void readLimits(TString folder) {
    // Vector con las masas de Wprime que quieres procesar
  std::vector<int> masses = {400, 600, 1000, 1600, 2000, 2600, 3000, 3600, 4000, 4600, 5000, 5600, 6000, 6600};  // Añade todas las masas que necesites

// Creamos un objeto TSystemDirectory para listar los archivos en el directorio
    TSystemDirectory dir(folder, folder);
    TList* files = dir.GetListOfFiles();

    if (!files) {
        std::cerr << "Error al leer el directorio: " << folder << std::endl;
        return;
    }

    // Loop sobre las masas
    for (int mass : masses) {
        // Expresión regular para encontrar archivos con la masa correcta
        TString pattern = TString::Format("higgsCombine_Wprime%d.MarkovChainMC.mH120.*.root", mass);
        TRegexp regex(pattern);

        // Iteramos sobre los archivos del directorio
        TIter next(files);
        TSystemFile* file;
        while ((file = (TSystemFile*)next())) {
            TString fileName = file->GetName();

            // Verificamos si el archivo coincide con el patrón
            if (!file->IsDirectory() && fileName.Index(regex) != -1) {
                TString fullPath = folder + fileName;

                // Abrimos el fichero ROOT
                TFile* rootFile = TFile::Open(fullPath);
                if (!rootFile || rootFile->IsZombie()) {
                    std::cerr << "Error al abrir el fichero: " << fullPath << std::endl;
                    continue;
                }

                // Accedemos al TTree "limit"
                TTree* tree = (TTree*)rootFile->Get("limit");
                if (!tree) {
                    std::cerr << "Error al acceder al TTree 'limit' en el fichero: " << fullPath << std::endl;
                    rootFile->Close();
                    continue;
                }

                // Variable para almacenar el valor de la branch "limit"
                double limitValue;
                tree->SetBranchAddress("limit", &limitValue);

		tree->GetEntry(0);
		std::cout << "Masa Wprime " << mass << " - Valor de 'limit': " << limitValue << std::endl;

                // Cerramos el fichero ROOT
                rootFile->Close();
            }
        }
    }

    // Limpiamos
    delete files;
}



void DUMMY(){

  readLimits("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/outputs/SSM/2023/muon/unblind/");
  
}
