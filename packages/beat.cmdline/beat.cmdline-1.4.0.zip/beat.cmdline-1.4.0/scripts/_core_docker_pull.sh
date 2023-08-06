#!/usr/bin/env bash

basedir=`pwd`

if [ ! -e ${basedir}/_ci/functions.sh ]; then
  # this will happen when executing buildout for the first time
  mkdir ${basedir}/_ci
  curl --silent "https://gitlab.idiap.ch/bob/bob.admin/raw/master/gitlab/install.sh" > ${basedir}/_ci/install.sh
  chmod 755 ${basedir}/_ci/install.sh
  ${basedir}/_ci/install.sh ${basedir}/_ci master #installs ci support scripts
fi

if [ "${BUILDOUT}" == "true" ]; then
  # when executing in the context of buildout, define dummies
  export CI_PROJECT_URL=https://gitlab.idiap.ch/beat/beat.core
  export CI_PROJECT_DIR=beat
  export CI_PROJECT_PATH=beat/beat.core
  export CI_PROJECT_NAME=beat.core
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

check_env DOCKER_REGISTRY

# Select here images that are required for minimal operation (or tests)
IMAGES=(
    "${DOCKER_REGISTRY}/beat/beat.env.system.python:1.3.0r4"
    "${DOCKER_REGISTRY}/beat/beat.env.db.examples:1.4.0r4"
    "${DOCKER_REGISTRY}/beat/beat.env.cxx:2.0.0r1"
    "${DOCKER_REGISTRY}/beat/beat.env.client:2.0.0r1"
    )
check_array_env IMAGES

missing=()
log_info "Checking for minimal set of docker images..."
for k in ${IMAGES[@]}; do
    hash_=$(docker images -q ${k})
    if [ -z "${hash_}" ]; then
        missing+=(${k})
        log_warn "${k} NOT available - downloading...";
    else
        log_info "${k} already available - not re-downloading";
    fi
done

# If there are some images missing, download them
if [[ "${#missing[@]}" > 0 ]]; then
  # Log in the registry if needed
  if [ -z "$CI_SERVER" ]; then
    if ! grep -q "${DOCKER_REGISTRY}" ~/.docker/config.json ; then
      run_cmd docker login "${DOCKER_REGISTRY}"
    fi
  else
    check_pass CI_BUILD_TOKEN
    log_info docker login -u gitlab-ci-token -p "*************" "${DOCKER_REGISTRY}"
    docker login -u gitlab-ci-token -p "${CI_BUILD_TOKEN}" "${DOCKER_REGISTRY}"
  fi

  # Pull the images
  for k in "${missing[@]}"; do
    run_cmd docker pull ${k}
  done
fi
