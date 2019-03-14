#!/usr/bin/env bash
DATA_DIR="/home/kootnet_data"
PYTHON_ENV_DIR="python-env"
APT_GET_INSTALL="libatlas3-base fonts-freefont-ttf python3 python3-pip python3-tk python3-venv"
# Make sure its running with root
if [[ $EUID != 0 ]]; then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
printf '\nChecking & creating required folders\n'
mkdir /mnt/supernas 2>/dev/null
mkdir /opt/kootnet-control-center 2>/dev/null
mkdir /opt/kootnet-control-center/logs 2>/dev/null
mkdir ${DATA_DIR} 2>/dev/null
chmod 777 ${DATA_DIR} 2>/dev/null
cd ${DATA_DIR} 2>/dev/null
# Install dependencies and upgrade pip
printf '\nVerifying dependencies\n'
apt-get update
apt-get -y install ${APT_GET_INSTALL}
python3 -m venv --system-site-packages ${PYTHON_ENV_DIR}
source ${DATA_DIR}/${PYTHON_ENV_DIR}/bin/activate
python3 -m pip install -U pip
pip3 install -r /opt/kootnet-control-center/requirements.txt
pip3 install -U numpy
