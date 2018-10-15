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
import re
import os
import logging
from logging.handlers import RotatingFileHandler
from tkinter import simpledialog
from datetime import datetime
from urllib.request import urlopen

script_directory = str(os.path.dirname(os.path.realpath(__file__)))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:  %(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = RotatingFileHandler(script_directory + '/logs/Sensor_Commands_log.txt', maxBytes=256000, backupCount=5)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

config_file = "config.txt"


def check_online_status(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor status. """
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
    """ Socket connection to sensor IP. Return sensor system information. """
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'GetSystemData')
        var_data = pickle.loads(sock_g.recv(4096))
        final_data = var_data.split(',')
        sock_g.close()
        logger.debug("Getting Sensor Data from " + str(ip) + " - OK")

    except Exception as error:
        logger.warning("Getting Sensor Data from " + ip + " - Failed: " + str(error))
        final_data = ["Network Timeout", ip, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]

    return final_data


def get_sensor_readings(ip, net_timeout):
    """
    Socket connection to sensor IP. Return sensor's readings.

    Returned data is a list of 2 comma separated strings.

    The first string is the Interval readings, the second, Trigger readings.
    """
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'GetSensorReadings')
        var_data = pickle.loads(sock_g.recv(4096))
        sock_g.close()
        logger.debug("Getting Sensor Readings from " + str(ip) + " - OK")
    except Exception as error:
        var_data = ""
        logger.warning("Getting Sensor Readings from " + ip + " - Failed: " + str(error))

    return var_data


def get_sensor_config(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor configuration. """
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

    sensor_system = get_system_info(ip, net_timeout)

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


def download_interval_db(ip, download_to_location):
    """ Socket connection to sensor IP. Download Interval SQLite3 database. """
    try:
        remote_database = urlopen("http://" + ip + ":8009/SensorIntervalDatabase.sqlite")
        local_file = open(download_to_location + "/SensorIntervalDatabase" + ip[-3:] + ".sqlite", 'wb')
        local_file.write(remote_database.read())
        remote_database.close()
        local_file.close()
        logger.info("Download Interval DB from " + ip + " Complete")
    except Exception as error:
        logger.error("Download Interval DB from " + ip + " Failed: " + str(error))


def download_trigger_db(ip, download_to_location):
    """ Socket connection to sensor IP. Download Trigger SQLite3 database. """
    try:
        remote_database = urlopen("http://" + ip + ":8009/SensorTriggerDatabase.sqlite")
        local_file = open(download_to_location + "/SensorTriggerDatabase" + ip[-3:] + ".sqlite", 'wb')
        local_file.write(remote_database.read())
        remote_database.close()
        local_file.close()
        logger.info("Download Trigger DB from " + ip + " Complete")
    except Exception as error:
        logger.error("Download Trigger DB from " + ip + " Failed: " + str(error))


def upgrade_program_smb(ip):
    """ Socket connection to sensor IP. Send command to initiate SMB Upgrade Script. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'UpgradeSMB')
        logger.info("SMB Upgrade on " + ip + " - OK")
    except Exception as error:
        logger.warning("SMB Upgrade on " + ip + " - Failed: " + str(error))
    sock_g.close()


def upgrade_program_online(ip):
    """ Socket connection to sensor IP. Send command to initiate HTTP Upgrade Script. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'UpgradeOnline')
        logger.info("HTTP Upgrade on " + ip + " - OK")
    except Exception as error:
        logger.warning("HTTP Upgrade on " + ip + " - Failed: " + str(error))
    sock_g.close()


def upgrade_os_linux(ip):
    """ Socket connection to sensor IP. Send command to initiate Operating System upgrade. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'UpgradeSystemOS')
        logger.info("Linux OS Upgrade on " + ip + " - OK")
    except Exception as error:
        logger.warning("Linux OS Upgrade on " + ip + " - Failed: " + str(error))
    sock_g.close()


def reboot_sensor(ip):
    """ Socket connection to sensor IP. Send command to initiate a system reboot. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'RebootSystem')
        logger.info("Reboot on " + ip + " - OK")
    except Exception as error:
        logger.warning("Reboot on " + ip + " - Failed: " + str(error))
    sock_g.close()


def shutdown_sensor(ip):
    """ Socket connection to sensor IP. Send command to initiate system shutdown. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'ShutdownSystem')
        logger.info("Shutdown on " + ip + " - OK")
    except Exception as error:
        logger.warning("Shutdown on " + ip + " - Failed: " + str(error))
    sock_g.close()


def restart_services(ip):
    """ Socket connection to sensor IP. Send command to initiate KootNet Sensor services restart. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'RestartServices')
        logger.info("Restarting Services on " + ip + " - OK")
    except Exception as error:
        logger.warning("Restarting Services on " + ip + " - Failed: " + str(error))
    sock_g.close()


def set_hostname(ip):
    """ Socket connection to sensor IP. Send command to update the system hostname. """
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
    """ Socket connection to sensor IP. Send command to set the sensors date and time to match the computers. """
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


def set_sensor_config(ip, str_config):
    """ Socket connection to sensor IP. Send command set the sensor Configuration. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    str_config = "SetConfiguration" + str_config

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(str_config.encode())
        logger.info("Set Configuration on " + ip + " - OK")
    except Exception as error:
        logger.warning("Set Configuration on " + ip + " - Failed: " + str(error))
    sock_g.close()
