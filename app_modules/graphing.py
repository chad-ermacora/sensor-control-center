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
from datetime import datetime, timedelta
import app_modules.app_logger as app_logger


class CreateSQLColumnsReadable:
    """ Creates an object to hold all human readable SQL column names. """

    def __init__(self):
        self.no_sensor = ""
        self.date_time = "Date & Time"
        self.sensor_name = "Sensor Name"
        self.ip = "IP"
        self.system_uptime = "Sensor Uptime"
        self.cpu_temp = "CPU Temperature"
        self.environmental_temp = "Env Temperature"
        self.pressure = "Pressure"
        self.humidity = "Humidity"
        self.lumen = "Lumen"
        self.colours = "Colours"
        self.accelerometer_xyz = "Accelerometer XYZ"
        self.magnetometer_xyz = "Magnetometer XYZ"
        self.gyroscope_xyz = "Gyroscope XYZ"


class CreateSQLColumnNames:
    """ Creates an object to hold all SQL column names. """

    def __init__(self):
        self.sql_interval_table = "IntervalData"
        self.sql_trigger_table = "TriggerData"
        self.sql_other_table = "OtherData"
        self.date_time = "DateTime"
        self.sensor_name = "SensorName"
        self.ip = "IP"
        self.system_uptime = "SensorUpTime"
        self.cpu_temp = "SystemTemp"
        self.environmental_temp = "EnvironmentTemp"
        self.environmental_temp_offset = "EnvTempOffset"
        self.pressure = "Pressure"
        self.humidity = "Humidity"
        self.lumen = "Lumen"
        self.rgb = ["Red", "Green", "Blue"]
        self.six_chan_color = ["Red", "Orange", "Yellow", "Green", "Blue", "Violet"]
        self.accelerometer_xyz = ["Acc_X", "Acc_Y", "Acc_Z"]
        self.magnetometer_xyz = ["Mag_X", "Mag_Y", "Mag_Z"]
        self.gyroscope_xyz = ["Gyro_X", "Gyro_Y", "Gyro_Z"]

        self.other_notes = "Notes"
        self.other_user_datetime = "UserDateTime"


class CreateMeasurementsTypes:
    """ Creates an object to hold all sensor measurement types. """

    def __init__(self):
        self.no_measurement = ""
        self.celsius = " °C"
        self.pressure = " hPa"
        self.humidity = " %RH"
        self.lumen = " Lumen"
        self.rgb = " RGB"
        self.six_chan_color = " ROYGBV"
        self.xyz = " XYZ"


class CreateGraphData:
    """ Creates an object to hold all the data needed for a graph. """

    def __init__(self):
        self.enable_plotly_webgl = False
        self.db_location = ""
        self.graph_table = "IntervalData"
        self.save_to = ""
        self.graph_start = "1111-08-21 00:00:01"
        self.graph_end = "9999-01-01 00:00:01"
        self.datetime_offset = 0.0
        self.sql_queries_skip = 12
        self.bypass_sql_skip = False
        self.enable_custom_temp_offset = True
        self.temperature_offset = 0.0

        self.sub_plots = []
        self.row_count = 0
        self.graph_collection = []

        self.graph_columns = ["DateTime", "SensorName", "SensorUpTime", "IP", "SystemTemp",
                              "EnvironmentTemp", "EnvTempOffset", "Pressure", "Humidity", "Lumen",
                              "Red", "Orange", "Yellow", "Green", "Blue", "Violet"]
        self.max_sql_queries = 200000

        # Graph data holders for SQL DataBase
        self.sql_time = []
        self.sql_ip = []
        self.sql_host_name = []
        self.sql_up_time = []
        self.sql_cpu_temp = []
        self.sql_hat_temp = []
        self.sql_temp_offset = []
        self.sql_pressure = []
        self.sql_humidity = []
        self.sql_lumen = []
        self.sql_red = []
        self.sql_orange = []
        self.sql_yellow = []
        self.sql_green = []
        self.sql_blue = []
        self.sql_violet = []
        self.sql_acc_x = []
        self.sql_acc_y = []
        self.sql_acc_z = []
        self.sql_mg_x = []
        self.sql_mg_y = []
        self.sql_mg_z = []
        self.sql_gyro_x = []
        self.sql_gyro_y = []
        self.sql_gyro_z = []


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
