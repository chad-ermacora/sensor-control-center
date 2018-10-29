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

import app_logger
import app_sensor_commands


class CreateSensorLogsWindow:
    def __init__(self, app, ip_selection, current_config):
        self.ip_selection = ip_selection
        self.current_config = current_config

        self.window = Window(app,
                             title="Sensor Logs",
                             width=895,
                             height=450,
                             layout="grid",
                             visible=False)

        self.app_menubar = MenuBar(self.window,
                                   toplevel=[["Download"]],
                                   options=[[["Download All Sensors Logs",
                                              self._download_logs]]])

        self.text_choose = Text(self.window,
                                text="Log Output",
                                color="blue",
                                grid=[1, 1],
                                align="top")

        self.radio_log_type = ButtonGroup(self.window,
                                          options=["Network Log", "Primary Log", "Sensors Log"],
                                          horizontal="True",
                                          grid=[1, 1],
                                          align="right")

        self.textbox_log = TextBox(self.window,
                                   text="Sensor Log",
                                   grid=[1, 2],
                                   width=110,
                                   height=22,
                                   multiline=True,
                                   align="left")

        self.button_get = PushButton(self.window,
                                     text="View last few lines\nof first sensor's log",
                                     command=self._get_log,
                                     grid=[1, 3],
                                     align="right")

    def _get_log(self):
        """ Select the remote sensor log you wish to view. """
        ip_list = self.ip_selection.get_verified_ip_list()
        if self.radio_log_type.value == "Network Log":
            log = app_sensor_commands.get_network_log(ip_list[0], self.current_config.network_timeout_data)
        elif self.radio_log_type.value == "Primary Log":
            log = app_sensor_commands.get_sensor_primary_log(ip_list[0], self.current_config.network_timeout_data)
        elif self.radio_log_type.value == "Sensors Log":
            log = app_sensor_commands.get_sensors_log(ip_list[0], self.current_config.network_timeout_data)
        else:
            log = "Bad Log Request"

        self.textbox_log.value = log
        app_logger.app_logger.info("Remote Sensor Log Retrieved")

    def _download_logs(self):
        ip_list = self.ip_selection.get_verified_ip_list()
        if len(ip_list) >= 1:
            threads = []
            download_to_location = filedialog.askdirectory()

            if download_to_location is not "" and download_to_location is not None:
                for ip in ip_list:
                    download_obj = app_sensor_commands.CreateHTTPDownload()
                    download_obj.ip = ip
                    download_obj.url = "/logs/"
                    download_obj.save_to_location = download_to_location

                    threads.append(Thread(target=app_sensor_commands.download_logs,
                                          args=[download_obj]))

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()

                info("Downloads", "Sensor Log Downloads Complete")
            else:
                warn("Warning", "User Cancelled Download Operation")
        else:
            warn("No IP Selected", "Please Select at least 1 Sensor IP")
