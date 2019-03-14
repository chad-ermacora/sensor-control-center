#!/usr/bin/env bash
# Make sure SMB_SHARE points to the root share holding both Sensor & Control Center folders
SMB_SERVER="//xps-development01"
SMB_SHARE="/PyProjects"
SMB_SENSOR="/sensor-rp"
SMB_CONTROL_CENTER="/sensor-control-center"
CIFS_OPTIONS="username=myself,password='123'"
RSYNC_EXCLUDE="--exclude .git --exclude .idea --exclude __pycache__ --exclude config.txt \
--exclude test_files/SensorIntervalGraph.html --exclude test_files/SensorTriggerGraph.html"
# Make sure its running with root
if [[ $EUID != 0 ]]; then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
# Start Script
killall nano 2>/dev/null
# Make sure cifs is installed for SMB mount
apt-get install cifs-utils
# Download and Upgrade Sensor Programs off SMB
printf '\nConnecting to SMB & copying files\n'
mount -t cifs ${SMB_SERVER}${SMB_SHARE} /mnt/supernas -o ${CIFS_OPTIONS}
sleep 1
printf 'Copying control center files\n\n'
rsync -q -r -4 -P /mnt/supernas${SMB_CONTROL_CENTER}/ /opt/kootnet-control-center/ ${RSYNC_EXCLUDE}
sleep 1
umount /mnt/supernas
# Install needed programs and dependencies
bash /opt/kootnet-control-center/scripts/install_dependencies.sh
# Create user Shortcuts
bash /opt/kootnet-control-center/scripts/create_shortcuts.sh
# Make sure log files exist to set permissions
bash /opt/kootnet-control-center/scripts/set_permissions.sh
