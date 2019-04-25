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
from plotly import tools, offline

import app_modules.app_logger as app_logger
from app_modules.graphing import CreateSQLColumnNames, adjust_datetime
import app_modules.graphing_offline_extras as plot_extras


def start_plotly_graph(graph_data):
    """ Creates a Offline Plotly graph from a SQL database. """
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
            graph_data.sql_time = sql_column_data
        elif str(var_column) == sql_column_names.ip:
            graph_data.sql_ip = sql_column_data
        elif str(var_column) == sql_column_names.sensor_name:
            graph_data.sql_host_name = sql_column_data
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

                var_sql_query = "SELECT EnvTempOffset FROM " + \
                                str(graph_data.graph_table) + \
                                " WHERE DateTime BETWEEN datetime('" + \
                                str(get_sql_graph_start) + \
                                "') AND datetime('" + \
                                str(get_sql_graph_end) + \
                                "') LIMIT " + \
                                str(graph_data.max_sql_queries)

                sql_temp_offset_data = _get_sql_data(graph_data, var_sql_query)

                warn_message = False
                count = 0
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
    _plotly_graph(graph_data)
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
    graph_data.sub_plots = []
    graph_data.row_count = 0
    graph_data.graph_collection = []

    if len(graph_data.sql_time) > 1:
        if len(graph_data.sql_host_name) > 1:
            plot_extras.graph_host_name(graph_data)

        if len(graph_data.sql_up_time) > 1:
            plot_extras.graph_sql_uptime(graph_data)

        if len(graph_data.sql_cpu_temp) > 1 or len(graph_data.sql_hat_temp) > 1:
            plot_extras.graph_sql_cpu_env_temperature(graph_data)

        if len(graph_data.sql_pressure) > 2:
            plot_extras.graph_sql_pressure(graph_data)

        if len(graph_data.sql_humidity) > 2:
            plot_extras.graph_sql_humidity(graph_data)

        if len(graph_data.sql_lumen) > 2:
            plot_extras.graph_sql_lumen(graph_data)

        if len(graph_data.sql_red) > 2:
            plot_extras.graph_sql_ems_colours(graph_data)

        if len(graph_data.sql_acc_x) > 2:
            plot_extras.graph_sql_accelerometer(graph_data)

        if len(graph_data.sql_mg_x) > 2:
            plot_extras.graph_sql_magnetometer(graph_data)

        if len(graph_data.sql_gyro_x) > 2:
            plot_extras.graph_sql_gyroscope(graph_data)

        fig = tools.make_subplots(rows=graph_data.row_count, cols=1, subplot_titles=graph_data.sub_plots)

        for graph in graph_data.graph_collection:
            fig.add_trace(graph[0], graph[1], graph[2])
        if len(graph_data.sql_ip) > 1:
            fig['layout'].update(title="Sensor IP: " + str(graph_data.sql_ip[0]))

        if graph_data.row_count > 4:
            fig['layout'].update(height=2048)

        try:
            offline.plot(fig, filename=graph_data.save_to + 'PlotlySensorGraph.html', auto_open=True)
            app_logger.app_logger.debug("Plotly Graph Creation - OK")
        except Exception as error:
            app_logger.app_logger.error("Plotly Graph Creation - Failed - " + str(error))
            warn("Graph Failed", str(error))
    else:
        app_logger.app_logger.error("Graph Plot Failed - No SQL data found in Database within the selected Time Frame")
        warn("Error", "No SQL Data to Graph")
