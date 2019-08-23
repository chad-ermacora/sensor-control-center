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
import guizero
from threading import Thread
from tkinter import simpledialog
from app_modules import app_logger
from app_modules import app_variables
from app_modules import app_useful_functions
from app_modules import sensor_commands

network_commands = app_variables.CreateNetworkSendCommands()
get_commands = app_variables.CreateNetworkGetCommands()


class CreateSensorDisplayWindow:
    """ Creates a GUI window for displaying sensor readings on the remote sensor Display. """

    def __init__(self, app, ip_selection, current_config):
        self.ip_selection = ip_selection
        self.current_config = current_config
        self.readable_column_names = app_variables.CreateSQLColumnsReadable()
        self.sql_columns = app_variables.CreateSQLColumnNames()

        self.window = guizero.Window(app,
                                     title="Remote Sensor Display",
                                     width=275,
                                     height=400,
                                     layout="grid",
                                     visible=False)

        self.text_temperature_offset = guizero.Text(self.window,
                                                    text="Env Temp Offset:",
                                                    color='green',
                                                    grid=[1, 11],
                                                    align="left")

        self.textbox_temperature_offset = guizero.TextBox(self.window,
                                                          text="",
                                                          width=5,
                                                          grid=[2, 11],
                                                          align="left")

        self.checkbox_default_offset = guizero.CheckBox(self.window,
                                                        text="Use Sensor\nDefault",
                                                        command=self._click_checkbox_offset,
                                                        grid=[2, 11],
                                                        align="right")

        self.checkbox_custom_text = guizero.CheckBox(self.window,
                                                     text="Text Message",
                                                     command=self._text_checkbox,
                                                     grid=[1, 16],
                                                     align="left")

        self.checkbox_master = guizero.CheckBox(self.window,
                                                text="All Sensors",
                                                command=self._master_checkbox,
                                                grid=[2, 16],
                                                align="left")

        self.text_space1 = guizero.Text(self.window,
                                        text=" ",
                                        grid=[1, 17],
                                        align="left")

        self.checkbox_up_time = guizero.CheckBox(self.window,
                                                 text=self.readable_column_names.system_uptime,
                                                 args=[self.sql_columns.system_uptime],
                                                 grid=[1, 27],
                                                 align="left")

        self.checkbox_cpu_temp = guizero.CheckBox(self.window,
                                                  text=self.readable_column_names.cpu_temp,
                                                  args=[self.sql_columns.cpu_temp],
                                                  grid=[1, 28],
                                                  align="left")

        self.checkbox_temperature = guizero.CheckBox(self.window,
                                                     text=self.readable_column_names.environmental_temp,
                                                     args=[self.sql_columns.environmental_temp],
                                                     grid=[1, 29],
                                                     align="left")

        self.checkbox_pressure = guizero.CheckBox(self.window,
                                                  text=self.readable_column_names.pressure,
                                                  args=[self.sql_columns.pressure],
                                                  grid=[1, 30],
                                                  align="left")

        self.checkbox_altitude = guizero.CheckBox(self.window,
                                                  text=self.readable_column_names.altitude,
                                                  args=[self.sql_columns.altitude],
                                                  grid=[1, 31],
                                                  align="left")

        self.checkbox_humidity = guizero.CheckBox(self.window,
                                                  text=self.readable_column_names.humidity,
                                                  args=[self.sql_columns.humidity],
                                                  grid=[1, 32],
                                                  align="left")

        self.checkbox_distance = guizero.CheckBox(self.window,
                                                  text=self.readable_column_names.distance,
                                                  args=[self.sql_columns.distance],
                                                  grid=[1, 33],
                                                  align="left")

        self.checkbox_gas = guizero.CheckBox(self.window,
                                             text=self.readable_column_names.gas,
                                             args=[self.sql_columns.gas],
                                             grid=[1, 34],
                                             align="left")

        self.checkbox_particulate_matter = guizero.CheckBox(self.window,
                                                            text=self.readable_column_names.particulate_matter,
                                                            args=[self.sql_columns.particulate_matter],
                                                            grid=[2, 27],
                                                            align="left")

        self.checkbox_lumen = guizero.CheckBox(self.window,
                                               text=self.readable_column_names.lumen,
                                               args=[self.sql_columns.lumen],
                                               grid=[2, 28],
                                               align="left")

        self.checkbox_colour = guizero.CheckBox(self.window,
                                                text=self.readable_column_names.colours,
                                                args=[self.sql_columns.rgb],
                                                grid=[2, 29],
                                                align="left")

        self.checkbox_ultra_violet = guizero.CheckBox(self.window,
                                                      text=self.readable_column_names.ultra_violet,
                                                      args=[self.sql_columns.ultra_violet],
                                                      grid=[2, 30],
                                                      align="left")

        self.checkbox_acc = guizero.CheckBox(self.window,
                                             text=self.readable_column_names.accelerometer_xyz,
                                             args=[self.sql_columns.accelerometer_xyz],
                                             grid=[2, 31],
                                             align="left")

        self.checkbox_mag = guizero.CheckBox(self.window,
                                             text=self.readable_column_names.magnetometer_xyz,
                                             args=[self.sql_columns.magnetometer_xyz],
                                             grid=[2, 32],
                                             align="left")

        self.checkbox_gyro = guizero.CheckBox(self.window,
                                              text=self.readable_column_names.gyroscope_xyz,
                                              args=[self.sql_columns.gyroscope_xyz],
                                              grid=[2, 33],
                                              align="left")

        self.text_space4 = guizero.Text(self.window,
                                        text=" ",
                                        grid=[1, 45],
                                        align="right")

        self.button_send_to_display = guizero.PushButton(self.window,
                                                         text="Show Reading\non Remote\nSensor Display",
                                                         command=self._remote_sensor_display_selection,
                                                         grid=[1, 46, 2, 1],
                                                         align="top")

        # Window Tweaks
        self.window.tk.resizable(False, False)
        self.checkbox_default_offset.value = 1
        self._set_config()
        self._click_checkbox_offset()
        self.checkbox_up_time.value = 0
        self.checkbox_temperature.value = 0
        self.checkbox_pressure.value = 0
        self.checkbox_humidity.value = 0
        self.checkbox_lumen.value = 0
        self.checkbox_colour.value = 0

    def _master_checkbox(self):
        """ Checks all sensor selection checkboxes. """
        if self.checkbox_master.value:
            self._enable_all_checkboxes()
        else:
            self._disable_all_checkboxes()

    def _text_checkbox(self):
        """ Uncheck and Disables other checkboxes. """
        self._disable_all_checkboxes()
        if self.checkbox_custom_text.value:
            self.checkbox_master.value = 0
            self.checkbox_master.disable()

            self.checkbox_up_time.disable()
            self.checkbox_cpu_temp.disable()
            self.checkbox_temperature.disable()
            self.checkbox_pressure.disable()
            self.checkbox_altitude.disable()
            self.checkbox_humidity.disable()
            self.checkbox_distance.disable()
            self.checkbox_gas.disable()
            self.checkbox_particulate_matter.disable()
            self.checkbox_lumen.disable()
            self.checkbox_colour.disable()
            self.checkbox_ultra_violet.disable()
            self.checkbox_acc.disable()
            self.checkbox_mag.disable()
            self.checkbox_gyro.disable()
        else:
            self.checkbox_master.enable()

            self.checkbox_up_time.enable()
            self.checkbox_cpu_temp.enable()
            self.checkbox_temperature.enable()
            self.checkbox_pressure.enable()
            self.checkbox_altitude.enable()
            self.checkbox_humidity.enable()
            self.checkbox_distance.enable()
            self.checkbox_gas.enable()
            self.checkbox_particulate_matter.enable()
            self.checkbox_lumen.enable()
            self.checkbox_colour.enable()
            self.checkbox_ultra_violet.enable()
            self.checkbox_acc.enable()
            self.checkbox_mag.enable()
            self.checkbox_gyro.enable()

    def _click_checkbox_offset(self):
        """ Enable or disable custom Env temperature offset for a graph. """
        if self.checkbox_default_offset.value:
            self.textbox_temperature_offset.disable()
            self.current_config.enable_custom_temp_offset = False
        else:
            self.textbox_temperature_offset.enable()
            self.current_config.enable_custom_temp_offset = True
            try:
                self.current_config.temperature_offset = float(self.textbox_temperature_offset.value)
            except Exception as error:
                self.current_config.temperature_offset = 0
                guizero.warn("Invalid Temperature Offset", "Please check and correct 'Env Temp Offset'")
                app_logger.app_logger.warning("Invalid Graph 'Env Temp Offset': " + str(error))

    def _set_config(self):
        """ Sets the programs Configuration to the provided settings. """
        self.textbox_temperature_offset.value = self.current_config.temperature_offset

    def _remote_sensor_display_selection(self):
        network_timeout = self.current_config.network_timeout_data
        ip_list = self.ip_selection.get_verified_ip_list()

        if len(ip_list) > 0:
            command_data = sensor_commands.CreateSensorNetworkCommand(ip_list[0], network_timeout, "")
            display_message = ""

            if self.checkbox_custom_text.value:
                add_text = simpledialog.askstring("Send Text to Sensor Display", "")
                display_message += add_text
            if self.checkbox_up_time.value:
                command_data.command = get_commands.system_uptime
                add_text = sensor_commands.get_data(command_data)
                display_message += " UpTime: " + add_text
            if self.checkbox_cpu_temp.value:
                command_data.command = get_commands.cpu_temp
                add_text = sensor_commands.get_data(command_data)
                display_message += " CPU Temp: " + add_text
            if self.checkbox_temperature.value:
                command_data.command = get_commands.environmental_temp
                add_text = sensor_commands.get_data(command_data)
                display_message += " Env Temp: " + add_text
            if self.checkbox_pressure.value:
                command_data.command = get_commands.pressure
                add_text = sensor_commands.get_data(command_data)
                display_message += " Pressure: " + add_text
            if self.checkbox_altitude.value:
                command_data.command = get_commands.altitude
                add_text = sensor_commands.get_data(command_data)
                display_message += " Altitude: " + add_text
            if self.checkbox_humidity.value:
                command_data.command = get_commands.humidity
                add_text = sensor_commands.get_data(command_data)
                display_message += " Humidity: " + add_text
            if self.checkbox_distance.value:
                command_data.command = get_commands.distance
                add_text = sensor_commands.get_data(command_data)
                display_message += " Distance: " + add_text
            if self.checkbox_gas.value:
                command_data.command = get_commands.gas_reduced
                add_text = sensor_commands.get_data(command_data)
                display_message += " GAS: " + add_text
            if self.checkbox_particulate_matter.value:
                command_data.command = get_commands.pm_1
                add_text = sensor_commands.get_data(command_data)
                display_message += " PM: " + add_text
            if self.checkbox_lumen.value:
                command_data.command = get_commands.lumen
                add_text = sensor_commands.get_data(command_data)
                display_message += " Lumen: " + add_text
            if self.checkbox_colour.value:
                command_data.command = get_commands.rgb
                add_text = sensor_commands.get_data(command_data)
                display_message += " Colour: " + add_text
            if self.checkbox_ultra_violet.value:
                command_data.command = get_commands.ultra_violet_a
                add_text = sensor_commands.get_data(command_data)
                display_message += " UV: " + add_text
            if self.checkbox_acc.value:
                command_data.command = get_commands.accelerometer_xyz
                add_text = sensor_commands.get_data(command_data)
                display_message += " Acc: " + add_text
            if self.checkbox_mag.value:
                command_data.command = get_commands.magnetometer_xyz
                add_text = sensor_commands.get_data(command_data)
                display_message += " Mag: " + add_text
            if self.checkbox_gyro.value:
                command_data.command = get_commands.gyroscope_xyz
                add_text = sensor_commands.get_data(command_data)
                display_message += " Gyro: " + add_text

            if display_message != "":
                self.send_text_message(display_message)
        else:
            app_useful_functions.no_ip_selected_message()

    def _get_column_checkboxes(self):
        """ Returns selected SQL Columns from the Graph Window, depending on the Data Source Selected. """
        sql_columns = app_variables.CreateSQLColumnNames()
        column_checkboxes = [sql_columns.date_time, sql_columns.sensor_name, sql_columns.ip]

        if self.checkbox_up_time.value:
            column_checkboxes.append(sql_columns.system_uptime)
        if self.checkbox_cpu_temp.value:
            column_checkboxes.append(sql_columns.cpu_temp)
        if self.checkbox_temperature.value:
            column_checkboxes.append(sql_columns.environmental_temp)
        if self.checkbox_pressure.value:
            column_checkboxes.append(sql_columns.pressure)
        if self.checkbox_altitude.value:
            column_checkboxes.append(sql_columns.altitude)
        if self.checkbox_humidity.value:
            column_checkboxes.append(sql_columns.humidity)
        if self.checkbox_distance.value:
            column_checkboxes.append(sql_columns.distance)
        if self.checkbox_gas.value:
            for column in sql_columns.gas:
                column_checkboxes.append(column)
        if self.checkbox_particulate_matter.value:
            for column in sql_columns.particulate_matter:
                column_checkboxes.append(column)
        if self.checkbox_lumen.value:
            column_checkboxes.append(sql_columns.lumen)
        if self.checkbox_colour.value:
            for column in sql_columns.six_chan_color:
                column_checkboxes.append(column)
        if self.checkbox_ultra_violet.value:
            for column in sql_columns.ultra_violet:
                column_checkboxes.append(column)
        if self.checkbox_acc.value:
            for column in sql_columns.accelerometer_xyz:
                column_checkboxes.append(column)
        if self.checkbox_mag.value:
            for column in sql_columns.magnetometer_xyz:
                column_checkboxes.append(column)
        if self.checkbox_gyro.value:
            for column in sql_columns.gyroscope_xyz:
                column_checkboxes.append(column)

        if self.checkbox_gyro.value or self.checkbox_mag.value or self.checkbox_acc.value:
            column_checkboxes.append(sql_columns.date_time)
            column_checkboxes.append(sql_columns.ip)
            column_checkboxes.append(sql_columns.sensor_name)

        app_logger.app_logger.debug(str(column_checkboxes))
        return column_checkboxes

    def _enable_all_for_live(self):
        """ Uncheck and allows all possible 'Live Graph' sensor type checkboxes. """
        self.checkbox_up_time.enable()
        self.checkbox_up_time.value = 0
        self.checkbox_cpu_temp.enable()
        self.checkbox_cpu_temp.value = 0
        self.checkbox_temperature.enable()
        self.checkbox_temperature.value = 0
        self.checkbox_pressure.enable()
        self.checkbox_pressure.value = 0
        self.checkbox_altitude.enable()
        self.checkbox_altitude.value = 0
        self.checkbox_humidity.enable()
        self.checkbox_humidity.value = 0
        self.checkbox_distance.enable()
        self.checkbox_distance.value = 0
        self.checkbox_gas.enable()
        self.checkbox_gas.value = 0
        self.checkbox_particulate_matter.enable()
        self.checkbox_particulate_matter.value = 0
        self.checkbox_lumen.enable()
        self.checkbox_lumen.value = 0
        self.checkbox_colour.enable()
        self.checkbox_colour.value = 0
        self.checkbox_ultra_violet.enable()
        self.checkbox_ultra_violet.value = 0
        self.checkbox_acc.enable()
        self.checkbox_acc.value = 0
        self.checkbox_mag.enable()
        self.checkbox_mag.value = 0
        self.checkbox_gyro.enable()
        self.checkbox_gyro.value = 0

    def _enable_all_checkboxes(self):
        """ Check all sensor type checkboxes. """
        self.checkbox_up_time.value = 1
        self.checkbox_cpu_temp.value = 1
        self.checkbox_temperature.value = 1
        self.checkbox_pressure.value = 1
        self.checkbox_altitude.value = 1
        self.checkbox_humidity.value = 1
        self.checkbox_distance.value = 1
        self.checkbox_gas.value = 1
        self.checkbox_particulate_matter.value = 1
        self.checkbox_lumen.value = 1
        self.checkbox_colour.value = 1
        self.checkbox_ultra_violet.value = 1
        self.checkbox_acc.value = 1
        self.checkbox_mag.value = 1
        self.checkbox_gyro.value = 1

    def _disable_all_checkboxes(self):
        """ Uncheck all sensor type checkboxes. """
        self.checkbox_up_time.value = 0
        self.checkbox_cpu_temp.value = 0
        self.checkbox_temperature.value = 0
        self.checkbox_pressure.value = 0
        self.checkbox_altitude.value = 0
        self.checkbox_humidity.value = 0
        self.checkbox_distance.value = 0
        self.checkbox_gas.value = 0
        self.checkbox_particulate_matter.value = 0
        self.checkbox_lumen.value = 0
        self.checkbox_colour.value = 0
        self.checkbox_ultra_violet.value = 0
        self.checkbox_acc.value = 0
        self.checkbox_mag.value = 0
        self.checkbox_gyro.value = 0

    def send_text_message(self, message):
        """ Sends Message to display on the sensors installed display. """
        app_logger.sensor_logger.debug("Sending message to sensor")

        network_timeout = self.current_config.network_timeout_data
        ip_list = self.ip_selection.get_verified_ip_list()
        ip = ip_list[0]
        if len(ip_list) > 0:
            app_logger.sensor_logger.debug("Sent Message: " + str(message))

            command = network_commands.display_message
            sensor_command = sensor_commands.CreateSensorNetworkCommand(ip, network_timeout, command)
            sensor_command.command_data = message
            message_thread = Thread(target=sensor_commands.put_command, args=[sensor_command])
            message_thread.daemon = True
            message_thread.start()
        else:
            app_useful_functions.no_ip_selected_message()
