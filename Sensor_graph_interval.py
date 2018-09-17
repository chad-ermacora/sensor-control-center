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
import plotly
import sqlite3
import plotly.graph_objs as go
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta
from plotly import tools

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:  %(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = RotatingFileHandler('logs/Sensor_graph_interval_log.txt', maxBytes=256000, backupCount=5)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class CreateGraphIntervalData:
    logger.debug("CreateGraphIntervalData Instance Created")

    def __init__(self):
        self.db_location = ""
        self.save_file_to = ""
        self.skip_sql = 0
        self.temperature_offset = 0
        self.time_offset = 0
        self.graph_start = ""
        self.graph_end = ""
        self.graph_type = ""
        self.graph_table = "Sensor_Data"
        self.graph_columns = ["Time", "hostName", "uptime", "ip", "cpuTemp", "hatTemp",
                              "pressure", "humidity", "lumens", "red", "green", "blue",
                              "mg_X", "mg_Y", "mg_Z"]

        self.max_sql_queries = 200000
        # self.repeat_max_sql_query = 5

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
        self.sql_data_mg_x = []
        self.sql_data_mg_y = []
        self.sql_data_mg_z = []


def open_html(outfile):
    try:
        file_var = "file:///" + outfile
        webbrowser.open(file_var, new=2)
        logger.debug("Graph HTML File Opened - OK")
    except Exception as error:
        logger.error("Graph HTML File Opened - Failed - " + str(error))


def check_sql_end(var_date_end, var_date_now, var_date_old):
    now_year = str(var_date_now)[0:4]
    now_month = str(var_date_now)[5:7]
    now_day = str(var_date_now)[8:10]
    now_hour = str(var_date_now)[11:13]
    now_min = str(var_date_now)[14:16]
    now_sec = str(var_date_now)[17:19]
    now_date = int(now_year + now_month + now_day
                   + now_hour + now_min + now_sec)

    end_year = str(var_date_end)[0:4]
    end_month = str(var_date_end)[5:7]
    end_day = str(var_date_end)[8:10]
    end_hour = str(var_date_end)[11:13]
    end_min = str(var_date_end)[14:16]
    end_sec = str(var_date_end)[17:19]
    end_date = int(end_year + end_month + end_day +
                   end_hour + end_min + end_sec)

    old_year = str(var_date_old)[0:4]
    old_month = str(var_date_old)[5:7]
    old_day = str(var_date_old)[8:10]
    old_hour = str(var_date_old)[11:13]
    old_min = str(var_date_old)[14:16]
    old_sec = str(var_date_old)[17:19]
    old_date = int(old_year + old_month + old_day +
                   old_hour + old_min + old_sec)

    if now_date > end_date:
        var_do = "end"
        logger.debug("now_date end")
        logger.debug("now_date " + str(now_date))
        logger.debug("old_date " + str(old_date))
        logger.debug("end_date " + str(end_date))

    else:
        var_do = "proceed"

    if var_do != "end":
        if old_year > now_year:
            var_do = "skip"
            logger.debug("old_year is newer then now_year - skip")
            logger.debug("now_date " + str(now_date))
            logger.debug("old_date " + str(old_date))
            logger.debug("end_date " + str(end_date))

    return var_do


def start_graph(graph_interval_data):
    logger.debug("SQL Columns " + str(graph_interval_data.graph_columns))
    logger.debug("SQL Table(s) " + str(graph_interval_data.graph_table))
    logger.debug("SQL Start DateTime " + str(graph_interval_data.graph_start))
    logger.debug("SQL End DateTime " + str(graph_interval_data.graph_end))
    logger.debug("SQL DataBase Location " + str(graph_interval_data.db_location))

    graph_interval_data.graph_start = adjust_datetime(graph_interval_data.graph_start, graph_interval_data.time_offset)
    graph_interval_data.graph_end = adjust_datetime(graph_interval_data.graph_end, graph_interval_data.time_offset)

    for var_column in graph_interval_data.graph_columns:
        var_sql_query = "SELECT " + \
            str(var_column) + \
            " FROM " + \
            str(graph_interval_data.graph_table) + \
            " WHERE Time BETWEEN date('" + \
            str(graph_interval_data.graph_start) + \
            "') AND date('" + \
            str(graph_interval_data.graph_end) + \
            "') LIMIT " + \
            str(graph_interval_data.max_sql_queries)

        sql_column_data = get_sql_data(graph_interval_data, var_sql_query)

        if str(var_column) == "Time":
            graph_interval_data.sql_data_time = sql_column_data
        elif str(var_column) == "hostName":
            graph_interval_data.sql_data_host_name = sql_column_data
        elif str(var_column) == "uptime":
            graph_interval_data.sql_data_up_time = sql_column_data
        elif str(var_column) == "ip":
            graph_interval_data.sql_data_ip = sql_column_data
        elif str(var_column) == "cpuTemp":
            graph_interval_data.sql_data_cpu_temp = sql_column_data
        elif str(var_column) == "hatTemp":
            graph_interval_data.sql_data_hat_temp = sql_column_data
        elif str(var_column) == "pressure":
            graph_interval_data.sql_data_pressure = sql_column_data
        elif str(var_column) == "humidity":
            graph_interval_data.sql_data_humidity = sql_column_data
        elif str(var_column) == "lumens":
            graph_interval_data.sql_data_lumen = sql_column_data
        elif str(var_column) == "red":
            graph_interval_data.sql_data_red = sql_column_data
        elif str(var_column) == "green":
            graph_interval_data.sql_data_green = sql_column_data
        elif str(var_column) == "blue":
            graph_interval_data.sql_data_blue = sql_column_data
        elif str(var_column) == "mg_X":
            graph_interval_data.sql_data_mg_x = sql_column_data
        elif str(var_column) == "mg_Y":
            graph_interval_data.sql_data_mg_y = sql_column_data
        elif str(var_column) == "mg_Z":
            graph_interval_data.sql_data_mg_z = sql_column_data
        else:
            logger.error(var_column + " - Does Not Exist")

    trace_graph(graph_interval_data)


def adjust_datetime(var_datetime, time_offset):
    try:
        var_datetime = datetime.strptime(var_datetime, "%Y-%m-%d %H:%M:%S")
    except Exception as error:
        logger.error("datetime already converted from str - " + str(error))

    try:
        time_offset = int(time_offset)
    except Exception as error:
        logger.error("Hour Offset already converted from str - " + str(error))

    new_time = var_datetime + timedelta(hours=time_offset)

    return str(new_time)


def get_sql_data(graph_interval_data, sql_command):
    return_data = []
    try:
        conn = sqlite3.connect(str(graph_interval_data.db_location))
        c = conn.cursor()

        try:
            c.execute(sql_command)
            sql_column_data = c.fetchall()
            count = 0
            skip_count = 0
            for data in sql_column_data:
                if skip_count > int(graph_interval_data.skip_sql):
                    return_data.append(str(data)[2:-3])
                    skip_count = 0

                skip_count = skip_count + 1
                count = count + 1

            c.close()
            conn.close()

        except Exception as error:
            logger.error("Failed SQL Query Failed: " + str(error))

    except Exception as error:
        logger.error("Failed DB Connection: " + str(error))

    logger.debug("SQL execute Command " + str(sql_command))
    logger.debug("SQL Column Data Length: " + str(len(return_data)))
    print(return_data[6])
    return return_data


def trace_graph(graph_interval_data):
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

    trace_cpu_temp = go.Scatter(x=graph_interval_data.sql_data_time,
                                y=graph_interval_data.sql_data_cpu_temp,
                                name="CPU Temp")

    trace_hat_temp = go.Scatter(x=graph_interval_data.sql_data_time,
                                y=graph_interval_data.sql_data_hat_temp,
                                name="HAT Temp")

    trace_pressure = go.Scatter(x=graph_interval_data.sql_data_time,
                                y=graph_interval_data.sql_data_pressure,
                                name="Pressure hPa")

    trace_lumen = go.Scatter(x=graph_interval_data.sql_data_time,
                             y=graph_interval_data.sql_data_lumen,
                             name="Lumen",
                             marker=mark_yellow)

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

    trace_uptime = go.Scatter(x=graph_interval_data.sql_data_time,
                              y=graph_interval_data.sql_data_up_time,
                              name="Sensor Uptime")

    fig = tools.make_subplots(rows=5,
                              cols=1,
                              subplot_titles=('CPU / HAT Temp',
                                              'Pressure hPa',
                                              'Lumen',
                                              'RGB',
                                              'Sensor Uptime Hours'))

    fig.append_trace(trace_cpu_temp, 1, 1)
    fig.append_trace(trace_hat_temp, 1, 1)
    fig.append_trace(trace_pressure, 2, 1)
    fig.append_trace(trace_lumen, 3, 1)
    fig.append_trace(trace_red, 4, 1)
    fig.append_trace(trace_green, 4, 1)
    fig.append_trace(trace_blue, 4, 1)
    fig.append_trace(trace_uptime, 5, 1)

    fig['layout'].update(title="Sensor Name on First/Last Data Point: " +
                               "str(graph_interval_data.sql_data_host_name[0])" + " / " +
                               "str(graph_interval_data.sql_data_host_name[-1])" + " - " +
                               "str(graph_interval_data.sql_data_ip[0])",
                               height=2048)

    plotly.offline.plot(fig, filename=graph_interval_data.save_file_to + 'PlotSensors.html', auto_open=True)
