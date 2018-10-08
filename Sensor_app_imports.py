import webbrowser
import sys
import os
import logging
from urllib.request import urlopen
from tkinter import filedialog
from guizero import info
from Sensor_commands import get_system_info, get_sensor_config
from Sensor_config import load_file as load_config
from logging.handlers import RotatingFileHandler

var_app_about = '''
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
'''
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:  %(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = RotatingFileHandler('logs/KootNet_log.txt', maxBytes=256000, backupCount=5)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

app_location_directory = str(os.path.dirname(sys.argv[0])) + "/"
html_template_details1 = "additional_files/html_template_details1.html"
html_template_details2 = "additional_files/html_template_details2.html"
html_template_details3 = "additional_files/html_template_details3.html"
html_template_config1 = "additional_files/html_template_config1.html"
html_template_config2 = "additional_files/html_template_config2.html"
html_template_config3 = "additional_files/html_template_config3.html"


def get_about_text():
    logger.debug("Getting KootNet Sensors About Text")
    return var_app_about


def html_system_codes():
    logger.debug("Getting Sensor Details HTML replacement Codes")

    html_replacement_vars = ["{{sysHostName}}",
                             "{{sysIP}}",
                             "{{sysDateTime}}",
                             "{{sysUpTime}}",
                             "{{sysCPUTemp}}",
                             "{{sqldb1}}",
                             "{{sqldb2}}",
                             "{{SensorConfig}}"]

    return html_replacement_vars


def html_config_codes():
    logger.debug("Getting Sensor Config HTML replacement Codes")

    html_replacement_vars = ["{{sysHostName}}",
                             "{{sysIP}}",
                             "{{sysDateTime}}",
                             "{{SQLDataBaseEnable}}",
                             "{{IntervalDuration}}",
                             "{{TriggerDuration}}",
                             "{{CustomEnable}}",
                             "{{CustomAcc}}",
                             "{{CustomMag}}",
                             "{{CustomGyro}}"]

    return html_replacement_vars


def open_html(outfile):
    try:
        file_var = "file:///" + outfile
        webbrowser.open(file_var, new=2)
        logger.debug("Graph HTML File Opened - OK")
    except Exception as error:
        logger.error("Graph HTML File Opened - Failed - " + str(error))


def open_url(url):
    webbrowser.open(url)


def sensor_html_report(ip_list, html_type):
    final_file = ''
    sensor_html = ''
    replace_word = ''
    current_sensor_html = ''
    temp_config = load_config()
    net_timeout = int(temp_config.network_details_timeout)

    if html_type == "SystemDetails":
        replacement_codes = html_system_codes()
    else:
        replacement_codes = html_config_codes()

    try:
        if html_type == "SystemDetails":
            html_file_part = open(str(app_location_directory + html_template_details1), 'r')
        else:
            html_file_part = open(str(app_location_directory + html_template_config1), 'r')
        final_file = html_file_part.read()
        html_file_part.close()
        if html_type == "SystemDetails":
            html_file_part = open(str(app_location_directory + html_template_details2), 'r')
        else:
            html_file_part = open(str(app_location_directory + html_template_config2), 'r')
        sensor_html = html_file_part.read()
        html_file_part.close()
        logger.debug("Open html_template_details1.html & html_template_details2.html Template - OK")
    except Exception as error:
        logger.error("Open Template - Failed: " + str(error))

    # For each IP in the list, Get its sensor data
    # Inserting them into a final HTML file, based on a 3 part template
    for ip in ip_list:
        try:
            current_sensor_html = sensor_html

            if html_type == "SystemDetails":
                sensor_data = get_system_info(ip, net_timeout)
            else:
                sensor_data = get_sensor_config(ip, net_timeout)

            count2 = 0
            for code in replacement_codes:
                if count2 == 0:
                    replace_word = str(sensor_data[0])
                elif count2 == 1:
                    replace_word = str(sensor_data[1])
                elif count2 == 2:
                    replace_word = str(sensor_data[2])
                elif count2 == 3:
                    if html_type == "SystemDetails":
                        uptime_days = int(float(sensor_data[3]) // 1440)
                        uptime_hours = int((float(sensor_data[3]) % 1440) // 60)
                        uptime_min = int(float(sensor_data[3]) % 60)
                        replace_word = str(uptime_days) + " Days / " + str(uptime_hours) + "." + str(uptime_min) + " Hours"
                    else:
                        replace_word = str(sensor_data[3])
                elif count2 == 4:
                    if html_type == "SystemDetails":
                        sensor_data[4] = round(float(sensor_data[4]), 2)
                    replace_word = str(sensor_data[4])
                elif count2 == 5:
                    replace_word = str(sensor_data[5])
                elif count2 == 6:
                    replace_word = str(sensor_data[6])
                elif count2 == 7:
                    replace_word = str(sensor_data[7])
                elif count2 == 8:
                    replace_word = str(sensor_data[8])
                elif count2 == 9:
                    replace_word = str(sensor_data[9])
                else:
                    logger.error("Wrong format for Sensor Values - Try Updating the Program")

                current_sensor_html = current_sensor_html.replace(code, replace_word)
                count2 = count2 + 1
        except Exception as error:
                logger.error("Sensor get probably failed: " + str(error))

        # Add's each sensor that checked Online, into the final HTML variable
        final_file = final_file + current_sensor_html
    try:
        if html_type == "SystemDetails":
            html_file_part = open(str(app_location_directory + html_template_details3), 'r')
        else:
            html_file_part = open(str(app_location_directory + html_template_config3), 'r')

        html_end = html_file_part.read()
        html_file_part.close()
        final_file = final_file + html_end
        logger.debug("Created Sensor Details - HTML File - OK")
    except Exception as error:
        logger.error("Open html_template_details3.html Template Failed: " + str(error))

    # Write the final html variable to file
    try:
        save_to_location = str(temp_config.save_to + "SensorsDetails.html")
        file_out = open(save_to_location, 'w')
        file_out.write(final_file)
        file_out.close()
        open_html(save_to_location)
        logger.debug("Sensor Details - HTML Save File - OK")
    except Exception as error:
        logger.error("Sensor Details - HTML Save File - Failed: " + str(error))


def download_interval_db(ip_list):
    j = filedialog.askdirectory()

    for ip in ip_list:
        try:
            remote_database = urlopen("http://" + str(ip) + ":8009/SensorIntervalDatabase.sqlite")
            local_file = open(j + "/SensorIntervalDatabase" + ip[-3:] + ".sqlite", 'wb')
            local_file.write(remote_database.read())
            remote_database.close()
            local_file.close()
            logger.info("Download Interval DB from " + ip + " Complete")
        except Exception as error:
            logger.error("Download Interval DB from " + str(ip) + " Failed: " + str(error))

    info("Information", "Interval DataBase Download(s) Complete")
    logger.debug("Interval DataBase Download(s) Complete")


def download_trigger_db(ip_list):
    j = filedialog.askdirectory()

    for ip in ip_list:
        try:
            remote_database = urlopen("http://" + str(ip) + ":8009/SensorTriggerDatabase.sqlite")
            local_file = open(j + "/SensorTriggerDatabase" + ip[-3:] + ".sqlite", 'wb')
            local_file.write(remote_database.read())
            remote_database.close()
            local_file.close()
            logger.info("Download Trigger DB from " + ip + " Complete")
        except Exception as error:
            logger.error("Download Trigger DB from " + ip + " Failed: " + str(error))

    info("Information", "Trigger DataBase Download(s) Complete")
    logger.debug("Trigger DataBase Download(s) Complete")
