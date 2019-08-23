#!/usr/bin/env bash
DATA_DIR='/home/kootnet_data'  # This is hardcoded into linux services
if [[ "$1" != "" ]]
then
  USER_NAME=$1
else
  USER_NAME="pi"
fi
mkdir ${DATA_DIR} 2>/dev/null
mkdir ${DATA_DIR}/scripts 2>/dev/null
cat > ${DATA_DIR}/scripts/control_center_uninstall.sh << EOF
#!/usr/bin/env bash
# This script will remove all KootNet Sensors - Control Center program files off the computer
USER_NAME=
EOF
truncate -s-1 ${DATA_DIR}/scripts/control_center_uninstall.sh
echo '"'${USER_NAME}'"' >> ${DATA_DIR}/scripts/control_center_uninstall.sh
cat >> ${DATA_DIR}/scripts/control_center_uninstall.sh << EOF
# Make sure its running with root
if [[ $EUID != 0 ]]; then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
printf "\nUninstalling Kootnet Control Center\n"
rm -f /home/${USER_NAME}/Desktop/KootNet-Control-Center.desktop 2>/dev/null
rm -f /usr/share/applications/KootNet-Control-Center.desktop 2>/dev/null
rm -f -R /opt/kootnet-control-center 2>/dev/null
rm -f /opt/kootnet-control-center/installed_datetime.txt
printf "\nKootnet Control Center Uninstalled\n"
rm -f /home/kootnet_data/scripts/control_center_uninstall.sh
EOF
