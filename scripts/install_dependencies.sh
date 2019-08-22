#!/usr/bin/env bash
DATA_DIR="/home/kootnet_data"
PYTHON_ENV_DIR="python-env"
CONFIG_DIR="/etc/kootnet"
APT_GET_INSTALL="libatlas3-base fonts-freefont-ttf python3 python3-pip python3-tk python3-venv"
# Make sure its running with root
if [[ $EUID != 0 ]]
then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
printf '\nChecking & Creating Required Folders\n'
mkdir ${CONFIG_DIR} 2>/dev/null
mkdir ${DATA_DIR} 2>/dev/null
chmod 777 ${DATA_DIR} 2>/dev/null
cd ${DATA_DIR} 2>/dev/null || exit
# Install dependencies and upgrade pip
printf '\nVerifying Dependencies\n'
apt-get update
apt-get -y install ${APT_GET_INSTALL}
python3 -m venv --system-site-packages ${PYTHON_ENV_DIR}
# shellcheck source=/dev/null
source ${DATA_DIR}/${PYTHON_ENV_DIR}/bin/activate
python3 -m pip install -U pip
pip3 install -r /opt/kootnet-control-center/requirements.txt
# Create Installed File to prevent re-runs.  Create install_version file for program first run.
date > /opt/kootnet-control-center/installed_datetime.txt
deactivate
