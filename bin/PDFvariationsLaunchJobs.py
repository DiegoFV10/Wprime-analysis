import subprocess
import concurrent.futures

task_name = "FeaturePlot"
modules_files = [f"PDFreweight_{i}" for i in range(103)]
versions = [f"zzzz_PDFreweight_{i}" for i in range(103)]

common_args = [
    "--config-name", "Wprime_2022_config",
    "--category-name", "preselection",
    "--process-group-name", "2022ReReco",
    "--stack", "--log-y", "--hide-data", "False",
    "--save-root", "--plot-systematics", "False",
    "--dataset-names", "Wlnu120to200,Wlnu120to200_postEE,Wlnu200to400,Wlnu200to400_postEE,Wlnu400to800,Wlnu400to800_postEE,Wlnu800to1500,Wlnu800to1500_postEE,Wlnu1500to2500,Wlnu1500to2500_postEE,Wlnu2500to4000,Wlnu2500to4000_postEE,Wlnu4000to6000,Wlnu4000to6000_postEE,Wlnu6000,Wlnu6000_postEE,Wlnu_ptW-40to100_1J,Wlnu_ptW-40to100_1J_postEE,Wlnu_ptW-40to100_2J,Wlnu_ptW-40to100_2J_postEE,Wlnu_ptW-100to200_1J,Wlnu_ptW-100to200_1J_postEE,Wlnu_ptW-100to200_2J,Wlnu_ptW-100to200_2J_postEE,Wlnu_ptW-200to400_1J,Wlnu_ptW-200to400_1J_postEE,Wlnu_ptW-200to400_2J,Wlnu_ptW-200to400_2J_postEE,Wlnu_ptW-400to600_1J,Wlnu_ptW-400to600_1J_postEE,Wlnu_ptW-400to600_2J,Wlnu_ptW-400to600_2J_postEE,Wlnu_ptW-600_1J,Wlnu_ptW-600_1J_postEE,Wlnu_ptW-600_2J,Wlnu_ptW-600_2J_postEE,Wjets,Wjets_postEE,TT_2l2nu,TT_2l2nu_postEE,TT_lnu2q,TT_lnu2q_postEE,ST_tW-lnu2q,ST_tW-lnu2q_postEE,ST_tW-2l2nu,ST_tW-2l2nu_postEE,ST_tbarW-lnu2q,ST_tbarW-lnu2q_postEE,ST_tbarW-2l2nu,ST_tbarW-2l2nu_postEE,ST_s-top,ST_s-top_postEE,ST_s-tbar,ST_s-tbar_postEE,ST_t-top,ST_t-top_postEE,ST_t-tbar,ST_t-tbar_postEE,Zmumu_M-50to120,Zmumu_M-50to120_postEE,Zmumu_M-120to200,Zmumu_M-120to200_postEE,Zmumu_M-200to400,Zmumu_M-200to400_postEE,Zmumu_M-400to800,Zmumu_M-400to800_postEE,Zmumu_M-800to1500,Zmumu_M-800to1500_postEE,Zmumu_M-1500to2500,Zmumu_M-1500to2500_postEE,Zmumu_M-2500to4000,Zmumu_M-2500to4000_postEE,Zmumu_M-4000to6000,Zmumu_M-4000to6000_postEE,Zmumu_M-6000,Zmumu_M-6000_postEE,Ztautau_M-50to120,Ztautau_M-50to120_postEE,Ztautau_M-120to200,Ztautau_M-120to200_postEE,Ztautau_M-200to400,Ztautau_M-200to400_postEE,Ztautau_M-400to800,Ztautau_M-400to800_postEE,Ztautau_M-800to1500,Ztautau_M-800to1500_postEE,Ztautau_M-1500to2500,Ztautau_M-1500to2500_postEE,Ztautau_M-2500to4000,Ztautau_M-2500to4000_postEE,Ztautau_M-4000to6000,Ztautau_M-4000to6000_postEE,Ztautau_M-6000,Ztautau_M-6000_postEE,Znunu_HT-100to200,Znunu_HT-100to200_postEE,Znunu_HT-200to400,Znunu_HT-200to400_postEE,Znunu_HT-400to800,Znunu_HT-400to800_postEE,Znunu_HT-800to1500,Znunu_HT-800to1500_postEE,Znunu_HT-1500to2500,Znunu_HT-1500to2500_postEE,Znunu_HT-2500,Znunu_HT-2500_postEE,WW_2l2nu,WW_2l2nu_postEE,WW_lnu2q,WW_lnu2q_postEE,WZ_2l2q,WZ_2l2q_postEE,WZ_3lnu,WZ_3lnu_postEE,WZ_lnu2q,WZ_lnu2q_postEE,Wg_pT-10to100,Wg_pT-10to100_postEE,Wg_pT-100to200,Wg_pT-100to200_postEE,Wg_pT-200to400,Wg_pT-200to400_postEE,Wg_pT-400to600,Wg_pT-400to600_postEE,Wg_pT-600,Wg_pT-600_postEE",
    "--MergeCategorizationStats-version", "2022reprocess",
    "--MergeCategorization-version", "2022reprocess",
    "--run-period", "preEE",
    "--workers", "200",
    "--PrePlot-workflow", "htcondor",
    "--PrePlot-max-runtime", "3h",
    "--PrePlot-transfer-logs"
]

# Execute FeaturePlot task with different parameters in parallel
def run_task(modules_file, version):
    command = ["law", "run", task_name] + common_args + [
        "--PrePlot-preplot-modules-file", modules_file,
        "--version", version
    ]
    
    print(f"Running {task_name} with --PrePlot-preplot-modules-file={modules_file} and --version={version}")
    subprocess.run(command, check=True)

max_workers = 10  # Max number of simultaneous jobs

with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Execute all tasks
    futures = [executor.submit(run_task, modules_file, version) 
               for modules_file, version in zip(modules_files, versions)]

    # Wait for all tasks to finish
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"Error in execution of task: {e}")

print("All tasks have been completed!")
