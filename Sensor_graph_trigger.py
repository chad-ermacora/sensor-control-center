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
from tkinter import filedialog
from plotly import tools

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:  %(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = RotatingFileHandler('logs/Sensor_graph_trigger_log.txt', maxBytes=256000, backupCount=5)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

get_sql_entries = 200000


def motion_graph(sql_start,
                 sql_end,
                 save_location,
                 time_offset,
                 graph_type):

    tmp_textbox_log1 = "\nStarting Motion Graph\n"
    j = filedialog.askopenfilename()

    tmp_textbox_log1 = tmp_textbox_log1 + "\nsql_start " + str(sql_start)
    tmp_textbox_log1 = tmp_textbox_log1 + "\nsql_end " + str(sql_end)

    var_time_final = []
    var_x_final = []
    var_y_final = []
    var_z_final = []
    var_hostname_final = []

    try:
        var_count_now = 0
        var_time = get_sql_data("Time", "Motion_Data", sql_start, sql_end, j)
        var_ip = get_sql_data("IP", "Motion_Data", sql_start, sql_end, j)
        var_x = get_sql_data("X", "Motion_Data", sql_start, sql_end, j)
        var_y = get_sql_data("Y", "Motion_Data", sql_start, sql_end, j)
        var_z = get_sql_data("Z", "Motion_Data", sql_start, sql_end, j)
        var_hostname = get_sql_data("hostName", "Motion_Data",
                                    sql_start, sql_end, j)
        tmp_textbox_log1 = tmp_textbox_log1 + "\nSQL Data - Retrieved OK"

        for i in var_time:
            var_check = check_sql_end(sql_end, i, i)
            if var_check == "proceed":
                try:
                    var_x_final.append(float(var_x[var_count_now]))
                    var_y_final.append(float(var_y[var_count_now]))
                    var_z_final.append(float(var_z[var_count_now]))
                except:
                    print("Motion XYZ to float Failed - Bad data entry")

                var_hostname_final.append(str(var_hostname[var_count_now]))

                try:
                    tmp_time = datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
                    var_time_new = tmp_time + timedelta(hours=time_offset)
                    var_time_final.append(str(var_time_new))
                except:
                    print("Motion str datetime to datetime Failed - " + \
                          "Bad data entry")

            elif var_check == "skip":
                continue
            elif var_check == "end":
                break
            var_count_now = var_count_now + 1
        tmp_textbox_log1 = tmp_textbox_log1 + "\nSQL Data - Processed OK"
    except:
        tmp_textbox_log1 = tmp_textbox_log1 + \
            "\nSQL Data - Processing Failed, bad date format or No Data"

    try:
        var_Time2 = get_sql_data("Time",
                                 "Motion_Data",
                                 var_time_final[-1],
                                 sql_end,
                                 j)

        var_X2 = get_sql_data("X",
                              "Motion_Data",
                              var_time_final[-1],
                              sql_end,
                              j)

        var_Y2 = get_sql_data("Y",
                              "Motion_Data",
                              var_time_final[-1],
                              sql_end,
                              j)

        var_Z2 = get_sql_data("Z",
                              "Motion_Data",
                              var_time_final[-1],
                              sql_end,
                              j)

        var_hostName2 = get_sql_data("hostName",
                                     "Motion_Data",
                                     var_time_final[-1],
                                     sql_end,
                                     j)

        var_time2_date_old = var_time_final[-1]
        tmp_textbox_log1 = tmp_textbox_log1 + \
            "\nSQL Data Batch 2 - Retrieved OK"

        var_count_now = 0
        for i in var_Time2:
            var_check1 = check_sql_end(sql_end,
                                       i,
                                       var_time2_date_old)

            if var_check1 == "proceed":
                var_x_final.append(float(var_X2[var_count_now]))
                var_y_final.append(float(var_Y2[var_count_now]))
                var_z_final.append(float(var_Z2[var_count_now]))
                var_hostname_final.append(str(var_hostName2[var_count_now]))

                tmp_time = datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
                var_time_new = tmp_time + timedelta(hours=time_offset)
                var_time_final.append(str(var_time_new))

            elif var_check1 == "skip":
                continue
            elif var_check1 == "end":
                break
            var_count_now = var_count_now + 1
            var_time2_date_old = i
        tmp_textbox_log1 = tmp_textbox_log1 + \
            "\nSQL Data Batch 2 - Processed OK"
    except:
        tmp_textbox_log1 = tmp_textbox_log1 + \
            "\nSQL Data Batch 2 - " + \
            "Proccessing Failed, bad date format or No Data"

    tmp_textbox_log1 = tmp_textbox_log1 + "\nData Successfuly Imported"

    tmp_textbox_log1 = tmp_textbox_log1 + \
        "\n\nvar_Time_final Data Points " + \
        str(len(var_time_final))

    tmp_textbox_log1 = tmp_textbox_log1 + \
        "\nvar_X_final Data Points " + \
        str(len(var_x_final))

    tmp_textbox_log1 = tmp_textbox_log1 + \
        "\nvar_Y_final Data Points " +\
        str(len(var_y_final))

    tmp_textbox_log1 = tmp_textbox_log1 + \
        "\nvar_Z_final Data Points " + \
        str(len(var_z_final))

    tmp_textbox_log1 = tmp_textbox_log1 + \
        "\nvar_hostName_final Data Points " + \
        str(len(var_hostname_final))

    if graph_type == "scatterT3":
        graphmess1 = graph_scatterT3(var_time_final,
                                     var_x_final,
                                     var_y_final,
                                     var_z_final,
                                     var_ip,
                                     var_hostname_final,
                                     save_location)

        tmp_textbox_log1 = tmp_textbox_log1 + graphmess1

    elif graph_type == "Other":
        print("Other")

    return tmp_textbox_log1


def graph_scatterT3(var_Time,
                    var_X,
                    var_Y,
                    var_Z,
                    var_IP,
                    var_hostName,
                    save_location):

    tmp_textbox_log1 = ""
    trace_X = go.Scatter(x=var_Time, y=var_X, mode='markers', name="X")
    trace_Y = go.Scatter(x=var_Time, y=var_Y, mode='markers', name="Y")
    trace_Z = go.Scatter(x=var_Time, y=var_Z, mode='markers', name="Z")

    fig = tools.make_subplots(rows=3, cols=1, subplot_titles=('X', 'Y', 'Z'))
    fig.append_trace(trace_X, 1, 1)
    fig.append_trace(trace_Y, 2, 1)
    fig.append_trace(trace_Z, 3, 1)

    fig['layout'].update(title="Sensor Name on First/Last Data Point: \n" +
                         var_hostName[0] +
                         " / " +
                         var_hostName[-1] +
                         " - " +
                         var_IP[0],
                         height=1024)
    try:
        plotly.offline.plot(fig,
                            filename=save_location + 'PlotMotion.html',
                            auto_open=True)

        tmp_textbox_log1 = tmp_textbox_log1 + "\n\nPlot Complete\n"
    except:
        tmp_textbox_log1 = tmp_textbox_log1 + "\n\nPlot Failed\n"

    return tmp_textbox_log1
