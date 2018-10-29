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
import webbrowser
from queue import Queue
from threading import Thread
from time import strftime

import app_config
import app_logger
import app_sensor_commands
from app_useful import convert_minutes_string

script_directory = app_config.script_directory
data_queue = Queue()


class HTMLSystem:
    def __init__(self, current_config):
        self.config_settings = current_config
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
                                  "{{CustomEnabled}}",
                                  "{{Version}}",
                                  "{{LastUpdated}}"]

        self.local_time_code = ["{{LocalDateTime}}"]

    def get_sensor_data(self, ip):
        command_data = app_sensor_commands.CreateCommandData(ip, self.config_settings.network_timeout_data,
                                                             "GetSystemData")
        sensor_system = app_sensor_commands.get_data(command_data).split(",")
        sensor_system[3] = convert_minutes_string(sensor_system[3])

        data_queue.put([ip, sensor_system])


class HTMLReadings:
    def __init__(self, current_config):
        self.config_settings = current_config
        self.template1 = script_directory + "/additional_files/html_template_readings1.html"
        self.template2 = script_directory + "/additional_files/html_template_readings2.html"
        self.template3 = script_directory + "/additional_files/html_template_readings3.html"
        self.file_output_name = "SensorsReadingsReport.html"

        self.replacement_codes = ["{{IntervalTypes}}",
                                  "{{IntervalReadings}}",
                                  "{{TriggerTypes}}",
                                  "{{TriggerReadings}}"]

        self.local_time_code = ["{{LocalDateTime}}"]

    def get_sensor_data(self, ip):
        command_data = app_sensor_commands.CreateCommandData(ip,
                                                             self.config_settings.network_timeout_data,
                                                             "GetSensorReadings")
        sensor_data = app_sensor_commands.get_data(command_data)
        data_queue.put([ip, sensor_data])


class HTMLConfig:
    def __init__(self, current_config):
        self.config_settings = current_config
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

        self.local_time_code = ["{{LocalDateTime}}"]

    def get_sensor_data(self, ip):
        command_data = app_sensor_commands.CreateCommandData(ip,
                                                             self.config_settings.network_timeout_data,
                                                             "GetSystemData")
        sensor_system = app_sensor_commands.get_data(command_data).split(",")
        sensor_system[3] = convert_minutes_string(sensor_system[3])

        command_data.command = "GetConfiguration"
        sensor_config = app_sensor_commands.get_data(command_data).split(",")

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
        data_queue.put([ip, final_sensor_config])


def sensor_html_report(report_configuration, ip_list):
    """ Creates and opens a HTML Report based on provided IP's and report configurations data. """
    final_file = _get_file_content(report_configuration.template1)
    sensor_html_template = _get_file_content(report_configuration.template2)

    # Add first HTML Template file to final HTML output file
    # Insert each sensors data into final HTML output file through the 2nd template & replacement codes
    report_data_pool = []
    threads = []

    for ip in ip_list:
        threads.append(Thread(target=report_configuration.get_sensor_data, args=[ip]))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    while not data_queue.empty():
        report_data_pool.append(data_queue.get())
        data_queue.task_done()

    report_data_pool.sort()

    for sensor_data in report_data_pool:
        try:
            current_sensor_html = sensor_html_template

            current_sensor_html = _replace_with_codes(sensor_data[1],
                                                      report_configuration.replacement_codes,
                                                      current_sensor_html)

            final_file = final_file + current_sensor_html
        except Exception as error:
            app_logger.app_logger.error("Report Failure: " + str(error))

    # Merge the result with the Final HTML Template file.
    current_datetime = strftime("%Y-%m-%d %H:%M - %Z")
    template3 = _get_file_content(report_configuration.template3)
    # Add Local computer's DateTime to 3rd template
    template3 = _replace_with_codes([current_datetime],
                                    report_configuration.local_time_code,
                                    template3)
    final_file = final_file + template3

    try:
        save_to_location = str(report_configuration.config_settings.save_to + report_configuration.file_output_name)
        _save_data_to_file(final_file, save_to_location)
        _open_html(save_to_location)
        app_logger.app_logger.debug("Sensor Report - HTML Save File - OK")
    except Exception as error:
        app_logger.app_logger.error("Sensor Report - HTML Save File - Failed: " + str(error))


def _get_file_content(file_location):
    try:
        tmp_file = open(file_location, "r")
        file_content = tmp_file.read()
        tmp_file.close()
    except Exception as error:
        app_logger.app_logger.error("Unable to get file contents: " + str(error))
        file_content = "Unable to get file contents: " + str(error)

    return file_content


def _replace_with_codes(data, codes, template):
    count = 0
    for code in codes:
        try:
            replace_word = str(data[count])
        except Exception as error:
            replace_word = "No Data"
            app_logger.app_logger.error("Invalid Sensor Data: " + str(error))

        template = template.replace(code, replace_word)
        count = count + 1

    return template


def _save_data_to_file(data, file_location):
    try:
        file_out = open(file_location, "w")
        file_out.write(data)
        file_out.close()
    except Exception as error:
        app_logger.app_logger.error("Unable to save file: " + str(error))


def _open_html(outfile):
    """ Opens a HTML file in the default web browser. """
    try:
        webbrowser.open_new_tab("file:///" + outfile)
        app_logger.app_logger.debug("Graph HTML File Opened - OK")
    except Exception as error:
        app_logger.app_logger.error("Graph HTML File Opened - Failed - " + str(error))
