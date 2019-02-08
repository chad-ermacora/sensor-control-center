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
from threading import Thread
from tkinter import filedialog

from guizero import Window, Text, TextBox, ButtonGroup, PushButton, MenuBar, info, warn

import app_modules.app_logger as app_logger
import app_modules.app_sensor_commands as app_sensor_commands
from app_modules.app_useful import no_ip_selected_message


class CreateSensorLogsWindow:
    """ Creates a GUI window for viewing and or downloading sensor logs. """

    def __init__(self, app, ip_selection, current_config):
        self.ip_selection = ip_selection
        self.current_config = current_config

        self.window = Window(app,
                             title="Sensor Logs",
                             width=975,
                             height=450,
                             layout="grid",
                             visible=False)

        self.app_menubar = MenuBar(self.window,
                                   toplevel=[["Download"]],
                                   options=[[["Download All Selected Sensors Logs",
                                              self._download_logs]]])

        self.text_select_ip = Text(self.window,
                                   text="Select Sensor IPs in the main window",
                                   color="#CB0000",
                                   grid=[1, 1],
                                   align="left")

        self.text_choose = Text(self.window,
                                text="Last lines of selected log",
                                color="blue",
                                grid=[1, 1],
                                align="top")

        self.radio_log_type = ButtonGroup(self.window,
                                          options=["Primary Log", "Network Log", "Sensors Log"],
                                          horizontal="True",
                                          grid=[1, 1],
                                          align="right")

        self.textbox_log = TextBox(self.window,
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

        self.button_get = PushButton(self.window,
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
            command_data = app_sensor_commands.CreateSensorNetworkCommand(ip_list[0], network_timeout, "GetNetworkLog")
            if self.radio_log_type.value == "Network Log":
                log = app_sensor_commands.get_data(command_data)
            elif self.radio_log_type.value == "Primary Log":
                command_data.command = "GetPrimaryLog"
                log = app_sensor_commands.get_data(command_data)
            elif self.radio_log_type.value == "Sensors Log":
                command_data.command = "GetSensorsLog"
                log = app_sensor_commands.get_data(command_data)
            else:
                app_logger.app_logger.error("Bad Log Request")
                log = "Bad Log Request"
            self.textbox_log.value = log
        else:
            no_ip_selected_message()

    def _download_logs(self):
        """ Download all selected and online sensors logs. """
        ip_list = self.ip_selection.get_verified_ip_list()
        if len(ip_list) > 0:
            threads = []
            download_to_location = filedialog.askdirectory()
            network_timeout = self.current_config.network_timeout_data

            if download_to_location is not "" and download_to_location is not None:
                for ip in ip_list:
                    sensor_command = app_sensor_commands.CreateSensorNetworkCommand(ip, network_timeout, "")
                    sensor_command.save_to_location = download_to_location
                    threads.append(Thread(target=app_sensor_commands.download_logs, args=[sensor_command]))

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()

                info("Downloads", "Sensor Log Downloads Complete")
            else:
                warn("Warning", "User Cancelled Download Operation")
        else:
            no_ip_selected_message()
