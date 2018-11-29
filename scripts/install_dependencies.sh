#!/usr/bin/env bash
PIP3_INSTALL="guizero request plotly matplotlib"
APT_GET_INSTALL="libatlas3-base fonts-freefont-ttf"
# Make sure its running with root
if [[ $EUID != 0 ]]; then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
# Install dependencies and upgrade pip
printf '\nVerifying dependencies\n'
apt-get update
apt-get -y install ${APT_GET_INSTALL}
python3 -m pip install -U pip
pip3 install ${PIP3_INSTALL}
