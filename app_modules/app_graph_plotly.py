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

from guizero import warn
from plotly import tools, offline, graph_objs as go

import app_modules.app_logger as app_logger
from app_modules.app_graph import CreateSQLColumnNames, adjust_datetime


def start_plotly_graph(graph_data):
    """ Creates a Offline Plotly graph from a SQL database. """
    graph_data.graph_table = "IntervalData"
    app_logger.app_logger.debug("SQL Columns: " + str(graph_data.graph_columns))
    app_logger.app_logger.debug("SQL Table(s): " + str(graph_data.graph_table))
    app_logger.app_logger.debug("SQL Start DateTime: " + str(graph_data.graph_start))
    app_logger.app_logger.debug("SQL End DateTime: " + str(graph_data.graph_end))
    app_logger.app_logger.debug("SQL DataBase Location: " + str(graph_data.db_location))

    # Adjust dates to Database timezone in UTC 0
    sql_column_names = CreateSQLColumnNames()
    new_time_offset = int(graph_data.datetime_offset) * -1
    get_sql_graph_start = adjust_datetime(graph_data.graph_start, new_time_offset)
    get_sql_graph_end = adjust_datetime(graph_data.graph_end, new_time_offset)
    for var_column in graph_data.graph_columns:
        if var_column == sql_column_names.accelerometer_xyz[0] \
                or var_column == sql_column_names.magnetometer_xyz[0] \
                or var_column == sql_column_names.gyroscope_xyz[0]:
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
        if str(var_column) == sql_column_names.date_time:
            count = 0
            for data in sql_column_data:
                sql_column_data[count] = adjust_datetime(data, int(graph_data.datetime_offset))
                count = count + 1
            if graph_data.graph_table == "TriggerData":
                graph_data.sql_trigger_time = sql_column_data
            else:
                graph_data.sql_interval_time = sql_column_data

        elif str(var_column) == sql_column_names.ip:
            if graph_data.graph_table == "TriggerData":
                graph_data.sql_trigger_ip = sql_column_data
            else:
                graph_data.sql_interval_ip = sql_column_data
        elif str(var_column) == sql_column_names.sensor_name:
            if graph_data.graph_table == "TriggerData":
                graph_data.sql_trigger_host_name = sql_column_data
            else:
                graph_data.sql_interval_host_name = sql_column_data
        elif str(var_column) == sql_column_names.system_uptime:
            graph_data.sql_up_time = sql_column_data
        elif str(var_column) == sql_column_names.cpu_temp:
            graph_data.sql_cpu_temp = sql_column_data
        elif str(var_column) == sql_column_names.environmental_temp:
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
                    app_logger.app_logger.warning("Plotly Graph: " +
                                                  "One or more missing entries in 'EnvironmentTemp' or 'EnvTempOffset'")

            graph_data.sql_hat_temp = sql_column_data
        elif str(var_column) == sql_column_names.pressure:
            graph_data.sql_pressure = sql_column_data
        elif str(var_column) == sql_column_names.humidity:
            graph_data.sql_humidity = sql_column_data
        elif str(var_column) == sql_column_names.lumen:
            graph_data.sql_lumen = sql_column_data
        elif str(var_column) == sql_column_names.six_chan_color[0]:
            graph_data.sql_red = sql_column_data
        elif str(var_column) == sql_column_names.six_chan_color[1]:
            graph_data.sql_orange = sql_column_data
        elif str(var_column) == sql_column_names.six_chan_color[2]:
            graph_data.sql_yellow = sql_column_data
        elif str(var_column) == sql_column_names.six_chan_color[3]:
            graph_data.sql_green = sql_column_data
        elif str(var_column) == sql_column_names.six_chan_color[4]:
            graph_data.sql_blue = sql_column_data
        elif str(var_column) == sql_column_names.six_chan_color[5]:
            graph_data.sql_violet = sql_column_data

        elif str(var_column) == sql_column_names.accelerometer_xyz[0]:
            graph_data.sql_acc_x = sql_column_data
        elif str(var_column) == sql_column_names.accelerometer_xyz[1]:
            graph_data.sql_acc_y = sql_column_data
        elif str(var_column) == sql_column_names.accelerometer_xyz[2]:
            graph_data.sql_acc_z = sql_column_data
        elif str(var_column) == sql_column_names.magnetometer_xyz[0]:
            graph_data.sql_mg_x = sql_column_data
        elif str(var_column) == sql_column_names.magnetometer_xyz[1]:
            graph_data.sql_mg_y = sql_column_data
        elif str(var_column) == sql_column_names.magnetometer_xyz[2]:
            graph_data.sql_mg_z = sql_column_data
        elif str(var_column) == sql_column_names.gyroscope_xyz[0]:
            graph_data.sql_gyro_x = sql_column_data
        elif str(var_column) == sql_column_names.gyroscope_xyz[1]:
            graph_data.sql_gyro_y = sql_column_data
        elif str(var_column) == sql_column_names.gyroscope_xyz[2]:
            graph_data.sql_gyro_z = sql_column_data
        else:
            app_logger.app_logger.error(var_column + " - Does Not Exist")
    if graph_data.enable_plotly_webgl:
        _plotly_graph(graph_data)
    else:
        _plotly_graph_old(graph_data)
    app_logger.app_logger.debug("Interval DB Graph Complete")


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
        # Skip if all None
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

        mark_orange = dict(size=10,
                           color='rgba(255, 102, 0, .9)',
                           line=dict(width=2, color='rgb(0, 0, 0)'))

        mark_yellow = dict(size=10,
                           color='rgba(230, 230, 0, .9)',
                           line=dict(width=2, color='rgb(0, 0, 0)'))

        mark_green = dict(size=10,
                          color='rgba(0, 255, 0, .9)',
                          line=dict(width=2, color='rgb(0, 0, 0)'))

        mark_blue = dict(size=10,
                         color='rgba(0, 0, 255, .9)',
                         line=dict(width=2, color='rgb(0, 0, 0)'))

        mark_violet = dict(size=10,
                           color='rgba(153, 0, 204, .9)',
                           line=dict(width=2, color='rgb(0, 0, 0)'))

        mark_x = dict(size=5,
                      color='rgba(255, 0, 0, 1)')

        mark_y = dict(size=5,
                      color='rgba(0, 255, 0, 1)')

        mark_z = dict(size=5,
                      color='rgba(0, 0, 255, 1)')

        if len(graph_data.sql_interval_host_name) > 1:
            row_count = row_count + 1
            first_hostname = graph_data.sql_interval_host_name[0]
            last_hostname = graph_data.sql_interval_host_name[-1]
            tmp_sensor_name = "First & Last Sensor Name: " + str(first_hostname) + " <---> " + str(last_hostname)

            trace_sensor_name = go.Scattergl(x=graph_data.sql_interval_time,
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

                trace_sensor_name = go.Scattergl(x=graph_data.sql_trigger_time,
                                                 y=graph_data.sql_trigger_host_name,
                                                 name="Sensor Name")

                graph_collection.append([trace_sensor_name, row_count, 1])
                sub_plots.append(tmp_sensor_name)
                app_logger.app_logger.debug("Graph Sensor Sensor Name Added")

        if len(graph_data.sql_up_time) > 1:
            row_count = row_count + 1

            trace_uptime = go.Scattergl(x=graph_data.sql_interval_time,
                                        y=graph_data.sql_up_time,
                                        name="Sensor Uptime")

            graph_collection.append([trace_uptime, row_count, 1])
            sub_plots.append('Sensor Uptime')
            app_logger.app_logger.debug("Graph Sensor Uptime Added")

        if len(graph_data.sql_cpu_temp) > 1 or len(graph_data.sql_hat_temp) > 1:
            row_count = row_count + 1

            trace_cpu_temp = go.Scattergl(x=graph_data.sql_interval_time,
                                          y=graph_data.sql_cpu_temp,
                                          name="CPU Temp",
                                          marker=mark_red)

            trace_hat_temp = go.Scattergl(x=graph_data.sql_interval_time,
                                          y=graph_data.sql_hat_temp,
                                          name="Environmental Temp",
                                          marker=mark_green)

            graph_collection.append([trace_cpu_temp, row_count, 1])
            graph_collection.append([trace_hat_temp, row_count, 1])
            sub_plots.append('Temperature')
            app_logger.app_logger.debug("Graph CPU / Environmental Temperature Added")

        if len(graph_data.sql_pressure) > 2:
            row_count = row_count + 1

            trace_pressure = go.Scattergl(x=graph_data.sql_interval_time,
                                          y=graph_data.sql_pressure,
                                          name="Pressure hPa")

            graph_collection.append([trace_pressure, row_count, 1])
            sub_plots.append('Pressure hPa')
            app_logger.app_logger.debug("Graph Pressure hPa Added")

        if len(graph_data.sql_humidity) > 2:
            row_count = row_count + 1

            trace_humidity = go.Scattergl(x=graph_data.sql_interval_time,
                                          y=graph_data.sql_humidity,
                                          name="Humidity %")

            graph_collection.append([trace_humidity, row_count, 1])
            sub_plots.append('Humidity')
            app_logger.app_logger.debug("Graph Humidity Added")

        if len(graph_data.sql_lumen) > 2:
            row_count = row_count + 1

            trace_lumen = go.Scattergl(x=graph_data.sql_interval_time,
                                       y=graph_data.sql_lumen,
                                       name="Lumen",
                                       marker=mark_yellow)

            graph_collection.append([trace_lumen, row_count, 1])
            sub_plots.append('Lumen')
            app_logger.app_logger.debug("Graph Lumen Added")

        if len(graph_data.sql_red) > 2:
            row_count = row_count + 1

            trace_red = go.Scattergl(x=graph_data.sql_interval_time,
                                     y=graph_data.sql_red,
                                     name="Red",
                                     marker=mark_red)

            trace_orange = go.Scattergl(x=graph_data.sql_interval_time,
                                        y=graph_data.sql_orange,
                                        name="Orange",
                                        marker=mark_orange)

            trace_yellow = go.Scattergl(x=graph_data.sql_interval_time,
                                        y=graph_data.sql_yellow,
                                        name="Yellow",
                                        marker=mark_yellow)

            trace_green = go.Scattergl(x=graph_data.sql_interval_time,
                                       y=graph_data.sql_green,
                                       name="Green",
                                       marker=mark_green)

            trace_blue = go.Scattergl(x=graph_data.sql_interval_time,
                                      y=graph_data.sql_blue,
                                      name="Blue",
                                      marker=mark_blue)

            trace_violet = go.Scattergl(x=graph_data.sql_interval_time,
                                        y=graph_data.sql_violet,
                                        name="Violet",
                                        marker=mark_violet)

            graph_collection.append([trace_red, row_count, 1])
            graph_collection.append([trace_orange, row_count, 1])
            graph_collection.append([trace_yellow, row_count, 1])
            graph_collection.append([trace_green, row_count, 1])
            graph_collection.append([trace_blue, row_count, 1])
            graph_collection.append([trace_violet, row_count, 1])
            sub_plots.append('Electromagnetic Spectrum')
            app_logger.app_logger.debug("Graph Electromagnetic Spectrum Added")

        if len(graph_data.sql_acc_x) > 2:
            row_count = row_count + 1

            trace_gyro_x = go.Scattergl(x=graph_data.sql_trigger_time,
                                        y=graph_data.sql_acc_x,
                                        name="Accelerometer X",
                                        mode='markers',
                                        marker=mark_x)

            trace_gyro_y = go.Scattergl(x=graph_data.sql_trigger_time,
                                        y=graph_data.sql_acc_y,
                                        name="Accelerometer Y",
                                        mode='markers',
                                        marker=mark_y)

            trace_gyro_z = go.Scattergl(x=graph_data.sql_trigger_time,
                                        y=graph_data.sql_acc_z,
                                        name="Accelerometer Z",
                                        mode='markers',
                                        marker=mark_z)

            graph_collection.append([trace_gyro_x, row_count, 1])
            graph_collection.append([trace_gyro_y, row_count, 1])
            graph_collection.append([trace_gyro_z, row_count, 1])
            sub_plots.append('Accelerometer XYZ')
            app_logger.app_logger.debug("Graph Accelerometer XYZ Added")

        if len(graph_data.sql_mg_x) > 2:
            row_count = row_count + 1

            trace_gyro_x = go.Scattergl(x=graph_data.sql_trigger_time,
                                        y=graph_data.sql_mg_x,
                                        name="Magnetic X",
                                        mode='markers',
                                        marker=mark_x)

            trace_gyro_y = go.Scattergl(x=graph_data.sql_trigger_time,
                                        y=graph_data.sql_mg_y,
                                        name="Magnetic Y",
                                        mode='markers',
                                        marker=mark_y)

            trace_gyro_z = go.Scattergl(x=graph_data.sql_trigger_time,
                                        y=graph_data.sql_mg_z,
                                        name="Magnetic Z",
                                        mode='markers',
                                        marker=mark_z)

            graph_collection.append([trace_gyro_x, row_count, 1])
            graph_collection.append([trace_gyro_y, row_count, 1])
            graph_collection.append([trace_gyro_z, row_count, 1])
            sub_plots.append('Magnetic XYZ')
            app_logger.app_logger.debug("Graph Magnetic XYZ Added")

        if len(graph_data.sql_gyro_x) > 2:
            row_count = row_count + 1

            trace_gyro_x = go.Scattergl(x=graph_data.sql_trigger_time,
                                        y=graph_data.sql_gyro_x,
                                        name="Gyroscopic X",
                                        mode='markers',
                                        marker=mark_x)

            trace_gyro_y = go.Scattergl(x=graph_data.sql_trigger_time,
                                        y=graph_data.sql_gyro_y,
                                        name="Gyroscopic Y",
                                        mode='markers',
                                        marker=mark_y)

            trace_gyro_z = go.Scattergl(x=graph_data.sql_trigger_time,
                                        y=graph_data.sql_gyro_z,
                                        name="Gyroscopic Z",
                                        mode='markers',
                                        marker=mark_z)

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
            offline.plot(fig, filename=graph_data.save_to + 'PlotlySensorGraph.html', auto_open=True)
            app_logger.app_logger.debug("Plotly Graph Creation - OK")
        except Exception as error:
            app_logger.app_logger.error("Plotly Graph Creation - Failed - " + str(error))
            warn("Graph Failed", str(error))
    else:
        app_logger.app_logger.error(
            "Graph Plot Failed - No SQL data found in Database within the selected Time Frame")
        warn("Error", "No SQL Data to Graph")


def _plotly_graph_old(graph_data):
    """ Create and open a HTML offline Plotly graph with the data provided. """
    sub_plots = []
    row_count = 0
    graph_collection = []

    if len(graph_data.sql_interval_time) > 1 or len(graph_data.sql_trigger_time) > 1:
        mark_red = dict(size=10,
                        color='rgba(255, 0, 0, .9)',
                        line=dict(width=2, color='rgb(0, 0, 0)'))

        mark_orange = dict(size=10,
                           color='rgba(255, 102, 0, .9)',
                           line=dict(width=2, color='rgb(0, 0, 0)'))

        mark_yellow = dict(size=10,
                           color='rgba(230, 230, 0, .9)',
                           line=dict(width=2, color='rgb(0, 0, 0)'))

        mark_green = dict(size=10,
                          color='rgba(0, 255, 0, .9)',
                          line=dict(width=2, color='rgb(0, 0, 0)'))

        mark_blue = dict(size=10,
                         color='rgba(0, 0, 255, .9)',
                         line=dict(width=2, color='rgb(0, 0, 0)'))

        mark_violet = dict(size=10,
                           color='rgba(153, 0, 204, .9)',
                           line=dict(width=2, color='rgb(0, 0, 0)'))

        mark_x = dict(size=3,
                      color='rgba(255, 0, 0, 1)')

        mark_y = dict(size=3,
                      color='rgba(0, 255, 0, 1)')

        mark_z = dict(size=3,
                      color='rgba(0, 0, 255, 1)')

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
                                        name="CPU Temp",
                                        marker=mark_red)

            trace_hat_temp = go.Scatter(x=graph_data.sql_interval_time,
                                        y=graph_data.sql_hat_temp,
                                        name="Environmental Temp",
                                        marker=mark_green)

            graph_collection.append([trace_cpu_temp, row_count, 1])
            graph_collection.append([trace_hat_temp, row_count, 1])
            sub_plots.append('Temperature')
            app_logger.app_logger.debug("Graph CPU / Environmental Temperature Added")

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

            trace_orange = go.Scatter(x=graph_data.sql_interval_time,
                                      y=graph_data.sql_orange,
                                      name="Orange",
                                      marker=mark_orange)

            trace_yellow = go.Scatter(x=graph_data.sql_interval_time,
                                      y=graph_data.sql_yellow,
                                      name="Yellow",
                                      marker=mark_yellow)

            trace_green = go.Scatter(x=graph_data.sql_interval_time,
                                     y=graph_data.sql_green,
                                     name="Green",
                                     marker=mark_green)

            trace_blue = go.Scatter(x=graph_data.sql_interval_time,
                                    y=graph_data.sql_blue,
                                    name="Blue",
                                    marker=mark_blue)

            trace_violet = go.Scatter(x=graph_data.sql_interval_time,
                                      y=graph_data.sql_violet,
                                      name="Violet",
                                      marker=mark_violet)

            graph_collection.append([trace_red, row_count, 1])
            graph_collection.append([trace_orange, row_count, 1])
            graph_collection.append([trace_yellow, row_count, 1])
            graph_collection.append([trace_green, row_count, 1])
            graph_collection.append([trace_blue, row_count, 1])
            graph_collection.append([trace_violet, row_count, 1])
            sub_plots.append('Electromagnetic Spectrum')
            app_logger.app_logger.debug("Graph Electromagnetic Spectrum Added")

        if len(graph_data.sql_acc_x) > 2:
            row_count = row_count + 1

            trace_gyro_x = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_acc_x,
                                      name="Accelerometer X",
                                      mode='markers',
                                      marker=mark_x)

            trace_gyro_y = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_acc_y,
                                      name="Accelerometer Y",
                                      mode='markers',
                                      marker=mark_y)

            trace_gyro_z = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_acc_z,
                                      name="Accelerometer Z",
                                      mode='markers',
                                      marker=mark_z)

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
                                      mode='markers',
                                      marker=mark_x)

            trace_gyro_y = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_mg_y,
                                      name="Magnetic Y",
                                      mode='markers',
                                      marker=mark_y)

            trace_gyro_z = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_mg_z,
                                      name="Magnetic Z",
                                      mode='markers',
                                      marker=mark_z)

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
                                      mode='markers',
                                      marker=mark_x)

            trace_gyro_y = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_gyro_y,
                                      name="Gyroscopic Y",
                                      mode='markers',
                                      marker=mark_y)

            trace_gyro_z = go.Scatter(x=graph_data.sql_trigger_time,
                                      y=graph_data.sql_gyro_z,
                                      name="Gyroscopic Z",
                                      mode='markers',
                                      marker=mark_z)

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
            offline.plot(fig, filename=graph_data.save_to + 'PlotlySensorGraph.html', auto_open=True)
            app_logger.app_logger.debug("Plotly Graph Creation - OK")
        except Exception as error:
            app_logger.app_logger.error("Plotly Graph Creation - Failed - " + str(error))
            warn("Graph Failed", str(error))
    else:
        app_logger.app_logger.error(
            "Graph Plot Failed - No SQL data found in Database within the selected Time Frame")
        warn("Error", "No SQL Data to Graph")
