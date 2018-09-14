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


def get_defaults():
    logger.debug("Getting Default Configuration Variables")
    save_to = str(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\'))
    save_to = save_to.replace('\\', '/')
    graph_start = "2018-08-21 00:00:01"
    graph_end = "2200-01-01 00:00:01"
    time_offset = "-7"
    sql_queries_skip = "12"
    temperature_offset = "-4"
    network_check_timeout = "2"
    network_details_timeout = "5"
    allow_power_controls = "0"
    allow_reset_config = "0"

    default_settings = [save_to,
                        graph_start,
                        graph_end,
                        time_offset,
                        sql_queries_skip,
                        temperature_offset,
                        network_check_timeout,
                        network_details_timeout,
                        allow_power_controls,
                        allow_reset_config]

    return default_settings


def load_file():
    try:
        os.path.isfile(config_file)
        local_file = open(config_file, 'r')
        config_settings = local_file.read().split(',')
        count = 0

        for config_option in config_settings:
            # First Import doesn't have the extra space
            if count == 0:
                config_settings[count] = config_option[1:-1]
            else:
                config_settings[count] = config_option[2:-1]
            count = count + 1

        local_file.close()
        logger.info("Configuration File Load - OK")
        return config_settings

    except Exception as error:
        logger.warning("Configuration File Load Failed - Using Defaults: " + str(error))
        return get_defaults()


def check_settings(config_settings):
    logger.info("Checking Configuration Settings")
    checked_settings = []

    save_to_default, \
        graph_start_default, \
        graph_end_default, \
        time_offset_default, \
        sql_queries_skip_default, \
        temperature_offset_default, \
        network_check_timeout_default, \
        network_details_timeout_default, \
        allow_power_controls_default, \
        allow_reset_config_default = get_defaults()

    save_to, \
        graph_start, \
        graph_end, \
        time_offset, \
        sql_queries_skip, \
        temperature_offset, \
        network_check_timeout, \
        network_details_timeout, \
        allow_power_controls, \
        allow_reset_config = config_settings

    if os.path.isdir(save_to):
        checked_settings.append(str(save_to))
    else:
        logger.error("Bad Setting - Save to Folder - Using Default")
        checked_settings.append(str(save_to_default))

    if len(graph_start) == 19:
        checked_settings.append(str(graph_start))
    else:
        logger.error("Bad Setting - Graph Start Date Range - Using Default")
        checked_settings.append(str(graph_start_default))

    if len(graph_end) == 19:
        checked_settings.append(str(graph_end))
    else:
        logger.error("Bad Setting - Graph End Date Range - Using Default")
        checked_settings.append(str(graph_end_default))

    try:
        float(time_offset)
        checked_settings.append(str(time_offset))
    except Exception as error:
        logger.error("Bad Setting - DataBase Hours Offset - Using Default: " + str(error))
        checked_settings.append(str(time_offset_default))

    try:
        int(sql_queries_skip)
        checked_settings.append(str(sql_queries_skip))
    except Exception as error:
        logger.error("Bad Setting - Skip SQL Queries - Using Default: " + str(error))
        checked_settings.append(str(sql_queries_skip_default))

    try:
        float(temperature_offset)
        checked_settings.append(str(temperature_offset))
    except Exception as error:
        logger.error("Bad Setting - Temperature Offset - Using Default: " + str(error))
        checked_settings.append(str(temperature_offset_default))

    try:
        int(network_check_timeout)
        checked_settings.append(str(network_check_timeout))
    except Exception as error:
        logger.error("Bad Setting - Sensor Check Timeout - Using Default: " + str(error))
        checked_settings.append(str(network_check_timeout_default))

    try:
        int(network_details_timeout)
        checked_settings.append(str(network_details_timeout))
    except Exception as error:
        logger.error("Bad Setting - Get Details Timeout - Using Default: " + str(error))
        checked_settings.append(str(network_details_timeout_default))

    try:
        allow_power_controls = str(allow_power_controls)
        int(allow_power_controls)
        checked_settings.append(int(allow_power_controls))
    except Exception as error:
        logger.error("Bad Setting - Enable Sensor Shutdown/Reboot - Using Defaults: " + str(error))
        checked_settings.append(int(allow_power_controls_default))

    try:
        allow_reset_config = str(allow_reset_config)
        int(allow_reset_config)
        checked_settings.append(int(allow_reset_config))
    except Exception as error:
        logger.error("Bad Setting - Enable Config Reset - Using Default: " + str(error))
        checked_settings.append(int(allow_reset_config_default))

    return checked_settings


def save_file(var_settings):
    var_settings[8] = str(var_settings[8])
    var_settings[9] = str(var_settings[9])
    var_final_write = str(var_settings)[1:-1]

    try:
        local_file = open(config_file, 'w')
        local_file.write(var_final_write)
        local_file.close()
        logger.info("Settings Save - OK")
    except Exception as error:
        logger.error("Settings Save - Failed: " + str(error))
