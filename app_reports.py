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
import app_sensor_commands
import webbrowser
import os
import logging
import app_config
from logging.handlers import RotatingFileHandler

script_directory = str(os.path.dirname(os.path.realpath(__file__))).replace("\\", "/")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:  %(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = RotatingFileHandler(script_directory + '/logs/KootNet_log.txt', maxBytes=256000, backupCount=5)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class HTMLSystem:
    def __init__(self):
        self.config_settings = app_config.get_from_file()
        self.template1 = script_directory + "/additional_files/html_template_system1.html"
        self.template2 = script_directory + "/additional_files/html_template_system2.html"
        self.template3 = script_directory + "/additional_files/html_template_system3.html"
        self.file_output_name = "SensorsSystemReport.html"

        self.replacement_codes = ["{{HostName}}",
                                  "{{IP}}",
                                  "{{DateTime}}",
                                  "{{UpTime}}",
                                  "{{CPUTemp}}",
                                  "{{FreeDisk}}",
                                  "{{IntervalSize}}",
                                  "{{TriggerSize}}",
                                  "{{SQLWriteEnabled}}",
                                  "{{CustomEnabled}}"]

    def get_sensor_data(self, ip):
        sensor_data = app_sensor_commands.get_sensor_system(ip, self.config_settings.network_timeout_data)
        # Convert the sensor's system uptime of minutes to human readable day/hour.min
        sensor_data[3] = _convert_minutes_string(sensor_data[3])

        return sensor_data


class HTMLReadings:
    def __init__(self):
        self.config_settings = app_config.get_from_file()
        self.template1 = script_directory + "/additional_files/html_template_readings1.html"
        self.template2 = script_directory + "/additional_files/html_template_readings2.html"
        self.template3 = script_directory + "/additional_files/html_template_readings3.html"
        self.file_output_name = "SensorsReadingsReport.html"

        self.replacement_codes = ["{{IntervalTypes}}",
                                  "{{IntervalReadings}}",
                                  "{{TriggerTypes}}",
                                  "{{TriggerReadings}}"]

    def get_sensor_data(self, ip):
        sensor_data = app_sensor_commands.get_sensor_readings(ip, self.config_settings.network_timeout_data)

        return sensor_data


class HTMLConfig:
    def __init__(self):
        self.config_settings = app_config.get_from_file()
        self.template1 = script_directory + "/additional_files/html_template_config1.html"
        self.template2 = script_directory + "/additional_files/html_template_config2.html"
        self.template3 = script_directory + "/additional_files/html_template_config3.html"
        self.file_output_name = "SensorsConfigReport.html"

        self.replacement_codes = ["{{HostName}}",
                                  "{{IP}}",
                                  "{{DateTime}}",
                                  "{{IntervalDuration}}",
                                  "{{TriggerDuration}}",
                                  "{{SQLWriteEnabled}}",
                                  "{{CustomEnabled}}",
                                  "{{CustomAcc}}",
                                  "{{CustomMag}}",
                                  "{{CustomGyro}}"]

    def get_sensor_data(self, ip):
        sensor_data = app_sensor_commands.get_sensor_config(ip, self.config_settings.network_timeout_data)

        return sensor_data


def sensor_html_report(report_configuration, ip_list):
    """ Creates and opens a HTML Report based on provided IP's and report configurations data. """
    final_file = _get_file_content(report_configuration.template1)
    sensor_html_template = _get_file_content(report_configuration.template2)

    # Add first HTML Template file to final HTML output file
    # Insert each sensors data into final HTML output file through the 2nd template & replacement codes
    for ip in ip_list:
        try:
            current_sensor_html = sensor_html_template
            sensor_data = report_configuration.get_sensor_data(ip)

            current_sensor_html = _replace_with_codes(sensor_data,
                                                      report_configuration.replacement_codes,
                                                      current_sensor_html)

            final_file = final_file + current_sensor_html
        except Exception as error:
                logger.error("Report Failure: " + str(error))

    # Merge the result with the Final HTML Template file.
    template3 = _get_file_content(report_configuration.template3)
    final_file = final_file + template3

    try:
        save_to_location = str(report_configuration.config_settings.save_to + report_configuration.file_output_name)
        _save_data_to_file(final_file, save_to_location)
        _open_html(save_to_location)
        logger.debug("Sensor Report - HTML Save File - OK")
    except Exception as error:
        logger.error("Sensor Report - HTML Save File - Failed: " + str(error))


def _get_file_content(file_location):
    try:
        tmp_file = open(file_location, "r")
        file_content = tmp_file.read()
        tmp_file.close()
    except Exception as error:
        logger.error("Unable to get file contents: " + str(error))
        file_content = "Unable to get file contents: " + str(error)

    return file_content


def _convert_minutes_string(var_minutes):
    try:
        uptime_days = int(float(var_minutes) // 1440)
        uptime_hours = int((float(var_minutes) % 1440) // 60)
        uptime_min = int(float(var_minutes) % 60)
        str_day_hour_min = str(uptime_days) + " Days / " + str(uptime_hours) + "." + str(uptime_min) + " Hours"
    except Exception as error:
        logger.error("Unable to convert Minutes to days/hours.min: " + str(error))
        str_day_hour_min = var_minutes

    return str_day_hour_min


def _replace_with_codes(data, codes, template):
    count = 0
    for code in codes:
        try:
            replace_word = str(data[count])
        except Exception as error:
            replace_word = "No Data"
            logger.error("Invalid Sensor Data: " + str(error))

        template = template.replace(code, replace_word)
        count = count + 1

    return template


def _save_data_to_file(data, file_location):
    try:
        file_out = open(file_location, "w")
        file_out.write(data)
        file_out.close()
    except Exception as error:
        logger.error("Unable to save file: " + str(error))


def _open_html(outfile):
    """ Opens a HTML file in the default web browser. """
    try:
        webbrowser.open_new_tab("file:///" + outfile)
        logger.debug("Graph HTML File Opened - OK")
    except Exception as error:
        logger.error("Graph HTML File Opened - Failed - " + str(error))
