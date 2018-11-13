#!/usr/bin/env bash
# Make sure SMB_SHARE points to the root share holding both Sensor & Control Center folders
USER_DIR="/home/pi/"
SMB_SERVER="//gamercube1"
SMB_SHARE="/PyCharmProjects"
SMB_SENSOR="/sensor-rp"
SMB_CONTROL_CENTER="/sensor-control-center"
CIFS_OPTIONS="username=myself,password='123'"
RSYNC_EXCLUDE="--exclude .git --exclude .idea --exclude __pycache__ --exclude config.txt --exclude test_files/SensorIntervalGraph.html --exclude test_files/SensorTriggerGraph.html"
PIP3_INSTALL="guizero request plotly matplotlib"
# Make sure its running with root
if [[ $EUID != 0 ]]; then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
# Start Script
# Kill any open nano & make sure folders are created
killall nano 2>/dev/null
printf '\nChecking & creating required folders\n'
mkdir /mnt/supernas 2>/dev/null
mkdir /opt/kootnet-control-center 2>/dev/null
mkdir /opt/kootnet-control-center/logs 2>/dev/null
# Download and Upgrade Sensor Programs off SMB
printf '\nConnecting to SMB & copying files\n'
mount -t cifs ${SMB_SERVER}${SMB_SHARE} /mnt/supernas -o ${CIFS_OPTIONS}
sleep 1
printf 'Copying control center files\n\n'
rsync -q -r -4 -P /mnt/supernas${SMB_CONTROL_CENTER}/ /opt/kootnet-control-center/ ${RSYNC_EXCLUDE}
sleep 1
umount /mnt/supernas
# Install needed programs and dependencies
printf '\nChecking dependencies\n'
python3 -m pip install -U pip
pip3 install ${PIP3_INSTALL}
# python3 -m pip install -U numpy
# Sensor Control Center shortcut
cat > ${USER_DIR}/Desktop/KootNet-Control-Center.desktop << "EOF"
[Desktop Entry]
Name=Kootnet Sensors - Control Center
Comment=Monitor and Manage KootNet Sensors
Icon=/opt/kootnet-control-center/additional_files/icon.ico
Exec=/usr/bin/python3 /opt/kootnet-control-center/main_guizero.py
Type=Application
Encoding=UTF-8
Terminal=false
Categories=Utility;Science;
EOF
cp -f ${USER_DIR}/Desktop/KootNet-Control-Center.desktop /usr/share/applications/KootNet-Control-Center.desktop
# Sensor reconfiguration and test shortcut
cat > ${USER_DIR}/Desktop/KootNet-Sensor-Config.desktop << "EOF"
[Desktop Entry]
Name=Kootnet Sensors - Configuration & Test
Comment=Reconfigure sensor & display sensor readings
Icon=/usr/share/icons/PiX/128x128/mimetypes/shellscript.png
Exec=/bin/bash /opt/kootnet-sensors/upgrade/edit_sensor_config.sh
Type=Application
Encoding=UTF-8
Terminal=true
Categories=Utility;Science;
EOF
cp -f ${USER_DIR}/Desktop/KootNet-Sensor-Config.desktop /usr/share/applications/KootNet-Sensor-Config.desktop
# Make sure log files exist to set permissions
touch /opt/kootnet-control-center/config.txt
touch /opt/kootnet-control-center/logs/KootNet_log.txt
touch /opt/kootnet-control-center/logs/Sensor_Commands_log.txt
chmod 766 /opt/kootnet-control-center/config.txt
chmod 775 /opt/kootnet-control-center -R
chmod 766 /opt/kootnet-control-center/logs/*.txt
chmod 766 ${USER_DIR}/Desktop/*.desktop
