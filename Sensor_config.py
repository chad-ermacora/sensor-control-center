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
import os
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:  %(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = RotatingFileHandler('logs/Sensor_config_log.txt', maxBytes=256000, backupCount=5)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

app_location_directory = str(os.path.dirname(sys.argv[0])) + "/"
config_file = app_location_directory + "config.txt"


class CreateConfigSettings:

    def __init__(self):
        save_to = str(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\'))
        self.save_to = save_to.replace('\\', '/')
        self.graph_start = "2018-08-21 00:00:01"
        self.graph_end = "2200-01-01 00:00:01"
        self.time_offset = "-7"
        self.sql_queries_skip = "12"
        self.temperature_offset = "-4"
        self.network_check_timeout = "2"
        self.network_details_timeout = "5"
        self.allow_power_controls = 0
        self.allow_reset_config = 0


def load_file():
    config_settings = ConfigSettings()

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

        logger.debug("Configuration File Load - OK")
        return config_settings

    except Exception as error:
        logger.warning("Configuration File Load Failed - Using All or Some Defaults: " + str(error) + " - ")
        return config_settings


def check_settings(config_settings):
    logger.debug("Checking Configuration Settings")
    default_settings = ConfigSettings()

    if os.path.isdir(config_settings.save_to):
        logger.debug("Setting Save to Folder - OK")
    else:
        logger.error("Setting Save to Folder - BAD - Using Default")
        config_settings.save_to = default_settings.save_to

    if len(config_settings.graph_start) == 19:
        logger.debug("Setting Graph Start Date Range - OK")
    else:
        logger.error("Setting Graph Start Date Range - BAD - Using Default")
        config_settings = default_settings

    if len(config_settings.graph_end) == 19:
        logger.debug("Setting Graph End Date Range - OK")
    else:
        logger.error("Setting Graph End Date Range - BAD - Using Default")
        config_settings.graph_end = default_settings.graph_end

    try:
        float(config_settings.time_offset)
        logger.debug("Setting DataBase Hours Offset - OK")
    except Exception as error:
        logger.error("Setting DataBase Hours Offset - BAD - Using Default" + str(error) + " - ")
        config_settings.time_offset = default_settings.time_offset

    try:
        int(config_settings.sql_queries_skip)
        logger.debug("Setting Skip SQL Queries - OK")
    except Exception as error:
        logger.error("Setting Skip SQL Queries - BAD - Using Default" + str(error) + " - ")
        config_settings.sql_queries_skip = default_settings.sql_queries_skip

    try:
        float(config_settings.temperature_offset)
        logger.debug("Setting Temperature Offset - OK")
    except Exception as error:
        logger.error("Setting Temperature Offset - BAD - Using Default" + str(error) + " - ")
        config_settings.temperature_offset = default_settings.temperature_offset

    try:
        int(config_settings.network_check_timeout)
        logger.debug("Setting Sensor Check Timeout - OK")
    except Exception as error:
        logger.error("Setting Sensor Check Timeout - BAD - Using Default" + str(error) + " - ")
        config_settings.network_check_timeout = default_settings.network_check_timeout

    try:
        int(config_settings.network_details_timeout)
        logger.debug("Setting Get Details Timeout - OK")
    except Exception as error:
        logger.error("Setting Get Details Timeout - BAD - Using Default" + str(error) + " - ")
        config_settings.network_details_timeout = default_settings.network_details_timeout

    try:
        if config_settings.allow_power_controls >= 0:
            logger.debug("Setting Enable Sensor Shutdown/Reboot - OK")
    except Exception as error:
        logger.error("Setting Enable Sensor Shutdown/Reboot - BAD - Using Default" + str(error) + " - ")
        config_settings.allow_power_controls = default_settings.allow_power_controls

    try:
        if config_settings.allow_reset_config >= 0:
            logger.debug("Setting Enable Config Reset - OK")
    except Exception as error:
        logger.error("Setting Enable Config Reset - BAD - Using Default" + str(error) + " - ")
        config_settings.allow_reset_config = default_settings.allow_reset_config

    return config_settings


def save_file(temp_config_settings):
    config_settings = check_settings(temp_config_settings)

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

    try:
        local_file = open(config_file, 'w')
        local_file.write(var_final_write)
        local_file.close()
        logger.debug("Configuration Settings Save to File - OK")
    except Exception as error:
        logger.error("Configuration Settings Save to File - Failed: " + str(error) + " - ")
