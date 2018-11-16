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
from tkinter import simpledialog
from urllib.request import urlopen

import app_logger


class CreateCommandData:
    def __init__(self, ip, net_timeout, command):
        self.ip = ip
        self.net_timeout = net_timeout
        self.command = command


class CreateNetworkGetCommands:
    def __init__(self):
        self.sensor_configuration = "GetConfiguration"
        self.system_data = "GetSystemData"
        self.sensors_log = "GetSensorsLog"
        self.primary_log = "GetPrimaryLog"
        self.network_log = "GetNetworkLog"
        self.sensor_readings = "GetSensorReadings"
        self.sensor_name = "GetHostName"
        self.system_uptime = "GetSystemUptime"
        self.cpu_temp = "GetCPUTemperature"
        self.environmental_temp = "GetEnvTemperature"
        self.pressure = "GetPressure"
        self.humidity = "GetHumidity"
        self.lumen = "GetLumen"
        self.rgb = "GetRGB"
        self.accelerometer_xyz = "GetAccelerometerXYZ"
        self.magnetometer_xyz = "GetMagnetometerXYZ"
        self.gyroscope_xyz = "GetGyroscopeXYZ"


class CreateNetworkSendCommands:
    def __init__(self):
        self.restart_services = "RestartServices"
        self.shutdown_system = "ShutdownSystem"
        self.reboot_system = "RebootSystem"
        self.upgrade_system_os = "UpgradeSystemOS"
        self.upgrade_online = "UpgradeOnline"
        self.upgrade_smb = "UpgradeSMB"
        self.clean_upgrade_online = "CleanOnline"
        self.clean_upgrade_smb = "CleanSMB"
        self.set_host_name = "ChangeHostName"
        self.set_datetime = "SetDateTime"
        self.set_configuration = "SetConfiguration"


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


def request_new_name(ip):
    tmp_hostname = simpledialog.askstring(ip, "New Hostname: ")
    app_logger.sensor_logger.debug(tmp_hostname)

    if tmp_hostname is not None and tmp_hostname is not "":
        new_hostname = re.sub('\W', '_', tmp_hostname)
        app_logger.sensor_logger.debug(new_hostname)
        return new_hostname
    else:
        app_logger.sensor_logger.warning("Hostname Cancelled or blank")


def send_command(command_data):
    """ Socket connection to sensor IP. Sends provided text as command. """
    socket.setdefaulttimeout(command_data.net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((command_data.ip, 10065))
        sock_g.send(command_data.command.encode())
        app_logger.sensor_logger.info(command_data.command + " to " + command_data.ip + " - OK")
    except Exception as error:
        app_logger.sensor_logger.warning(command_data.command + " to " + command_data.ip + " - Failed: " + str(error))
    sock_g.close()


def get_data(command_data):
    """ Socket connection to sensor IP. Return sensor's data. """
    socket.setdefaulttimeout(command_data.net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((command_data.ip, 10065))
        sock_g.send(command_data.command.encode())
        var_data = pickle.loads(sock_g.recv(4096))
        sock_g.close()
        app_logger.sensor_logger.debug(command_data.command + " to " + command_data.ip + " - OK")
    except Exception as error:
        var_data = ""
        app_logger.sensor_logger.warning(command_data.command + " to " + command_data.ip + " - Failed: " + str(error))
    return var_data
