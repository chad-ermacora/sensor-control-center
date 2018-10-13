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
import os
import logging
from sensor_commands import get_system_info, get_sensor_config
from app_config import load_file as load_config
from logging.handlers import RotatingFileHandler

script_directory = str(os.path.dirname(os.path.realpath(__file__)))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:  %(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = RotatingFileHandler(script_directory + '/logs/KootNet_log.txt', maxBytes=256000, backupCount=5)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

html_template_system1 = script_directory + "/additional_files/html_template_system1.html"
html_template_system2 = script_directory + "/additional_files/html_template_system2.html"
html_template_system3 = script_directory + "/additional_files/html_template_system3.html"
html_template_config1 = script_directory + "/additional_files/html_template_config1.html"
html_template_config2 = script_directory + "/additional_files/html_template_config2.html"
html_template_config3 = script_directory + "/additional_files/html_template_config3.html"


def html_system_codes():
    logger.debug("Getting Sensor Details HTML replacement Codes")

    html_replacement_vars = ["{{HostName}}",
                             "{{IP}}",
                             "{{DateTime}}",
                             "{{UpTime}}",
                             "{{CPUTemp}}",
                             "{{FreeDisk}}",
                             "{{IntervalSize}}",
                             "{{TriggerSize}}",
                             "{{SQLWriteEnabled}}",
                             "{{CustomEnabled}}"]

    return html_replacement_vars


def html_config_codes():
    logger.debug("Getting Sensor Config HTML replacement Codes")

    html_replacement_vars = ["{{HostName}}",
                             "{{IP}}",
                             "{{DateTime}}",
                             "{{IntervalDuration}}",
                             "{{TriggerDuration}}",
                             "{{SQLWriteEnabled}}",
                             "{{CustomEnabled}}",
                             "{{CustomAcc}}",
                             "{{CustomMag}}",
                             "{{CustomGyro}}"]

    return html_replacement_vars


def open_html(outfile):
    try:
        webbrowser.open_new_tab("file:///" + outfile)
        logger.debug("Graph HTML File Opened - OK")
    except Exception as error:
        logger.error("Graph HTML File Opened - Failed - " + str(error))


def sensor_system_report(ip_list):
    final_file = ''
    sensor_html = ''
    temp_config = load_config()
    net_timeout = int(temp_config.network_details_timeout)

    try:
        html_file_part = open(html_template_system1, 'r')
        final_file = html_file_part.read()
        html_file_part.close()
        html_file_part = open(html_template_system2, 'r')
        sensor_html = html_file_part.read()
        html_file_part.close()
        logger.debug("Open First 2 System Report Templates - OK")
    except Exception as error:
        logger.error("Open First 2 System Report Templates - Failed: " + str(error))

    # For each IP in the list, Get its data per Report "Type"
    # Inserting them into a final HTML file, based on a 3 part template
    replacement_codes = html_system_codes()
    for ip in ip_list:
        try:
            current_sensor_html = sensor_html
            sensor_data = get_system_info(ip, net_timeout)

            uptime_days = int(float(sensor_data[3]) // 1440)
            uptime_hours = int((float(sensor_data[3]) % 1440) // 60)
            uptime_min = int(float(sensor_data[3]) % 60)
            sensor_data[3] = str(uptime_days) + " Days / " + str(uptime_hours) + "." + str(uptime_min) + " Hours"

            count = 0
            for code in replacement_codes:
                try:
                    replace_word = str(sensor_data[count])
                except Exception as error:
                    replace_word = "Failed"
                    logger.error("Invalid Sensor Data: " + str(error))

                current_sensor_html = current_sensor_html.replace(code, replace_word)
                count = count + 1

            final_file = final_file + current_sensor_html
        except Exception as error:
                logger.error("System Report Failure: " + str(error))

    try:
        html_file_part = open(html_template_system3, 'r')
        html_end = html_file_part.read()
        html_file_part.close()
        final_file = final_file + html_end
        logger.debug("Created System Report - HTML File - OK")
    except Exception as error:
        logger.error("Open 3rd System Report Template File Failed: " + str(error))

    try:
        save_to_location = str(temp_config.save_to + "SensorsSystem.html")
        file_out = open(save_to_location, 'w')
        file_out.write(final_file)
        file_out.close()
        open_html(save_to_location)
        logger.debug("Sensor System Report - HTML Save File - OK")
    except Exception as error:
        logger.error("Sensor System Report - HTML Save File - Failed: " + str(error))


def sensor_config_report(ip_list):
    final_file = ''
    sensor_html = ''
    temp_config = load_config()
    net_timeout = int(temp_config.network_details_timeout)

    try:
        html_file_part = open(html_template_config1, 'r')
        final_file = html_file_part.read()
        html_file_part.close()
        html_file_part = open(html_template_config2, 'r')
        sensor_html = html_file_part.read()
        html_file_part.close()
        logger.debug("Open First 2 Config Report Templates - OK")
    except Exception as error:
        logger.error("Open First 2 Config Report Templates - Failed: " + str(error))

    # For each IP in the list, Get its data per Report "Type"
    # Inserting them into a final HTML file, based on a 3 part template
    replacement_codes = html_config_codes()
    for ip in ip_list:
        try:
            current_sensor_html = sensor_html
            sensor_data = get_sensor_config(ip, net_timeout)

            count = 0
            for code in replacement_codes:
                current_sensor_html = current_sensor_html.replace(code, str(sensor_data[count]))
                count = count + 1
            final_file = final_file + current_sensor_html
        except Exception as error:
                logger.error("Config Report Failure: " + str(error))

    try:
        html_file_part = open(html_template_config3, 'r')
        html_end = html_file_part.read()
        html_file_part.close()
        final_file = final_file + html_end
        logger.debug("Created Sensor Config Report - HTML File - OK")
    except Exception as error:
        logger.error("Open 3rd Template File Failed: " + str(error))

    # Write to a HTML file
    try:
        save_to_location = str(temp_config.save_to + "SensorsConfig.html")
        file_out = open(save_to_location, 'w')
        file_out.write(final_file)
        file_out.close()
        open_html(save_to_location)
        logger.debug("Sensor Config Report  - HTML Save File - OK")
    except Exception as error:
        logger.error("Sensor Config Report  - HTML Save File - Failed: " + str(error))
