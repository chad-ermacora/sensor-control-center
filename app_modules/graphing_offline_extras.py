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
from plotly import graph_objs as go
from app_modules import app_logger
from app_modules import graphing_variables


def graph_host_name(graph_data):
    """ Add Host Name to the plotly graph. """
    graph_data.row_count = graph_data.row_count + 1
    first_hostname = graph_data.sql_host_name[0]
    last_hostname = graph_data.sql_host_name[-1]
    tmp_sensor_name = "First & Last Sensor Name: " + str(first_hostname) + " <---> " + str(last_hostname)

    graph_data.temp_text_name = "Sensor Name"
    graph_data.temp_sql = graph_data.sql_host_name

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_generic_line
    else:
        graph_data.set_marker = graphing_variables.mark_generic_dot

    if graph_data.enable_plotly_webgl:
        trace_sensor_name = _add_scatter_gl(graph_data)
    else:
        trace_sensor_name = _add_scatter_cpu(graph_data)

    graph_data.graph_collection.append([trace_sensor_name, graph_data.row_count, 1])
    graph_data.sub_plots.append(tmp_sensor_name)
    app_logger.app_logger.debug("Graph Sensor Sensor Name Added")


def graph_sql_uptime(graph_data):
    """ Add Sensor Uptime to the plotly graph. """
    graph_data.row_count = graph_data.row_count + 1

    graph_data.temp_text_name = "Sensor Uptime"
    graph_data.temp_sql = graph_data.sql_up_time

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_generic_line
    else:
        graph_data.set_marker = graphing_variables.mark_generic_dot

    if graph_data.enable_plotly_webgl:
        trace_uptime = _add_scatter_gl(graph_data)
    else:
        trace_uptime = _add_scatter_cpu(graph_data)

    graph_data.graph_collection.append([trace_uptime, graph_data.row_count, 1])
    graph_data.sub_plots.append("Sensor Uptime")
    app_logger.app_logger.debug("Graph Sensor Uptime Added")


def graph_sql_cpu_env_temperature(graph_data):
    """ Add CPU Temperature to the plotly graph. """
    graph_data.row_count = graph_data.row_count + 1

    graph_data.temp_text_name = "CPU Temp"
    graph_data.temp_sql = graph_data.sql_cpu_temp

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_red_line
    else:
        graph_data.set_marker = graphing_variables.mark_red_dot

    if graph_data.enable_plotly_webgl:
        trace_cpu_temp = _add_scatter_gl(graph_data)
    else:
        trace_cpu_temp = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "Environmental Temp"
    graph_data.temp_sql = graph_data.sql_hat_temp

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_green_line
    else:
        graph_data.set_marker = graphing_variables.mark_green_dot

    if graph_data.enable_plotly_webgl:
        trace_hat_temp = _add_scatter_gl(graph_data)
    else:
        trace_hat_temp = _add_scatter_cpu(graph_data)

    graph_data.graph_collection.append([trace_cpu_temp, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_hat_temp, graph_data.row_count, 1])
    graph_data.sub_plots.append('Temperature °C')
    app_logger.app_logger.debug("Graph CPU / Environmental Temperature Added")


def graph_sql_pressure(graph_data):
    """ Add Pressure to the plotly graph. """
    graph_data.row_count = graph_data.row_count + 1

    graph_data.temp_text_name = "Pressure hPa"
    graph_data.temp_sql = graph_data.sql_pressure

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_generic_line
    else:
        graph_data.set_marker = graphing_variables.mark_generic_dot

    if graph_data.enable_plotly_webgl:
        trace_pressure = _add_scatter_gl(graph_data)
    else:
        trace_pressure = _add_scatter_cpu(graph_data)

    graph_data.graph_collection.append([trace_pressure, graph_data.row_count, 1])
    graph_data.sub_plots.append('Pressure hPa')
    app_logger.app_logger.debug("Graph Pressure hPa Added")


def graph_sql_altitude(graph_data):
    """ Add Altitude to the plotly graph. """
    graph_data.row_count = graph_data.row_count + 1

    graph_data.temp_text_name = "Altitude meters"
    graph_data.temp_sql = graph_data.sql_altitude

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_generic_line
    else:
        graph_data.set_marker = graphing_variables.mark_generic_dot

    if graph_data.enable_plotly_webgl:
        trace_altitude = _add_scatter_gl(graph_data)
    else:
        trace_altitude = _add_scatter_cpu(graph_data)

    graph_data.graph_collection.append([trace_altitude, graph_data.row_count, 1])
    graph_data.sub_plots.append('Altitude meters')
    app_logger.app_logger.debug("Graph Altitude meters Added")


def graph_sql_humidity(graph_data):
    """ Add Humidity to the plotly graph. """
    graph_data.row_count = graph_data.row_count + 1

    graph_data.temp_text_name = "Humidity %"
    graph_data.temp_sql = graph_data.sql_humidity

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_generic_line
    else:
        graph_data.set_marker = graphing_variables.mark_generic_dot

    if graph_data.enable_plotly_webgl:
        trace_humidity = _add_scatter_gl(graph_data)
    else:
        trace_humidity = _add_scatter_cpu(graph_data)

    graph_data.graph_collection.append([trace_humidity, graph_data.row_count, 1])
    graph_data.sub_plots.append('Humidity')
    app_logger.app_logger.debug("Graph Humidity Added")


def graph_sql_distance(graph_data):
    """ Add Distance to the plotly graph. """
    graph_data.row_count = graph_data.row_count + 1

    graph_data.temp_text_name = "Distance meters?"
    graph_data.temp_sql = graph_data.sql_distance

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_generic_line
    else:
        graph_data.set_marker = graphing_variables.mark_generic_dot

    if graph_data.enable_plotly_webgl:
        trace_distance = _add_scatter_gl(graph_data)
    else:
        trace_distance = _add_scatter_cpu(graph_data)

    graph_data.graph_collection.append([trace_distance, graph_data.row_count, 1])
    graph_data.sub_plots.append('Distance meters?')
    app_logger.app_logger.debug("Graph Distance Added")


def graph_sql_gas(graph_data):
    """ Add Gas resistance to the plotly graph. """
    graph_data.row_count = graph_data.row_count + 1

    graph_data.temp_text_name = "Gas Resistance"
    graph_data.temp_sql = graph_data.sql_gas_resistance

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_red_line
    else:
        graph_data.set_marker = graphing_variables.mark_red_dot

    if graph_data.enable_plotly_webgl:
        trace_gas_resistance = _add_scatter_gl(graph_data)
    else:
        trace_gas_resistance = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "Gas Oxidising"
    graph_data.temp_sql = graph_data.sql_gas_oxidising

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_orange_line
    else:
        graph_data.set_marker = graphing_variables.mark_orange_dot

    if graph_data.enable_plotly_webgl:
        trace_gas_oxidising = _add_scatter_gl(graph_data)
    else:
        trace_gas_oxidising = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "Gas Reducing"
    graph_data.temp_sql = graph_data.sql_gas_reducing

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_yellow_line
    else:
        graph_data.set_marker = graphing_variables.mark_yellow_dot

    if graph_data.enable_plotly_webgl:
        trace_gas_reducing = _add_scatter_gl(graph_data)
    else:
        trace_gas_reducing = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "Gas NH3"
    graph_data.temp_sql = graph_data.sql_gas_nh3

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_green_line
    else:
        graph_data.set_marker = graphing_variables.mark_green_dot

    if graph_data.enable_plotly_webgl:
        trace_gas_nh3 = _add_scatter_gl(graph_data)
    else:
        trace_gas_nh3 = _add_scatter_cpu(graph_data)

    graph_data.graph_collection.append([trace_gas_resistance, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_gas_oxidising, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_gas_reducing, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_gas_nh3, graph_data.row_count, 1])
    graph_data.sub_plots.append('Gas Resistance')
    app_logger.app_logger.debug("Graph Gas Resistance Added")


def graph_sql_particulate_matter(graph_data):
    """ Add Particulate Matter to the plotly graph. """
    graph_data.row_count = graph_data.row_count + 1

    graph_data.temp_text_name = "PM1"
    graph_data.temp_sql = graph_data.sql_pm_1

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_red_line
    else:
        graph_data.set_marker = graphing_variables.mark_red_dot

    if graph_data.enable_plotly_webgl:
        trace_pm_1 = _add_scatter_gl(graph_data)
    else:
        trace_pm_1 = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "PM2.5"
    graph_data.temp_sql = graph_data.sql_pm_2_5

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_orange_line
    else:
        graph_data.set_marker = graphing_variables.mark_orange_dot

    if graph_data.enable_plotly_webgl:
        trace_pm_2_5 = _add_scatter_gl(graph_data)
    else:
        trace_pm_2_5 = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "PM10"
    graph_data.temp_sql = graph_data.sql_pm_10

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_yellow_line
    else:
        graph_data.set_marker = graphing_variables.mark_yellow_dot

    if graph_data.enable_plotly_webgl:
        trace_pm_10 = _add_scatter_gl(graph_data)
    else:
        trace_pm_10 = _add_scatter_cpu(graph_data)

    graph_data.graph_collection.append([trace_pm_1, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_pm_2_5, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_pm_10, graph_data.row_count, 1])
    graph_data.sub_plots.append('Particulate Matter')
    app_logger.app_logger.debug("Graph Particulate Matter Added")


def graph_sql_lumen(graph_data):
    """ Add Lumen to the plotly graph. """
    graph_data.row_count = graph_data.row_count + 1

    graph_data.temp_text_name = "Lumen"
    graph_data.temp_sql = graph_data.sql_lumen

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_yellow_line
    else:
        graph_data.set_marker = graphing_variables.mark_yellow_dot

    if graph_data.enable_plotly_webgl:
        trace_lumen = _add_scatter_gl(graph_data)
    else:
        trace_lumen = _add_scatter_cpu(graph_data)

    graph_data.graph_collection.append([trace_lumen, graph_data.row_count, 1])
    graph_data.sub_plots.append('Lumen')
    app_logger.app_logger.debug("Graph Lumen Added")


def graph_sql_ems_colours(graph_data):
    """ Add Electromagnetic Spectrum (usually the visible spectrum) to the plotly graph. """
    graph_data.row_count = graph_data.row_count + 1

    graph_data.temp_text_name = "Red"
    graph_data.temp_sql = graph_data.sql_red

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_red_line
    else:
        graph_data.set_marker = graphing_variables.mark_red_dot

    if graph_data.enable_plotly_webgl:
        trace_red = _add_scatter_gl(graph_data)
    else:
        trace_red = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "Orange"
    graph_data.temp_sql = graph_data.sql_orange

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_orange_line
    else:
        graph_data.set_marker = graphing_variables.mark_orange_dot

    if graph_data.enable_plotly_webgl:
        trace_orange = _add_scatter_gl(graph_data)
    else:
        trace_orange = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "Yellow"
    graph_data.temp_sql = graph_data.sql_yellow

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_yellow_line
    else:
        graph_data.set_marker = graphing_variables.mark_yellow_dot

    if graph_data.enable_plotly_webgl:
        trace_yellow = _add_scatter_gl(graph_data)
    else:
        trace_yellow = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "Green"
    graph_data.temp_sql = graph_data.sql_green

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_green_line
    else:
        graph_data.set_marker = graphing_variables.mark_green_dot

    if graph_data.enable_plotly_webgl:
        trace_green = _add_scatter_gl(graph_data)
    else:
        trace_green = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "Blue"
    graph_data.temp_sql = graph_data.sql_blue

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_blue_line
    else:
        graph_data.set_marker = graphing_variables.mark_blue_dot

    if graph_data.enable_plotly_webgl:
        trace_blue = _add_scatter_gl(graph_data)
    else:
        trace_blue = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "Violet"
    graph_data.temp_sql = graph_data.sql_violet

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_violet_line
    else:
        graph_data.set_marker = graphing_variables.mark_violet_dot

    if graph_data.enable_plotly_webgl:
        trace_violet = _add_scatter_gl(graph_data)
    else:
        trace_violet = _add_scatter_cpu(graph_data)

    graph_data.graph_collection.append([trace_red, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_orange, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_yellow, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_green, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_blue, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_violet, graph_data.row_count, 1])
    graph_data.sub_plots.append('Electromagnetic Spectrum')
    app_logger.app_logger.debug("Graph Electromagnetic Spectrum Added")


def graph_sql_ultra_violet(graph_data):
    """ Add Ultra Violet to the plotly graph. """
    graph_data.row_count = graph_data.row_count + 1

    graph_data.temp_text_name = "UV Index"
    graph_data.temp_sql = graph_data.sql_uv_index

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_red_line
    else:
        graph_data.set_marker = graphing_variables.mark_red_dot

    if graph_data.enable_plotly_webgl:
        trace_uv_index = _add_scatter_gl(graph_data)
    else:
        trace_uv_index = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "UVA"
    graph_data.temp_sql = graph_data.sql_uv_a

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_orange_line
    else:
        graph_data.set_marker = graphing_variables.mark_orange_dot

    if graph_data.enable_plotly_webgl:
        trace_uva = _add_scatter_gl(graph_data)
    else:
        trace_uva = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "UVB"
    graph_data.temp_sql = graph_data.sql_uv_b

    if graph_data.graph_table is "IntervalData":
        graph_data.set_marker = graphing_variables.mark_yellow_line
    else:
        graph_data.set_marker = graphing_variables.mark_yellow_dot

    if graph_data.enable_plotly_webgl:
        trace_uvb = _add_scatter_gl(graph_data)
    else:
        trace_uvb = _add_scatter_cpu(graph_data)

    graph_data.graph_collection.append([trace_uv_index, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_uva, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_uvb, graph_data.row_count, 1])
    graph_data.sub_plots.append('Ultra Violet')
    app_logger.app_logger.debug("Graph Ultra Violet Added")


def graph_sql_accelerometer(graph_data):
    """ Add Accelerometer to the plotly graph. """
    graph_data.row_count = graph_data.row_count + 1

    graph_data.temp_text_name = "Accelerometer X"
    graph_data.temp_sql = graph_data.sql_acc_x

    graph_data.set_marker = graphing_variables.mark_x_dot

    if graph_data.enable_plotly_webgl:
        trace_acc_x = _add_scatter_gl(graph_data)
    else:
        trace_acc_x = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "Accelerometer Y"
    graph_data.temp_sql = graph_data.sql_acc_y

    graph_data.set_marker = graphing_variables.mark_y_dot

    if graph_data.enable_plotly_webgl:
        trace_acc_y = _add_scatter_gl(graph_data)
    else:
        trace_acc_y = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "Accelerometer Z"
    graph_data.temp_sql = graph_data.sql_acc_z

    graph_data.set_marker = graphing_variables.mark_z_dot

    if graph_data.enable_plotly_webgl:
        trace_acc_z = _add_scatter_gl(graph_data)
    else:
        trace_acc_z = _add_scatter_cpu(graph_data)

    graph_data.graph_collection.append([trace_acc_x, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_acc_y, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_acc_z, graph_data.row_count, 1])
    graph_data.sub_plots.append('Accelerometer XYZ')
    app_logger.app_logger.debug("Graph Accelerometer XYZ Added")


def graph_sql_magnetometer(graph_data):
    """ Add Magnetometer to the plotly graph. """
    graph_data.row_count = graph_data.row_count + 1

    graph_data.temp_text_name = "Magnetic X"
    graph_data.temp_sql = graph_data.sql_mg_x

    graph_data.set_marker = graphing_variables.mark_x_dot

    if graph_data.enable_plotly_webgl:
        trace_mag_x = _add_scatter_gl(graph_data)
    else:
        trace_mag_x = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "Magnetic Y"
    graph_data.temp_sql = graph_data.sql_mg_y

    graph_data.set_marker = graphing_variables.mark_y_dot

    if graph_data.enable_plotly_webgl:
        trace_mag_y = _add_scatter_gl(graph_data)
    else:
        trace_mag_y = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "Magnetic Z"
    graph_data.temp_sql = graph_data.sql_mg_z

    graph_data.set_marker = graphing_variables.mark_z_dot

    if graph_data.enable_plotly_webgl:
        trace_mag_z = _add_scatter_gl(graph_data)
    else:
        trace_mag_z = _add_scatter_cpu(graph_data)

    graph_data.graph_collection.append([trace_mag_x, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_mag_y, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_mag_z, graph_data.row_count, 1])
    graph_data.sub_plots.append('Magnetic XYZ')
    app_logger.app_logger.debug("Graph Magnetic XYZ Added")


def graph_sql_gyroscope(graph_data):
    """ Add Gyroscope to the plotly graph. """
    graph_data.row_count = graph_data.row_count + 1

    graph_data.temp_text_name = "Gyroscopic X"
    graph_data.temp_sql = graph_data.sql_gyro_x

    graph_data.set_marker = graphing_variables.mark_x_dot

    if graph_data.enable_plotly_webgl:
        trace_gyro_x = _add_scatter_gl(graph_data)
    else:
        trace_gyro_x = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "Gyroscopic Y"
    graph_data.temp_sql = graph_data.sql_gyro_y

    graph_data.set_marker = graphing_variables.mark_y_dot

    if graph_data.enable_plotly_webgl:
        trace_gyro_y = _add_scatter_gl(graph_data)
    else:
        trace_gyro_y = _add_scatter_cpu(graph_data)

    graph_data.temp_text_name = "Gyroscopic Z"
    graph_data.temp_sql = graph_data.sql_gyro_z

    graph_data.set_marker = graphing_variables.mark_z_dot

    if graph_data.enable_plotly_webgl:
        trace_gyro_z = _add_scatter_gl(graph_data)
    else:
        trace_gyro_z = _add_scatter_cpu(graph_data)

    graph_data.graph_collection.append([trace_gyro_x, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_gyro_y, graph_data.row_count, 1])
    graph_data.graph_collection.append([trace_gyro_z, graph_data.row_count, 1])
    graph_data.sub_plots.append('Gyroscopic XYZ')
    app_logger.app_logger.debug("Graph Gyroscopic XYZ Added")


def _add_scatter_gl(graph_data):
    """ Use line graph for Interval data and dot markers for Trigger data. Uses OpenGL Rendering """
    if graph_data.graph_table is "IntervalData":
        trace = go.Scattergl(x=graph_data.sql_time,
                             y=graph_data.temp_sql,
                             name=graph_data.temp_text_name,
                             marker=graph_data.set_marker)
    else:
        trace = go.Scattergl(x=graph_data.sql_time,
                             y=graph_data.temp_sql,
                             name=graph_data.temp_text_name,
                             mode="markers",
                             marker=graph_data.set_marker)

    return trace


def _add_scatter_cpu(graph_data):
    """ Use line graph for Interval data and dot markers for Trigger data. Uses CPU Rendering """
    if graph_data.graph_table is "IntervalData":
        trace = go.Scatter(x=graph_data.sql_time,
                           y=graph_data.temp_sql,
                           name=graph_data.temp_text_name,
                           marker=graph_data.set_marker)
    else:
        trace = go.Scatter(x=graph_data.sql_time,
                           y=graph_data.temp_sql,
                           name=graph_data.temp_text_name,
                           mode="markers",
                           marker=graph_data.set_marker)

    return trace
