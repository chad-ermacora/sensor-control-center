import webbrowser
import sys
import os
from urllib.request import urlopen
from tkinter import filedialog
from Sensor_commands import get
from Sensor_config import load_file

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
html_template_1 = "additional_files/html_template_1.html"
html_template_2 = "additional_files/html_template_2.html"
html_template_3 = "additional_files/html_template_3.html"


def get_about_text():
    return var_app_about


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
    temp_settings = load_file()
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
            sensor_data = get(ip)
    
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
                    log_print_text = log_print_text + "\nWrong format for Sensor Values\nTry Updating the Program"
    
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

