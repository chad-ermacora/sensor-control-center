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
from app_modules import app_logger
from app_modules import app_variables
from app_modules import app_useful_functions
from app_modules import sensor_commands


class CreateSensorConfigWindow:
    """ Creates a GUI window for changing 1 or more sensor's configuration or installed sensors file. """

    def __init__(self, app, ip_selection, current_config):
        self.ip_selection = ip_selection
        self.current_config = current_config

        self.window = guizero.Window(app,
                                     title="Sensors Configuration",
                                     width=615,
                                     height=385,
                                     layout="grid",
                                     visible=False)

        self.text_select = guizero.Text(self.window,
                                        text="Select Sensor IPs in the main window",
                                        grid=[1, 1, 3, 1],
                                        color='#CB0000',
                                        align="left")

        self.textbox_config = guizero.TextBox(self.window,
                                              text=app_variables.default_sensor_config_text.strip(),
                                              grid=[1, 2],
                                              width=75,
                                              height=18,
                                              multiline=True,
                                              scrollbar=True,
                                              align="right")

        self.button_get_config = guizero.PushButton(self.window,
                                                    text="Get Sensor\nConfiguration",
                                                    command=self.button_get,
                                                    grid=[1, 10],
                                                    align="left")

        self.text_select_combo = guizero.Text(self.window,
                                              text="Select Configuration File to Edit",
                                              grid=[1, 10],
                                              color='blue',
                                              align="top")

        self.combo_dropdown_selection = guizero.Combo(self.window,
                                                      options=["Configuration", "Installed Sensors", "Wifi",
                                                               "Trigger Variances"],
                                                      grid=[1, 10],
                                                      command=self.combo_selection,
                                                      align="bottom")

        self.button_set_config = guizero.PushButton(self.window,
                                                    text="Set Sensor\nConfiguration",
                                                    command=self.button_set,
                                                    grid=[1, 10],
                                                    align="right")

        # Window Tweaks
        self.window.tk.resizable(False, False)
        self.textbox_config.bg = "black"
        self.textbox_config.text_color = "white"
        self.textbox_config.tk.config(insertbackground="red")

    def combo_selection(self):
        """ Select sensor 'Configuration' or 'Installed Sensors'. """
        if self.combo_dropdown_selection.value == "Installed Sensors":
            self.button_get_config.text = "Get Installed\nSensors"
            self.button_set_config.text = "Set Installed\nSensors"
            self.textbox_config.value = app_variables.default_installed_sensors_text.strip()
        elif self.combo_dropdown_selection.value == "Configuration":
            self.button_get_config.text = "Get Sensor\nConfiguration"
            self.button_set_config.text = "Set Sensor\nConfiguration"
            self.textbox_config.value = app_variables.default_sensor_config_text.strip()
        elif self.combo_dropdown_selection.value == "Wifi":
            self.button_get_config.text = "Get Sensor\nWifi Configuration"
            self.button_set_config.text = "Set Sensor\nWifi Configuration"
            self.textbox_config.value = app_variables.default_wifi_config_text.strip()
        elif self.combo_dropdown_selection.value == "Trigger Variances":
            self.button_get_config.text = "Get Sensor\nTrigger Variances"
            self.button_set_config.text = "Set Sensor\nTrigger Variances"
            self.textbox_config.value = app_variables.default_variance_config_text.strip()

    def button_get(self):
        """ Displays the selected configuration of the first selected and online sensor. """
        ip_list = self.ip_selection.get_verified_ip_list()
        if len(ip_list) > 0:
            network_commands = app_variables.CreateNetworkGetCommands()
            try:
                if self.combo_dropdown_selection.value == "Installed Sensors":
                    command = sensor_commands.CreateSensorNetworkCommand(ip_list[0],
                                                                         self.current_config.network_timeout_data,
                                                                         network_commands.installed_sensors_file)
                elif self.combo_dropdown_selection.value == "Configuration":
                    command = sensor_commands.CreateSensorNetworkCommand(ip_list[0],
                                                                         self.current_config.network_timeout_data,
                                                                         network_commands.sensor_configuration_file)
                elif self.combo_dropdown_selection.value == "Wifi":
                    command = sensor_commands.CreateSensorNetworkCommand(ip_list[0],
                                                                         self.current_config.network_timeout_data,
                                                                         network_commands.wifi_config_file)
                elif self.combo_dropdown_selection.value == "Trigger Variances":
                    command = sensor_commands.CreateSensorNetworkCommand(ip_list[0],
                                                                         self.current_config.network_timeout_data,
                                                                         network_commands.variance_config)
                else:
                    command = sensor_commands.CreateSensorNetworkCommand(ip_list[0],
                                                                         self.current_config.network_timeout_data,
                                                                             "")
                    command.command = ""

                self.textbox_config.value = str(sensor_commands.get_data(command))

            except Exception as error:
                app_logger.sensor_logger.error(str(error))
        else:
            app_useful_functions.no_ip_selected_message()

    def button_set(self):
        """ Sends the update configuration command to the Sensor Units IP, along with the new configuration. """
        network_commands = app_variables.CreateNetworkSendCommands()
        ip_list = self.ip_selection.get_verified_ip_list()
        threads = []

        if len(ip_list) > 0:
            for ip in ip_list:
                try:
                    if self.combo_dropdown_selection.value == "Installed Sensors":
                        command = sensor_commands.CreateSensorNetworkCommand(ip,
                                                                             self.current_config.network_timeout_data,
                                                                             network_commands.set_installed_sensors)
                    elif self.combo_dropdown_selection.value == "Configuration":
                        command = sensor_commands.CreateSensorNetworkCommand(ip,
                                                                             self.current_config.network_timeout_data,
                                                                             network_commands.set_configuration)
                    elif self.combo_dropdown_selection.value == "Wifi":
                        command = sensor_commands.CreateSensorNetworkCommand(ip,
                                                                             self.current_config.network_timeout_data,
                                                                             network_commands.set_wifi_configuration)
                    elif self.combo_dropdown_selection.value == "Trigger Variances":
                        command = sensor_commands.CreateSensorNetworkCommand(ip,
                                                                             self.current_config.network_timeout_data,
                                                                             network_commands.set_variance_configuration)
                    else:
                        command = sensor_commands.CreateSensorNetworkCommand(ip,
                                                                             self.current_config.network_timeout_data,
                                                                                 "")
                        command.command = ""

                    command.command_data = self.textbox_config.value.strip()

                    threads.append(Thread(target=sensor_commands.put_command, args=[command]))
                except Exception as error:
                    app_logger.sensor_logger.error(str(error))

            for thread in threads:
                thread.start()

            guizero.info("Sensors " + self.combo_dropdown_selection.value + " Set",
                         self.combo_dropdown_selection.value + " set & services restarted on:\n" + str(ip_list)[1:-1])
        else:
            app_useful_functions.no_ip_selected_message()
