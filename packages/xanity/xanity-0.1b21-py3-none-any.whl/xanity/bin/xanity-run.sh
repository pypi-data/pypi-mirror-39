#!/usr/bin/env bash

set -e

panicandquit(){
  if [[ -v ocwd ]]; then
    cd $ocwd
  fi
  exit 1
}

parse(){
for i in $@
do
  case $i in
      --debugger)
      export PDB='1'
      ;;

      -D=*|--directory=*)
      export xanity_root="${i#*=}"
      ;;
      #shift # past argument=value
      #;;

      #-s=*|--searchpath=*)
      #SEARCHPATH="${i#*=}"
      #shift # past argument=value
      #;;

      #-l=*|--lib=*)
      #LIBPATH="${i#*=}"
      #shift # past argument=value
      #;;

      #--default)
      #DEFAULT=YES
      #shift # past argument with no value
      #;;
      #*)
      #      # unknown option
      #;;
  esac
done
}

runit(){
  # SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
  # echo "experiment root dir is $SCRIPTPATH"
  # cd "$SCRIPTPATH"

  if [[ ! -v 'xanity_root' ]]; then
    if [[ ! -d .xanity ]]; then
      echo "you're not in a xanity project and you didnt specify one with the -D option"
      panicandquit
    fi
    xanity_root="${PWD}"

  else
    if [[ ! -d "$xanity_root/.xanity" ]]; then
      echo 'dir provided is not xanity_root'
      panicandquit
    fi
    export ocwd="${PWD}"
    cd $xanity_root
  fi

  if [[ ! -f .xanity/setupcomplete ]];then
      echo "you have to run setup first.  call './setup' then try this again."
      panicandquit
  else
      UUID="$(cat .xanity/setupcomplete)"
      echo "using UUID = $UUID"
  fi

  source xanity-enable-conda.sh
  conda activate $UUID && echo "stepped in to conda env" || { echo "problem entering conda" && panicandquit ; }

  if [[ $PDB == '1' ]]; then
    echo "entering PDB DEBUGGER with arguments: $@"
    python -m pdb xanity.__main__ $@
  else
    echo "starting python with arguments: $@"
    python -m xanity.__main__ $@
  fi

  status=$?
  conda deactivate && echo "stepped out of conda env" || { echo "problem exiting conda" && panicandquit ; }

  [[ status ]] && return 1 || return 0
 }

parse $@
runit $@ && exit 0 || exit 1
