#!/usr/bin/env bash
CONFIG_DIR="/etc/kootnet"
# Make sure its running with root
if [[ $EUID != 0 ]]
then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
# Make sure file permissions are correct
printf "\nSetting permissions\n"
touch ${CONFIG_DIR}/control_center.conf
touch /opt/kootnet-control-center/logs/KootNet_log.txt
touch /opt/kootnet-control-center/logs/Sensor_Commands_log.txt
chmod 777 ${CONFIG_DIR} -R
chmod 775 /opt/kootnet-control-center -R
chmod 766 /opt/kootnet-control-center/config.txt
chmod 766 /opt/kootnet-control-center/logs/*.txt
