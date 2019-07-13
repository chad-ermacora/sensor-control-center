#!/usr/bin/env bash
# Upgrade from Online HTTP server
HTTP_SERVER="http://kootenay-networks.com"
HTTP_FOLDER="/utils/koot_net_sensors/Installers/raspbian"
HTTP_ZIP="/KootNetSensors.zip"
# Make sure its running with root
if [[ $EUID != 0 ]]
then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
# Start Script
if [[ -f /opt/kootnet-control-center/installed_datetime.txt ]]
then
  printf '\nStarting Kootnet Control Center Upgrade - Online HTTP\n'
else
  read -p "Enter the username you want a desktop shortcut on (Default is pi): " USER_NAME
  printf '\nStarting Kootnet Control Center Install - Online HTTP\n'
fi
mkdir /opt/kootnet-control-center 2>/dev/null
mkdir /opt/kootnet-control-center/logs 2>/dev/null
# Clean up previous downloads if any
rm -f /tmp/KootNetSensors.zip 2>/dev/null
rm -R /tmp/SensorHTTPUpgrade 2>/dev/null
mkdir /tmp/SensorHTTPUpgrade 2>/dev/null
printf '\n\nStarting Download\n'
wget -q --show-progress ${HTTP_SERVER}${HTTP_FOLDER}${HTTP_ZIP} -P /tmp/
printf 'Download Complete\nUnzipping & Installing Files\n'
unzip -q /tmp/KootNetSensors.zip -d /tmp/SensorHTTPUpgrade
cp -f -R /tmp/SensorHTTPUpgrade/sensor-control-center/* /opt/kootnet-control-center
if [[ -f /opt/kootnet-control-center/installed_datetime.txt ]]
then
  printf "Upgrade Complete"
else
  # Install needed programs and dependencies
  bash /opt/kootnet-control-center/scripts/install_dependencies.sh
  # Create user Shortcuts
  bash /opt/kootnet-control-center/scripts/create_shortcuts.sh ${USER_NAME}
  # Create Custom Uninstaller
  bash /opt/kootnet-control-center/scripts/create_custom_uninstall.sh ${USER_NAME}
  printf "\nInstall Complete\n"
fi
bash /opt/kootnet-control-center/scripts/set_permissions.sh
