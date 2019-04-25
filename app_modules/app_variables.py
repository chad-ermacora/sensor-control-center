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
from guizero import warn
from sys import path
import app_modules.app_logger as app_logger

script_directory = str(path[0]).replace("\\", "/")

html_file_output_name_system = "SensorsSystemReport.html"
html_template_system1_location = script_directory + "/additional_files/html_template_system1.html"
html_template_system2_location = script_directory + "/additional_files/html_template_system2.html"
html_template_system3_location = script_directory + "/additional_files/html_template_system3.html"

html_file_output_name_readings = "SensorsReadingsReport.html"
html_template_readings1_location = script_directory + "/additional_files/html_template_readings1.html"
html_template_readings2_location = script_directory + "/additional_files/html_template_readings2.html"
html_template_readings3_location = script_directory + "/additional_files/html_template_readings3.html"

html_file_output_name_config = "SensorsConfigReport.html"
html_template_config1_location = script_directory + "/additional_files/html_template_config1.html"
html_template_config2_location = script_directory + "/additional_files/html_template_config2.html"
html_template_config3_location = script_directory + "/additional_files/html_template_config3.html"

reports_system_replacement_codes = ["{{HostName}}",
                                    "{{IP}}",
                                    "{{DateTime}}",
                                    "{{UpTime}}",
                                    "{{Version}}",
                                    "{{CPUTemp}}",
                                    "{{FreeDisk}}",
                                    "{{SQLDBSize}}",
                                    "{{LastUpdated}}"]

reports_readings_replacement_codes = ["{{SensorTypes}}",
                                      "{{SensorReadings}}"]

reports_config_replacement_codes = ["{{HostName}}",
                                    "{{IP}}",
                                    "{{DateTime}}",
                                    "{{IntervalSQLWriteEnabled}}",
                                    "{{TriggerSQLWriteEnabled}}",
                                    "{{IntervalDuration}}",
                                    "{{CustomTempOffset}}",
                                    "{{TemperatureOffset}}",
                                    "{{InstalledSensors}}"]

reports_local_time_code = ["{{LocalDateTime}}"]

default_installed_sensors_text = """
Change the number in front of each line. Enable = 1 & Disable = 0
1 = Gnu/Linux - Raspbian
0 = Raspberry Pi Zero W
0 = Raspberry Pi 3BPlus
0 = Raspberry Pi Sense HAT
0 = Pimoroni BH1745
0 = Pimoroni AS7262
0 = Pimoroni BME680
0 = Pimoroni EnviroPHAT
0 = Pimoroni LSM303D
0 = Pimoroni VL53L1X
0 = Pimoroni LTR-559
"""

default_sensor_config_text = """
Enable = 1 & Disable = 0 (Recommended: Do not change if you are unsure)
0 = Enable Debug Logging
1 = Record Interval Sensors to SQL Database
1 = Record Trigger Sensors to SQL Database
300.0 = Seconds between Interval recordings
0 = Enable Custom Temperature Offset
0.0 = Custom Temperature Offset
"""

default_wifi_config_text = """
# Update or Add additional wireless network connections as required
# Add your wireless name to the end of 'ssid=' 
# Add the password to the end of 'psk=' in double quotes

ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

# Change 'country' to your country, common codes are included below
# GB (United Kingdom), FR (France), US (United States), CA (Canada)
country=CA

network={
        ssid="SomeOtherNetwork"
        psk="SuperSecurePassword"
        key_mgmt=WPA-PSK
}
"""

default_variance_config_text = """
Enable or Disable & set Variance settings.  0 = Disabled, 1 = Enabled.
1 = Enable Sensor Uptime
1209600.0 = Seconds between SQL Writes of Sensor Uptime

1 = Enable CPU Temperature
10.0 = CPU Temperature variance
99999.99 = Seconds between 'CPU Temperature' readings

1 = Enable Environmental Temperature
10.0 = Environmental Temperature variance
99999.99 = Seconds between 'Environmental Temperature' readings

1 = Enable Pressure
50 = Pressure variance
99999.99 = Seconds between 'Pressure' readings

1 = Enable Humidity
25.0 = Humidity variance
99999.99 = Seconds between 'Humidity' readings

1 = Enable Lumen
600.0 = Lumen variance
99999.99 = Seconds between 'Lumen' readings

1 = Enable Red
10.0 = Red variance
99999.99 = Seconds between 'Red' readings

1 = Enable Orange
10.0 = Orange variance
99999.99 = Seconds between 'Orange' readings

1 = Enable Yellow
10.0 = Yellow variance
99999.99 = Seconds between 'Yellow' readings

1 = Enable Green
10.0 = Green variance
99999.99 = Seconds between 'Green' readings

1 = Enable Blue
10.0 = Blue variance
99999.99 = Seconds between 'Blue' readings

1 = Enable Violet
10.0 = Violet variance
99999.99 = Seconds between 'Violet' readings

1 = Enable Accelerometer
99999.99 = Accelerometer variance
99999.99 = Seconds between 'Accelerometer' readings

1 = Enable Magnetometer
99999.99 = Magnetometer variance
99999.99 = Seconds between 'Magnetometer' readings

1 = Enable Gyroscope
99999.99 = Gyroscope variance
99999.99 = Seconds between 'Gyroscope' readings
"""

sql_default_textbox_note = """
Use this textbox to create a note to enter into one or more sensor
SQL Databases.  Use the Date & Time in the top right to enter the note
beside corresponding sensor data.

Example Notes:
The increase in temperature is due to the approaching wildfire.
  - Generic Worker SN:33942

The increase in lumen at night, may be an indication of the rare 
laser emitting sheep in the area.  
Notice how it only shows in the Near-Infrared spectrum. 
  - Random Zoologist
"""


def no_ip_selected_message():
    """ Displays a GUI message asking the user to select an IP address. """
    warn("No Sensor IP", "Please select at least one online sensor IP\n\nSelect sensor IPs in the main window")


def convert_minutes_string(var_minutes):
    """ Converts provided minutes into a human readable string. """
    str_day_hour_min = ""

    try:
        uptime_days = int(float(var_minutes) // 1440)
        uptime_hours = int((float(var_minutes) % 1440) // 60)
        uptime_min = int(float(var_minutes) % 60)
        if uptime_days:
            if uptime_days > 1:
                str_day_hour_min = str(uptime_days) + " Days, "
            else:
                str_day_hour_min = str(uptime_days) + " Day, "
        if uptime_hours:
            if uptime_hours > 1:
                str_day_hour_min += str(uptime_hours) + " Hours & "
            else:
                str_day_hour_min += str(uptime_hours) + " Hour & "

        str_day_hour_min += str(uptime_min) + " Min"

    except Exception as error:
        app_logger.app_logger.error("Unable to convert Minutes to days/hours.min: " + str(error))
        str_day_hour_min = var_minutes

    return str_day_hour_min


def save_data_to_file(data, file_location):
    """ Save data to a local file. """
    try:
        file_out = open(file_location, "w")
        file_out.write(data)
        file_out.close()
    except Exception as error:
        app_logger.app_logger.error("Unable to save file: " + str(error))


def open_html_file(outfile):
    """ Opens a local HTML file in the default web browser. """
    try:
        webbrowser.open_new_tab("file:///" + outfile)
        app_logger.app_logger.debug("Graph HTML File Opened - OK")
    except Exception as error:
        app_logger.app_logger.error("Graph HTML File Opened - Failed - " + str(error))


def get_file_content(file_location):
    """ Returns the content of a local file. """
    try:
        tmp_file = open(file_location, "r")
        file_content = tmp_file.read()
        tmp_file.close()
    except Exception as error:
        app_logger.app_logger.error("Unable to get file contents: " + str(error))
        file_content = "Unable to get file contents: " + str(error)

    return file_content
