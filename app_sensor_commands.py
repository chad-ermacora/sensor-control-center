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


class CreateHTTPDownload:
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = ":8009"
        self.url = "/"
        self.file_name = "wrong_file.default"
        self.save_to_location = "/home/pi/"


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


def get_network_log(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensors network log. """
    log = _get_data(ip, net_timeout, "GetNetworkLog")
    return log


def get_sensor_primary_log(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensors operations log. """
    log = _get_data(ip, net_timeout, "GetOperationsLog")
    return log


def get_sensors_log(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensors "sensors" log. """
    log = _get_data(ip, net_timeout, "GetSensorsLog")
    return log


def get_sensor_system(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor system information. """
    var_data = _get_data(ip, net_timeout, "GetSystemData")
    final_data = var_data.split(',')
    return final_data


def get_sensor_readings(ip, net_timeout):
    """
    Socket connection to sensor IP. Return sensor's readings.

    Returned data is a list of 2 comma separated strings.

    The first string is the Interval readings, the second, Trigger readings.
    """
    var_data = _get_data(ip, net_timeout, "GetSensorReadings")
    return var_data


def get_sensor_hostname(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's hostname. """
    var_data = _get_data(ip, net_timeout, "GetHostName")
    return var_data


def get_sensor_uptime(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's System Uptime. """
    var_data = _get_data(ip, net_timeout, "GetSystemUptime")
    return var_data


def get_sensor_cpu_temperature(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's System CPU Temperature. """
    var_data = _get_data(ip, net_timeout, "GetCPUTemperature")
    return var_data


def get_sensor_temperature(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's temperature. """
    var_data = _get_data(ip, net_timeout, "GetEnvTemperature")
    return var_data


def get_sensor_pressure(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's Pressure in hPa. """
    var_data = _get_data(ip, net_timeout, "GetPressure")
    return var_data


def get_sensor_humidity(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's Humidity in %RH. """
    var_data = _get_data(ip, net_timeout, "GetHumidity")
    return var_data


def get_sensor_lumen(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's Lumen. """
    var_data = _get_data(ip, net_timeout, "GetLumen")
    return var_data


def get_sensor_rgb(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor's Red, Green, Blue readings. """
    var_data = _get_data(ip, net_timeout, "GetRGB")
    return var_data


def get_sensor_config(ip, net_timeout):
    """ Socket connection to sensor IP. Return sensor configuration. """
    var_data = _get_data(ip, net_timeout, "GetConfiguration")
    sensor_config = var_data.split(",")
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


def download_logs(download_obj):
    """ Download 3 log files. """
    download_obj.file_name = "Primary_log.txt"
    download_http_file(download_obj)

    download_obj.file_name = "Sensors_log.txt"
    download_http_file(download_obj)

    download_obj.file_name = "Network_log.txt"
    download_http_file(download_obj)


def download_http_file(obj_download):
    """ Download provided HTTP file to locally chosen directory. """
    try:
        http_file = urlopen(
            "http://" + obj_download.ip + obj_download.port + obj_download.url + obj_download.file_name)
        local_file = open(obj_download.save_to_location + "/_" + obj_download.ip[-3:] + obj_download.file_name, 'wb')
        local_file.write(http_file.read())
        http_file.close()
        local_file.close()
        app_logger.sensor_logger.info("Download " + obj_download.file_name + " from " + obj_download.ip + " Complete")
    except Exception as error:
        app_logger.sensor_logger.error(
            "Download " + obj_download.file_name + " from " + obj_download.ip + " Failed: " + str(error))


def upgrade_program_smb(ip):
    """ Socket connection to sensor IP. Send command to initiate SMB Upgrade Script. """
    _send_command(ip, "UpgradeSMB")


def upgrade_program_online(ip):
    """ Socket connection to sensor IP. Send command to initiate HTTP Upgrade Script. """
    _send_command(ip, "UpgradeOnline")


def clean_upgrade_smb(ip):
    """ Socket connection to sensor IP. Send command to initiate HTTP Upgrade Script. """
    _send_command(ip, "CleanSMB")


def clean_upgrade_online(ip):
    """ Socket connection to sensor IP. Send command to initiate HTTP Upgrade Script. """
    _send_command(ip, "CleanOnline")


def upgrade_os_linux(ip):
    """ Socket connection to sensor IP. Send command to initiate Operating System upgrade. """
    _send_command(ip, "UpgradeSystemOS")


def reboot_sensor(ip):
    """ Socket connection to sensor IP. Send command to initiate a system reboot. """
    _send_command(ip, "RebootSystem")


def shutdown_sensor(ip):
    """ Socket connection to sensor IP. Send command to initiate system shutdown. """
    _send_command(ip, "ShutdownSystem")


def restart_services(ip):
    """ Socket connection to sensor IP. Send command to initiate KootNet Sensor services restart. """
    _send_command(ip, "RestartServices")


def set_hostname(ip):
    """ Socket connection to sensor IP. Send command to update the system hostname. """
    tmp_hostname = simpledialog.askstring(str(ip), "New Hostname: ")
    app_logger.sensor_logger.debug(tmp_hostname)

    if tmp_hostname is not None and tmp_hostname is not "":
        new_hostname = re.sub('\W', '_', tmp_hostname)
        app_logger.sensor_logger.debug(new_hostname)

        command_str = 'ChangeHostName' + str(new_hostname)
        _send_command(ip, command_str)
    else:
        app_logger.sensor_logger.warning("Hostname Cancelled or blank on " + ip)


def set_datetime(ip):
    """ Socket connection to sensor IP. Send command to set the sensors date and time to match the computers. """
    new_datetime = datetime.now().strftime("%Y-%m-%d%H:%M:%S")
    app_logger.sensor_logger.debug(new_datetime)
    command_str = 'SetDateTime' + str(new_datetime)
    _send_command(ip, command_str)


def set_sensor_config(ip, str_config):
    """ Socket connection to sensor IP. Send command set the sensor Configuration. """
    command_str = "SetConfiguration" + str_config
    _send_command(ip, command_str)


def _send_command(ip, command):
    """ Socket connection to sensor IP. Sends provided text as command. """
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(command.encode())
        app_logger.sensor_logger.info(str(command) + " sent to " + ip + " - OK")
    except Exception as error:
        app_logger.sensor_logger.warning(str(command) + " sent to " + ip + " - Failed: " + str(error))
    sock_g.close()


def _get_data(ip, net_timeout, command):
    """ Socket connection to sensor IP. Return sensor's data. """
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(command.encode())
        var_data = pickle.loads(sock_g.recv(4096))
        sock_g.close()
        app_logger.sensor_logger.debug(command + " from " + str(ip) + " - OK")
    except Exception as error:
        var_data = "N/A"
        app_logger.sensor_logger.warning(command + " from " + str(ip) + " - Failed: " + str(error))
    return var_data
