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


class CreateSQLColumnNames:
    def __init__(self):
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


class CreateSQLColumnsReadable:
    def __init__(self):
        self.no_sensor = ""
        self.date_time = "Date & Time"
        self.sensor_name = "Sensor Name"
        self.ip = "IP"
        self.system_uptime = "System Uptime"
        self.cpu_temp = "CPU Temperature"
        self.environmental_temp = "Enviro Temperature"
        self.pressure = "Pressure"
        self.humidity = "Humidity"
        self.lumen = "Lumen"
        self.rgb = "Colours"
        self.six_chan_color = "6 Channel Colour"
        self.accelerometer_xyz = "Accelerometer XYZ"
        self.magnetometer_xyz = "Magnetometer XYZ"
        self.gyroscope_xyz = "Gyroscope XYZ"


class CreateMeasurementsTypes:
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
    app_logger.app_logger.debug("CreateGraphData Instance Created")

    def __init__(self):
        self.db_location = ""
        self.save_to = ""
        self.graph_start = "1111-08-21 00:00:01"
        self.graph_end = "9999-01-01 00:00:01"
        self.datetime_offset = 0.0
        self.sql_queries_skip = 12
        self.bypass_sql_skip = False
        self.enable_custom_temp_offset = True
        self.temperature_offset = 0.0

        self.graph_columns = ["DateTime", "SensorName", "SensorUpTime", "IP", "SystemTemp", "EnvironmentTemp",
                              "EnvTempOffset", "Pressure", "Humidity", "Lumen", "Red", "Green", "Blue"]
        self.max_sql_queries = 200000

        # Graph data holders for SQL DataBase
        self.sql_interval_time = []
        self.sql_interval_ip = []
        self.sql_interval_host_name = []

        self.sql_up_time = []
        self.sql_cpu_temp = []
        self.sql_hat_temp = []
        self.sql_temp_offset = []
        self.sql_pressure = []
        self.sql_humidity = []
        self.sql_lumen = []
        self.sql_red = []
        self.sql_green = []
        self.sql_blue = []

        self.sql_trigger_time = []
        self.sql_trigger_ip = []
        self.sql_trigger_host_name = []
        self.sql_acc_x = []
        self.sql_acc_y = []
        self.sql_acc_z = []
        self.sql_mg_x = []
        self.sql_mg_y = []
        self.sql_mg_z = []
        self.sql_gyro_x = []
        self.sql_gyro_y = []
        self.sql_gyro_z = []


class CreateLiveGraph:
    def __init__(self, sensor_type, ip, current_config):
        self.sensor_type = sensor_type
        self.sensor_type_name = ""
        self.measurement_type = ""
        self.ip = ip
        self.current_config = current_config
        self.temperature_offset = self.current_config.temperature_offset
        self.get_commands = app_sensor_commands.CreateNetworkGetCommands()

        self.sql_column_names = CreateSQLColumnNames()
        self.readable_column_names = CreateSQLColumnsReadable()
        self.sensor_measurements = CreateMeasurementsTypes()

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
        network_timeout = self.current_config.network_timeout_data
        command_data = app_sensor_commands.CreateSensorNetworkCommand(self.ip, network_timeout, "")

        command_data.command = self.get_commands.sensor_name
        sensor_name = app_sensor_commands.get_data(command_data)

        sensor_reading, sensor_type_name, measurement_type = self._get_sensor_reading_name_unit(command_data)
        try:
            self.ax1.clear()
            self.y.append(sensor_reading)
            self.x.append(x_frame)
            self.ax1.plot(self.x, self.y)

            if self.sensor_type is "SensorUpTime":
                sensor_reading = convert_minutes_string(sensor_reading)

            pyplot.title(sensor_name + "  ||  " + self.ip + "\n" + sensor_type_name)
            pyplot.xlabel("Start Time: " + self.first_datetime +
                          "  ||  Updated: " + current_time +
                          "\nCurrent Reading: " + str(sensor_reading) + measurement_type)

            if self.sensor_type is "SensorUpTime":
                measurement_type = "Minutes"

            pyplot.ylabel(measurement_type)
            pyplot.xticks([])
        except Exception as error:
            app_logger.app_logger.error("Live Graph - Invalid Sensor Data: " + str(error))

    def _get_sensor_reading_name_unit(self, command_data):
        """ Returns the sensors reading(s), name and unit type based on the provided command_data object. """
        if self.sensor_type is self.sql_column_names.system_uptime:
            command_data.command = self.get_commands.system_uptime
            try:
                sensor_reading = int(round(float(app_sensor_commands.get_data(command_data)), 0))
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor

            sensor_type_name = self.readable_column_names.system_uptime
            measurement_type = self.sensor_measurements.no_measurement
        elif self.sensor_type is self.sql_column_names.cpu_temp:
            command_data.command = self.get_commands.cpu_temp
            try:
                sensor_reading = round(float(app_sensor_commands.get_data(command_data)), 3)
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor

            sensor_type_name = self.readable_column_names.cpu_temp
            measurement_type = self.sensor_measurements.celsius
        elif self.sensor_type is self.sql_column_names.environmental_temp:
            try:
                if self.current_config.enable_custom_temp_offset:
                    # Temp offset is set to programs when initiating Live Graph
                    pass
                else:
                    command_data.command = self.get_commands.env_temp_offset
                    try:
                        self.temperature_offset = float(app_sensor_commands.get_data(command_data))
                    except Exception as error:
                        app_logger.app_logger.warning("Live Graph - Invalid Sensor provided temp offset: " + str(error))
                        self.temperature_offset = 0.0

                command_data.command = self.get_commands.environmental_temp
                try:
                    sensor_reading = round(float(app_sensor_commands.get_data(command_data)) +
                                           float(self.temperature_offset), 3)
                except Exception as error:
                    app_logger.app_logger.warning("Live Graph - Invalid Env Temperature: " + str(error))
                    sensor_reading = self.readable_column_names.no_sensor
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor

            sensor_type_name = self.readable_column_names.environmental_temp
            measurement_type = self.sensor_measurements.celsius
        elif self.sensor_type is self.sql_column_names.pressure:
            command_data.command = self.get_commands.pressure
            try:
                sensor_reading = int(round(float(app_sensor_commands.get_data(command_data)), 0))
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor

            sensor_type_name = self.readable_column_names.pressure
            measurement_type = self.sensor_measurements.pressure
        elif self.sensor_type is self.sql_column_names.humidity:
            command_data.command = self.get_commands.humidity

            try:
                sensor_reading = int(round(float(app_sensor_commands.get_data(command_data)), 0))
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor

            sensor_type_name = self.readable_column_names.humidity
            measurement_type = self.sensor_measurements.humidity
        elif self.sensor_type is self.sql_column_names.lumen:
            command_data.command = self.get_commands.lumen
            try:
                sensor_reading = int(round(float(app_sensor_commands.get_data(command_data)), 0))
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor

            sensor_type_name = self.readable_column_names.lumen
            measurement_type = self.sensor_measurements.lumen
        elif self.sensor_type == self.sql_column_names.rgb[0]:
            try:
                command_data.command = self.get_commands.rgb
                ems_colors = app_sensor_commands.get_data(command_data)[1:-1].split(",")

                colors = []
                for color in ems_colors:
                    colors.append(color)

                if len(colors) > 3:
                    sensor_reading = [round(float(colors[0]), 3),
                                      round(float(colors[1]), 3),
                                      round(float(colors[2]), 3),
                                      round(float(colors[3]), 3),
                                      round(float(colors[4]), 3),
                                      round(float(colors[5]), 3)]
                    sensor_type_name = self.readable_column_names.six_chan_color
                    measurement_type = self.sensor_measurements.six_chan_color
                else:
                    sensor_reading = [round(float(colors[0]), 3),
                                      round(float(colors[1]), 3),
                                      round(float(colors[2]), 3)]
                    sensor_type_name = self.readable_column_names.rgb
                    measurement_type = self.sensor_measurements.rgb

            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
                sensor_type_name = self.readable_column_names.rgb
                measurement_type = self.sensor_measurements.rgb
        elif self.sensor_type == self.sql_column_names.accelerometer_xyz[0]:
            try:
                command_data.command = self.get_commands.accelerometer_xyz
                var_x, var_y, var_z = app_sensor_commands.get_data(command_data)[1:-1].split(",")
                sensor_reading = [round(float(var_x), 3), round(float(var_y), 3), round(float(var_z), 3)]
                sensor_type_name = self.readable_column_names.accelerometer_xyz
                measurement_type = self.sensor_measurements.xyz
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
                sensor_type_name = self.readable_column_names.accelerometer_xyz
                measurement_type = self.sensor_measurements.xyz
        elif self.sensor_type == self.sql_column_names.magnetometer_xyz[0]:
            try:
                command_data.command = self.get_commands.magnetometer_xyz
                var_x, var_y, var_z = app_sensor_commands.get_data(command_data)[1:-1].split(",")
                sensor_reading = [round(float(var_x), 3), round(float(var_y), 3), round(float(var_z), 3)]
                sensor_type_name = self.readable_column_names.magnetometer_xyz
                measurement_type = self.sensor_measurements.xyz
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
                sensor_type_name = self.readable_column_names.magnetometer_xyz
                measurement_type = self.sensor_measurements.xyz
        elif self.sensor_type == self.sql_column_names.gyroscope_xyz[0]:
            try:
                command_data.command = self.get_commands.gyroscope_xyz
                var_x, var_y, var_z = app_sensor_commands.get_data(command_data)[1:-1].split(",")
                sensor_reading = [round(float(var_x), 3), round(float(var_y), 3), round(float(var_z), 3)]
                sensor_type_name = self.readable_column_names.gyroscope_xyz
                measurement_type = self.sensor_measurements.xyz
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
                sensor_type_name = self.readable_column_names.gyroscope_xyz
                measurement_type = self.sensor_measurements.xyz
        else:
            sensor_reading = "N/A"
            sensor_type_name = "Invalid Sensor"
            measurement_type = " Missing Program Support"

        return sensor_reading, sensor_type_name, measurement_type


def start_plotly_graph(graph_data):
    graph_data.graph_table = "IntervalData"
    app_logger.app_logger.debug("SQL Columns: " + str(graph_data.graph_columns))
    app_logger.app_logger.debug("SQL Table(s): " + str(graph_data.graph_table))
    app_logger.app_logger.debug("SQL Start DateTime: " + str(graph_data.graph_start))
    app_logger.app_logger.debug("SQL End DateTime: " + str(graph_data.graph_end))
    app_logger.app_logger.debug("SQL DataBase Location: " + str(graph_data.db_location))

    # Adjust dates to Database timezone in UTC 0
    new_time_offset = int(graph_data.datetime_offset) * -1
    get_sql_graph_start = _adjust_datetime(graph_data.graph_start, new_time_offset)
    get_sql_graph_end = _adjust_datetime(graph_data.graph_end, new_time_offset)
    for var_column in graph_data.graph_columns:
        if var_column == "Acc_X" or var_column == "Mag_X" or var_column == "Gyro_X":
            graph_data.graph_table = "TriggerData"
            graph_data.bypass_sql_skip = True

        var_sql_query = "SELECT " + \
                        str(var_column) + \
                        " FROM " + \
                        str(graph_data.graph_table) + \
                        " WHERE DateTime BETWEEN datetime('" + \
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
                sql_column_data[count] = _adjust_datetime(data, int(graph_data.datetime_offset))
                count = count + 1
            if graph_data.graph_table == "TriggerData":
                graph_data.sql_trigger_time = sql_column_data
            else:
                graph_data.sql_interval_time = sql_column_data

        elif str(var_column) == "IP":
            if graph_data.graph_table == "TriggerData":
                graph_data.sql_trigger_ip = sql_column_data
            else:
                graph_data.sql_interval_ip = sql_column_data
        elif str(var_column) == "SensorName":
            if graph_data.graph_table == "TriggerData":
                graph_data.sql_trigger_host_name = sql_column_data
            else:
                graph_data.sql_interval_host_name = sql_column_data
        elif str(var_column) == "SensorUpTime":
            graph_data.sql_up_time = sql_column_data
        elif str(var_column) == "SystemTemp":
            graph_data.sql_cpu_temp = sql_column_data
        elif str(var_column) == "EnvironmentTemp":
            count = 0
            if graph_data.enable_custom_temp_offset:
                for data in sql_column_data:
                    try:
                        sql_column_data[count] = str(float(data) + float(graph_data.temperature_offset))
                        count = count + 1
                    except Exception as error:
                        count = count + 1
                        app_logger.app_logger.error("Bad SQL entry from Column 'EnvironmentTemp' - " + str(error))
            else:
                graph_data.bypass_sql_skip = False
                graph_data.graph_table = "IntervalData"
                get_sql_temp_offset_command = "SELECT EnvTempOffset FROM IntervalData " + \
                                              "WHERE DateTime BETWEEN datetime('" + \
                                              str(get_sql_graph_start) + \
                                              "') AND datetime('" + \
                                              str(get_sql_graph_end) + \
                                              "') LIMIT " + \
                                              str(graph_data.max_sql_queries)
                sql_temp_offset_data = _get_sql_data(graph_data, get_sql_temp_offset_command)

                warn_message = False
                for data in sql_column_data:
                    try:
                        sql_column_data[count] = str(float(data) + float(sql_temp_offset_data[count]))
                        count = count + 1
                    except IndexError:
                        count = count + 1
                        warn_message = True
                    except ValueError:
                        count = count + 1
                        warn_message = True

                if warn_message:
                    app_logger.app_logger.warning("One or more missing entries in 'EnvironmentTemp' or 'EnvTempOffset'")

            graph_data.sql_hat_temp = sql_column_data
        elif str(var_column) == "Pressure":
            graph_data.sql_pressure = sql_column_data
        elif str(var_column) == "Humidity":
            graph_data.sql_humidity = sql_column_data
        elif str(var_column) == "Lumen":
            graph_data.sql_lumen = sql_column_data
        elif str(var_column) == "Red":
            graph_data.sql_red = sql_column_data
        elif str(var_column) == "Green":
            graph_data.sql_green = sql_column_data
        elif str(var_column) == "Blue":
            graph_data.sql_blue = sql_column_data

        elif str(var_column) == "Acc_X":
            graph_data.sql_acc_x = sql_column_data
        elif str(var_column) == "Acc_Y":
            graph_data.sql_acc_y = sql_column_data
        elif str(var_column) == "Acc_Z":
            graph_data.sql_acc_z = sql_column_data
        elif str(var_column) == "Mag_X":
            graph_data.sql_mg_x = sql_column_data
        elif str(var_column) == "Mag_Y":
            graph_data.sql_mg_y = sql_column_data
        elif str(var_column) == "Mag_Z":
            graph_data.sql_mg_z = sql_column_data
        elif str(var_column) == "Gyro_X":
            graph_data.sql_gyro_x = sql_column_data
        elif str(var_column) == "Gyro_Y":
            graph_data.sql_gyro_y = sql_column_data
        elif str(var_column) == "Gyro_Z":
            graph_data.sql_gyro_z = sql_column_data
        else:
            app_logger.app_logger.error(var_column + " - Does Not Exist")
    _plotly_graph(graph_data)
    app_logger.app_logger.debug("Interval DB Graph Complete")


def _adjust_datetime(var_datetime, datetime_offset):
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
        database_connection = sqlite3.connect(str(graph_interval_data.db_location))
        sqlite_database = database_connection.cursor()
        sqlite_database.execute(sql_command)
        sql_column_data = sqlite_database.fetchall()
        sqlite_database.close()
        database_connection.close()
    except Exception as error:
        app_logger.app_logger.error("DB Error: " + str(error))
        sql_column_data = []

    count = 0
    skip_count = 0
    null_data_entries = 0
    for data in sql_column_data:
        if str(data) == "(None,)":
            null_data_entries += 1
        if skip_count >= int(graph_interval_data.sql_queries_skip) or graph_interval_data.bypass_sql_skip:
            return_data.append(str(data)[2:-3])
            skip_count = 0

        skip_count = skip_count + 1
        count = count + 1

    app_logger.app_logger.debug("SQL execute Command: " + str(sql_command))
    app_logger.app_logger.debug("SQL Column Data Length: " + str(len(return_data)))
    if null_data_entries == len(sql_column_data):
        # Skip if all NULL
        return []
    else:
        return return_data


def _plotly_graph(graph_data):
    """ Create and open a HTML offline Plotly graph with the data provided. """
    sub_plots = []
    row_count = 0
    graph_collection = []

    if len(graph_data.sql_interval_time) > 1 or len(graph_data.sql_trigger_time) > 1:
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

        if len(graph_data.sql_interval_host_name) > 1:
            row_count = row_count + 1
            first_hostname = graph_data.sql_interval_host_name[0]
            last_hostname = graph_data.sql_interval_host_name[-1]
            tmp_sensor_name = "First & Last Sensor Name: " + str(first_hostname) + " <---> " + str(last_hostname)

            trace_sensor_name = go.Scatter(x=graph_data.sql_interval_time,
                                           y=graph_data.sql_interval_host_name,
                                           name="Sensor Name")

            graph_collection.append([trace_sensor_name, row_count, 1])
            sub_plots.append(tmp_sensor_name)
            app_logger.app_logger.debug("Graph Sensor Sensor Name Added")
        else:
            if len(graph_data.sql_trigger_host_name) > 1:
                row_count = row_count + 1
                first_hostname = graph_data.sql_trigger_host_name[0]
                last_hostname = graph_data.sql_trigger_host_name[-1]
                tmp_sensor_name = "First & Last Sensor Name: " + str(first_hostname) + " <---> " + str(last_hostname)

                trace_sensor_name = go.Scatter(x=graph_data.sql_trigger_time,
                                               y=graph_data.sql_trigger_host_name,
                                               name="Sensor Name")

                graph_collection.append([trace_sensor_name, row_count, 1])
                sub_plots.append(tmp_sensor_name)
                app_logger.app_logger.debug("Graph Sensor Sensor Name Added")

        if len(graph_data.sql_up_time) > 1:
            row_count = row_count + 1

            trace_uptime = go.Scatter(x=graph_data.sql_interval_time,
                                      y=graph_data.sql_up_time,
                                      name="Sensor Uptime")

            graph_collection.append([trace_uptime, row_count, 1])
            sub_plots.append('Sensor Uptime')
            app_logger.app_logger.debug("Graph Sensor Uptime Added")

        if len(graph_data.sql_cpu_temp) > 1 or len(graph_data.sql_hat_temp) > 1:
            row_count = row_count + 1

            trace_cpu_temp = go.Scatter(x=graph_data.sql_interval_time,
                                        y=graph_data.sql_cpu_temp,
                                        name="CPU Temp")

            trace_hat_temp = go.Scatter(x=graph_data.sql_interval_time,
                                        y=graph_data.sql_hat_temp,
                                        name="Environmental Temp")

            graph_collection.append([trace_cpu_temp, row_count, 1])
            graph_collection.append([trace_hat_temp, row_count, 1])
            sub_plots.append('CPU / Environmental Temp')
            app_logger.app_logger.debug("Graph CPU / Environmental Temp Added")

        if len(graph_data.sql_pressure) > 2:
            row_count = row_count + 1

            trace_pressure = go.Scatter(x=graph_data.sql_interval_time,
                                        y=graph_data.sql_pressure,
                                        name="Pressure hPa")

            graph_collection.append([trace_pressure, row_count, 1])
            sub_plots.append('Pressure hPa')
            app_logger.app_logger.debug("Graph Pressure hPa Added")

        if len(graph_data.sql_humidity) > 2:
            row_count = row_count + 1

            trace_humidity = go.Scatter(x=graph_data.sql_interval_time,
                                        y=graph_data.sql_humidity,
                                        name="Humidity %")

            graph_collection.append([trace_humidity, row_count, 1])
            sub_plots.append('Humidity')
            app_logger.app_logger.debug("Graph Humidity Added")

        if len(graph_data.sql_lumen) > 2:
            row_count = row_count + 1

            trace_lumen = go.Scatter(x=graph_data.sql_interval_time,
                                     y=graph_data.sql_lumen,
                                     name="Lumen",
                                     marker=mark_yellow)

            graph_collection.append([trace_lumen, row_count, 1])
            sub_plots.append('Lumen')
            app_logger.app_logger.debug("Graph Lumen Added")

        if len(graph_data.sql_red) > 2:
            row_count = row_count + 1

            trace_red = go.Scatter(x=graph_data.sql_interval_time,
                                   y=graph_data.sql_red,
                                   name="Red",
                                   marker=mark_red)

            trace_green = go.Scatter(x=graph_data.sql_interval_time,
                                     y=graph_data.sql_green,
                                     name="Green",
                                     marker=mark_green)

            trace_blue = go.Scatter(x=graph_data.sql_interval_time,
                                    y=graph_data.sql_blue,
                                    name="Blue",
                                    marker=mark_blue)

            graph_collection.append([trace_red, row_count, 1])
            graph_collection.append([trace_green, row_count, 1])
            graph_collection.append([trace_blue, row_count, 1])
            sub_plots.append('Colour RGB')
            app_logger.app_logger.debug("Graph Colour RGB Added")

        if len(graph_data.sql_acc_x) > 2:
            row_count = row_count + 1

            trace_gyro_x = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_acc_x,
                                      name="Accelerometer X",
                                      mode='markers')

            trace_gyro_y = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_acc_y,
                                      name="Accelerometer Y",
                                      mode='markers')

            trace_gyro_z = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_acc_z,
                                      name="Accelerometer Z",
                                      mode='markers')

            graph_collection.append([trace_gyro_x, row_count, 1])
            graph_collection.append([trace_gyro_y, row_count, 1])
            graph_collection.append([trace_gyro_z, row_count, 1])
            sub_plots.append('Accelerometer XYZ')
            app_logger.app_logger.debug("Graph Accelerometer XYZ Added")

        if len(graph_data.sql_mg_x) > 2:
            row_count = row_count + 1

            trace_gyro_x = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_mg_x,
                                      name="Magnetic X",
                                      mode='markers')

            trace_gyro_y = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_mg_y,
                                      name="Magnetic Y",
                                      mode='markers')

            trace_gyro_z = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_mg_z,
                                      name="Magnetic Z",
                                      mode='markers')

            graph_collection.append([trace_gyro_x, row_count, 1])
            graph_collection.append([trace_gyro_y, row_count, 1])
            graph_collection.append([trace_gyro_z, row_count, 1])
            sub_plots.append('Magnetic XYZ')
            app_logger.app_logger.debug("Graph Magnetic XYZ Added")

        if len(graph_data.sql_gyro_x) > 2:
            row_count = row_count + 1

            trace_gyro_x = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_gyro_x,
                                      name="Gyroscopic X",
                                      mode='markers')

            trace_gyro_y = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_gyro_y,
                                      name="Gyroscopic Y",
                                      mode='markers')

            trace_gyro_z = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_gyro_z,
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
            fig.add_trace(graph[0], graph[1], graph[2])
        if len(graph_data.sql_interval_ip) > 1:
            fig['layout'].update(title="Sensor IP: " + str(graph_data.sql_interval_ip[0]))
        else:
            fig['layout'].update(title="Sensor IP: " + str(graph_data.sql_trigger_ip[0]))

        if row_count > 4:
            fig['layout'].update(height=2048)

        try:
            plotly.offline.plot(fig, filename=graph_data.save_to + 'PlotlySensorGraph.html', auto_open=True)
            app_logger.app_logger.debug("Plotly Graph Creation - OK")
        except Exception as error:
            app_logger.app_logger.error("Plotly Graph Creation - Failed - " + str(error))
            warn("Graph Failed", str(error))
    else:
        app_logger.app_logger.error(
            "Graph Plot Failed - No SQL data found in Database within the selected Time Frame")
        warn("Error", "No SQL Data to Graph")
