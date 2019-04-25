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
import guizero
import webbrowser
from datetime import datetime, timedelta
from app_modules import app_logger


def no_ip_selected_message():
    """ Displays a GUI message asking the user to select an IP address. """
    guizero.warn("No Sensor IP", "Please select at least one online sensor IP\n\nSelect sensor IPs in the main window")


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


def adjust_datetime(var_datetime, datetime_offset):
    """
    Adjusts the provided datetime by the provided hour offset and returns the result as a string.

    Used for graph datetime's accurate to 0.001 second
    """
    tmp_ms = ""
    if len(var_datetime) > 19:
        try:
            tmp_ms = str(var_datetime)[-4:]
            var_datetime = datetime.strptime(str(var_datetime)[:-4], "%Y-%m-%d %H:%M:%S")
        except Exception as error:
            app_logger.app_logger.error("Unable to Convert Trigger datetime string to datetime format - " + str(error))
    else:
        try:
            var_datetime = datetime.strptime(var_datetime, "%Y-%m-%d %H:%M:%S")
        except Exception as error:
            app_logger.app_logger.error("Unable to Convert Interval datetime string to datetime format - " + str(error))

    try:
        new_time = var_datetime + timedelta(hours=datetime_offset)
    except Exception as error:
        app_logger.app_logger.error("Unable to convert Hour Offset to int - " + str(error))
        new_time = var_datetime

    app_logger.app_logger.debug("Adjusted datetime: " + str(new_time))
    return str(new_time) + tmp_ms
