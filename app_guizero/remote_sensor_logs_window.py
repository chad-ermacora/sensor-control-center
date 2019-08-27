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
from app_modules import app_logger
from app_modules import app_variables
from app_modules import app_useful_functions
from app_modules import sensor_commands


class CreateSensorLogsWindow:
    """ Creates a GUI window for viewing and or downloading sensor logs. """

    def __init__(self, app, ip_selection, current_config):
        self.ip_selection = ip_selection
        self.current_config = current_config
        self.network_get_commands = app_variables.CreateNetworkGetCommands()

        self.window = guizero.Window(app,
                                     title="Sensor Logs",
                                     width=975,
                                     height=450,
                                     layout="grid",
                                     visible=False)

        self.app_menubar = guizero.MenuBar(self.window,
                                           toplevel=[["Download"]],
                                           options=[[["Download All Selected Sensors Logs",
                                                      self._download_logs]]])

        self.text_select_ip = guizero.Text(self.window,
                                           text="Select Sensor IPs in the main window",
                                           color="#CB0000",
                                           grid=[1, 1],
                                           align="left")

        self.text_choose = guizero.Text(self.window,
                                        text="Last lines of selected log",
                                        color="blue",
                                        grid=[1, 1],
                                        align="top")

        self.radio_log_type = guizero.ButtonGroup(self.window,
                                                  options=["Primary Log", "Network Log", "Sensors Log"],
                                                  horizontal="True",
                                                  grid=[1, 1],
                                                  align="right")

        self.textbox_log = guizero.TextBox(self.window,
                                           text="\nPlease select the log type in the top right" +
                                                " and press 'Update Sensor Log View' in the bottom right\n\n" +
                                                "You may also use the 'Download' menu in the top left to " +
                                                "download ALL logs from selected sensors to a chosen folder",
                                           grid=[1, 2],
                                           width=118,
                                           height=22,
                                           multiline=True,
                                           scrollbar=True,
                                           align="left")

        self.button_get = guizero.PushButton(self.window,
                                             text="Update Sensor\nLog View",
                                             command=self._get_log,
                                             grid=[1, 3],
                                             align="right")

        # Window Tweaks
        self.window.tk.resizable(False, False)
        self.textbox_log.bg = "black"
        self.textbox_log.text_color = "white"
        self.textbox_log.tk.config(insertbackground="red")

    def _get_log(self):
        """ Displays the chosen remote sensor log. """
        ip_list = self.ip_selection.get_verified_ip_list()
        if len(ip_list) > 0:
            network_timeout = self.current_config.network_timeout_data
            command_data = sensor_commands.CreateSensorNetworkCommand(ip_list[0], network_timeout, "GetNetworkLog")
            if self.radio_log_type.value == "Network Log":
                log = sensor_commands.get_data(command_data)
            elif self.radio_log_type.value == "Primary Log":
                command_data.command = "GetPrimaryLog"
                log = sensor_commands.get_data(command_data)
            elif self.radio_log_type.value == "Sensors Log":
                command_data.command = "GetSensorsLog"
                log = sensor_commands.get_data(command_data)
            else:
                app_logger.app_logger.error("Bad Log Request")
                log = "Bad Log Request"
            self.textbox_log.value = log
        else:
            app_useful_functions.no_ip_selected_message()

    def _download_logs(self):
        """ Download all selected and online sensors logs. """
        ip_list = self.ip_selection.get_verified_ip_list()
        if len(ip_list) > 0:
            network_command_data = sensor_commands.CreateSensorNetworkCommand("",
                                                                              self.current_config.network_timeout_data,
                                                                              self.network_get_commands.download_zipped_logs)
            for ip in ip_list:
                network_command_data.ip = ip
                network_command_data.check_for_port_in_ip()
                download_url = "https://" + \
                               network_command_data.ip + \
                               ":" + \
                               network_command_data.port + \
                               "/" + \
                               network_command_data.command
                print(download_url)
                sensor_commands.download_zipped_logs(download_url)
        else:
            app_useful_functions.no_ip_selected_message()
