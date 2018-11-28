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
import re
from shutil import copyfileobj

import requests

import app_logger


class CreateSensorNetworkCommand:
    def __init__(self, ip, network_timeout, command):
        self.ip = ip
        self.network_timeout = network_timeout
        self.command = command
        self.command_data = ""
        self.save_to_location = "/home/pi/"


class CreateNetworkGetCommands:
    def __init__(self):
        self.sensor_sql_database = "DownloadSQLDatabase"
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
        self.env_temp_offset = "GetTempOffsetEnv"
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
        self.set_host_name = "SetHostName"
        self.set_datetime = "SetDateTime"
        self.set_configuration = "SetConfiguration"
        self.put_sql_note = "PutDatabaseNote"


def check_sensor_status(ip, network_timeout):
    """ Socket connection to sensor IP. Return sensor status. """
    sensor_command = CreateSensorNetworkCommand(ip, network_timeout, "CheckOnlineStatus")
    sensor_status_check = get_data(sensor_command)

    if sensor_status_check == "OK":
        sensor_status = "Online"
    else:
        sensor_status = "Offline"

    app_logger.sensor_logger.debug("IP: " + str(ip) + sensor_status)
    return sensor_status


def download_logs(sensor_command):
    """ Download 3 log files. """
    sensor_command.command = "DownloadPrimaryLog"

    log_file_data = get_data(sensor_command)
    try:
        log_file = open(sensor_command.save_to_location + "/_" + sensor_command.ip[-3:] + "PrimaryLog.txt", "w")
        log_file.write(log_file_data)
        log_file.close()
    except Exception as error:
        print(error)

    sensor_command.command = "DownloadNetworkLog"
    log_file_data = get_data(sensor_command)
    try:
        log_file = open(sensor_command.save_to_location + "/_" + sensor_command.ip[-3:] + "NetworkLog.txt", "w")
        log_file.write(log_file_data)
        log_file.close()
    except Exception as error:
        print(error)

    sensor_command.command = "DownloadSensorsLog"
    log_file_data = get_data(sensor_command)
    try:
        log_file = open(sensor_command.save_to_location + "/_" + sensor_command.ip[-3:] + "SensorsLog.txt", "w")
        log_file.write(log_file_data)
        log_file.close()
    except Exception as error:
        print(error)


def get_validated_hostname(hostname):
    if hostname is not None and hostname is not "":
        final_hostname = re.sub('\W', '_', hostname)
        app_logger.sensor_logger.debug(final_hostname)
        return final_hostname
    else:
        app_logger.sensor_logger.warning("Hostname Cancelled or blank")
        return "Cancelled"


def send_command(sensor_command):
    """ Sends command to sensor (based on provided command data). """
    url = "http://" + sensor_command.ip + ":10065/" + sensor_command.command

    try:
        requests.get(url, timeout=sensor_command.network_timeout, headers={'Connection': 'close'})
        app_logger.sensor_logger.debug(sensor_command.command + " to " + sensor_command.ip + " - OK")
    except Exception as error:
        if sensor_command.command != "RestartServices":
            app_logger.sensor_logger.warning(sensor_command.command + " to " + sensor_command.ip + " - Failed")
            app_logger.sensor_logger.debug(str(error))


def put_command(sensor_command):
    """ Sends command to sensor (based on provided command data). """
    url = "http://" + sensor_command.ip + ":10065/" + sensor_command.command

    try:
        requests.put(url, timeout=sensor_command.network_timeout, data={'command_data': sensor_command.command_data})
        app_logger.sensor_logger.debug(sensor_command.command + " to " + sensor_command.ip + " - OK")
    except Exception as error:
        app_logger.sensor_logger.warning(sensor_command.command + " to " + sensor_command.ip + " - Failed")
        app_logger.sensor_logger.debug(str(error))


def get_data(sensor_command):
    """ Returns requested sensor data (based on the provided command data). """
    url = "http://" + sensor_command.ip + ":10065/" + sensor_command.command

    try:
        tmp_return_data = requests.get(url, timeout=sensor_command.network_timeout)
        app_logger.sensor_logger.debug(sensor_command.command + " to " + sensor_command.ip + " - OK")
        return_data = tmp_return_data.text
    except Exception as error:
        return_data = "Sensor Offline"
        app_logger.sensor_logger.warning(sensor_command.command + " to " + sensor_command.ip + " - Failed")
        app_logger.sensor_logger.debug(str(error))

    return return_data


# Edit this for downloading Logs and SQL
def download_sensor_database(sensor_command):
    """ Returns requested sensor file (based on the provided command data). """
    url = "http://" + sensor_command.ip + ":10065/" + sensor_command.command

    try:
        return_data = requests.get(url, timeout=sensor_command.network_timeout, stream=True)
        app_logger.sensor_logger.debug(sensor_command.command + " to " + sensor_command.ip + " - OK")
        sensor_database = open(sensor_command.save_to_location + "/" +
                               sensor_command.ip[-3:] + "SensorRecordingDatabase" +
                               ".sqlite", "wb")
        copyfileobj(return_data.raw, sensor_database)
        sensor_database.close()
    except Exception as error:
        app_logger.sensor_logger.warning(sensor_command.command + " to " + sensor_command.ip + " - Failed")
        app_logger.sensor_logger.debug(str(error))
