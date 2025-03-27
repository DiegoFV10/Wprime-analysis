import ROOT
import json

def root_to_json(root_file, json_file):

    root_f = ROOT.TFile(root_file, "READ")

    hist_to_key = {
        "W_boson_PDFError": "isW",
        "Top_PDFError": "isTop",
        "Z_boson_PDFError": "isZ",
        "DiBoson_PDFError": "isVV"
    }

    correctionlib_data = {
        "schema_version": 2,
        "corrections": []
    }

    # Loop over backgorund processes
    for hist_name, json_key in hist_to_key.items():
        hist = root_f.Get(hist_name)

        correction = {
            "name": json_key,
            "version": 0,
            "inputs": [
                {
                    "name": "mT_range",
                    "type": "real",
                    "description": "Transverse mass range"
                }
            ],
            "output": {
                "name": "pdf_error",
                "type": "real",
                "description": f"PDF error for {json_key}"
            },
            "data": {
                "nodetype": "binning",
                "input": "mT_range",
                "flow": "clamp",
                "edges": [],
                "content": []
            }
        }
        
        # Loop over histogram bins
        for bin in range(1, hist.GetNbinsX() + 1):
            mT_min = hist.GetBinLowEdge(bin)
            mT_max = hist.GetBinLowEdge(bin + 1)
            pdf_error = hist.GetBinContent(bin)

            correction["data"]["edges"].append(mT_min)
            correction["data"]["content"].append(pdf_error)

        correction["data"]["edges"].append(mT_max)

        correctionlib_data["corrections"].append(correction)

    # Write out JSON file
    with open(json_file, 'w') as f:
        json.dump(correctionlib_data, f, indent=4)

    print(f"Datos guardados en {json_file}")

    root_f.Close()

path = "/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/nanoaod_base_analysis/data/cmssw/CMSSW_13_0_13/src/Wprime/Modules/PDF/";
root_to_json(path + "PDFErrors.root", path + "pdf_errors.json")
