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
from app_modules import app_logger
from app_modules import app_variables
from app_modules import app_useful_functions
from app_modules import sensor_commands

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
        self.get_commands = app_variables.CreateNetworkGetCommands()

        self.sql_column_names = app_variables.CreateSQLColumnNames()
        self.readable_column_names = app_variables.CreateSQLColumnsReadable()
        self.sensor_measurements = app_variables.CreateMeasurementsTypes()

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
        command_data = sensor_commands.CreateSensorNetworkCommand(self.ip, network_timeout, "")

        command_data.command = self.get_commands.sensor_name
        sensor_name = sensor_commands.get_data(command_data)

        sensor_reading, sensor_type_name, measurement_type = self._get_sensor_reading_name_unit(command_data)
        try:
            self.ax1.clear()
            self.y.append(sensor_reading)
            self.x.append(x_frame)
            self.ax1.plot(self.x, self.y)

            if self.sensor_type is "SensorUpTime":
                sensor_reading = app_useful_functions.convert_minutes_string(sensor_reading)

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
            sensor_type_name = self.readable_column_names.system_uptime
            measurement_type = self.sensor_measurements.no_measurement

            command_data.command = self.get_commands.system_uptime
            try:
                sensor_reading = int(round(float(sensor_commands.get_data(command_data)), 0))
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
        elif self.sensor_type is self.sql_column_names.cpu_temp:
            sensor_type_name = self.readable_column_names.cpu_temp
            measurement_type = self.sensor_measurements.celsius

            command_data.command = self.get_commands.cpu_temp
            try:
                sensor_reading = round(float(sensor_commands.get_data(command_data)), 3)
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
        elif self.sensor_type is self.sql_column_names.environmental_temp:
            sensor_type_name = self.readable_column_names.environmental_temp
            measurement_type = self.sensor_measurements.celsius

            try:
                if self.current_config.enable_custom_temp_offset:
                    # Temp offset is set to programs when initiating Live Graph
                    pass
                else:
                    command_data.command = self.get_commands.env_temp_offset
                    try:
                        self.temperature_offset = float(sensor_commands.get_data(command_data))
                    except Exception as error:
                        app_logger.app_logger.warning("Live Graph - Invalid Sensor provided temp offset: " + str(error))
                        self.temperature_offset = 0.0

                command_data.command = self.get_commands.environmental_temp
                try:
                    sensor_reading = round(float(sensor_commands.get_data(command_data)) +
                                           float(self.temperature_offset), 3)
                except Exception as error:
                    app_logger.app_logger.warning("Live Graph - Invalid Env Temperature: " + str(error))
                    sensor_reading = self.readable_column_names.no_sensor
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
        elif self.sensor_type is self.sql_column_names.pressure:
            sensor_type_name = self.readable_column_names.pressure
            measurement_type = self.sensor_measurements.pressure

            command_data.command = self.get_commands.pressure
            try:
                sensor_reading = int(round(float(sensor_commands.get_data(command_data)), 0))
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
        elif self.sensor_type is self.sql_column_names.altitude:
            sensor_type_name = self.readable_column_names.altitude
            measurement_type = self.sensor_measurements.altitude

            command_data.command = self.get_commands.altitude
            try:
                sensor_reading = int(round(float(sensor_commands.get_data(command_data)), 0))
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
        elif self.sensor_type is self.sql_column_names.humidity:
            sensor_type_name = self.readable_column_names.humidity
            measurement_type = self.sensor_measurements.humidity

            command_data.command = self.get_commands.humidity
            try:
                sensor_reading = int(round(float(sensor_commands.get_data(command_data)), 0))
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
        elif self.sensor_type is self.sql_column_names.distance:
            sensor_type_name = self.readable_column_names.distance
            measurement_type = self.sensor_measurements.distance

            command_data.command = self.get_commands.distance
            try:
                sensor_reading = int(round(float(sensor_commands.get_data(command_data)), 0))
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
        elif self.sensor_type == self.sql_column_names.gas[0]:
            sensor_type_name = self.readable_column_names.gas + " - "
            measurement_type = self.sensor_measurements.gas

            try:
                command_data.command = self.get_commands.gas_index
                gas_index_reading = sensor_commands.get_data(command_data)
                command_data.command = self.get_commands.gas_oxidised
                gas_oxidising_reading = sensor_commands.get_data(command_data)
                command_data.command = self.get_commands.gas_reduced
                gas_reducing_reading = sensor_commands.get_data(command_data)
                command_data.command = self.get_commands.gas_nh3
                gas_nh3_reading = sensor_commands.get_data(command_data)

                sensor_reading = []
                count = 0
                if gas_index_reading != "NoSensor":
                    sensor_reading.append(round(float(gas_index_reading), 3))
                    sensor_type_name += "Resistance Index "
                    count += 1
                if gas_oxidising_reading != "NoSensor":
                    sensor_reading.append(round(float(gas_oxidising_reading), 3))
                    if count > 0:
                        sensor_type_name += "||"
                    sensor_type_name += " Oxidising "
                    count += 1
                if gas_reducing_reading != "NoSensor":
                    sensor_reading.append(round(float(gas_reducing_reading), 3))
                    if count > 0:
                        sensor_type_name += "||"
                    sensor_type_name += " Reducing "
                    count += 1
                if gas_nh3_reading != "NoSensor":
                    sensor_reading.append(round(float(gas_nh3_reading), 3))
                    if count > 0:
                        sensor_type_name += "||"
                    sensor_type_name += " NH3"
                    count += 1
                if count == 0:
                    sensor_reading = self.readable_column_names.no_sensor
            except Exception as error:
                app_logger.app_logger.warning("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
        elif self.sensor_type == self.sql_column_names.particulate_matter[0]:
            sensor_type_name = self.readable_column_names.particulate_matter
            measurement_type = self.sensor_measurements.particulate_matter

            try:
                command_data.command = self.get_commands.pm_1
                particulate_matter_1_reading = sensor_commands.get_data(command_data)
                command_data.command = self.get_commands.pm_2_5
                particulate_matter_2_5_reading = sensor_commands.get_data(command_data)
                command_data.command = self.get_commands.pm_10
                particulate_matter_10_reading = sensor_commands.get_data(command_data)

                sensor_reading = []
                count = 0
                if particulate_matter_1_reading != "NoSensor":
                    sensor_reading.append(round(float(particulate_matter_1_reading), 3))
                    sensor_type_name += " PM1 "
                    count += 1
                if particulate_matter_2_5_reading != "NoSensor":
                    sensor_reading.append(round(float(particulate_matter_2_5_reading), 3))
                    if count > 0:
                        sensor_type_name += "||"
                    sensor_type_name += " PM2.5 "
                    count += 1
                if particulate_matter_10_reading != "NoSensor":
                    sensor_reading.append(round(float(particulate_matter_10_reading), 3))
                    if count > 0:
                        sensor_type_name += "||"
                    sensor_type_name += " PM10"
                if count == 0:
                    sensor_reading = self.readable_column_names.no_sensor
            except Exception as error:
                app_logger.app_logger.warning("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
        elif self.sensor_type is self.sql_column_names.lumen:
            sensor_type_name = self.readable_column_names.lumen
            measurement_type = self.sensor_measurements.lumen

            command_data.command = self.get_commands.lumen
            try:
                sensor_reading = int(round(float(sensor_commands.get_data(command_data)), 0))
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
        elif self.sensor_type == self.sql_column_names.six_chan_color[0]:
            sensor_type_name = self.readable_column_names.colours
            measurement_type = self.sensor_measurements.rgb

            command_data.command = self.get_commands.rgb
            try:
                ems_colors = sensor_commands.get_data(command_data)[1:-1].split(",")

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
                    measurement_type = self.sensor_measurements.six_chan_color
                else:
                    sensor_reading = [round(float(colors[0]), 3),
                                      round(float(colors[1]), 3),
                                      round(float(colors[2]), 3)]
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
        elif self.sensor_type == self.sql_column_names.ultra_violet[0]:
            sensor_type_name = self.readable_column_names.ultra_violet
            measurement_type = self.sensor_measurements.ultra_violet

            try:
                command_data.command = self.get_commands.ultra_violet_a
                ultra_violet_a_reading = sensor_commands.get_data(command_data)
                command_data.command = self.get_commands.ultra_violet_b
                ultra_violet_b_reading = sensor_commands.get_data(command_data)

                sensor_reading = []
                count = 0
                if ultra_violet_a_reading != "NoSensor":
                    sensor_reading.append(round(float(ultra_violet_a_reading), 3))
                    sensor_type_name += " UVA "
                    count += 1
                if ultra_violet_b_reading != "NoSensor":
                    sensor_reading.append(round(float(ultra_violet_b_reading), 3))
                    if count > 0:
                        sensor_type_name += "||"
                    sensor_type_name += " UVB"
                if count == 0:
                    sensor_reading = self.readable_column_names.no_sensor
            except Exception as error:
                app_logger.app_logger.warning("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
        elif self.sensor_type == self.sql_column_names.accelerometer_xyz[0]:
            sensor_type_name = self.readable_column_names.accelerometer_xyz
            measurement_type = self.sensor_measurements.xyz

            command_data.command = self.get_commands.accelerometer_xyz
            try:
                var_x, var_y, var_z = sensor_commands.get_data(command_data)[1:-1].split(",")
                sensor_reading = [round(float(var_x), 3), round(float(var_y), 3), round(float(var_z), 3)]
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
        elif self.sensor_type == self.sql_column_names.magnetometer_xyz[0]:
            sensor_type_name = self.readable_column_names.magnetometer_xyz
            measurement_type = self.sensor_measurements.xyz

            command_data.command = self.get_commands.magnetometer_xyz
            try:
                var_x, var_y, var_z = sensor_commands.get_data(command_data)[1:-1].split(",")
                sensor_reading = [round(float(var_x), 3), round(float(var_y), 3), round(float(var_z), 3)]
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
        elif self.sensor_type == self.sql_column_names.gyroscope_xyz[0]:
            sensor_type_name = self.readable_column_names.gyroscope_xyz
            measurement_type = self.sensor_measurements.xyz

            command_data.command = self.get_commands.gyroscope_xyz
            try:
                var_x, var_y, var_z = sensor_commands.get_data(command_data)[1:-1].split(",")
                sensor_reading = [round(float(var_x), 3), round(float(var_y), 3), round(float(var_z), 3)]
            except Exception as error:
                app_logger.app_logger.debug("Live Graph - Invalid Sensor Data: " + str(error))
                sensor_reading = self.readable_column_names.no_sensor
        else:
            sensor_reading = "N/A"
            sensor_type_name = "Invalid Sensor"
            measurement_type = " Missing Program Support"

        return sensor_reading, sensor_type_name, measurement_type
