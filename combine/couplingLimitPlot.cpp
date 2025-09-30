#include <TCanvas.h>
#include <TGraph.h>
#include <TGraphAsymmErrors.h>
#include <TLegend.h>
#include <TLine.h>
#include <TAxis.h>
#include <TColor.h>
#include <TStyle.h>
#include <fstream>
#include <vector>
#include <string>
#include <iostream>

void couplingPlot(string inp_path, string year, string checkName, string inp_file) {
  
  // Open input file
  string fullInput = inp_path + year + "/Individual/" + checkName + "/" + inp_file;
  std::ifstream infile(fullInput);
  std::string header;
  std::getline(infile, header);

  std::vector<double> mass, low95, low68, expected, up68, up95, observed;
  double m, l95, l68, exp, u68, u95, obs;

  while (infile >> m >> l95 >> l68 >> exp >> u68 >> u95 >> obs) {
    mass.push_back(m);
    low95.push_back(l95);
    low68.push_back(l68);
    expected.push_back(exp);
    up68.push_back(u68);
    up95.push_back(u95);
    observed.push_back(obs);
  }

  int n = mass.size();

  // 68% & 95% CL intervals graphs
  TGraphAsymmErrors* band95 = new TGraphAsymmErrors(n);
  TGraphAsymmErrors* band68 = new TGraphAsymmErrors(n);

  for (int i = 0; i < n; i++) {
    band95->SetPoint(i, mass[i], expected[i]);
    band95->SetPointError(i, 0, 0, expected[i]-low95[i], up95[i]-expected[i]);

    band68->SetPoint(i, mass[i], expected[i]);
    band68->SetPointError(i, 0, 0, expected[i]-low68[i], up68[i]-expected[i]);
  }

  int col95 = TColor::GetColor("#f5bb54");
  int col68 = TColor::GetColor("#607641");

  band95->SetFillColor(col95);
  band68->SetFillColor(col68);

  // Expected & observed graphs
  TGraph* g_expected = new TGraph(n, &mass[0], &expected[0]);
  g_expected->SetLineStyle(7);
  g_expected->SetLineWidth(3);
  g_expected->SetLineColor(kBlack);

  TGraph* g_observed = new TGraph(n, &mass[0], &observed[0]);
  g_observed->SetLineStyle(1);
  g_observed->SetLineWidth(2);
  g_observed->SetLineColor(kBlack);

  // Horizontal line for SSM W' limit
  double xmin = mass.front();
  double xmax = mass.back();
  double ymin = 0.005;
  double ymax = 10.0;
  TLine* line1 = new TLine(xmin, 1.0, xmax, 1.0);
  line1->SetLineColor(kBlue);
  line1->SetLineStyle(7);
  line1->SetLineWidth(3);

  // Canvas
  TCanvas* c = new TCanvas("c", "Coupling Limits", 800, 600);
  c->SetLogy();

  // Draw graphs in order
  band95->SetTitle("");
  band95->GetXaxis()->SetTitle("M_{W'} (GeV)");
  band95->GetXaxis()->SetTitleOffset(1.2);
  band95->GetXaxis()->SetRangeUser(xmin, xmax);
  band95->GetYaxis()->SetTitle("g_{W'}/g_{W}");
  band95->SetMinimum(ymin);
  band95->SetMaximum(ymax);
  band95->Draw("A3");

  band68->Draw("3 SAME");
  g_expected->Draw("L SAME");
  g_observed->Draw("L SAME");
  line1->Draw("SAME");

  // Legend and comsetics
  TLegend* leg = new TLegend(0.60, 0.25, 0.90, 0.48);
  leg->SetBorderSize(0);
  leg->SetFillStyle(0);
  leg->AddEntry(g_observed, "Observed", "l");
  leg->AddEntry(g_expected, "Expected", "l");
  leg->AddEntry(band68, "#pm 1 s.d.", "f");
  leg->AddEntry(band95, "#pm 2 s.d.", "f");
  leg->AddEntry(line1, "SSM W' LO", "l");
  leg->Draw();

  TString channel_label = "#bf{#mu + p_{T}^{miss}}";
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

  // Save Plots
  c->SaveAs((inp_path + year + "/FullCoupling/couplingLimits_muon"+ year + "_" + checkName + ".png").c_str());
  c->SaveAs((inp_path + year + "/FullCoupling/couplingLimits_muon"+ year + "_" + checkName + ".pdf").c_str());
  
}

void couplingLimitPlot() {

  //couplingPlot("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/plots/CouplingLimits/", "2022", "fullCuts", "intersections_allMasses.txt");

  //couplingPlot("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/plots/CouplingLimits/", "2023", "fullCuts", "intersections_allMasses.txt");
  
  couplingPlot("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/plots/CouplingLimits/", "22+23", "fullCuts", "intersections_allMasses.txt");
  
}
