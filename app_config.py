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
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

script_directory = str(os.path.dirname(os.path.realpath(__file__)))

if not os.path.exists(os.path.dirname(script_directory + "/logs/")):
    os.makedirs(os.path.dirname(script_directory + "/logs/"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:  %(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = RotatingFileHandler(script_directory + '/logs/KootNet_log.txt', maxBytes=256000, backupCount=5)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

config_file = str(os.path.dirname(os.path.realpath(__file__))) + "/config.txt"


class CreateConfigSettings:
    """ Creates a object holding all the Control Centers default configuration options. """

    def __init__(self):
        self.save_to = str(os.path.expanduser('~/Desktop/')).replace('\\', '/')
        self.graph_start = "2018-09-12 00:00:01"
        self.graph_end = "2200-01-01 00:00:01"
        self.time_offset = "-7"
        self.sql_queries_skip = "3"
        self.temperature_offset = "-4"
        self.network_check_timeout = "2"
        self.network_details_timeout = "5"
        self.allow_power_controls = 0
        self.allow_reset_config = 0
        self.ip_list = ["192.168.10.11", "192.168.10.12", "192.168.10.13", "192.168.10.14",
                        "192.168.10.15", "192.168.10.16", "192.168.10.17", "192.168.10.18",
                        "192.168.10.19", "192.168.10.20", "192.168.10.21", "192.168.10.22",
                        "192.168.10.23", "192.168.10.24", "192.168.10.25", "192.168.10.26"]


def load_from_file():
    """ Loads the Control Center configurations from file and returns the settings. """
    config_settings = CreateConfigSettings()

    try:
        os.path.isfile(config_file)
        local_file = open(config_file, 'r')
        tmp_config_settings = local_file.read().split(',')
        local_file.close()

        config_settings.save_to = tmp_config_settings[0]
        config_settings.graph_start = tmp_config_settings[1]
        config_settings.graph_end = tmp_config_settings[2]
        config_settings.time_offset = tmp_config_settings[3]
        config_settings.sql_queries_skip = tmp_config_settings[4]
        config_settings.temperature_offset = tmp_config_settings[5]
        config_settings.network_check_timeout = tmp_config_settings[6]
        config_settings.network_details_timeout = tmp_config_settings[7]

        if int(tmp_config_settings[8]) >= 0:
            config_settings.allow_power_controls = int(tmp_config_settings[8])
        else:
            logger.error("Setting Enable Sensor Shutdown/Reboot - BAD - Using Default")

        if int(tmp_config_settings[9]) >= 0:
            config_settings.allow_reset_config = int(tmp_config_settings[9])
        else:
            logger.error("Setting Enable Config Reset - BAD - Using Default")

        count = 0
        while count < 16:
            try:
                tmp_setting_location = 10 + count
                config_settings.ip_list[count] = tmp_config_settings[tmp_setting_location]
                count = count + 1
            except Exception as error:
                logger.error("Unable to Load IP # - " + str(count) + " - " + str(error))
                count = count + 1

        logger.debug("Configuration File Load - OK")

    except Exception as error:
        logger.warning("Configuration File Load Failed - Using All or Some Defaults: " + str(error))

    return config_settings


def check_config(config_settings):
    """
    Checks the provided Control Center configuration for validity and returns it.

    Invalid options are replaced with defaults.
    """
    logger.debug("Checking Configuration Settings")
    default_settings = CreateConfigSettings()

    if os.path.isdir(config_settings.save_to):
        logger.debug("Setting Save to Folder - OK")
    else:
        logger.error("Setting Save to Folder - BAD - Using Default")
        config_settings.save_to = default_settings.save_to

    try:
        datetime.strptime(config_settings.graph_start, "%Y-%m-%d %H:%M:%S")
        logger.debug("Setting Graph Start Date Range - OK")
    except Exception as error:
        logger.error("Setting Graph Start Date Range - BAD - Using Default - " + str(error))
        config_settings.graph_start = default_settings.graph_start

    try:
        datetime.strptime(config_settings.graph_end, "%Y-%m-%d %H:%M:%S")
        logger.debug("Setting Graph End Date Range - OK")
    except Exception as error:
        logger.error("Setting Graph End Date Range - BAD - Using Default - " + str(error))
        config_settings.graph_end = default_settings.graph_end

    try:
        float(config_settings.time_offset)
        logger.debug("Setting DataBase Hours Offset - OK")
    except Exception as error:
        logger.error("Setting DataBase Hours Offset - BAD - Using Default: " + str(error))
        config_settings.time_offset = default_settings.time_offset

    try:
        int(config_settings.sql_queries_skip)
        logger.debug("Setting Skip SQL Queries - OK")
    except Exception as error:
        logger.error("Setting Skip SQL Queries - BAD - Using Default: " + str(error))
        config_settings.sql_queries_skip = default_settings.sql_queries_skip

    try:
        float(config_settings.temperature_offset)
        logger.debug("Setting Temperature Offset - OK")
    except Exception as error:
        logger.error("Setting Temperature Offset - BAD - Using Default: " + str(error))
        config_settings.temperature_offset = default_settings.temperature_offset

    try:
        int(config_settings.network_check_timeout)
        logger.debug("Setting Sensor Check Timeout - OK")
    except Exception as error:
        logger.error("Setting Sensor Check Timeout - BAD - Using Default: " + str(error))
        config_settings.network_check_timeout = default_settings.network_check_timeout

    try:
        int(config_settings.network_details_timeout)
        logger.debug("Setting Get Details Timeout - OK")
    except Exception as error:
        logger.error("Setting Get Details Timeout - BAD - Using Default: " + str(error))
        config_settings.network_details_timeout = default_settings.network_details_timeout

    try:
        if config_settings.allow_power_controls >= 0:
            logger.debug("Setting Enable Sensor Shutdown/Reboot - OK")
    except Exception as error:
        logger.error("Setting Enable Sensor Shutdown/Reboot - BAD - Using Default: " + str(error))
        config_settings.allow_power_controls = default_settings.allow_power_controls

    try:
        if config_settings.allow_reset_config >= 0:
            logger.debug("Setting Enable Config Reset - OK")
    except Exception as error:
        logger.error("Setting Enable Config Reset - BAD - Using Default: " + str(error))
        config_settings.allow_reset_config = default_settings.allow_reset_config

    count = 0
    while count < 16:
        if 6 < len(config_settings.ip_list[count]) < 16:
                count = count + 1
        else:
            logger.error("Setting IP List - BAD - Using Default: Bad IP #" + str(count))
            config_settings.ip_list[count] = default_settings.ip_list[count]
            count = count + 1

    return config_settings


def save_config_to_file(temp_config_settings):
    """ Saves provided Control Center configuration to file. """
    config_settings = check_config(temp_config_settings)

    var_final_write = str(config_settings.save_to)
    var_final_write = var_final_write + ',' + str(config_settings.graph_start)
    var_final_write = var_final_write + ',' + str(config_settings.graph_end)
    var_final_write = var_final_write + ',' + str(config_settings.time_offset)
    var_final_write = var_final_write + ',' + str(config_settings.sql_queries_skip)
    var_final_write = var_final_write + ',' + str(config_settings.temperature_offset)
    var_final_write = var_final_write + ',' + str(config_settings.network_check_timeout)
    var_final_write = var_final_write + ',' + str(config_settings.network_details_timeout)
    var_final_write = var_final_write + ',' + str(config_settings.allow_power_controls)
    var_final_write = var_final_write + ',' + str(config_settings.allow_reset_config)
    for ip in config_settings.ip_list:
        var_final_write = var_final_write + ',' + str(ip)

    try:
        local_file = open(config_file, 'w')
        local_file.write(var_final_write)
        local_file.close()
        logger.debug("Configuration Settings Save to File - OK")
    except Exception as error:
        logger.error("Configuration Settings Save to File - Failed: " + str(error))
