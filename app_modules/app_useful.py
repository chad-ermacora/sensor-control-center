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

import app_modules.app_logger as app_logger

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
1 = Record Sensors to SQL Database
300.0 = Duration between Interval recordings in Seconds
0.15 = Duration between Trigger reading checks in Seconds
0 = Enable Custom Variances
0.0 = Custom Accelerometer variance
0.0 = Custom Magnetometer variance
0.0 = Custom Gyroscope variance
0 = Enable Custom Temperature Offset
0.0 = Custom Temperature Offset
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