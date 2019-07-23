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
import webbrowser
import requests
from app_modules import app_logger
from app_modules import app_variables


class CreateSensorNetworkCommand:
    """ Creates object instance of variables needed for network commands. """
    def __init__(self, ip, network_timeout, command):
        self.ip = ip
        self.port = "10065"
        self.network_timeout = network_timeout
        self.command = command
        self.command_data = ""
        self.save_to_location = "/home/pi/"

    def check_for_port_in_ip(self):
        ip_list = self.ip.split(":")
        if len(ip_list) > 1:
            self.ip = ip_list[0]
            self.port = ip_list[1]


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


def download_sensor_database(address_and_port):
    """ Returns requested sensor file (based on the provided command data). """
    network_commands = app_variables.CreateNetworkGetCommands()
    url = "http://" + address_and_port + "/" + network_commands.sensor_sql_database

    try:
        webbrowser.open_new_tab(url)
    except Exception as error:
        app_logger.sensor_logger.warning("Download Sensor SQL Database Failed on " + str(address_and_port))
        app_logger.sensor_logger.debug(str(error))


def download_logs(sensor_command):
    """ Download 3 log files. """
    sensor_get_commands = app_variables.CreateNetworkGetCommands()

    sensor_command.command = sensor_get_commands.download_primary_log
    _get_logs(sensor_command, "PrimaryLog.txt")

    sensor_command.command = sensor_get_commands.download_network_log
    _get_logs(sensor_command, "NetworkLog.txt")

    sensor_command.command = sensor_get_commands.download_sensors_log
    _get_logs(sensor_command, "SensorsLog.txt")


def _get_logs(sensor_command, log_name):
    """ Download and save specified log file with given name. """
    log_file_data = get_data(sensor_command)
    log_file_location = sensor_command.save_to_location + "/" + sensor_command.ip[-3:].replace(".", "_") + log_name

    try:
        log_file = open(log_file_location, "w")
        log_file.write(log_file_data)
        log_file.close()
    except Exception as error:
        app_logger.sensor_logger.error("Log Save Failed: " + str(error))


def get_validated_hostname(hostname):
    """ Return validated hostname. """
    if hostname is not None and hostname is not "":
        final_hostname = re.sub("[^A-Za-z0-9_]", "_", hostname)
        app_logger.sensor_logger.debug(final_hostname)
        return final_hostname
    else:
        app_logger.sensor_logger.warning("Hostname Cancelled or blank")
        return "Cancelled"


def send_command(sensor_command):
    """ Sends command to sensor (based on provided command data). """
    sensor_command.check_for_port_in_ip()
    url = "http://" + sensor_command.ip + ":" + sensor_command.port + "/" + sensor_command.command

    try:
        requests.get(url=url, timeout=sensor_command.network_timeout, headers={'Connection': 'close'})
        app_logger.sensor_logger.debug(sensor_command.command + " to " + sensor_command.ip + " - OK")
    except Exception as error:
        app_logger.sensor_logger.debug(str(error))


def put_command(sensor_command):
    """ Sends command to sensor (based on provided command data). """
    sensor_command.check_for_port_in_ip()
    url = "http://" + sensor_command.ip + ":" + sensor_command.port + "/" + sensor_command.command

    try:
        requests.put(url=url, timeout=sensor_command.network_timeout, data={'command_data': sensor_command.command_data})
        app_logger.sensor_logger.info(sensor_command.command + " to " + sensor_command.ip + " - OK")
    except Exception as error:
        app_logger.sensor_logger.debug(str(error))


def get_data(sensor_command):
    """ Returns requested sensor data (based on the provided command data). """
    sensor_command.check_for_port_in_ip()
    url = "http://" + sensor_command.ip + ":" + sensor_command.port + "/" + sensor_command.command

    try:
        tmp_return_data = requests.get(url=url, timeout=sensor_command.network_timeout)
        app_logger.sensor_logger.debug(sensor_command.command + " to " + sensor_command.ip + " - OK")
        return_data = tmp_return_data.text
    except Exception as error:
        return_data = "Sensor Offline"
        if sensor_command.command == "CheckOnlineStatus":
            app_logger.sensor_logger.warning("Sensor " + str(sensor_command.ip) + " Offline")
        else:
            app_logger.sensor_logger.warning("Sensor " + str(sensor_command.ip) + " Error")
        app_logger.sensor_logger.debug(str(error))
    return return_data
