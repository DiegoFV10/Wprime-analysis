#include <TCanvas.h>
#include <TGraph.h>
#include <TGraphErrors.h>
#include <TGraphAsymmErrors.h>
#include <TLegend.h>
#include <TLatex.h>
#include <TStyle.h>
#include <TColor.h>
#include <TSpline.h>
#include <algorithm>
#include <cassert>
#include <cmath>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iostream>
#include <limits>
#include <map>
#include <regex>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

namespace fs = std::filesystem;

struct LimitPoint {
  double expected{NAN};
  double low68{NAN};
  double up68{NAN};
  double low95{NAN};
  double up95{NAN};
  double observed{NAN};
};

// Robust readers (compatible with various Combine outputs)
bool readExpectedFile(const std::string &filename, double &median, double &low68, double &up68, double &low95, double &up95) {
  std::ifstream in(filename);
  if (!in) return false;
  std::string line;

  // Accept "median expected limit"
  std::regex r_med_1(R"(median expected limit: r < ([0-9]*\.?[0-9]+))");
  std::regex r_68_1(R"(68% expected band : ([0-9]*\.?[0-9]+) < r < ([0-9]*\.?[0-9]+))");
  std::regex r_95_1(R"(95% expected band : ([0-9]*\.?[0-9]+) < r < ([0-9]*\.?[0-9]+))");

  // Also accept standard Combine prints ("Expected 50.0%: r < ...")
  std::regex r_med_2(R"(Expected 50\.0%: r < ([0-9]*\.?[0-9]+))");
  std::regex r_16_2(R"(Expected 16\.0%: r < ([0-9]*\.?[0-9]+))");
  std::regex r_84_2(R"(Expected 84\.0%: r < ([0-9]*\.?[0-9]+))");
  std::regex r_2p5_2(R"(Expected 2\.5%: r < ([0-9]*\.?[0-9]+))");
  std::regex r_97p5_2(R"(Expected 97\.5%: r < ([0-9]*\.?[0-9]+))");

  bool got_med=false, got_68=false, got_95=false;
  double p16=NAN, p84=NAN, p2p5=NAN, p97p5=NAN;

  while (std::getline(in,line)) {
    std::smatch m;
    if (std::regex_search(line,m,r_med_1)) { median = std::stod(m[1]); got_med=true; }
    if (std::regex_search(line,m,r_68_1)) { low68 = std::stod(m[1]); up68 = std::stod(m[2]); got_68=true; }
    if (std::regex_search(line,m,r_95_1)) { low95 = std::stod(m[1]); up95 = std::stod(m[2]); got_95=true; }

    if (std::regex_search(line,m,r_med_2)) { median = std::stod(m[1]); got_med=true; }
    if (std::regex_search(line,m,r_16_2)) { p16 = std::stod(m[1]); }
    if (std::regex_search(line,m,r_84_2)) { p84 = std::stod(m[1]); }
    if (std::regex_search(line,m,r_2p5_2)) { p2p5 = std::stod(m[1]); }
    if (std::regex_search(line,m,r_97p5_2)) { p97p5 = std::stod(m[1]); }
  }
  in.close();

  if (!got_68 && !std::isnan(p16) && !std::isnan(p84)) {
    low68 = p16; up68 = p84; got_68 = true;
  }
  if (!got_95 && !std::isnan(p2p5) && !std::isnan(p97p5)) {
    low95 = p2p5; up95 = p97p5; got_95 = true;
  }

  return got_med && got_68 && got_95;
}

bool readObservedFile(const std::string &filename, double &observed) {
  std::ifstream in(filename);
  if (!in) return false;
  std::string line;
  std::regex r_obs_1(R"(Limit: r < ([0-9]*\.?[0-9]+))");
  std::regex r_obs_2(R"(Observed Limit: r < ([0-9]*\.?[0-9]+))");
  while (std::getline(in,line)) {
    std::smatch m;
    if (std::regex_search(line,m,r_obs_1) || std::regex_search(line,m,r_obs_2)) {
      observed = std::stod(m[1]);
      in.close();
      return true;
    }
  }
  in.close();
  return false;
}

// Find a file by applying a regex to the *filename* while scanning recursively under baseDir
std::string findFile(const fs::path &baseDir, const std::regex &nameRe) {
  for (auto const &p : fs::recursive_directory_iterator(baseDir)) {
    if (!p.is_regular_file()) continue;
    const std::string name = p.path().filename().string();
    if (std::regex_match(name, nameRe)) return p.path().string();
  }
  return "";
}


// Brent's method for a scalar function f on [a,b] where f(a) and f(b) have opposite signs
static double brent_root(const std::function<double(double)>& f, double a, double b, double tol=1e-10, int maxIter=100) {
  
  double fa = f(a);
  double fb = f(b);
  if (std::isnan(fa) || std::isnan(fb)) return NAN;
  if (fa == 0.0) return a;
  if (fb == 0.0) return b;
  if (fa * fb > 0) return NAN; // no sign change

  double c = a;
  double fc = fa;
  double s = b;
  double fs = fb;
  bool mflag = true;
  double d = 0.0;

  for (int iter = 0; iter < maxIter; ++iter) {
    if (fa != fc && fb != fc) {
      // Inverse quadratic interpolation
      s = a * (fb * fc) / ((fa - fb) * (fa - fc))
        + b * (fa * fc) / ((fb - fa) * (fb - fc))
        + c * (fa * fb) / ((fc - fa) * (fc - fb));
    } else {
      // Secant method
      s = b - fb * (b - a) / (fb - fa);
    }

    double cond1 = (s < (3 * a + b) / 4.0 || s > b);
    double cond2 = (mflag && std::abs(s - b) >= std::abs(b - c) / 2.0);
    double cond3 = (!mflag && std::abs(s - b) >= std::abs(c - d) / 2.0);
    double cond4 = (mflag && std::abs(b - c) < tol);
    double cond5 = (!mflag && std::abs(c - d) < tol);

    if (cond1 || cond2 || cond3 || cond4 || cond5) {
      s = 0.5 * (a + b);
      mflag = true;
    } else {
      mflag = false;
    }

    fs = f(s);
    d = c; c = b; fc = fb;

    if (std::isnan(fs)) return NAN; // something went wrong in evaluation

    if (fa * fs < 0) { b = s; fb = fs; }
    else { a = s; fa = fs; }

    if (std::abs(fa) < std::abs(fb)) {
      std::swap(a, b);
      std::swap(fa, fb);
    }

    if (std::abs(b - a) < tol) return b;
  }
  return NAN; // did not converge
}

// Find first intersection using cubic splines + Brent's method. Returns NAN if none found.
// We sample the interval [x_min,x_max] densely to bracket roots, then refine with Brent.

double findIntersection(const std::vector<double>& x, const std::vector<double>& y_limit, const std::vector<double>& y_theory) {
  
  assert(x.size()==y_limit.size() && x.size()==y_theory.size());

  // Collect finite points for each curve
  std::vector<double> xl, yl, xt, yt;
  for (size_t i=0;i<x.size();++i){
    if (!std::isnan(y_limit[i])) { xl.push_back(x[i]); yl.push_back(y_limit[i]); }
    if (!std::isnan(y_theory[i])) { xt.push_back(x[i]); yt.push_back(y_theory[i]); }
  }

  if (xl.size() < 2 || xt.size() < 2) return NAN; // not enough points to build splines

  // domain overlap
  double xmin_l = xl.front(), xmax_l = xl.back();
  double xmin_t = xt.front(), xmax_t = xt.back();
  double x_min = std::max(xmin_l, xmin_t);
  double x_max = std::min(xmax_l, xmax_t);
  if (x_min >= x_max) return NAN;

  // Build splines
  TSpline3 *s_lim = nullptr;
  TSpline3 *s_th  = nullptr;
  try {
    s_lim = new TSpline3("s_lim", &xl[0], &yl[0], (int)xl.size());
    s_th  = new TSpline3("s_th",  &xt[0], &yt[0], (int)xt.size());
  } catch (...) {
    delete s_lim; delete s_th;
    return NAN;
  }

  // difference function
  auto diff = [&](double xx)->double {
    double v1 = s_lim->Eval(xx);
    double v2 = s_th->Eval(xx);
    if (std::isnan(v1) || std::isnan(v2)) return std::numeric_limits<double>::quiet_NaN();
    return v1 - v2;
  };

  // dense scan to find bracket
  const int Nscan = 500; // increase for more robust bracketing if needed
  double prev_x = x_min;
  double prev_f = diff(prev_x);
  if (prev_f == 0.0) {
    delete s_lim; delete s_th;
    return prev_x;
  }

  double dx = (x_max - x_min) / (Nscan - 1);
  double found_root = NAN;
  for (int i = 1; i < Nscan; ++i) {
    double xi = x_min + i * dx;
    double fi = diff(xi);
    if (std::isnan(fi) || std::isnan(prev_f)) { prev_x = xi; prev_f = fi; continue; }
    if (fi == 0.0) { found_root = xi; break; }
    if (prev_f * fi < 0.0) {
      // bracket found between prev_x and xi
      std::function<double(double)> fwrap = [&](double xx){ return diff(xx); };
      double root = brent_root(fwrap, prev_x, xi, 1e-12, 200);
      if (!std::isnan(root)) { found_root = root; break; }
    }
    prev_x = xi; prev_f = fi;
  }

  delete s_lim; delete s_th;
  return found_root; // may be NAN
}


// Main worker: for each mass, build curves vs coupling, draw, and write intersections

void plotVScoupling(const std::string &baseDir, string year, const std::string &xsecTable, const std::string &outDir, bool drawObserved=true) {
  
  fs::create_directories(outDir);

  // Vectors for masses & couplings
  const std::vector<int> masses = {600,1000,1600,2000,2600,3000,3600,4000,4600,5000,5600,6000,6600}; // I have removed the 400 mass point
  const std::vector<double> couplings = {0.01,0.1,1,2,3,5};

  // Load cross sections from file (mass, coupling, xsec)
  std::map<int, std::map<double,double>> theory; // mass -> (coupling -> xsec)
  {
    std::ifstream xs(xsecTable);
    if (!xs.is_open()) {
      std::cerr << "Cannot open file containing cross sections: " << xsecTable << "\n";
      return;
    }
    int m; double c, sigma;
    while (xs >> m >> c >> sigma) theory[m][c] = sigma;
    xs.close();
  }

  gStyle->SetOptStat(0);

  const std::string outTxt = (fs::path(outDir)/"intersections_allMasses.txt").string();
  std::ofstream fout(outTxt);
  fout << "#mass low95 low68 expected up68 up95 observed\n";

  for (int m : masses) {
    // Collect points (expected bands, observed) per coupling
    std::vector<LimitPoint> points(couplings.size());

    for (size_t i = 0; i < couplings.size(); ++i) {
      const double c = couplings[i];

      // Build regexes to find files. Allow scientific or decimal numbers in token.
      std::ostringstream ce; ce.setf(std::ios::fixed); ce.precision((c<0.1)?2: (c<1?1:0)); ce << c; // format to match filenames for coupling
      const std::string cstr = ce.str();

      std::regex re_exp("^Wprime" + std::to_string(m) + "_kR" + cstr + R"(\.[0-9]+\.[0-9]+\.out$)");
      std::regex re_obs("^UnblindM" + std::to_string(m) + "_kR" + cstr + R"(\.[0-9]+\.[0-9]+\.out$)");

      // Search expected output file in results directory & read expected limits
      const std::string fexp = findFile(baseDir, re_exp);
      if (fexp.empty()) {
        std::cerr << "[WARN] Could not find expected limits file for M="<<m<<", kR="<<cstr<<"\n";
      } else {
        double med, l68, u68, l95, u95;
        if (readExpectedFile(fexp,med,l68,u68,l95,u95)) {
          points[i].expected = med;
          points[i].low68 = l68;
          points[i].up68  = u68;
          points[i].low95 = l95;
          points[i].up95  = u95;
        } else {
          std::cerr << "[WARN] Unexpected format for expected limits file: " << fexp << "\n";
        }
      }

      // Search observed output file in results directory & read observed limits
      if (drawObserved) {
        const std::string fobs = findFile(baseDir, re_obs);
        if (fobs.empty()) {
          std::cerr << "[WARN] Could not find observed limits file for M="<<m<<", kR="<<cstr<<"\n";
        } else {
          double obs;
          if (readObservedFile(fobs, obs)) points[i].observed = obs;
          else std::cerr << "[WARN] Unexpected format for expected limits file: " << fobs << "\n";
        }
      }
    }

    // Build Y arrays for curves
    std::vector<double> xs = couplings; // x axis
    std::vector<double> y_theory; y_theory.reserve(xs.size());
    for (double c : xs) {
      auto itM = theory.find(m);
      if (itM==theory.end() || itM->second.find(c)==itM->second.end()) {
        y_theory.push_back(NAN);
      } else y_theory.push_back(itM->second[c]);
    }

    auto getY = [&](auto getter){
      std::vector<double> y; y.reserve(xs.size());
      for (auto const &pt : points) y.push_back(getter(pt));
      return y;
    };

    auto y_exp = getY([](const LimitPoint&p){return p.expected;});
    auto y_lo68 = getY([](const LimitPoint&p){return p.low68;});
    auto y_hi68 = getY([](const LimitPoint&p){return p.up68;});
    auto y_lo95 = getY([](const LimitPoint&p){return p.low95;});
    auto y_hi95 = getY([](const LimitPoint&p){return p.up95;});
    auto y_obs  = getY([](const LimitPoint&p){return p.observed;});

    // Errors for bands relative to expected
    std::vector<double> eYL68(xs.size()), eYH68(xs.size()), eYL95(xs.size()), eYH95(xs.size());
    for (size_t i = 0; i < xs.size(); ++i){
      if (!std::isnan(y_exp[i]) && !std::isnan(y_lo68[i]) && !std::isnan(y_hi68[i])){
        eYL68[i]= y_exp[i]-y_lo68[i]; eYH68[i]= y_hi68[i]-y_exp[i];
      } else { eYL68[i]=eYH68[i]=0; }
      if (!std::isnan(y_exp[i]) && !std::isnan(y_lo95[i]) && !std::isnan(y_hi95[i])){
        eYL95[i]= y_exp[i]-y_lo95[i]; eYH95[i]= y_hi95[i]-y_exp[i];
      } else { eYL95[i]=eYH95[i]=0; }
    }

    // Create canvas per mass
    TCanvas *c1 = new TCanvas(Form("c_M%d",m),"",800,600);
    c1->SetLogy();
    c1->SetLogx();

    // Convert vectors to raw pointers for ROOT graphs
    auto ptr = [](std::vector<double> &v){ return v.empty()? nullptr : &v[0]; };

    // Draw expected bands
    TGraphAsymmErrors *g95 = new TGraphAsymmErrors(xs.size(), ptr(xs), ptr(y_exp), nullptr, nullptr, ptr(eYL95), ptr(eYH95));
    g95->SetTitle("");
    g95->GetXaxis()->SetTitle("g_{W'}/g_{W}");
    g95->GetXaxis()->SetTitleOffset(1.2);
    g95->GetXaxis()->SetRangeUser(0.01, 5);
    g95->GetYaxis()->SetTitle("#sigma #times #it{B}  (fb)");
    g95->SetMinimum(0.01);
    g95->SetMaximum(10E3);
    g95->SetFillColor(TColor::GetColor("#f5bb54"));
    g95->Draw("A3");
    
    TGraphAsymmErrors *g68 = new TGraphAsymmErrors(xs.size(), ptr(xs), ptr(y_exp), nullptr, nullptr, ptr(eYL68), ptr(eYH68));
    g68->SetFillColor(TColor::GetColor("#607641"));
    g68->Draw("3 SAME");

    // Draw expected dashed curve
    TGraph *gExp = new TGraph(xs.size(), ptr(xs), ptr(y_exp));
    gExp->SetLineStyle(7);
    gExp->SetLineWidth(3);
    gExp->SetLineColor(kBlack);
    gExp->Draw("L SAME");

    // Draw observed curve
    TGraph *gObs = nullptr;
    if (drawObserved) {
      gObs = new TGraph(xs.size(), ptr(xs), ptr(y_obs));
      gObs->SetLineStyle(1);
      gObs->SetLineWidth(2);
      gObs->SetLineColor(kBlack);
      gObs->Draw("L SAME");
    }

    // Draw the theoretical curve
    TGraph *gTheory = new TGraph(xs.size(), ptr(xs), ptr(y_theory));
    gTheory->SetLineColor(kBlue);
    gTheory->SetLineWidth(2);
    gTheory->Draw("C SAME");

    // Legends and cosmetics
    TLegend *leg = new TLegend(0.58,0.65,0.88,0.88);
    leg->SetBorderSize(0);
    if (drawObserved) leg->AddEntry(gObs, "Observed", "l");
    leg->AddEntry(gExp,    "Expected", "l");
    leg->AddEntry(g68,     "#pm 1 s.d.", "f");
    leg->AddEntry(g95,     "#pm 2 s.d.", "f");
    leg->AddEntry(gTheory, "#sigma W' LO", "l");
    leg->Draw();

    TLatex mass_txt;
    mass_txt.SetNDC();
    mass_txt.SetTextSize(0.038);
    mass_txt.SetTextFont(42);
    mass_txt.DrawLatex(0.16,0.92, Form("#bf{M_{W'} = %d GeV}", m));

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

    // Save plot
    const std::string outPlot = (fs::path(outDir)/Form("couplingLimits_M%d.png",m)).string();
    c1->SaveAs(outPlot.c_str());

    // Compute intersections with theory curve (one per curve type)
    double x_int_low95 = findIntersection(xs, y_lo95, y_theory);
    double x_int_low68 = findIntersection(xs, y_lo68, y_theory);
    double x_int_exp   = findIntersection(xs, y_exp,  y_theory);
    double x_int_up68  = findIntersection(xs, y_hi68, y_theory);
    double x_int_up95  = findIntersection(xs, y_hi95, y_theory);
    double x_int_obs   = drawObserved ? findIntersection(xs, y_obs,  y_theory) : NAN;

    fout << m << " "
	 << (std::isnan(x_int_low95)? -1: x_int_low95) << " "
	 << (std::isnan(x_int_low68)? -1: x_int_low68) << " "
	 << (std::isnan(x_int_exp)? -1: x_int_exp) << " "
	 << (std::isnan(x_int_up68)? -1: x_int_up68) << " "
	 << (std::isnan(x_int_up95)? -1: x_int_up95) << " "
	 << (std::isnan(x_int_obs)? -1: x_int_obs) << "\n";
  }

  fout.close();
  
}



void couplingLimit_producer(){
  
  //plotVScoupling("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/outputs/CouplingLimits/2022/muon/fullCuts", "2022", "CouplingCrossSections.txt", "/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/plots/CouplingLimits/2022/Individual/fullCuts", true);

  //plotVScoupling("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/outputs/CouplingLimits/2023/muon/fullCuts", "2023", "CouplingCrossSections.txt", "/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/plots/CouplingLimits/2023/Individual/fullCuts", true);
  
  plotVScoupling("/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/outputs/CouplingLimits/22+23/muon/fullCuts", "22+23", "CouplingCrossSections.txt", "/afs/cern.ch/user/d/diegof/Wprime/Wprime-analysis/combine/plots/CouplingLimits/22+23/Individual/fullCuts", true);
  
}
