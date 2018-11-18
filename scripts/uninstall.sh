#!/usr/bin/env bash
# This script will remove all KootNet Sensors - Control Center program files off the computer
USER_DIR="/home/pi/"
# Make sure its running with root
if [[ $EUID != 0 ]]; then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
rm -f ${USER_DIR}/Desktop/KootNet-Control-Center.desktop
rm -f ${USER_DIR}/Desktop/KootNet-Sensor-Config.desktop
rm -f /usr/share/applications/KootNet-Control-Center.desktop
rm -f /usr/share/applications/KootNet-Sensor-Config.desktop
rm -f -R /opt/kootnet-control-center
