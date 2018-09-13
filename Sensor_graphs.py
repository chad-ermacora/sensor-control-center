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
from datetime import datetime, timedelta
from tkinter import filedialog
from plotly import tools

get_sql_entries = 200000


def open_html(outfile):
    try:
        file_var = "file:///" + outfile
        webbrowser.open(file_var, new=2)
        print("open_html OK")
    except:
        print("open_html Failed")


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
        print("now_date end")
        print("now_date " + str(now_date))
        print("old_date " + str(old_date))
        print("end_date " + str(end_date))

    else:
        var_do = "proceed"

    if var_do != "end":
        if old_year > now_year:
            var_do = "skip"
            print("old_year is newer then now_year - skip")
            print("now_date " + str(now_date))
            print("old_date " + str(old_date))
            print("end_date " + str(end_date))

    return var_do


def get_sql_data(var_column, var_table, var_start, var_end, conn_db):
    var_sql_data = []
    print("\nvar_column " + str(var_column))
    print("var_table " + str(var_table))
    print("var_start " + str(var_start))
    print("var_end " + str(var_end))
    print("conn_db " + str(conn_db))

    var_sql_query = "SELECT " + \
        str(var_column) + \
        " FROM " + \
        str(var_table) + \
        " WHERE Time BETWEEN date('" + \
        str(var_start) + \
        "') AND date('" + \
        str(var_end) + \
        "') LIMIT " + \
        str(get_sql_entries)

    try:
        conn = sqlite3.connect(str(conn_db))
        c = conn.cursor()
        try:
            c.execute(var_sql_query)
            var_sql_data = c.fetchall()
            count = 0
            for i in var_sql_data:
                var_sql_data[count] = str(i)[2:-3]
                count = count + 1

            c.close()
            conn.close()
        except:
            print("Failed SQL Query Failed")
    except:
        print("Failed DB Connection")

    return var_sql_data


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


def sensors_graph(sql_start,
                  sql_end,
                  skip_row,
                  save_to_folder,
                  time_offset,
                  temp_offset,
                  graph_type):

    tmp_textbox_log1 = "\nStarting Sensor Graph\n"
    j = filedialog.askopenfilename()

    tmp_textbox_log1 = tmp_textbox_log1 + "\nsql_start " + str(sql_start)
    tmp_textbox_log1 = tmp_textbox_log1 + "\nsql_end " + str(sql_end)

    var_hostName = get_sql_data('hostName',
                                'Sensor_Data',
                                sql_start,
                                sql_end,
                                j)

    var_uptime = get_sql_data('uptime',
                              'Sensor_Data',
                              sql_start,
                              sql_end,
                              j)

    var_ip = get_sql_data('ip',
                          'Sensor_Data',
                          sql_start,
                          sql_end,
                          j)

    var_cpuTemp = get_sql_data('cpuTemp',
                               'Sensor_Data',
                               sql_start,
                               sql_end,
                               j)

    var_hatTemp = get_sql_data('hatTemp',
                               'Sensor_Data',
                               sql_start,
                               sql_end,
                               j)

    var_pressure = get_sql_data('pressure',
                                'Sensor_Data',
                                sql_start,
                                sql_end,
                                j)

    var_humidity = get_sql_data('humidity',
                                'Sensor_Data',
                                sql_start,
                                sql_end,
                                j)

    var_lumens = get_sql_data('lumens',
                              'Sensor_Data',
                              sql_start,
                              sql_end,
                              j)

    var_red = get_sql_data('red',
                           'Sensor_Data',
                           sql_start,
                           sql_end,
                           j)

    var_green = get_sql_data('green',
                             'Sensor_Data',
                             sql_start,
                             sql_end,
                             j)

    var_blue = get_sql_data('blue',
                            'Sensor_Data',
                            sql_start,
                            sql_end,
                            j)

    var_Time = get_sql_data('Time',
                            'Sensor_Data',
                            sql_start,
                            sql_end,
                            j)

    tmp_textbox_log1 = tmp_textbox_log1 + "\nSQL Query Successful"

    var_Time_final = []
    var_hostName_final = []
    var_uptime_final = []
    var_ip_final = []
    var_cpuTemp_final = []
    var_hatTemp_final = []
    var_pressure_final = []
    var_humidity_final = []
    var_lumens_final = []
    var_red_final = []
    var_green_final = []
    var_blue_final = []

    count = 0
    count2 = 0 + skip_row
    total_count = len(var_hostName)
    while count < total_count:
        if count2 == count:
            count2 = count2 + skip_row
            var_hostName_final.append(str(var_hostName[count]))
            
            try:
                var_uptime[count] = int((str(var_uptime[count]))) / 60
            except:
                print("Graph Uptime to int Failed - Bad data entry")

            var_uptime_final.append(str(var_uptime[count]))
            var_ip_final.append(str(var_ip[count]))
            
            try:
                var_cpuTemp_final.append(str(float(var_cpuTemp[count])))
                var_hatTemp_final.append(str(float(var_hatTemp[count]) +
                                             float(temp_offset)))
            except:
                print("Graph CPU or HAT Temp to float Failed - Bad data entry")

            var_pressure_final.append(str(var_pressure[count]))
            var_humidity_final.append(str(var_humidity[count]))
            var_lumens_final.append(str(var_lumens[count]))
            var_red_final.append(str(var_red[count]))
            var_green_final.append(str(var_green[count]))
            var_blue_final.append(str(var_blue[count]))
            
            try:
                tmp_time = datetime.strptime(var_Time[count], \
                                             "%Y-%m-%d %H:%M:%S")
                var_Time_new = tmp_time + timedelta(hours=time_offset)
                var_Time_final.append(str(var_Time_new))
            except:
                print("Graph Date str to datetime Failed - Bad data entry")

        count = count + 1

    tmp_textbox_log1 = tmp_textbox_log1 + "\nData Successfuly Imported"
    tmp_textbox_log1 = tmp_textbox_log1 + "\n\nHostName: " + \
        str(var_hostName_final[0])
    tmp_textbox_log1 = tmp_textbox_log1 + "\nIP: " + str(var_ip_final[0])
    tmp_textbox_log1 = tmp_textbox_log1 + \
        "\nvar_Time_final Data Points " + \
        str(len(var_Time_final))
    tmp_textbox_log1 = tmp_textbox_log1 + \
        "\nvar_uptime_final Data Points " + \
        str(len(var_uptime_final))
    tmp_textbox_log1 = tmp_textbox_log1 + \
        "\nvar_cpuTemp_final Data Points " + \
        str(len(var_cpuTemp_final))
    tmp_textbox_log1 = tmp_textbox_log1 + \
        "\nvar_hatTemp_final Data Points " + \
        str(len(var_hatTemp_final))
    tmp_textbox_log1 = tmp_textbox_log1 + \
        "\nvar_pressure_final Data Points " + \
        str(len(var_pressure_final))
    tmp_textbox_log1 = tmp_textbox_log1 + \
        "\nvar_lumens_final Data Points " + \
        str(len(var_lumens_final))
    tmp_textbox_log1 = tmp_textbox_log1 + \
        "\nvar_red_final Data Points " + \
        str(len(var_red_final))
    tmp_textbox_log1 = tmp_textbox_log1 + \
        "\nvar_green_final Data Points " + \
        str(len(var_green_final))
    tmp_textbox_log1 = tmp_textbox_log1 + \
        "\nvar_blue_final Data Points " + \
        str(len(var_blue_final))

    tmp_textbox_log1 = tmp_textbox_log1 + graph_trace(var_Time_final,
                                                      var_hostName_final,
                                                      var_uptime_final,
                                                      var_ip_final,
                                                      var_cpuTemp_final,
                                                      var_hatTemp_final,
                                                      var_pressure_final,
                                                      var_humidity_final,
                                                      var_lumens_final,
                                                      var_red_final,
                                                      var_green_final,
                                                      var_blue_final,
                                                      save_to_folder)


def graph_trace(var_Time_final,
                var_hostName_final,
                var_uptime_final,
                var_ip_final,
                var_cpuTemp_final,
                var_hatTemp_final,
                var_pressure_final,
                var_humidity_final,
                var_lumens_final,
                var_red_final,
                var_green_final,
                var_blue_final,
                save_to_folder):

    tmp_textbox_log1 = ''
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

    trace_cpuTemp = go.Scatter(x=var_Time_final,
                               y=var_cpuTemp_final,
                               name="CPU Temp")

    trace_hatTemp = go.Scatter(x=var_Time_final,
                               y=var_hatTemp_final,
                               name="HAT Temp")

    trace_pressure = go.Scatter(x=var_Time_final,
                                y=var_pressure_final,
                                name="Pressure hPa")

    trace_lumens = go.Scatter(x=var_Time_final,
                              y=var_lumens_final,
                              name="Lumens",
                              marker=mark_yellow)

    trace_red = go.Scatter(x=var_Time_final,
                           y=var_red_final,
                           name="Red",
                           marker=mark_red)

    trace_green = go.Scatter(x=var_Time_final,
                             y=var_green_final,
                             name="Green",
                             marker=mark_green)

    trace_blue = go.Scatter(x=var_Time_final,
                            y=var_blue_final,
                            name="Blue",
                            marker=mark_blue)

    trace_uptime = go.Scatter(x=var_Time_final,
                              y=var_uptime_final,
                              name="Sensor Uptime")

    fig = tools.make_subplots(rows=5,
                              cols=1,
                              subplot_titles=('CPU / HAT Temp',
                                              'Pressure hPa',
                                              'Lumens',
                                              'RGB',
                                              'Sensor Uptime Hours'))

    fig.append_trace(trace_cpuTemp, 1, 1)
    fig.append_trace(trace_hatTemp, 1, 1)
    fig.append_trace(trace_pressure, 2, 1)
    fig.append_trace(trace_lumens, 3, 1)
    fig.append_trace(trace_red, 4, 1)
    fig.append_trace(trace_green, 4, 1)
    fig.append_trace(trace_blue, 4, 1)
    fig.append_trace(trace_uptime, 5, 1)

    fig['layout'].update(title="Sensor Name on First/Last Data Point: \n" +
                         var_hostName_final[0] +
                         " / " +
                         var_hostName_final[-1] +
                         " - " +
                         var_ip_final[0],
                         height=2048)

    plotly.offline.plot(fig,
                        filename=save_to_folder + 'PlotSensors.html',
                        auto_open=True)

    tmp_textbox_log1 = tmp_textbox_log1 + "\n\nPlot Complete\n"

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
