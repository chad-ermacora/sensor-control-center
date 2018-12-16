#!/usr/bin/env bash
# Upgrade from Online HTTP server
HTTP_SERVER="http://kootenay-networks.com"
HTTP_FOLDER="/utils/koot_net_sensors/Installers/raspbian"
HTTP_ZIP="/KootNetSensors.zip"
# Make sure its running with root
if [[ $EUID != 0 ]]; then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
# Start Script
killall nano 2>/dev/null
printf '\nChecking & creating required folders\n'
mkdir /opt/kootnet-control-center 2>/dev/null
mkdir /opt/kootnet-control-center/logs 2>/dev/null
rm -R /tmp/SensorHTTPUpgrade 2>/dev/null
mkdir /tmp/SensorHTTPUpgrade 2>/dev/null
rm -f /tmp/KootNetSensors.zip 2>/dev/null
printf '\n\nDownloads started\n'
wget ${HTTP_SERVER}${HTTP_FOLDER}${HTTP_ZIP} -P /tmp/
printf 'Downloads complete\nUnzipping & installing files\n'
unzip /tmp/KootNetSensors.zip -d /tmp/SensorHTTPUpgrade
cp -f -R /tmp/SensorHTTPUpgrade/sensor-control-center/* /opt/kootnet-control-center
# Install needed programs and dependencies
bash /opt/kootnet-control-center/scripts/install_dependencies.sh
# Create user Shortcuts
bash /opt/kootnet-control-center/scripts/create_shortcuts.sh
# Make sure log files exist to set permissions
bash /opt/kootnet-control-center/scripts/set_permissions.sh
