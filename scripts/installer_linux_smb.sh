#!/usr/bin/env bash
# Upgrade from SMB server (Windows Share)
# Make sure SMB_SHARE points to the root share holding the upgrade zip file
SMB_SERVER="//xps-development01"
SMB_SHARE="/KootNetSMB"
SMB_FILE="/KootNetSensors.zip"
CIFS_OPTIONS="username=myself,password='123'"
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
  printf '\nStarting Kootnet Control Center Upgrade - SMB\n'
else
  read -p "Enter the username you want a desktop shortcut on (Default is pi): " USER_NAME
  printf '\nStarting Kootnet Control Center Install - SMB\n'
fi
mkdir /mnt/supernas 2>/dev/null
mkdir /opt/kootnet-control-center 2>/dev/null
mkdir /opt/kootnet-control-center/logs 2>/dev/null
# Clean up previous downloads if any
rm -f /tmp/KootNetSensors.zip 2>/dev/null
rm -R /tmp/SensorSMBUpgrade 2>/dev/null
mkdir /tmp/SensorSMBUpgrade 2>/dev/null
# Make sure cifs is installed for SMB mount
apt-get install cifs-utils
# Download and Upgrade Sensor Programs off SMB
printf '\nConnecting to SMB\n'
mount -t cifs ${SMB_SERVER}${SMB_SHARE} /mnt/supernas -o ${CIFS_OPTIONS}
sleep 1
printf '\nDownload Started\n'
cp /mnt/supernas${SMB_FILE} /tmp
unzip -q /tmp/KootNetSensors.zip -d /tmp/SensorSMBUpgrade
printf 'Download Complete\n\nUnzipping & Installing Files\n'
cp -f -R /tmp/SensorSMBUpgrade/sensor-control-center/* /opt/kootnet-control-center
printf 'Files Installed\n\n'
umount /mnt/supernas
if [[ -f /opt/kootnet-control-center/installed_datetime.txt ]]
then
  printf '\nUpgrade Complete\n'
else
  # Install needed programs and dependencies
  bash /opt/kootnet-control-center/scripts/install_dependencies.sh
  # Create user Shortcuts
  bash /opt/kootnet-control-center/scripts/create_shortcuts.sh ${USER_NAME}
  # Create Custom Uninstaller
  bash /opt/kootnet-control-center/scripts/create_custom_uninstall.sh ${USER_NAME}
  printf '\nInstall Complete\n'
fi
bash /opt/kootnet-control-center/scripts/set_permissions.sh
