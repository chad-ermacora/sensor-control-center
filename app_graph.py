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
import sqlite3
from datetime import datetime, timedelta

import plotly
from guizero import warn
from matplotlib import pyplot, animation, style
from plotly import tools, graph_objs as go

import app_logger
import app_sensor_commands
from app_useful import convert_minutes_string

style.use("dark_background")


class CreateGraphData:
    """ Creates an object to hold all the data needed for a graph. """
    app_logger.app_logger.debug("CreateGraphData Instance Created")

    def __init__(self):
        self.db_location = ""
        self.save_to = ""
        self.graph_start = "1111-08-21 00:00:01"
        self.graph_end = "9999-01-01 00:00:01"
        self.datetime_offset = 0.0
        self.sql_queries_skip = 12
        self.temperature_offset = -4.5

        self.graph_columns = ["DateTime", "SensorName", "SensorUpTime", "IP", "SystemTemp", "EnvironmentTemp",
                              "Pressure", "Humidity", "Lumen", "Red", "Green", "Blue"]
        self.max_sql_queries = 200000

        # Graph data holders for SQL DataBase
        self.sql_data_time = []
        self.sql_data_host_name = []
        self.sql_data_up_time = []
        self.sql_data_ip = []
        self.sql_data_cpu_temp = []

        self.sql_data_hat_temp = []
        self.sql_data_pressure = []
        self.sql_data_humidity = []
        self.sql_data_lumen = []
        self.sql_data_red = []
        self.sql_data_green = []
        self.sql_data_blue = []

        self.sql_data_acc_x = []
        self.sql_data_acc_y = []
        self.sql_data_acc_z = []
        self.sql_data_mg_x = []
        self.sql_data_mg_y = []
        self.sql_data_mg_z = []
        self.sql_data_gyro_x = []
        self.sql_data_gyro_y = []
        self.sql_data_gyro_z = []


class CreateLiveGraph:
    def __init__(self, sensor_type, ip, current_config):
        self.sensor_type = sensor_type
        self.ip = ip
        self.current_config = current_config
        self.get_commands = app_sensor_commands.CreateNetworkGetCommands()
        self.first_datetime = str(datetime.time(datetime.now()))[:8]

        self.fig = pyplot.figure()
        self.fig.canvas.set_window_title('Live Sensor Graph')
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.x = []
        self.y = []

        self.ani = animation.FuncAnimation(self.fig,
                                           self._update_graph,
                                           interval=float(self.current_config.live_refresh) * 1000)
        pyplot.show()

    def _update_graph(self, x_frame):
        current_time = str(datetime.time(datetime.now()))[:8]
        command_data = app_sensor_commands.CreateCommandData(self.ip,
                                                             self.current_config.network_timeout_data,
                                                             "")

        command_data.command = self.get_commands.sensor_name
        sensor_name = app_sensor_commands.get_data(command_data)
        try:
            if self.sensor_type is "SensorUpTime":
                command_data.command = self.get_commands.system_uptime
                sensor_reading = app_sensor_commands.get_data(command_data)
                sensor_type_name = "Sensor Uptime"
                measurement_type = ""
            elif self.sensor_type is "SystemTemp":
                command_data.command = self.get_commands.cpu_temp
                sensor_reading = app_sensor_commands.get_data(command_data)

                try:
                    sensor_reading = round(float(sensor_reading), 3)
                except Exception as error:
                    app_logger.app_logger.warning(str(error))

                sensor_type_name = "CPU Temperature"
                measurement_type = " °C"
            elif self.sensor_type is "EnvironmentTemp":
                command_data.command = self.get_commands.environmental_temp
                sensor_reading = app_sensor_commands.get_data(command_data)

                try:
                    sensor_reading = round(float(sensor_reading) +
                                           float(self.current_config.temperature_offset), 3)
                except Exception as error:
                    app_logger.app_logger.warning(str(error))

                sensor_type_name = "Environmental Temperature"
                measurement_type = " °C"
            elif self.sensor_type is "Pressure":
                command_data.command = self.get_commands.pressure
                sensor_reading = app_sensor_commands.get_data(command_data)
                sensor_type_name = "Pressure"
                measurement_type = " hPa"
            elif self.sensor_type is "Humidity":
                command_data.command = self.get_commands.humidity
                sensor_reading = app_sensor_commands.get_data(command_data)

                try:
                    sensor_reading = int(round(float(sensor_reading), 0))
                except Exception as error:
                    app_logger.app_logger.warning(str(error))

                sensor_type_name = "Humidity"
                measurement_type = " %RH"
            elif self.sensor_type is "Lumen":
                command_data.command = self.get_commands.lumen
                sensor_reading = app_sensor_commands.get_data(command_data)
                sensor_type_name = "Lumen"
                measurement_type = " Lumen"
            elif self.sensor_type == "RGB":
                try:
                    command_data.command = self.get_commands.rgb
                    red, green, blue = app_sensor_commands.get_data(command_data)
                    sensor_reading = [round(red, 3), round(green, 3), round(blue, 3)]
                    sensor_type_name = "RGB"
                    measurement_type = " RGB"
                except Exception as error:
                    app_logger.app_logger.debug(str(error))
                    sensor_reading = "NoSensor"
                    sensor_type_name = "RGB"
                    measurement_type = " RGB"

            elif self.sensor_type == "AccelerometerXYZ":
                try:
                    command_data.command = self.get_commands.accelerometer_xyz
                    var_x, var_y, var_z = app_sensor_commands.get_data(command_data)
                    sensor_reading = [round(var_x, 3), round(var_y, 3), round(var_z, 3)]
                    sensor_type_name = "Accelerometer XYZ"
                    measurement_type = " XYZ"
                except Exception as error:
                    app_logger.app_logger.debug(str(error))
                    sensor_reading = "NoSensor"
                    sensor_type_name = "Accelerometer XYZ"
                    measurement_type = " XYZ"
            elif self.sensor_type == "MagnetometerXYZ":
                try:
                    command_data.command = self.get_commands.magnetometer_xyz
                    var_x, var_y, var_z = app_sensor_commands.get_data(command_data)
                    sensor_reading = [round(var_x, 3), round(var_y, 3), round(var_z, 3)]
                    sensor_type_name = "Magnetometer XYZ"
                    measurement_type = " XYZ"
                except Exception as error:
                    app_logger.app_logger.debug(str(error))
                    sensor_reading = "NoSensor"
                    sensor_type_name = "Magnetometer XYZ"
                    measurement_type = " XYZ"
            elif self.sensor_type == "GyroscopeXYZ":
                try:
                    command_data.command = self.get_commands.gyroscope_xyz
                    var_x, var_y, var_z = app_sensor_commands.get_data(command_data)
                    sensor_reading = [round(var_x, 3), round(var_y, 3), round(var_z, 3)]
                    sensor_type_name = "Gyroscope XYZ"
                    measurement_type = " XYZ"
                except Exception as error:
                    app_logger.app_logger.debug(str(error))
                    sensor_reading = "NoSensor"
                    sensor_type_name = "Gyroscope XYZ"
                    measurement_type = " XYZ"
            else:
                sensor_reading = "NoSensor"
                sensor_type_name = " Invalid Sensor"
                measurement_type = ""

            self.ax1.clear()
            self.y.append(sensor_reading)
            self.x.append(x_frame)
            self.ax1.plot(self.x, self.y)

            if self.sensor_type is "SensorUpTime":
                sensor_reading = convert_minutes_string(sensor_reading)

            pyplot.title(sensor_name + "  ||  " + self.ip + "\n\n" + sensor_type_name)
            pyplot.xlabel("Start Time: " + self.first_datetime +
                          "  ||  Updated: " + current_time +
                          "  ||  " + str(sensor_reading) + measurement_type)

            if self.sensor_type is "SensorUpTime":
                measurement_type = "Minutes"

            pyplot.ylabel(measurement_type)
            pyplot.xticks([])
        except Exception as error:
            app_logger.app_logger.error("Live Graph - Invalid Sensor Data: " + str(error))


def start_graph_interval(graph_data):
    graph_data.graph_table = "IntervalData"
    app_logger.app_logger.debug("SQL Columns: " + str(graph_data.graph_columns))
    app_logger.app_logger.debug("SQL Table(s): " + str(graph_data.graph_table))
    app_logger.app_logger.debug("SQL Start DateTime: " + str(graph_data.graph_start))
    app_logger.app_logger.debug("SQL End DateTime: " + str(graph_data.graph_end))
    app_logger.app_logger.debug("SQL DataBase Location: " + str(graph_data.db_location))

    # Adjust dates to Database timezone in UTC 0
    new_time_offset = int(graph_data.datetime_offset) * -1
    get_sql_graph_start = _adjust_interval_datetime(graph_data.graph_start, new_time_offset)
    get_sql_graph_end = _adjust_interval_datetime(graph_data.graph_end, new_time_offset)
    for var_column in graph_data.graph_columns:
        var_sql_query = "SELECT " + \
                        str(var_column) + \
                        " FROM " + \
                        str(graph_data.graph_table) + \
                        " WHERE " + \
                        var_column + \
                        " IS NOT NULL AND DateTime BETWEEN datetime('" + \
                        str(get_sql_graph_start) + \
                        "') AND datetime('" + \
                        str(get_sql_graph_end) + \
                        "') LIMIT " + \
                        str(graph_data.max_sql_queries)

        sql_column_data = _get_sql_data(graph_data, var_sql_query)

        # Adjust SQL data from its UTC time, to user set timezone (Hour Offset)
        if str(var_column) == "DateTime":
            count = 0
            for data in sql_column_data:
                sql_column_data[count] = _adjust_interval_datetime(data, int(graph_data.datetime_offset))
                count = count + 1

            graph_data.sql_data_time = sql_column_data

        elif str(var_column) == "SensorName":
            graph_data.sql_data_host_name = sql_column_data
        elif str(var_column) == "SensorUpTime":
            graph_data.sql_data_up_time = sql_column_data
        elif str(var_column) == "IP":
            graph_data.sql_data_ip = sql_column_data
        elif str(var_column) == "SystemTemp":
            graph_data.sql_data_cpu_temp = sql_column_data
        elif str(var_column) == "EnvironmentTemp":
            count = 0
            for data in sql_column_data:
                try:
                    sql_column_data[count] = str(float(data) + float(graph_data.temperature_offset))
                    count = count + 1
                except Exception as error:
                    count = count + 1
                    app_logger.app_logger.error("Bad SQL entry from Column 'EnvironmentTemp' - " + str(error))

            graph_data.sql_data_hat_temp = sql_column_data

        elif str(var_column) == "Pressure":
            graph_data.sql_data_pressure = sql_column_data
        elif str(var_column) == "Humidity":
            graph_data.sql_data_humidity = sql_column_data
        elif str(var_column) == "Lumen":
            graph_data.sql_data_lumen = sql_column_data
        elif str(var_column) == "Red":
            graph_data.sql_data_red = sql_column_data
        elif str(var_column) == "Green":
            graph_data.sql_data_green = sql_column_data
        elif str(var_column) == "Blue":
            graph_data.sql_data_blue = sql_column_data
        else:
            app_logger.app_logger.error(var_column + " - Does Not Exist")
    _plotly_graph(graph_data)
    app_logger.app_logger.debug("Interval DB Graph Complete")


def start_graph_trigger(graph_data):
    graph_data.graph_table = "TriggerData"
    app_logger.app_logger.debug("SQL Columns: " + str(graph_data.graph_columns))
    app_logger.app_logger.debug("SQL Table(s): " + str(graph_data.graph_table))
    app_logger.app_logger.debug("SQL Start DateTime: " + str(graph_data.graph_start))
    app_logger.app_logger.debug("SQL End DateTime: " + str(graph_data.graph_end))
    app_logger.app_logger.debug("SQL DataBase Location: " + str(graph_data.db_location))

    # Adjust dates to Database timezone in UTC 0
    new_time_offset = int(graph_data.datetime_offset) * -1
    get_sql_graph_start = _adjust_interval_datetime(graph_data.graph_start, new_time_offset)
    get_sql_graph_end = _adjust_interval_datetime(graph_data.graph_end, new_time_offset)

    for var_column in graph_data.graph_columns:
        var_sql_query = "SELECT " + \
                        str(var_column) + \
                        " FROM " + \
                        str(graph_data.graph_table) + \
                        " WHERE " + \
                        var_column + \
                        " IS NOT NULL AND DateTime BETWEEN datetime('" + \
                        str(get_sql_graph_start) + \
                        ".000') AND datetime('" + \
                        str(get_sql_graph_end) + \
                        ".000') LIMIT " + \
                        str(graph_data.max_sql_queries)

        sql_column_data = _get_sql_data(graph_data, var_sql_query)

        if str(var_column) == "DateTime":
            count = 0
            for data in sql_column_data:
                sql_column_data[count] = _adjust_trigger_datetime(data, int(graph_data.datetime_offset))
                count = count + 1

            graph_data.sql_data_time = sql_column_data

        elif str(var_column) == "SensorName":
            graph_data.sql_data_host_name = sql_column_data
        elif str(var_column) == "IP":
            graph_data.sql_data_ip = sql_column_data
        elif str(var_column) == "Acc_X":
            graph_data.sql_data_acc_x = sql_column_data
        elif str(var_column) == "Acc_Y":
            graph_data.sql_data_acc_y = sql_column_data
        elif str(var_column) == "Acc_Z":
            graph_data.sql_data_acc_z = sql_column_data
        elif str(var_column) == "Mag_X":
            graph_data.sql_data_mg_x = sql_column_data
        elif str(var_column) == "Mag_Y":
            graph_data.sql_data_mg_y = sql_column_data
        elif str(var_column) == "Mag_Z":
            graph_data.sql_data_mg_z = sql_column_data
        elif str(var_column) == "Gyro_X":
            graph_data.sql_data_gyro_x = sql_column_data
        elif str(var_column) == "Gyro_Y":
            graph_data.sql_data_gyro_y = sql_column_data
        elif str(var_column) == "Gyro_Z":
            graph_data.sql_data_gyro_z = sql_column_data
        else:
            app_logger.app_logger.error(var_column + " - Does Not Exist")
    _plotly_graph(graph_data)
    app_logger.app_logger.debug("Trigger DB Graph Complete")


def _adjust_interval_datetime(var_datetime, datetime_offset):
    """
    Adjusts the provided datetime by the provided hour offset and returns the result.

    Used for graph datetime's accurate to 1 second
    """
    try:
        var_datetime = datetime.strptime(var_datetime, "%Y-%m-%d %H:%M:%S")
    except Exception as error:
        app_logger.app_logger.error("Unable to Convert datetime string to datetime format - " + str(error))

    try:
        new_time = var_datetime + timedelta(hours=datetime_offset)
    except Exception as error:
        app_logger.app_logger.error("Unable to convert Hour Offset to int - " + str(error))
        new_time = var_datetime

    app_logger.app_logger.debug("Adjusted datetime: " + str(new_time))
    return str(new_time)


def _adjust_trigger_datetime(var_datetime, datetime_offset):
    """
    Adjusts the provided datetime by the provided hour offset and returns the result.

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


def _get_sql_data(graph_interval_data, sql_command):
    """ Execute SQLite3 command and return the results. """
    return_data = []

    try:
        conn = sqlite3.connect(str(graph_interval_data.db_location))
        c = conn.cursor()
        c.execute(sql_command)
        sql_column_data = c.fetchall()

        count = 0
        skip_count = 0
        for data in sql_column_data:
            if skip_count >= int(graph_interval_data.sql_queries_skip):
                return_data.append(str(data)[2:-3])
                skip_count = 0

            skip_count = skip_count + 1
            count = count + 1

        c.close()
        conn.close()
    except Exception as error:
        app_logger.app_logger.error("DB Error: " + str(error))

    app_logger.app_logger.debug("SQL execute Command: " + str(sql_command))
    app_logger.app_logger.debug("SQL Column Data Length: " + str(len(return_data)))
    return return_data


def _plotly_graph(graph_interval_data):
    """ Create and open a HTML offline Plotly graph with the data provided. """
    sub_plots = []
    row_count = 0
    graph_collection = []

    if len(graph_interval_data.sql_data_time) > 1:
        mark_red = dict(size=10,
                        color='rgba(255, 0, 0, .9)',
                        line=dict(width=2, color='rgb(0, 0, 0)'))

        mark_green = dict(size=10,
                          color='rgba(0, 255, 0, .9)',
                          line=dict(width=2, color='rgb(0, 0, 0)'))

        mark_blue = dict(size=10,
                         color='rgba(0, 0, 255, .9)',
                         line=dict(width=2, color='rgb(0, 0, 0)'))

        mark_yellow = dict(size=10,
                           color='rgba(255, 80, 80, .9)',
                           line=dict(width=2, color='rgb(0, 0, 0)'))

        if len(graph_interval_data.sql_data_host_name) > 1:
            row_count = row_count + 1
            first_hostname = graph_interval_data.sql_data_host_name[0]
            last_hostname = graph_interval_data.sql_data_host_name[-1]
            tmp_sensor_name = "First & Last Sensor Name: " + str(first_hostname) + " <---> " + str(last_hostname)

            trace_sensor_name = go.Scatter(x=graph_interval_data.sql_data_time,
                                           y=graph_interval_data.sql_data_host_name,
                                           name="Sensor Name")

            graph_collection.append([trace_sensor_name, row_count, 1])
            sub_plots.append(tmp_sensor_name)
            app_logger.app_logger.debug("Graph Sensor Sensor Name Added")

        if len(graph_interval_data.sql_data_up_time) > 1:
            row_count = row_count + 1

            trace_uptime = go.Scatter(x=graph_interval_data.sql_data_time,
                                      y=graph_interval_data.sql_data_up_time,
                                      name="Sensor Uptime")

            graph_collection.append([trace_uptime, row_count, 1])
            sub_plots.append('Sensor Uptime')
            app_logger.app_logger.debug("Graph Sensor Uptime Added")

        if len(graph_interval_data.sql_data_cpu_temp) > 1 or len(graph_interval_data.sql_data_hat_temp) > 1:
            row_count = row_count + 1

            trace_cpu_temp = go.Scatter(x=graph_interval_data.sql_data_time,
                                        y=graph_interval_data.sql_data_cpu_temp,
                                        name="CPU Temp")

            trace_hat_temp = go.Scatter(x=graph_interval_data.sql_data_time,
                                        y=graph_interval_data.sql_data_hat_temp,
                                        name="Environmental Temp")

            graph_collection.append([trace_cpu_temp, row_count, 1])
            graph_collection.append([trace_hat_temp, row_count, 1])
            sub_plots.append('CPU / Environmental Temp')
            app_logger.app_logger.debug("Graph CPU / Environmental Temp Added")

        if len(graph_interval_data.sql_data_pressure) > 2:
            row_count = row_count + 1

            trace_pressure = go.Scatter(x=graph_interval_data.sql_data_time,
                                        y=graph_interval_data.sql_data_pressure,
                                        name="Pressure hPa")

            graph_collection.append([trace_pressure, row_count, 1])
            sub_plots.append('Pressure hPa')
            app_logger.app_logger.debug("Graph Pressure hPa Added")

        if len(graph_interval_data.sql_data_humidity) > 2:
            row_count = row_count + 1

            trace_humidity = go.Scatter(x=graph_interval_data.sql_data_time,
                                        y=graph_interval_data.sql_data_humidity,
                                        name="Humidity %")

            graph_collection.append([trace_humidity, row_count, 1])
            sub_plots.append('Humidity')
            app_logger.app_logger.debug("Graph Humidity Added")

        if len(graph_interval_data.sql_data_lumen) > 2:
            row_count = row_count + 1

            trace_lumen = go.Scatter(x=graph_interval_data.sql_data_time,
                                     y=graph_interval_data.sql_data_lumen,
                                     name="Lumen",
                                     marker=mark_yellow)

            graph_collection.append([trace_lumen, row_count, 1])
            sub_plots.append('Lumen')
            app_logger.app_logger.debug("Graph Lumen Added")

        if len(graph_interval_data.sql_data_red) > 2:
            row_count = row_count + 1

            trace_red = go.Scatter(x=graph_interval_data.sql_data_time,
                                   y=graph_interval_data.sql_data_red,
                                   name="Red",
                                   marker=mark_red)

            trace_green = go.Scatter(x=graph_interval_data.sql_data_time,
                                     y=graph_interval_data.sql_data_green,
                                     name="Green",
                                     marker=mark_green)

            trace_blue = go.Scatter(x=graph_interval_data.sql_data_time,
                                    y=graph_interval_data.sql_data_blue,
                                    name="Blue",
                                    marker=mark_blue)

            graph_collection.append([trace_red, row_count, 1])
            graph_collection.append([trace_green, row_count, 1])
            graph_collection.append([trace_blue, row_count, 1])
            sub_plots.append('Colour RGB')
            app_logger.app_logger.debug("Graph Colour RGB Added")

        if len(graph_interval_data.sql_data_acc_x) > 2:
            row_count = row_count + 1

            trace_gyro_x = go.Scatter(x=graph_interval_data.sql_data_time,
                                      y=graph_interval_data.sql_data_acc_x,
                                      name="Accelerometer X",
                                      mode='markers')

            trace_gyro_y = go.Scatter(x=graph_interval_data.sql_data_time,
                                      y=graph_interval_data.sql_data_acc_y,
                                      name="Accelerometer Y",
                                      mode='markers')

            trace_gyro_z = go.Scatter(x=graph_interval_data.sql_data_time,
                                      y=graph_interval_data.sql_data_acc_z,
                                      name="Accelerometer Z",
                                      mode='markers')

            graph_collection.append([trace_gyro_x, row_count, 1])
            graph_collection.append([trace_gyro_y, row_count, 1])
            graph_collection.append([trace_gyro_z, row_count, 1])
            sub_plots.append('Accelerometer XYZ')
            app_logger.app_logger.debug("Graph Accelerometer XYZ Added")

        if len(graph_interval_data.sql_data_mg_x) > 2:
            row_count = row_count + 1

            trace_gyro_x = go.Scatter(x=graph_interval_data.sql_data_time,
                                      y=graph_interval_data.sql_data_mg_x,
                                      name="Magnetic X",
                                      mode='markers')

            trace_gyro_y = go.Scatter(x=graph_interval_data.sql_data_time,
                                      y=graph_interval_data.sql_data_mg_y,
                                      name="Magnetic Y",
                                      mode='markers')

            trace_gyro_z = go.Scatter(x=graph_interval_data.sql_data_time,
                                      y=graph_interval_data.sql_data_mg_z,
                                      name="Magnetic Z",
                                      mode='markers')

            graph_collection.append([trace_gyro_x, row_count, 1])
            graph_collection.append([trace_gyro_y, row_count, 1])
            graph_collection.append([trace_gyro_z, row_count, 1])
            sub_plots.append('Magnetic XYZ')
            app_logger.app_logger.debug("Graph Magnetic XYZ Added")

        if len(graph_interval_data.sql_data_gyro_x) > 2:
            row_count = row_count + 1

            trace_gyro_x = go.Scatter(x=graph_interval_data.sql_data_time,
                                      y=graph_interval_data.sql_data_gyro_x,
                                      name="Gyroscopic X",
                                      mode='markers')

            trace_gyro_y = go.Scatter(x=graph_interval_data.sql_data_time,
                                      y=graph_interval_data.sql_data_gyro_y,
                                      name="Gyroscopic Y",
                                      mode='markers')

            trace_gyro_z = go.Scatter(x=graph_interval_data.sql_data_time,
                                      y=graph_interval_data.sql_data_gyro_z,
                                      name="Gyroscopic Z",
                                      mode='markers')

            graph_collection.append([trace_gyro_x, row_count, 1])
            graph_collection.append([trace_gyro_y, row_count, 1])
            graph_collection.append([trace_gyro_z, row_count, 1])
            sub_plots.append('Gyroscopic XYZ')
            app_logger.app_logger.debug("Graph Gyroscopic XYZ Added")

        fig = tools.make_subplots(rows=row_count,
                                  cols=1,
                                  subplot_titles=sub_plots)

        for graph in graph_collection:
            fig.append_trace(graph[0], graph[1], graph[2])

        fig['layout'].update(title="Sensor IP: " + str(graph_interval_data.sql_data_ip[0]))

        if row_count > 4:
            fig['layout'].update(height=2048)

        try:
            plotly.offline.plot(fig, filename=graph_interval_data.save_to + 'SensorGraph.html', auto_open=True)
            app_logger.app_logger.debug("Graph Creation - OK")
        except Exception as error:
            app_logger.app_logger.error("Graph Creation - Failed - " + str(error))
            warn("Graph Failed", str(error))
    else:
        app_logger.app_logger.error(
            "Interval Graph Plot Failed - No SQL data found in Database within the selected Time Frame")
        warn("Error", "No SQL Data to Graph")
