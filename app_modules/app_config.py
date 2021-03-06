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
import os.path
from sys import path
from datetime import datetime
from app_modules import app_logger
from app_guizero import platform_gui_tweaks


class CreateDefaultConfigSettings:
    """ Creates a object holding all the Control Centers default configuration options. """

    def __init__(self):
        # Sensor Server HTTP Authentication settings
        self.http_user = "Kootnet"
        self.http_password = "sensors"
        # Script location information
        self.script_directory = str(path[0]).replace("\\", "/")
        self.logs_directory = self.script_directory + "/logs"
        self.additional_files_directory = self.script_directory + "/additional_files"
        if platform_gui_tweaks.current_platform == "Linux":
            self.config_file = "/etc/kootnet/control_center.conf"
            self.config_folder = "/etc/kootnet/"
        else:
            self.config_file = self.script_directory + "/config.txt"
            self.config_folder = self.script_directory

        # Start of user configurable options
        if platform_gui_tweaks.current_platform == "Windows":
            self.save_to = str(os.path.expanduser('~/Documents/KootNetSensors/')).replace('\\', '/')
        else:
            self.save_to = str(os.path.expanduser('~/KootNetSensors/')).replace('\\', '/')

        self.enable_plotly_webgl = self.detect_plotly_render_type()

        self.graph_start = "2018-10-15 15:00:01"
        self.graph_end = "2200-01-01 00:00:01"
        self.datetime_offset = -7.0
        self.sql_queries_skip = 6
        self.enable_custom_temp_offset = True
        self.temperature_offset = 0.0
        self.live_refresh = 3
        self.network_timeout_sensor_check = 3
        self.network_timeout_data = 5
        self.allow_config_reset = 0
        self.ip_list = ["127.0.0.1", "192.168.10.11", "192.168.10.12", "192.168.10.13",
                        "192.168.10.14", "192.168.10.15", "192.168.10.16", "192.168.10.17",
                        "192.168.10.51", "192.168.10.52", "192.168.10.53", "192.168.10.54",
                        "192.168.10.55", "192.168.10.56", "192.168.10.57", "192.168.10.58"]

    def reset_to_defaults(self):
        """ Resets the User configurable options to a default state on object self. """
        default_config = CreateDefaultConfigSettings()

        self.save_to = default_config.save_to
        self.graph_start = default_config.graph_start
        self.graph_end = default_config.graph_end
        self.datetime_offset = default_config.datetime_offset
        self.sql_queries_skip = default_config.sql_queries_skip
        self.temperature_offset = default_config.temperature_offset
        self.live_refresh = default_config.live_refresh
        self.network_timeout_sensor_check = default_config.network_timeout_sensor_check
        self.network_timeout_data = default_config.network_timeout_data
        self.allow_config_reset = default_config.allow_config_reset
        self.ip_list = default_config.ip_list
        self.enable_plotly_webgl = self.detect_plotly_render_type()
        self.http_user = default_config.http_user
        self.http_password = default_config.http_password

    @staticmethod
    def get_str_datetime_now():
        """ Returns local computer time in YYYY-MM-DD HH:MM:SS. """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def detect_plotly_render_type():
        """ Checks supported system for OpenGL plotly rendering. Returns True if supported. """
        if platform_gui_tweaks.current_platform == "Linux":
            if platform_gui_tweaks.check_pi_model()[:12] == "Raspberry Pi":
                enable_plotly_webgl = False
            else:
                enable_plotly_webgl = True
        else:
            enable_plotly_webgl = True

        return enable_plotly_webgl


def get_from_file():
    """ Loads the Control Center configurations from file and returns the Verified settings. """
    config_settings = CreateDefaultConfigSettings()

    try:
        os.path.isfile(config_settings.config_file)
        local_file = open(config_settings.config_file, 'r')
        tmp_config_settings = local_file.read().split(',')
        local_file.close()

        config_settings.save_to = tmp_config_settings[0]
        config_settings.graph_start = tmp_config_settings[1]
        config_settings.graph_end = tmp_config_settings[2]
        config_settings.live_refresh = tmp_config_settings[3]
        config_settings.datetime_offset = tmp_config_settings[4]
        config_settings.sql_queries_skip = tmp_config_settings[5]
        config_settings.temperature_offset = tmp_config_settings[6]
        config_settings.live_refresh = tmp_config_settings[7]
        config_settings.network_timeout_sensor_check = tmp_config_settings[8]
        config_settings.network_timeout_data = tmp_config_settings[9]
        config_settings.allow_config_reset = int(tmp_config_settings[10])

        count = 0
        while count < 16:
            try:
                tmp_setting_location = 11 + count
                config_settings.ip_list[count] = tmp_config_settings[tmp_setting_location]
                count = count + 1
            except Exception as error:
                app_logger.app_logger.error("Unable to Load IP # - " + str(count) + " - " + str(error))
                count = count + 1

        config_settings.enable_plotly_webgl = tmp_config_settings[27]
        config_settings.http_user = tmp_config_settings[28]
        config_settings.http_password = tmp_config_settings[29]

        app_logger.app_logger.debug("Configuration File Load - OK")

    except Exception as error:
        app_logger.app_logger.warning("Configuration File Load Failed or Invalid Settings - Using Defaults")
        app_logger.app_logger.debug(str(error))

    check_config(config_settings)
    return config_settings


def check_config(config_settings):
    """
    Checks the provided Control Center configuration for validity and returns it.

    Invalid options are replaced with defaults.
    """
    bad_settings = False
    app_logger.app_logger.debug("Checking Configuration Settings")
    default_settings = CreateDefaultConfigSettings()

    if os.path.isdir(config_settings.save_to):
        app_logger.app_logger.debug("Setting Save to Folder - OK")
    else:
        app_logger.app_logger.error("Setting Save to Folder - BAD - Using Default")
        config_settings.save_to = default_settings.save_to
        bad_settings = True

    try:
        datetime.strptime(config_settings.graph_start, "%Y-%m-%d %H:%M:%S")
        app_logger.app_logger.debug("Setting Graph Start Date Range - OK")
    except Exception as error:
        app_logger.app_logger.error("Setting Graph Start Date Range - BAD - Using Default - " + str(error))
        config_settings.graph_start = default_settings.graph_start
        bad_settings = True

    try:
        datetime.strptime(config_settings.graph_end, "%Y-%m-%d %H:%M:%S")
        app_logger.app_logger.debug("Setting Graph End Date Range - OK")
    except Exception as error:
        app_logger.app_logger.error("Setting Graph End Date Range - BAD - Using Default - " + str(error))
        config_settings.graph_end = default_settings.graph_end
        bad_settings = True

    try:
        config_settings.live_refresh = int(config_settings.live_refresh)
        app_logger.app_logger.debug("Setting Graph End Date Range - OK")
    except Exception as error:
        app_logger.app_logger.error("Setting Graph End Date Range - BAD - Using Default - " + str(error))
        config_settings.live_refresh = default_settings.live_refresh
        bad_settings = True

    try:
        config_settings.datetime_offset = float(config_settings.datetime_offset)
        app_logger.app_logger.debug("Setting DataBase Hours Offset - OK")
    except Exception as error:
        app_logger.app_logger.error("Setting DataBase Hours Offset - BAD - Using Default: " + str(error))
        config_settings.datetime_offset = default_settings.datetime_offset
        bad_settings = True

    try:
        config_settings.sql_queries_skip = int(config_settings.sql_queries_skip)
        app_logger.app_logger.debug("Setting Skip SQL Queries - OK")
    except Exception as error:
        app_logger.app_logger.error("Setting Skip SQL Queries - BAD - Using Default: " + str(error))
        config_settings.sql_queries_skip = default_settings.sql_queries_skip
        bad_settings = True

    try:
        config_settings.temperature_offset = float(config_settings.temperature_offset)
        app_logger.app_logger.debug("Setting Temperature Offset - OK")
    except Exception as error:
        app_logger.app_logger.error("Setting Temperature Offset - BAD - Using Default: " + str(error))
        config_settings.temperature_offset = default_settings.temperature_offset
        bad_settings = True

    try:
        config_settings.live_refresh = int(config_settings.live_refresh)
        app_logger.app_logger.debug("Setting Live Refresh - OK")
    except Exception as error:
        app_logger.app_logger.error("Setting Live Refresh - BAD - Using Default: " + str(error))
        config_settings.live_refresh = default_settings.live_refresh
        bad_settings = True

    try:
        config_settings.network_timeout_sensor_check = int(config_settings.network_timeout_sensor_check)
        app_logger.app_logger.debug("Setting Sensor Check Timeout - OK")
    except Exception as error:
        app_logger.app_logger.error("Setting Sensor Check Timeout - BAD - Using Default: " + str(error))
        config_settings.network_timeout_sensor_check = default_settings.network_timeout_sensor_check
        bad_settings = True

    try:
        config_settings.network_timeout_data = int(config_settings.network_timeout_data)
        app_logger.app_logger.debug("Setting Get Details Timeout - OK")
    except Exception as error:
        app_logger.app_logger.error("Setting Get Details Timeout - BAD - Using Default: " + str(error))
        config_settings.network_timeout_data = default_settings.network_timeout_data
        bad_settings = True

    try:
        config_settings.allow_config_reset = int(config_settings.allow_config_reset)
        if 2 > config_settings.allow_config_reset >= 0:
            app_logger.app_logger.debug("Setting Enable Sensor Shutdown/Reboot - OK")
    except Exception as error:
        app_logger.app_logger.error("Setting Enable Sensor Shutdown/Reboot - BAD - Using Default: " + str(error))
        config_settings.allow_config_reset = default_settings.allow_config_reset
        bad_settings = True

    try:
        config_settings.enable_plotly_webgl = int(config_settings.enable_plotly_webgl)
        app_logger.app_logger.debug("Setting Enable Plotly WebGL - OK")
    except Exception as error:
        app_logger.app_logger.error("Setting Enable Plotly WebGL - BAD - Using Default: " + str(error))
        config_settings.enable_plotly_webgl = config_settings.detect_plotly_render_type()
        bad_settings = True

    try:
        config_settings.http_user = config_settings.http_user.strip()
        app_logger.app_logger.debug("Setting HTTP User - OK")
    except Exception as error:
        app_logger.app_logger.error("Setting HTTP User - BAD - Using Default: " + str(error))
        config_settings.http_user = default_settings.http_user
        bad_settings = True

    try:
        config_settings.http_password = config_settings.http_password.strip()
        app_logger.app_logger.debug("Setting HTTP Password - OK")
    except Exception as error:
        app_logger.app_logger.error("Setting HTTP Password - BAD - Using Default: " + str(error))
        config_settings.http_password = default_settings.http_password
        bad_settings = True

    if bad_settings:
        app_logger.app_logger.warning("One or more invalid settings have been reset to default and saved")
        save_config_to_file(config_settings)


def save_config_to_file(config_settings):
    """ Saves provided Control Center configuration to file. """
    check_config(config_settings)

    var_final_write = str(config_settings.save_to)
    var_final_write = var_final_write + "," + str(config_settings.graph_start)
    var_final_write = var_final_write + "," + str(config_settings.graph_end)
    var_final_write = var_final_write + "," + str(config_settings.live_refresh)
    var_final_write = var_final_write + "," + str(config_settings.datetime_offset)
    var_final_write = var_final_write + "," + str(config_settings.sql_queries_skip)
    var_final_write = var_final_write + "," + str(config_settings.temperature_offset)
    var_final_write = var_final_write + "," + str(config_settings.live_refresh)
    var_final_write = var_final_write + "," + str(config_settings.network_timeout_sensor_check)
    var_final_write = var_final_write + "," + str(config_settings.network_timeout_data)
    var_final_write = var_final_write + "," + str(config_settings.allow_config_reset)
    for ip in config_settings.ip_list:
        var_final_write = var_final_write + "," + str(ip)

    var_final_write = var_final_write + "," + str(config_settings.enable_plotly_webgl)
    var_final_write = var_final_write + "," + str(config_settings.http_user)
    var_final_write = var_final_write + "," + str(config_settings.http_password)

    try:
        local_file = open(config_settings.config_file, "w")
        local_file.write(var_final_write)
        local_file.close()
        app_logger.app_logger.debug("Configuration Settings Save to File - OK")
    except Exception as error:
        app_logger.app_logger.error("Configuration Settings Save to File - Failed: " + str(error))
