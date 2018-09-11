import webbrowser
import Sensor_commands
import sys
import os
from urllib.request import urlopen
from tkinter import filedialog

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
app_location_directory = str(os.path.dirname(sys.argv[0])) + "/"
config_file = app_location_directory + "config.txt"
html_template_1 = "additional_files/html_template_1.html"
html_template_2 = "additional_files/html_template_2.html"
html_template_3 = "additional_files/html_template_3.html"


def get_about_text():
    return var_app_about


def config_get_defaults():
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


def config_load_file():
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
        return config_settings

    except:
        print("Configuration File Load - Failed\nUsing Configuration Defaults")
        return config_get_defaults()


def config_check_settings(config_settings):
    checked_settings = []
    log_message = ""

    save_to_default, \
        graph_start_default, \
        graph_end_default, \
        time_offset_default, \
        sql_queries_skip_default, \
        temperature_offset_default, \
        network_check_timeout_default, \
        network_details_timeout_default, \
        allow_power_controls_default, \
        allow_reset_config_default = config_get_defaults()

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
        log_message = log_message + "Invalid Configuration Setting - " +\
                      "Save to Folder - Using Default"
        checked_settings.append(str(save_to_default))

    if len(graph_start) == 19:
        checked_settings.append(str(graph_start))
    else:
        log_message = log_message + "Invalid Configuration Setting - " +\
                      "Graph Start Date Range - Using Default"
        checked_settings.append(str(graph_start_default))

    if len(graph_end) == 19:
        checked_settings.append(str(graph_end))
    else:
        log_message = log_message + "Invalid Configuration Setting - " +\
                      "Graph End Date Range - Using Default"
        checked_settings.append(str(graph_end_default))

    try:
        float(time_offset)
        checked_settings.append(str(time_offset))
    except:
        log_message = log_message + "Invalid Configuration Setting -" + \
                      " DataBase Hours Offset - Using Default"
        checked_settings.append(str(time_offset_default))

    try:
        int(sql_queries_skip)
        checked_settings.append(str(sql_queries_skip))
    except:
        log_message = log_message + "Invalid Configuration Setting - " +\
                      "Skip SQL Queries - Using Default"
        checked_settings.append(str(sql_queries_skip_default))

    try:
        float(temperature_offset)
        checked_settings.append(str(temperature_offset))
    except:
        log_message = log_message + "Invalid Configuration Setting - " + \
                      "Temperature Offset - Using Default"
        checked_settings.append(str(temperature_offset_default))

    try:
        int(network_check_timeout)
        checked_settings.append(str(network_check_timeout))
    except:
        log_message = log_message + "Invalid Configuration Setting - " + \
                      "Sensor Check Timeout - Using Default"
        checked_settings.append(str(network_check_timeout_default))

    try:
        int(network_details_timeout)
        checked_settings.append(str(network_details_timeout))
    except:
        log_message = log_message + "Invalid Configuration Setting - " + \
                      "Get Details Timeout - Using Default"
        checked_settings.append(str(network_details_timeout_default))

    try:
        int(allow_power_controls)
        checked_settings.append(int(allow_power_controls))
    except:
        log_message = log_message + "Invalid Configuration Setting - " + \
                      "Enable Sensor Shutdown/Reboot - Using Defaults"
        checked_settings.append(int(allow_power_controls_default))

    try:
        int(allow_reset_config)
        checked_settings.append(int(str(allow_reset_config)))
    except:
        log_message = log_message + "Invalid Configuration Setting - " + \
                      "Enable Config Reset - Using Default"
        checked_settings.append(int(allow_reset_config_default))

    checked_settings.append(log_message)
    return checked_settings


def config_save(var_settings):
    var_final_write = str(var_settings)[1:-1]

    try:
        local_file = open(config_file, 'w')
        local_file.write(var_final_write)
        local_file.close()
        return_message = "Settings Save - OK"
    except:
        return_message = "Settings Save - Failed"

    return return_message


def html_replacement_codes():
    print("sensor_values(sensor)")

    html_replacement_vars = ["{{sysHostName}}",
                             "{{sysIP}}",
                             "{{sysDateTime}}",
                             "{{sysUpTime}}",
                             "{{sysCPUTemp}}",
                             "{{sqldb1}}",
                             "{{sqldb2}}"]

    return html_replacement_vars


def open_html(html_details_file):
    try:
        html_file_location = "file:///" + html_details_file
        webbrowser.open(html_file_location, new=2)
        print("open_html OK")
    except:
        print("open_html Failed")


def sensor_detailed_status(ip_list):
    log_print_text = ''
    final_file = ''
    replacement_codes = html_replacement_codes()
    temp_settings = config_load_file()
    sensor_html = ''
    replace_word = ''
    current_sensor_html = ''

    # Open the HTML Template file to use in variable replacement below.
    try:
        html_file_part = open(str(app_location_directory + html_template_1), 'r')
        final_file = html_file_part.read()
        html_file_part.close()
        html_file_part = open(str(app_location_directory + html_template_2), 'r')
        sensor_html = html_file_part.read()
        html_file_part.close()
    except:
        log_print_text = log_print_text + \
            "\nOpen html_template_1.html or " + \
            "html_template_2.html Template Failed"

    # For each IP in the list, Get its sensor data
    # Inserting them into a final HTML file, based on a 3 part template
    for ip in ip_list:
        try:
            current_sensor_html = sensor_html
            sensor_data = Sensor_commands.get(ip)
    
            count2 = 0
            for code in replacement_codes:
                if count2 == 0:
                    replace_word = str(sensor_data[0])
                elif count2 == 1:
                    replace_word = str(sensor_data[1])
                elif count2 == 2:
                    replace_word = str(sensor_data[2])
                elif count2 == 3:
                    uptime_days = int(float(sensor_data[3]) // 1440)
                    uptime_hours = int((float(sensor_data[3]) % 1440) // 60)
                    uptime_min = int(float(sensor_data[3]) % 60)
    
                    replace_word = str(uptime_days) + " Days / " + str(uptime_hours) + "." + str(uptime_min) + " Hours"
                elif count2 == 4:
                    replace_word = str(sensor_data[4])
                elif count2 == 5:
                    replace_word = str(sensor_data[5])
                elif count2 == 6:
                    replace_word = str(sensor_data[6])
                else:
                    log_print_text = log_print_text + \
                        "\nWrong format for Sensor " + \
                        "Values\nTry Updating the Program"
    
                current_sensor_html = current_sensor_html.replace(code, replace_word)
                count2 = count2 + 1
        except:
                print("Sensor get probably failed")

        # Add's each sensor that checked Online, into the final HTML variable
        final_file = final_file + current_sensor_html
    try:
        html_file_part = open(str(app_location_directory + html_template_3), 'r')
        html_end = html_file_part.read()
        html_file_part.close()
        final_file = final_file + html_end
    except:
        log_print_text = log_print_text + "\nOpen html_template_3.html Template Failed"

    # Write the final html variable to file
    try:
        save_to_folder = str(temp_settings[0] + "SensorsDetails.html")
        fout = open(save_to_folder, 'w')
        fout.write(final_file)
        fout.close()
        open_html(save_to_folder)
        log_print_text = log_print_text + \
            "\nSensor Details - HTML Save File - OK"
    except:
        log_print_text = log_print_text + \
            "\nSensor Details - HTML Save File - Failed"

    return log_print_text


def download_interval_db(ip_list):
    j = filedialog.askdirectory()
    log_message = "Downloading Interval Sensor DataBase(s)"

    for ip in ip_list:
        try:
            remote_database = urlopen("http://" + str(ip) +
                                      ':8009/SensorIntervalDatabase.sqlite')
            local_file = open(j + "/SensorIntervalDatabase" + ip[-3:] + ".sqlite", 'wb')
            local_file.write(remote_database.read())
            remote_database.close()
            local_file.close()
            log_message = log_message + "\nDownload from " + ip + " Complete"
        except:
            log_message = log_message + "\nFailed on " + str(ip) + " "

    log_message = log_message + "\n\nSensor DataBase Download(s) Complete"
    return log_message


def download_trigger_db(ip_list):
    j = filedialog.askdirectory()
    log_message = "Downloading Trigger Sensor DataBase(s)"

    for ip in ip_list:
        try:
            remote_database = urlopen("http://" + str(ip) +
                                      ':8009/SensorTriggerDatabase.sqlite')
            local_file = open(j + "/SensorTriggerDatabase" + ip[-3:] + ".sqlite", 'wb')
            local_file.write(remote_database.read())
            remote_database.close()
            local_file.close()
            log_message = log_message + "\nDownload from " + ip + " Complete"
        except:
            log_message = log_message + "\nConnection Failed on " + ip

    log_message = log_message + "\n\nTrigger DataBase Download(s) Complete"
    return log_message
