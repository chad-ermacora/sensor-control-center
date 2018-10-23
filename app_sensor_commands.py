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
import pickle
import re
import socket
from datetime import datetime
from tkinter import simpledialog
from urllib.request import urlopen

import app_logger


def check_sensor_status(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor status. """
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'CheckOnlineStatus')
        sensor_status = "Online"
        app_logger.sensor_logger.debug("IP: " + str(ip) + " Online")
    except Exception as error:
        app_logger.sensor_logger.info("IP: " + str(ip) + " Offline: " + str(error))
        sensor_status = "Offline"

    sock_g.close()

    return sensor_status


def get_sensor_system(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor system information. """
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'GetSystemData')
        var_data = pickle.loads(sock_g.recv(4096))
        final_data = var_data.split(',')
        sock_g.close()
        app_logger.sensor_logger.debug("Getting Sensor Data from " + str(ip) + " - OK")

    except Exception as error:
        app_logger.sensor_logger.warning("Getting Sensor Data from " + ip + " - Failed: " + str(error))
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
        app_logger.sensor_logger.debug("Getting Sensor Readings from " + str(ip) + " - OK")
    except Exception as error:
        var_data = ["Readings Failed on " + ip, str(error), "Readings Failed on " + ip, str(error)]
        app_logger.sensor_logger.warning("Getting Sensor Readings from " + ip + " - Failed: " + str(error))

    return var_data


def get_sensor_hostname(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's hostname. """
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'GetHostName')
        var_data = pickle.loads(sock_g.recv(4096))
        sock_g.close()
        app_logger.sensor_logger.debug("Getting Sensor Readings from " + str(ip) + " - OK")
    except Exception as error:
        var_data = 0
        app_logger.sensor_logger.warning("Getting Sensor Readings from " + ip + " - Failed: " + str(error))

    return var_data


def get_sensor_uptime(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's System Uptime. """
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'GetSystemUptime')
        var_data = pickle.loads(sock_g.recv(4096))
        sock_g.close()
        app_logger.sensor_logger.debug("Getting Sensor Readings from " + str(ip) + " - OK")
    except Exception as error:
        var_data = 0
        app_logger.sensor_logger.warning("Getting Sensor Readings from " + ip + " - Failed: " + str(error))

    return var_data


def get_sensor_cpu_temperature(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's System CPU Temperature. """
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'GetCPUTemperature')
        var_data = pickle.loads(sock_g.recv(4096))
        sock_g.close()
        app_logger.sensor_logger.debug("Getting Sensor Readings from " + str(ip) + " - OK")
    except Exception as error:
        var_data = 0
        app_logger.sensor_logger.warning("Getting Sensor Readings from " + ip + " - Failed: " + str(error))

    return var_data


def get_sensor_temperature(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's temperature. """
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'GetEnvTemperature')
        var_data = pickle.loads(sock_g.recv(4096))
        sock_g.close()
        app_logger.sensor_logger.debug("Getting Sensor Readings from " + str(ip) + " - OK")
    except Exception as error:
        var_data = 0
        app_logger.sensor_logger.warning("Getting Sensor Readings from " + ip + " - Failed: " + str(error))

    return var_data


def get_sensor_pressure(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's Pressure in hPa. """
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'GetPressure')
        var_data = pickle.loads(sock_g.recv(4096))
        sock_g.close()
        app_logger.sensor_logger.debug("Getting Sensor Readings from " + str(ip) + " - OK")
    except Exception as error:
        var_data = 0
        app_logger.sensor_logger.warning("Getting Sensor Readings from " + ip + " - Failed: " + str(error))

    return var_data


def get_sensor_humidity(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's Humidity in %RH. """
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'GetHumidity')
        var_data = pickle.loads(sock_g.recv(4096))
        sock_g.close()
        app_logger.sensor_logger.debug("Getting Sensor Readings from " + str(ip) + " - OK")
    except Exception as error:
        var_data = 0
        app_logger.sensor_logger.warning("Getting Sensor Readings from " + ip + " - Failed: " + str(error))

    return var_data


def get_sensor_lumen(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's Lumen. """
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'GetLumen')
        var_data = pickle.loads(sock_g.recv(4096))
        sock_g.close()
        app_logger.sensor_logger.debug("Getting Sensor Readings from " + str(ip) + " - OK")
    except Exception as error:
        var_data = 0
        app_logger.sensor_logger.warning("Getting Sensor Readings from " + ip + " - Failed: " + str(error))

    return var_data


def get_sensor_rgb(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's Red, Green, Blue readings. """
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'GetRGB')
        var_data = pickle.loads(sock_g.recv(4096))
        sock_g.close()
        app_logger.sensor_logger.debug("Getting Sensor Readings from " + str(ip) + " - OK")
    except Exception as error:
        var_data = 0
        app_logger.sensor_logger.warning("Getting Sensor Readings from " + ip + " - Failed: " + str(error))

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
        app_logger.sensor_logger.debug("Configuration Received from " + ip + " - OK")
    except Exception as error:
        sensor_config = ["0", "0", "0", "0", "0", "0", "0"]
        app_logger.sensor_logger.warning("Configuration Received from " + ip + " - Failed: " + str(error))
    sock_g.close()

    sensor_system = get_sensor_system(ip, net_timeout)

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
        app_logger.sensor_logger.info("Download Interval DB from " + ip + " Complete")
    except Exception as error:
        app_logger.sensor_logger.error("Download Interval DB from " + ip + " Failed: " + str(error))


def download_trigger_db(ip, download_to_location):
    """ Socket connection to sensor IP. Download Trigger SQLite3 database. """
    try:
        remote_database = urlopen("http://" + ip + ":8009/SensorTriggerDatabase.sqlite")
        local_file = open(download_to_location + "/SensorTriggerDatabase" + ip[-3:] + ".sqlite", 'wb')
        local_file.write(remote_database.read())
        remote_database.close()
        local_file.close()
        app_logger.sensor_logger.info("Download Trigger DB from " + ip + " Complete")
    except Exception as error:
        app_logger.sensor_logger.error("Download Trigger DB from " + ip + " Failed: " + str(error))


def upgrade_program_smb(ip):
    """ Socket connection to sensor IP. Send command to initiate SMB Upgrade Script. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'UpgradeSMB')
        app_logger.sensor_logger.info("SMB Upgrade on " + ip + " - OK")
    except Exception as error:
        app_logger.sensor_logger.warning("SMB Upgrade on " + ip + " - Failed: " + str(error))
    sock_g.close()


def upgrade_program_online(ip):
    """ Socket connection to sensor IP. Send command to initiate HTTP Upgrade Script. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'UpgradeOnline')
        app_logger.sensor_logger.info("HTTP Upgrade on " + ip + " - OK")
    except Exception as error:
        app_logger.sensor_logger.warning("HTTP Upgrade on " + ip + " - Failed: " + str(error))
    sock_g.close()


def upgrade_os_linux(ip):
    """ Socket connection to sensor IP. Send command to initiate Operating System upgrade. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'UpgradeSystemOS')
        app_logger.sensor_logger.info("Linux OS Upgrade on " + ip + " - OK")
    except Exception as error:
        app_logger.sensor_logger.warning("Linux OS Upgrade on " + ip + " - Failed: " + str(error))
    sock_g.close()


def reboot_sensor(ip):
    """ Socket connection to sensor IP. Send command to initiate a system reboot. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'RebootSystem')
        app_logger.sensor_logger.info("Reboot on " + ip + " - OK")
    except Exception as error:
        app_logger.sensor_logger.warning("Reboot on " + ip + " - Failed: " + str(error))
    sock_g.close()


def shutdown_sensor(ip):
    """ Socket connection to sensor IP. Send command to initiate system shutdown. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'ShutdownSystem')
        app_logger.sensor_logger.info("Shutdown on " + ip + " - OK")
    except Exception as error:
        app_logger.sensor_logger.warning("Shutdown on " + ip + " - Failed: " + str(error))
    sock_g.close()


def restart_services(ip):
    """ Socket connection to sensor IP. Send command to initiate KootNet Sensor services restart. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'RestartServices')
        app_logger.sensor_logger.info("Restarting Services on " + ip + " - OK")
    except Exception as error:
        app_logger.sensor_logger.warning("Restarting Services on " + ip + " - Failed: " + str(error))
    sock_g.close()


def set_hostname(ip):
    """ Socket connection to sensor IP. Send command to update the system hostname. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tmp_hostname = simpledialog.askstring(str(ip), "New Hostname: ")

    app_logger.sensor_logger.debug(tmp_hostname)

    if tmp_hostname is not None and tmp_hostname is not "":
        new_hostname = re.sub('\W', '_', tmp_hostname)
        app_logger.sensor_logger.debug(new_hostname)

        command_str = 'ChangeHostName' + str(new_hostname)
        try:
            sock_g.connect((ip, 10065))
            sock_g.send(command_str.encode())
            app_logger.sensor_logger.info("Sensor Name Change " + str(new_hostname) + " on " + ip + " - OK")
        except Exception as error:
            app_logger.sensor_logger.warning(
                "Sensor Name Change " + str(new_hostname) + " on " + ip + " - Failed: " + str(error))
        sock_g.close()
    else:
        app_logger.sensor_logger.warning("Hostname Cancelled or blank on " + ip)


def set_datetime(ip):
    """ Socket connection to sensor IP. Send command to set the sensors date and time to match the computers. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_datetime = datetime.now().strftime("%Y-%m-%d%H:%M:%S")
    app_logger.sensor_logger.debug(new_datetime)

    command_str = 'SetDateTime' + str(new_datetime)
    try:
        sock_g.connect((ip, 10065))
        sock_g.send(command_str.encode())
        app_logger.sensor_logger.info("Sensor Name Change " + str(new_datetime) + " on " + ip + " - OK")
    except Exception as error:
        app_logger.sensor_logger.warning(
            "Sensor Name Change " + str(new_datetime) + " on " + ip + " - Failed: " + str(error))
    sock_g.close()


def set_sensor_config(ip, str_config):
    """ Socket connection to sensor IP. Send command set the sensor Configuration. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    str_config = "SetConfiguration" + str_config

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(str_config.encode())
        app_logger.sensor_logger.info("Set Configuration on " + ip + " - OK")
    except Exception as error:
        app_logger.sensor_logger.warning("Set Configuration on " + ip + " - Failed: " + str(error))
    sock_g.close()
