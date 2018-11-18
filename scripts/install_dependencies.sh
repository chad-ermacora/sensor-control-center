#!/usr/bin/env bash
PIP3_INSTALL="guizero request plotly matplotlib"
# Make sure its running with root
if [[ $EUID != 0 ]]; then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
# Upgrade pip, build numpy, install packages
printf '\nVerifying dependencies\n'
python3 -m pip install -U pip
python3 -m pip install -U numpy
pip3 install ${PIP3_INSTALL}
