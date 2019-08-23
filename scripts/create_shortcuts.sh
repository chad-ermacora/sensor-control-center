#!/usr/bin/env bash
if [[ "$1" != "" ]]
then
  USER_NAME=$1
else
  USER_NAME="pi"
fi
# Sensor Control Center shortcut
printf "\nInstalling shortcuts\n"
cat > /usr/share/applications/KootNet-Control-Center.desktop << "EOF"
[Desktop Entry]
Name=Kootnet Sensors - Control Center
Comment=Monitor and Manage KootNet Sensors
Icon=/opt/kootnet-control-center/additional_files/icon.ico
Exec=/home/kootnet_data/python-env/bin/python3 /opt/kootnet-control-center/start_app_guizero.py
Type=Application
Encoding=UTF-8
Terminal=false
Categories=Utility;Science;
EOF
cp -f /usr/share/applications/KootNet-Control-Center.desktop /home/${USER_NAME}/Desktop/KootNet-Control-Center.desktop
chmod 777 /home/${USER_NAME}/Desktop/KootNet*.desktop
