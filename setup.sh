#!/usr/bin/env bash

action() {
    #
    # global variables
    #

    # determine the directory of this file
    cd nanoaod_base_analysis
    #local this_file="$( [ ! -z "$ZSH_VERSION" ] && echo "${(%):-%x}" || echo "${BASH_SOURCE[0]}" )"
    #local this_dir="$( cd "$( dirname "$this_file" )" && pwd )"
    export CMT_BASE="$PWD"

    # check if this setup script is sourced by a remote job
    if [ "$CMT_ON_HTCONDOR" = "1" ]; then
        export CMT_REMOTE_JOB="1"
    else
        export CMT_REMOTE_JOB="0"
    fi

    # check if we're on lxplus
    if [[ "$( hostname )" = lxplus*.cern.ch ]]; then
        export CMT_ON_LXPLUS="1"
    else
        export CMT_ON_LXPLUS="0"
    fi
    
    # check if we're on gaeui (ciemat)
    if [[ "$( hostname )" = gae*.ciemat.es ]]; then
        export CMT_ON_CIEMAT="1"
    else
        export CMT_ON_CIEMAT="0"
    fi

    # default cern name
    if [ -z "$CMT_CERN_USER" ]; then
        if [ "$CMT_ON_LXPLUS" = "1" ]; then
            export CMT_CERN_USER="$( whoami )"
        elif [ "$CMT_ON_CIEMAT" = "0" ]; then
            2>&1 echo "please set CMT_CERN_USER to your CERN user name and try again"
            return "1"
        fi
    fi

    # default ciemat name
    if [ -z "$CMT_CIEMAT_USER" ]; then
        if [ "$CMT_ON_CIEMAT" = "1" ]; then
            export CMT_CIEMAT_USER="$( whoami )"
        # elif [ "$CMT_ON_LXPLUS" = "0" ]; then
            # 2>&1 echo "please set CMT_CIEMAT_USER to your CIEMAT user name and try again"
            # return "1"
        fi
    fi

    # default data directory
    if [ -z "$CMT_DATA" ]; then
        if [ "$CMT_ON_LXPLUS" = "1" ]; then
            export CMT_DATA="$CMT_BASE/data"
        else
            # TODO: better default when not on lxplus
            export CMT_DATA="$CMT_BASE/data"
        fi
    fi

    # other defaults
    [ -z "$CMT_SOFTWARE" ] && export CMT_SOFTWARE="$CMT_DATA/software"
    [ -z "$CMT_STORE_LOCAL" ] && export CMT_STORE_LOCAL="$CMT_DATA/store"
    if [ -n "$CMT_CIEMAT_USER" ]; then
	#[ -z "$CMT_STORE_EOS" ] && export CMT_STORE_EOS="/nfs/cms/$CMT_CIEMAT_USER/cmt"
	[ -z "$CMT_STORE_EOS" ] && export CMT_STORE_EOS="/pnfs/ciemat.es/data/cms/store/user/diegof/cmt"
    elif [ -n "$CMT_CERN_USER" ]; then
	[ -z "$CMT_STORE_EOS" ] && export CMT_STORE_EOS="/eos/user/${CMT_CERN_USER:0:1}/$CMT_CERN_USER/cmt"
	[ -z "$CMT_STORE_EOS_MUOPOG" ] && export CMT_STORE_EOS_MUOPOG="/eos/cms/store/group/phys_muon/diegof/cmt" # UNCOMMENT FOR MUOPOG
    fi
    [ -z "$CMT_STORE" ] && export CMT_STORE="$CMT_STORE_EOS"
    [ -z "$CMT_JOB_DIR" ] && export CMT_JOB_DIR="$CMT_DATA/jobs"
    [ -z "$CMT_JOB_META_DIR" ] && export CMT_JOB_META_DIR="$CMT_DATA/jobs_meta"
    [ -z "$CMT_TMP_DIR" ] && export CMT_TMP_DIR="$CMT_DATA/tmp"
    [ -z "$CMT_CMSSW_BASE" ] && export CMT_CMSSW_BASE="$CMT_DATA/cmssw"
    [ -z "$CMT_SCRAM_ARCH" ] && export CMT_SCRAM_ARCH="el9_amd64_gcc11"
    [ -z "$CMT_CMSSW_VERSION" ] && export CMT_CMSSW_VERSION="CMSSW_13_0_13"
    [ -z "$CMT_PYTHON_VERSION" ] && export CMT_PYTHON_VERSION="3"
    
    if [ "$CMT_ON_CIEMAT" = "1" ]; then
       if [ -n "$CMT_TMPDIR" ]; then
         export TMPDIR="$CMT_TMPDIR"
       else
         export TMPDIR="/nfs/scratch_cms/$CMT_CIEMAT_USER/cmt/tmp" # Not needed? I set it up below
       fi
       mkdir -p "$TMPDIR"
    fi

    # specific eos dirs
    if [ -n "$CMT_CERN_USER" ]; then
	if [ -n "$CMT_STORE_EOS_MUOPOG" ]; then
	    [ -z "$CMT_STORE_EOS_PREPROCESSING" ] && export CMT_STORE_EOS_PREPROCESSING="$CMT_STORE_EOS_MUOPOG"
	    [ -z "$CMT_STORE_EOS_CATEGORIZATION" ] && export CMT_STORE_EOS_CATEGORIZATION="$CMT_STORE_EOS_MUOPOG"
	    [ -z "$CMT_STORE_EOS_MERGECATEGORIZATION" ] && export CMT_STORE_EOS_MERGECATEGORIZATION="$CMT_STORE_EOS_MUOPOG"
	else
	    [ -z "$CMT_STORE_EOS_PREPROCESSING" ] && export CMT_STORE_EOS_PREPROCESSING="$CMT_STORE_EOS"
	    [ -z "$CMT_STORE_EOS_CATEGORIZATION" ] && export CMT_STORE_EOS_CATEGORIZATION="$CMT_STORE_EOS"
	    [ -z "$CMT_STORE_EOS_MERGECATEGORIZATION" ] && export CMT_STORE_EOS_MERGECATEGORIZATION="$CMT_STORE_EOS"
	fi
    else
	[ -z "$CMT_STORE_EOS_PREPROCESSING" ] && export CMT_STORE_EOS_PREPROCESSING="$CMT_STORE_EOS"
	[ -z "$CMT_STORE_EOS_CATEGORIZATION" ] && export CMT_STORE_EOS_CATEGORIZATION="$CMT_STORE_EOS"
	[ -z "$CMT_STORE_EOS_MERGECATEGORIZATION" ] && export CMT_STORE_EOS_MERGECATEGORIZATION="$CMT_STORE_EOS"	
    fi	
    [ -z "$CMT_STORE_EOS_SHARDS" ] && export CMT_STORE_EOS_SHARDS="$CMT_STORE_EOS"
    [ -z "$CMT_STORE_EOS_EVALUATION" ] && export CMT_STORE_EOS_EVALUATION="$CMT_STORE_EOS"

    # create some dirs already
    mkdir -p "$CMT_TMP_DIR"


    #
    # helper functions
    #

    cmt_pip_install() {
        if [ "$CMT_PYTHON_VERSION" = "2" ]; then
            env pip install --ignore-installed --no-cache-dir --upgrade --prefix "$CMT_SOFTWARE" "$@"
        else
            env pip3 install --ignore-installed --no-cache-dir --upgrade --prefix "$CMT_SOFTWARE" "$@"
        fi
    }
    export -f cmt_pip_install

    cmt_add_py() {
        export PYTHONPATH="$1:$PYTHONPATH"
    }
    export -f cmt_add_py

    cmt_add_bin() {
        export PATH="$1:$PATH"
    }
    export -f cmt_add_bin

    cmt_add_lib() {
        export LD_LIBRARY_PATH="$1:$LD_LIBRARY_PATH"
    }
    export -f cmt_add_lib

    cmt_add_root_inc() {
        export ROOT_INCLUDE_PATH="$ROOT_INCLUDE_PATH:$1"
    }
    export -f cmt_add_root_inc

    
    #
    # minimal software stack
    #

    # add this repo to PATH and PYTHONPATH
    cmt_add_bin "$CMT_BASE/bin"
    cmt_add_py "$CMT_BASE"
    cmt_add_py "$CMT_BASE/../"

    # variables for external software
    export GLOBUS_THREAD_MODEL="none"
    export CMT_GFAL_DIR="$CMT_SOFTWARE/gfal2"
    export GFAL_PLUGIN_DIR="$CMT_GFAL_DIR/lib/gfal2-plugins"

    # certificate proxy handling
    #[ "$CMT_REMOTE_JOB" != "1" ] && export X509_USER_PROXY="/tmp/x509up_u$( id -u )" #old
    [ "$CMT_REMOTE_JOB" != "1" ] && export X509_USER_PROXY="$CMT_BASE/x509up"

    # software that is used in this project
    cmt_setup_software() {
        local origin="$( pwd )"
        local mode="$1"

        # get the python version
        if [ "$CMT_PYTHON_VERSION" = "2" ]; then
            local pyv="$( python -c "import sys; print('{0.major}.{0.minor}'.format(sys.version_info))" )"
        else
            local pyv="$( python3 -c "import sys; print('{0.major}.{0.minor}'.format(sys.version_info))" )"
        fi

        # remove software directories when forced
        if [ "$mode" = "force" ] || [ "$mode" = "force_cmssw" ]; then
            echo "remove CMSSW checkout in $CMT_CMSSW_BASE/$CMT_CMSSW_VERSION"
            rm -rf "$CMT_CMSSW_BASE/$CMT_CMSSW_VERSION"
        fi

        if [ "$mode" = "force" ] || [ "$mode" = "force_py" ]; then
            echo "remove software stack in $CMT_SOFTWARE"
            rm -rf "$CMT_SOFTWARE"
        fi

        if [ "$mode" = "force" ] || [ "$mode" = "force_gfal" ]; then
            echo "remove gfal installation in $CMT_GFAL_DIR"
            rm -rf "$CMT_GFAL_DIR"
        fi
	
	if [ "$mode" = "force" ] || [ "$mode" = "force_tools" ]; then
            echo "remove anlysis_tools and plotting_tools installation in $CMT_SOFTWARE/lib/python$pyv/site-packages"
	    rm -rf "$CMT_SOFTWARE/lib/python$pyv/site-packages/analysis_tools"
	    rm -rf "$CMT_SOFTWARE/lib/python$pyv/site-packages/plotting_tools"
        fi

        # setup cmssw
        export SCRAM_ARCH="$CMT_SCRAM_ARCH"
        source "/cvmfs/cms.cern.ch/cmsset_default.sh" ""
        if [ ! -d "$CMT_CMSSW_BASE/$CMT_CMSSW_VERSION" ]; then
            echo "setting up $CMT_CMSSW_VERSION at $CMT_CMSSW_BASE"
            mkdir -p "$CMT_CMSSW_BASE"
            cd "$CMT_CMSSW_BASE"
            scramv1 project CMSSW "$CMT_CMSSW_VERSION"
        fi
        cd "$CMT_CMSSW_BASE/$CMT_CMSSW_VERSION/src"
        
        eval `scramv1 runtime -sh`

        compile="0"
        export NANOTOOLS_PATH="PhysicsTools/NanoAODTools"
        if [ ! -d "$NANOTOOLS_PATH" ]; then
          git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
          compile="1"
        fi

        export BASEMODULES_PATH="Base/Modules"
        if [ ! -d "$BASEMODULES_PATH" ]; then
            git clone https://gitlab.cern.ch/cms-phys-ciemat/cmt-base-modules.git Base/Modules
	    git clone https://gitlab.cern.ch/cms-phys-ciemat/event-filters.git Base/Filters
          compile="1"
        fi

        export CORRECTIONS_PATH="Corrections"
        cmt_add_root_inc $(correction config --incdir)
        if [ ! -d "$CORRECTIONS_PATH" ]; then
            #git clone https://github.com/jaimeleonh/correctionlib-wrapper --branch cmssw_version  Corrections/Wrapper
            #git clone https://gitlab.cern.ch/cms-phys-ciemat/tau-corrections.git Corrections/TAU
            git clone https://gitlab.cern.ch/cms-phys-ciemat/jme-corrections.git Corrections/JME
	    cd Corrections/JME/data
            wget https://github.com/cms-jet/JECDatabase/raw/master/tarballs/Summer19UL18_V5_MC.tar.gz
            wget https://github.com/cms-jet/JECDatabase/raw/master/tarballs/Summer19UL17_V5_MC.tar.gz
            wget https://github.com/cms-jet/JECDatabase/raw/master/tarballs/Summer19UL16_V7_MC.tar.gz
            wget https://github.com/cms-jet/JECDatabase/raw/master/tarballs/Summer19UL16APV_V7_MC.tar.gz
            cd -
            git clone https://gitlab.cern.ch/cms-phys-ciemat/lum-corrections.git Corrections/LUM
            git clone https://gitlab.cern.ch/cms-phys-ciemat/muo-corrections.git Corrections/MUO
            git clone https://gitlab.cern.ch/cms-phys-ciemat/egm-corrections.git Corrections/EGM
            git clone https://gitlab.cern.ch/cms-phys-ciemat/btv-corrections.git Corrections/BTV
            compile="1"
        fi

	export GEMETHOD_PATH="GEM/Modules"
        if [ ! -d "$GEMETHOD_PATH" ]; then
            git clone https://gitlab.cern.ch/diegof/gem-modules.git GEM/Modules
            compile="1"
        fi

	export WPRIME_PATH="Wprime/Modules"
        if [ ! -d "$WPRIME_PATH" ]; then
            git clone https://gitlab.cern.ch/diegof/wprime-modules.git Wprime/Modules
            compile="1"
        fi
             
        export COMBINE_PATH="HiggsAnalysis/CombinedLimit"
        if [ ! -d "$COMBINE_PATH" ]; then
          git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git -b v9.1.0 HiggsAnalysis/CombinedLimit
          compile="1"
        fi

        export COMBINEHARVESTER_PATH="CombineHarvester"
        if [ ! -d "$COMBINEHARVESTER_PATH" ]; then
          git clone https://github.com/cms-analysis/CombineHarvester -b v2.1.0
          cd CombineHarvester
          rm -r CombinePdfs
          rm CombineTools/bin/*
          rm CombineTools/src/*
          rm CombineTools/interface/*
          rm CombineTools/macros/*
          cd -
          compile="1"
        fi

        if [ "$compile" == "1" ]
        then
            scram b
        fi

        eval `scramv1 runtime -sh`
        cd "$origin"

        # ammend software paths
        cmt_add_bin "$CMT_SOFTWARE/bin"
        cmt_add_py "$CMT_SOFTWARE/lib/python$pyv/site-packages:$CMT_SOFTWARE/lib64/python$pyv/site-packages"

        # setup custom software
        if [ ! -d "$CMT_SOFTWARE" ]; then
            echo "installing software stack at $CMT_SOFTWARE"
            mkdir -p "$CMT_SOFTWARE"

            cmt_pip_install pip
	    cmt_pip_install wheel
            cmt_pip_install setuptools
            cmt_pip_install libclang
            cmt_pip_install overrides
            cmt_pip_install build
            cmt_pip_install installer
            cmt_pip_install pyproject-hooks
            cmt_pip_install Flask
            cmt_pip_install ordereddict
            cmt_pip_install flake8
            cmt_pip_install luigi==2.8.13
            cmt_pip_install tabulate
            cmt_pip_install --no-deps git+https://github.com/riga/law
            cmt_pip_install --no-deps git+https://github.com/riga/plotlib
	    cmt_pip_install --no-deps git+https://github.com/riga/LBN
            cmt_pip_install --no-deps gast==0.2.2  # https://github.com/tensorflow/autograph/issues/1
            cmt_pip_install sphinx==5.2.2
            cmt_pip_install sphinx_rtd_theme	    
            cmt_pip_install sphinx_design
            cmt_pip_install urllib3==1.26.6
            cmt_pip_install envyaml

        fi

	# download analysis and plotting tools
        if [ ! -d "$CMT_SOFTWARE/lib/python$pyv/site-packages/analysis_tools" ]; then
	    echo "installing analysis_tools in $CMT_SOFTWARE/lib/python$pyv/site-packages"
	    cmt_pip_install git+https://gitlab.cern.ch/cms-phys-ciemat/analysis_tools.git
	fi
	if [ ! -d "$CMT_SOFTWARE/lib/python$pyv/site-packages/plotting_tools" ]; then
	    echo "installing plotting_tools in $CMT_SOFTWARE/lib/python$pyv/site-packages"
	    cmt_pip_install git+https://gitlab.cern.ch/cms-phys-ciemat/plotting_tools.git
	fi

        # gfal python bindings
        cmt_add_bin "$CMT_GFAL_DIR/bin"
        cmt_add_py "$CMT_GFAL_DIR/lib/python3/site-packages"
        cmt_add_lib "$CMT_GFAL_DIR/lib"

        if [ ! -d "$CMT_GFAL_DIR" ]; then
#            local lcg_base="/cvmfs/grid.cern.ch/centos7-ui-4.0.3-1_umd4v3/usr"
	    local lcg_base="/cvmfs/grid.cern.ch/centos7-ui-200122/usr"
            if [ ! -d "$lcg_base" ]; then
                2>&1 echo "LCG software directory $lcg_base not existing"
                return "1"
            fi

            mkdir -p "$CMT_GFAL_DIR"
            (
                cd "$CMT_GFAL_DIR"
                mkdir -p include bin lib/gfal2-plugins lib/python3/site-packages
                ln -s "$lcg_base"/include/gfal2* include
                ln -s "$lcg_base"/bin/gfal-* bin
                ln -s "$lcg_base"/lib64/libgfal* lib
                ln -s "$lcg_base"/lib64/gfal2-plugins/libgfal* lib/gfal2-plugins
                ln -s "$lcg_base"/lib64/python3.6/site-packages/gfal* lib/python3/site-packages
                cd lib/gfal2-plugins
                rm libgfal_plugin_http.so libgfal_plugin_xrootd.so
	       
                curl https://cernbox.cern.ch/remote.php/dav/public-files/qgrogVY4bwcuCXt/libgfal_plugin_xrootd.so > libgfal_plugin_xrootd.so
                # curl https://cernbox.cern.ch/index.php/s/qgrogVY4bwcuCXt/download > libgfal_plugin_xrootd.so
            )
        fi
    }
    export -f cmt_setup_software

    # setup the software initially when no explicitly skipped
    if [ "$CMT_SKIP_SOFTWARE" != "1" ]; then
        if [ "$CMT_FORCE_SOFTWARE" = "1" ]; then
            cmt_setup_software force
        elif [ "$CMT_FORCE_CMSSW" = "1" ]; then
            cmt_setup_software force_cmssw
        elif [ "$CMT_FORCE_PYTHON" = "1" ]; then
            cmt_setup_software force_py
        elif [ "$CMT_FORCE_TOOLS" = "1" ]; then
            cmt_setup_software force_tools
        else
            cmt_setup_software silent
        fi
    fi

    
    #
    # law setup
    #

    export LAW_HOME="$CMT_DATA/law"
    export LAW_CONFIG_FILE="$CMT_BASE/../law.cfg"
    [ -z "$CMT_SCHEDULER_PORT" ] && export CMT_SCHEDULER_PORT="80"
    if [ -z "$CMT_LOCAL_SCHEDULER" ]; then
        if [ -z "$CMT_SCHEDULER_HOST" ]; then
            export CMT_LOCAL_SCHEDULER="True"
        else
            export CMT_LOCAL_SCHEDULER="False"
        fi
    fi
    if [ -z "$CMT_LUIGI_WORKER_KEEP_ALIVE" ]; then
        if [ "$CMT_REMOTE_JOB" = "0" ]; then
            export CMT_LUIGI_WORKER_KEEP_ALIVE="False"
        else
            export CMT_LUIGI_WORKER_KEEP_ALIVE="False"
        fi
    fi

    # Set tmp dir for MergeCategorization
    if [ -n "$CMT_CERN_USER" ]; then
	if [ -n "$CMT_STORE_EOS_MUOPOG" ]; then
	    export LAW_TARGET_TMP_DIR="/eos/cms/store/group/phys_muon/diegof/tmp/"
	else
	    export LAW_TARGET_TMP_DIR="/eos/home-d/diegof/tmp/"
	fi
    else
        export LAW_TARGET_TMP_DIR="/pnfs/ciemat.es/data/cms/store/user/diegof/tmp/"
    fi

    # try to source the law completion script when available
    which law &> /dev/null && source "$( law completion )" ""
}
action "$@"
cd ..
#voms-proxy-init --voms cms -valid 192:0
