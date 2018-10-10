"""
    KootNet Sensors is a collection of programs and scripts to deploy,
    interact with, and collect readings from various Sensors.
    Copyright (C) 2018  Chad Ermacora  chad.ermacora@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import socket
import pickle
import os
import sys
import re
import logging
from logging.handlers import RotatingFileHandler
from tkinter import simpledialog
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:  %(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = RotatingFileHandler('logs/Sensor_Commands_log.txt', maxBytes=256000, backupCount=5)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

app_location_directory = str(os.path.dirname(sys.argv[0])) + "/"
config_file = app_location_directory + "config.txt"


def check_online_status(ip, net_timeout):
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'CheckOnlineStatus')
        sensor_status = "Online"
        logger.debug("IP: " + str(ip) + " Online")
    except Exception as error:
        logger.info("IP: " + str(ip) + " Offline: " + str(error))
        sensor_status = "Offline"

    sock_g.close()
    return sensor_status


def get_system_info(ip, net_timeout):
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'GetSystemData')
        var_data = pickle.loads(sock_g.recv(4096))
        sensor_data = var_data.split(",")
        sock_g.close()
        logger.debug("Getting Sensor Data from " + str(ip) + " - OK")
        return sensor_data
    except Exception as error:
        logger.warning("Getting Sensor Data from " + ip + " - Failed: " + str(error))
        offline_sensor_values = ["Network Timeout", ip, 0, 0, 0, 0, 0, 0, 0, 0, 0, "0000-00-00 00:00:00"]
        return offline_sensor_values


def upgrade_program_smb(ip):
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'UpgradeSMB')
        logger.info("SMB Upgrade on " + ip + " - OK")
    except Exception as error:
        logger.warning("SMB Upgrade on " + ip + " - Failed: " + str(error))
    sock_g.close()


def upgrade_program_online(ip):
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'UpgradeOnline')
        logger.info("HTTP Upgrade on " + ip + " - OK")
    except Exception as error:
        logger.warning("HTTP Upgrade on " + ip + " - Failed: " + str(error))
    sock_g.close()


def upgrade_os_linux(ip):
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'UpgradeSystemOS')
        logger.info("Linux OS Upgrade on " + ip + " - OK")
    except Exception as error:
        logger.warning("Linux OS Upgrade on " + ip + " - Failed: " + str(error))
    sock_g.close()


def reboot_sensor(ip):
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'RebootSystem')
        logger.info("Reboot on " + ip + " - OK")
    except Exception as error:
        logger.warning("Reboot on " + ip + " - Failed: " + str(error))
    sock_g.close()


def shutdown_sensor(ip):
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'ShutdownSystem')
        logger.info("Shutdown on " + ip + " - OK")
    except Exception as error:
        logger.warning("Shutdown on " + ip + " - Failed: " + str(error))
    sock_g.close()


def restart_services(ip):
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'RestartServices')
        logger.info("Restarting Services on " + ip + " - OK")
    except Exception as error:
        logger.warning("Restarting Services on " + ip + " - Failed: " + str(error))
    sock_g.close()


def set_hostname(ip):
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tmp_hostname = simpledialog.askstring(str(ip), "New Hostname: ")

    logger.debug(tmp_hostname)

    if tmp_hostname is not None and tmp_hostname is not "":
        new_hostname = re.sub('\W', '_', tmp_hostname)
        logger.debug(new_hostname)

        command_str = 'ChangeHostName' + str(new_hostname)
        try:
            sock_g.connect((ip, 10065))
            sock_g.send(command_str.encode())
            logger.info("Sensor Name Change " + str(new_hostname) + " on " + ip + " - OK")
        except Exception as error:
            logger.warning("Sensor Name Change " + str(new_hostname) + " on " + ip + " - Failed: " + str(error))
        sock_g.close()
    else:
        logger.warning("Hostname Cancelled or blank on " + ip)


def set_datetime(ip):
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_datetime = datetime.now().strftime("%Y-%m-%d%H:%M:%S")
    logger.debug(new_datetime)

    command_str = 'SetDateTime' + str(new_datetime)
    try:
        sock_g.connect((ip, 10065))
        sock_g.send(command_str.encode())
        logger.info("Sensor Name Change " + str(new_datetime) + " on " + ip + " - OK")
    except Exception as error:
        logger.warning("Sensor Name Change " + str(new_datetime) + " on " + ip + " - Failed: " + str(error))
    sock_g.close()


def get_sensor_config(ip, net_timeout):
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_g2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'GetConfiguration')
        var_data_config = pickle.loads(sock_g.recv(4096))
        sensor_config = var_data_config.split(",")
        logger.debug("Configuration Received from " + ip + " - OK")
    except Exception as error:
        sensor_config = ["0", "0", "0", "0", "0", "0", "0"]
        logger.warning("Configuration Received from " + ip + " - Failed: " + str(error))
    sock_g.close()

    try:
        sock_g2.connect((ip, 10065))
        sock_g2.send(b'GetSystemData')
        var_data_system = pickle.loads(sock_g2.recv(4096))
        sensor_system = var_data_system.split(",")
    except Exception as error:
        sensor_system = ["TimeOut", "0.0.0.0", "N/A"]
        logger.warning("Configuration Received from " + ip + " - Failed: " + str(error))
    sock_g2.close()

    final_sensor_config = [str(sensor_system[0]),
                           str(sensor_system[1]),
                           str(sensor_system[2]),
                           str(sensor_config[0]),
                           str(sensor_config[1]),
                           str(sensor_config[2]),
                           str(sensor_config[3]),
                           str(sensor_config[4]),
                           str(sensor_config[5]),
                           str(sensor_config[6])]

    return final_sensor_config


def set_sensor_config(ip, str_config):
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    str_config = "SetConfiguration" + str_config

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(str_config.encode())
        logger.info("Set Configuration on " + ip + " - OK")
    except Exception as error:
        logger.warning("Set Configuration on " + ip + " - Failed: " + str(error))
    sock_g.close()
