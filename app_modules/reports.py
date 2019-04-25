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

import app_modules.app_logger as app_logger
import app_modules.sensor_commands as app_sensor_commands
import app_modules.app_variables as useful

network_get_commands = app_sensor_commands.CreateNetworkGetCommands()


class _CreateBasicHTMLData:
    """ Create a Basic HTML Report data object based on provided report_type (System, Readings, Config). """
    def __init__(self, report_type, current_config):
        self.data_queue = Queue()

        if report_type == "System":
            self.template1 = useful.html_template_system1_location
            self.template2 = useful.html_template_system2_location
            self.template3 = useful.html_template_system3_location
            self.file_output_name = useful.html_file_output_name_system
            self.replacement_codes = useful.reports_system_replacement_codes

        elif report_type == "Readings":
            self.template1 = useful.html_template_readings1_location
            self.template2 = useful.html_template_readings2_location
            self.template3 = useful.html_template_readings3_location
            self.file_output_name = useful.html_file_output_name_readings
            self.replacement_codes = useful.reports_readings_replacement_codes

        elif report_type == "Config":
            self.template1 = useful.html_template_config1_location
            self.template2 = useful.html_template_config2_location
            self.template3 = useful.html_template_config3_location
            self.file_output_name = useful.html_file_output_name_config
            self.replacement_codes = useful.reports_config_replacement_codes

        self.local_time_code = useful.reports_local_time_code
        self.network_timeout = current_config.network_timeout_data
        self.save_to = current_config.save_to


class CreateHTMLSystemData(_CreateBasicHTMLData):
    """ Create a System HTML Report data object. """
    def __init__(self, current_config):
        super().__init__("System", current_config)

    def get_sensor_data(self, ip):
        """ Gets system report data from the provided sensor IP and puts it in the instance que. """
        command_data = app_sensor_commands.CreateSensorNetworkCommand(ip,
                                                                      self.network_timeout,
                                                                      network_get_commands.system_data)
        sensor_system = app_sensor_commands.get_data(command_data).split(",")

        try:
            sensor_system[3] = useful.convert_minutes_string(sensor_system[3])
        except Exception as error:
            app_logger.app_logger.error("Sensor System Report: " + str(error))

        self.data_queue.put([ip, sensor_system])


class CreateHTMLReadingsData(_CreateBasicHTMLData):
    """ Create a Readings HTML Report data object. """
    def __init__(self, current_config):
        super().__init__("Readings", current_config)

    def get_sensor_data(self, ip):
        """ Gets readings report data from the provided sensor IP and puts it in the instance que. """
        command_data = app_sensor_commands.CreateSensorNetworkCommand(ip,
                                                                      self.network_timeout,
                                                                      network_get_commands.sensor_readings)
        sensor_data = app_sensor_commands.get_data(command_data).split(",")
        self.data_queue.put([ip, sensor_data])


class CreateHTMLConfigData(_CreateBasicHTMLData):
    """ Create a Configuration HTML Report data object. """
    def __init__(self, current_config):
        super().__init__("Config", current_config)

    def get_sensor_data(self, ip):
        """ Gets configuration report data from the provided sensor IP and puts it in the instance que. """
        command_data = app_sensor_commands.CreateSensorNetworkCommand(ip,
                                                                      self.network_timeout,
                                                                      network_get_commands.system_data)
        sensor_system = app_sensor_commands.get_data(command_data).split(",")
        try:
            sensor_system[3] = useful.convert_minutes_string(sensor_system[3])
        except Exception as error:
            app_logger.app_logger.error("Sensor Config Report: " + str(error))

        command_data.command = network_get_commands.sensor_configuration
        sensor_config = app_sensor_commands.get_data(command_data).split(",")

        final_sensor_config = [str(sensor_system[0]),
                               str(sensor_system[1]),
                               str(sensor_system[2]),
                               str(sensor_config[0]),
                               str(sensor_config[1]),
                               str(sensor_config[2]),
                               str(sensor_config[3]),
                               str(sensor_config[4]),
                               str(sensor_config[5])]
        self.data_queue.put([ip, final_sensor_config])


def _sensor_report_worker(report_configuration, threads):
    """ Takes all the data from the threads (AKA Sensors) and creates a single HTML report. """
    template1 = useful.get_file_content(report_configuration.template1)
    # Add Local computer's DateTime to 3rd template
    current_datetime = strftime("%Y-%m-%d %H:%M - %Z")
    final_file = _replace_with_codes([current_datetime],
                                     report_configuration.local_time_code,
                                     template1)
    sensor_html_template = useful.get_file_content(report_configuration.template2)

    # Add first HTML Template file to final HTML output file
    # Insert each sensors data into final HTML output file through the 2nd template & replacement codes
    report_data_pool = []

    for thread in threads:
        thread.join()

    while not report_configuration.data_queue.empty():
        report_data_pool.append(report_configuration.data_queue.get())
        report_configuration.data_queue.task_done()

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

    template3 = useful.get_file_content(report_configuration.template3)
    final_file += template3

    try:
        save_file_location = report_configuration.save_to + report_configuration.file_output_name
        useful.save_data_to_file(final_file, save_file_location)
        useful.open_html_file(save_file_location)
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
    """ Replaces codes in the template with data and returns the template. """
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
