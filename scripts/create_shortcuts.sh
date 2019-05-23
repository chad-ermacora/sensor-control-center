#!/usr/bin/env bash
USER_DIR="/home/oo-dragon/"
# Sensor Control Center shortcut
printf "\nInstalling shortcuts\n"
cat > ${USER_DIR}/Desktop/KootNet-Control-Center.desktop << "EOF"
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
cp -f ${USER_DIR}/Desktop/KootNet-Control-Center.desktop /usr/share/applications/KootNet-Control-Center.desktop
