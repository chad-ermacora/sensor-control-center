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
from datetime import datetime

from matplotlib import pyplot, animation, style

import app_modules.app_logger as app_logger
import app_modules.app_sensor_commands as app_sensor_commands
from app_modules.app_graph import CreateMeasurementsTypes, CreateSQLColumnsReadable, CreateSQLColumnNames
from app_modules.app_useful import convert_minutes_string

style.use("dark_background")


class CreateLiveGraph:
    """ Creates an object that starts a Live Graph. """

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
        """ Update the Live Graph Instance. """
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
        elif self.sensor_type == self.sql_column_names.six_chan_color[0]:
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
                    sensor_type_name = self.readable_column_names.colours
                    measurement_type = self.sensor_measurements.six_chan_color
                else:
                    sensor_reading = [round(float(colors[0]), 3),
                                      round(float(colors[1]), 3),
                                      round(float(colors[2]), 3)]
                    sensor_type_name = self.readable_column_names.colours
                    measurement_type = self.sensor_measurements.rgb

            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
                sensor_type_name = self.readable_column_names.colours
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
