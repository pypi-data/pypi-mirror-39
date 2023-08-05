#!/usr/bin/env bash

if [[ -z $(type -t panicandquit) ]]; then
  #echo "pandq not defined"
  panicandquit(){
    exit 1
  }
fi

# check to see whether a conda version is installed:
if [[ "$(type -t conda)" == "function" ]] && [[ ! -z $(conda info | grep 'conda version') ]]; then
  CONDA_SH=''
  echo "already have conda access"

elif [[ -r "$HOME/anaconda/etc/profile.d/conda.sh" ]]; then
  CONDA_SH="$HOME/anaconda/etc/profile.d/conda.sh"

elif [[ -r "$HOME/miniconda/etc/profile.d/conda.sh" ]]; then
  CONDA_SH="$HOME/miniconda/etc/profile.d/conda.sh"

elif [[ -r "$HOME/anaconda3/etc/profile.d/conda.sh" ]]; then
  CONDA_SH="$HOME/anaconda3/etc/profile.d/conda.sh"

elif [[ -r "$HOME/miniconda3/etc/profile.d/conda.sh" ]]; then
  CONDA_SH="$HOME/miniconda3/etc/profile.d/conda.sh"

else
  echo 'could not find conda installation.  please visit https://conda.io/miniconda.html to install miniconda (recommended) or'
  echo 'https://conda.io to install the full conda'
  panicandquit
fi

if [[ -n $CONDA_SH ]]; then
  echo "found a conda/miniconda installation at:  $CONDA_SH"
  source "$CONDA_SH"
fi
