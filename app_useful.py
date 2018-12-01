import webbrowser

import app_logger

default_installed_sensors_text = """
Change the number in front of each line. Enable = 1 & Disable = 0
1 = Gnu/Linux - Raspbian
0 = Raspberry Pi Zero W
0 = Raspberry Pi 3BPlus
0 = Raspberry Pi Sense HAT
0 = Pimoroni BH1745
0 = Pimoroni BME680
0 = Pimoroni EnviroPHAT
0 = Pimoroni LSM303D
0 = Pimoroni VL53L1X
"""

default_sensor_config_text = """
Enable = 1 & Disable = 0 (Recommended: Don't change anything)
1 = Record Sensors to SQL Database
300 = Duration between Interval readings in Seconds
0.15 = Duration between Trigger readings in Seconds
0 = Enable Custom Settings
0.0 = Custom Accelerometer variance
0.0 = Custom Magnetometer variance
0.0 = Custom Gyroscope variance
0 = Enable Custom Temperature Offset
0.0 = Custom Temperature Offset
"""


def convert_minutes_string(var_minutes):
    """ Converts provided minutes into a human readable string. """
    try:
        uptime_days = int(float(var_minutes) // 1440)
        uptime_hours = int((float(var_minutes) % 1440) // 60)
        uptime_min = int(float(var_minutes) % 60)
        str_day_hour_min = str(uptime_days) + " Days / " + str(uptime_hours) + "." + str(uptime_min) + " Hours"
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
