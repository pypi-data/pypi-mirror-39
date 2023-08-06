#!/usr/bin/env bash

if [ $# == 0 ]; then
  echo "usage: $0 <beat-core-branch>"
  exit 1
fi

basedir=`pwd`

if [ ! -e ${basedir}/_ci/functions.sh ]; then
  # this will happen when executing buildout for the first time
  mkdir ${basedir}/_ci
  curl --silent "https://gitlab.idiap.ch/bob/bob.admin/raw/master/gitlab/install.sh" > ${basedir}/_ci/install.sh
  chmod 755 ${basedir}/_ci/install.sh
  ${basedir}/_ci/install.sh ${basedir}/_ci master #installs ci support scripts
else
  ${basedir}/_ci/install.sh ${basedir}/_ci master #updates ci support scripts
fi

if [ "${BUILDOUT}" == "true" ]; then
  # when executing in the context of buildout, define dummies
  export CI_PROJECT_URL=https://gitlab.idiap.ch/beat/beat.cmdline
  export CI_PROJECT_DIR=beat
  export CI_PROJECT_PATH=beat/beat.cmdline
  export CI_PROJECT_NAME=beat.cmdline
  export CI_COMMIT_REF_NAME=master
  export PYPIUSER=pypiuser
  export PYPIPASS=pypipass
  export DOCUSER=docuser
  export DOCPASS=docpass
  export CONDA_ROOT=${basedir}/miniconda
  export DOCKER_REGISTRY=docker.idiap.ch
  export DOCSERVER=https://www.idiap.ch/software/bob
fi

source ${basedir}/_ci/functions.sh

branch=$1
check_env branch

destdir="$(cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd)"
check_env destdir

run_cmd curl -o ${destdir}/_core_docker_pull.sh --silent "https://gitlab.idiap.ch/beat/beat.core/raw/${branch}/scripts/docker_pull.sh"
run_cmd chmod 755 ${destdir}/_core_docker_pull.sh
run_cmd ${destdir}/_core_docker_pull.sh
