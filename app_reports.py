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
from queue import Queue
from threading import Thread
from time import strftime

import app_logger
import app_sensor_commands
from app_useful import convert_minutes_string, get_file_content, save_data_to_file, open_html_file

data_queue = Queue()


class CreateHTMLSystemData:
    def __init__(self, current_config):
        self.config_settings = current_config
        self.template1 = current_config.script_directory + "/additional_files/html_template_system1.html"
        self.template2 = current_config.script_directory + "/additional_files/html_template_system2.html"
        self.template3 = current_config.script_directory + "/additional_files/html_template_system3.html"
        self.file_output_name = "SensorsSystemReport.html"

        self.replacement_codes = ["{{HostName}}",
                                  "{{IP}}",
                                  "{{DateTime}}",
                                  "{{UpTime}}",
                                  "{{Version}}",
                                  "{{CPUTemp}}",
                                  "{{FreeDisk}}",
                                  "{{SQLDBSize}}",
                                  "{{SQLWriteEnabled}}",
                                  "{{CustomEnabled}}",
                                  "{{LastUpdated}}"]

        self.local_time_code = ["{{LocalDateTime}}"]

    def get_sensor_data(self, ip):
        network_timeout = self.config_settings.network_timeout_data
        command_data = app_sensor_commands.CreateSensorNetworkCommand(ip, network_timeout, "GetSystemData")
        sensor_system = app_sensor_commands.get_data(command_data).split(",")

        try:
            sensor_system[3] = convert_minutes_string(sensor_system[3])
        except Exception as error:
            app_logger.app_logger.error("Sensor System Report: " + str(error))

        data_queue.put([ip, sensor_system])


class CreateHTMLReadingsData:
    def __init__(self, current_config):
        self.config_settings = current_config
        self.template1 = current_config.script_directory + "/additional_files/html_template_readings1.html"
        self.template2 = current_config.script_directory + "/additional_files/html_template_readings2.html"
        self.template3 = current_config.script_directory + "/additional_files/html_template_readings3.html"
        self.file_output_name = "SensorsReadingsReport.html"

        self.replacement_codes = ["{{SensorTypes}}",
                                  "{{SensorReadings}}"]

        self.local_time_code = ["{{LocalDateTime}}"]

    def get_sensor_data(self, ip):
        network_timeout = self.config_settings.network_timeout_data
        command_data = app_sensor_commands.CreateSensorNetworkCommand(ip, network_timeout, "GetSensorReadings")
        sensor_data = app_sensor_commands.get_data(command_data).split(",")
        data_queue.put([ip, sensor_data])


class CreateHTMLConfigData:
    def __init__(self, current_config):
        self.config_settings = current_config
        self.template1 = current_config.script_directory + "/additional_files/html_template_config1.html"
        self.template2 = current_config.script_directory + "/additional_files/html_template_config2.html"
        self.template3 = current_config.script_directory + "/additional_files/html_template_config3.html"
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
                                  "{{CustomGyro}}",
                                  "{{InstalledSensors}}"]

        self.local_time_code = ["{{LocalDateTime}}"]

    def get_sensor_data(self, ip):
        network_timeout = self.config_settings.network_timeout_data
        command_data = app_sensor_commands.CreateSensorNetworkCommand(ip, network_timeout, "GetSystemData")
        sensor_system = app_sensor_commands.get_data(command_data).split(",")
        try:
            sensor_system[3] = convert_minutes_string(sensor_system[3])
        except Exception as error:
            app_logger.app_logger.error("Sensor Config Report: " + str(error))

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
                               str(sensor_config[6]),
                               str(sensor_config[7])]
        data_queue.put([ip, final_sensor_config])


def _sensor_report_worker(report_configuration, threads):
    template1 = get_file_content(report_configuration.template1)
    # Add Local computer's DateTime to 3rd template
    current_datetime = strftime("%Y-%m-%d %H:%M - %Z")
    final_file = _replace_with_codes([current_datetime],
                                     report_configuration.local_time_code,
                                     template1)
    sensor_html_template = get_file_content(report_configuration.template2)

    # Add first HTML Template file to final HTML output file
    # Insert each sensors data into final HTML output file through the 2nd template & replacement codes
    report_data_pool = []

    for thread in threads:
        thread.join()

    while not data_queue.empty():
        report_data_pool.append(data_queue.get())
        data_queue.task_done()

    report_data_pool.sort()

    for sensor_data in report_data_pool:
        try:
            blank_sensor_html = sensor_html_template
            current_sensor_html = _replace_with_codes(sensor_data[1],
                                                      report_configuration.replacement_codes,
                                                      blank_sensor_html)
            final_file = final_file + current_sensor_html
        except Exception as error:
            app_logger.app_logger.error("Report Failure: " + str(error))

    # Merge the result with the Final HTML Template file.

    template3 = get_file_content(report_configuration.template3)
    final_file += template3

    try:
        save_to_location = str(report_configuration.config_settings.save_to + report_configuration.file_output_name)
        save_data_to_file(final_file, save_to_location)
        open_html_file(save_to_location)
        app_logger.app_logger.debug("Sensor Report - HTML Save File - OK")
    except Exception as error:
        app_logger.app_logger.error("Sensor Report - HTML Save File - Failed: " + str(error))


def sensor_html_report(report_configuration, ip_list):
    """ Creates and opens a HTML Report based on provided IP's and report configurations data. """
    threads = []

    for ip in ip_list:
        threads.append(Thread(target=report_configuration.get_sensor_data, args=[ip]))
    for thread in threads:
        thread.start()

    main_report_thread = Thread(target=_sensor_report_worker, args=[report_configuration, threads])
    main_report_thread.start()


def _replace_with_codes(data, codes, template):
    count = 0
    for code in codes:
        try:
            replace_word = str(data[count])
        except Exception as error:
            replace_word = "No Data"
            app_logger.app_logger.error("Invalid Sensor Data: " + str(error))

        template = template.replace(code, replace_word)
        count += 1

    return template
