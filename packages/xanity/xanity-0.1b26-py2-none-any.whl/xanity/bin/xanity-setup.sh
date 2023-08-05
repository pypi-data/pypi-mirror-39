#!/usr/bin/env bash

#  this file is a bash script that will create a python virtual environment at ./venv/
# and install some other necessary stuff.
# git clone is used to get latest code and
# "pip install -e" is used to install it in-place (in ./lib/) so the python
# source can be modified

set -e

ORIG_PWD="$(pwd)"
TARGET_DIR="$1"

panicandquit(){
  cd $ORIG_PWD
  exit 1
}

setup(){
    set -e

    if [[ -z "$TARGET_DIR" ]];then
      echo "must provide full path to xanity project to setup" && panicandquit
    else
      XANITYROOT="$TARGET_DIR"
      if [[ ! -d "$XANITYROOT/.xanity" ]];then
        echo 'provided path is not a xanity root'
        panicandquit
      else
        echo "using xanity path: $XANITYROOT"
        pushd "$XANITYROOT"
      fi
    fi

    if [[ ! -f .xanity/UUID ]]; then
      echo 'generating new UUID'
      UUID="$(basename $PWD)_$(dd if=/dev/urandom bs=512 count=1 status=none | tr -dc 'a-zA-Z' | fold -w 4 | head -n 1)"
      echo "$UUID" > .xanity/UUID
    else
      echo 'using existing UUID'
      UUID="$(cat .xanity/UUID)"
    fi
    echo "UUID = $UUID"

    if [[ -f .xanity/setupcomplete ]];then
      ouid="$(cat .xanity/setupcomplete)"
      if [[ "$UUID" == "$ouid" ]]; then
        echo "found setupcomplete file containing correct UUID... will update."
      else
        echo "existing setupcomplete file is incorrect... removing it."
        rm .xanity/setupcomplete
      fi
    fi

    ## read conda environment file
    if [[ ! ( -f conda_environment.yaml ) ]]; then
      echo 'could not find environment.yaml which contains the desired conda environment.  Please make one.'
      echo 'example environment.yaml file:\n\n'
      echo '    name: < my-env-name >         '
      echo '    channels:                     '
      echo '      - javascript                '
      echo '    dependencies:                 '
      echo '      - python=3.4                '
      echo '      - bokeh=0.9.2               '
      echo '      - numpy=1.9.*               '
      echo '      - nodejs=0.10.*             '
      echo '      - flask                     '
      echo '      - pip:                      '
      echo '        - Flask-Testing           '
      echo '        - \"--editable=git+ssh://git@gitlab.com/lars-gatech/pyspectre.git#egg=pyspectre\" '
      echo '        - "git+ssh://git@gitlab.com/lars-gatech/libpsf.git#egg=libpsf" '
      panicandquit
    else
      echo "found conda_environment.yaml file."
    fi

    xanityver="$(pip show -V xanity | grep Version | tr -s ' ' | cut -d ' ' -f 2 )"
    
    echo "xanity version $xanityver is installed. using same version in conda env"
    
    source xanity-enable-conda.sh

    if [[ "$( conda env list | grep $UUID )" == "" ]]; then
      echo "installing a new environment named ${UUID} using environment.yaml file..."
      { conda env create -f conda_environment.yaml -n "$UUID" ;} && echo 'created'
      # conda activate $UUID && echo "stepped into conda environment"
    else
      echo "found a conda env with name: ${UUID}. updating it from the environment.yaml file..."
      # conda activate $UUID && echo "stepped into conda environment"
      { conda env update -f conda_environment.yaml -n "$UUID" ;} && echo 'updated'
    fi
    
    conda activate $UUID \
          && pip install "xanity==${xanityver}" \
          && conda deactivate \
          && echo "updated xanity in xanity-conda env"
        
    #conda deactivate && echo "stepped out of conda environment"   
    echo "$UUID" > .xanity/setupcomplete
    return
}

setup $@ 2>&1 | tee .xanity/setup.log
exit 0
