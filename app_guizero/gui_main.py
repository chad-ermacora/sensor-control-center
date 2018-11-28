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
import os
import platform
import subprocess
import webbrowser
from threading import Thread
from tkinter import filedialog

from guizero import App, PushButton, MenuBar, info, warn, yesno

import app_config
import app_logger
import app_sensor_commands
from app_guizero.gui_about import CreateAboutWindow
from app_guizero.gui_config import CreateConfigWindow
from app_guizero.gui_graphing import CreateGraphingWindow, pyplot
from app_guizero.gui_ip_selection import CreateIPSelector
from app_guizero.gui_reports import CreateReportsWindow
from app_guizero.gui_sensor_commands import CreateSensorCommandsWindow
from app_guizero.gui_sensor_config import CreateSensorConfigWindow
from app_guizero.gui_sensor_logs import CreateSensorLogsWindow
from app_guizero.gui_sql_notes import CreateSQLNotesWindow


class CreateMainWindow:
    def __init__(self):
        self.current_config = app_config.get_from_file()

        self.app = App(title="KootNet Sensors - Control Center",
                       width=405,
                       height=295,
                       layout="grid")

        self.app.on_close(self._app_exit)

        self.ip_selection = CreateIPSelector(self.app, self.current_config)
        self._set_ip_list()

        self.window_control_center_config = CreateConfigWindow(self.app, self.current_config, self.ip_selection)
        self.window_reports = CreateReportsWindow(self.app, self.ip_selection, self.current_config)
        self.window_sensor_commands = CreateSensorCommandsWindow(self.app, self.ip_selection, self.current_config)
        self.window_sensor_sql_notes = CreateSQLNotesWindow(self.app, self.ip_selection, self.current_config)
        self.window_sensor_config = CreateSensorConfigWindow(self.app, self.ip_selection, self.current_config)
        self.window_sensor_logs = CreateSensorLogsWindow(self.app, self.ip_selection, self.current_config)
        self.window_graph = CreateGraphingWindow(self.app, self.ip_selection, self.current_config)
        self.window_about = CreateAboutWindow(self.app, self.current_config)

        self.app_menubar = MenuBar(self.app,
                                   toplevel=[["File"],
                                             ["Sensors"],
                                             ["Graphing"],
                                             ["Help"]],
                                   options=[[["Control Center Configuration",
                                              self.window_control_center_config.window.show],
                                             ["Open Logs",
                                              self._app_menu_open_logs],
                                             ["Save IP List",
                                              self.window_control_center_config.save_ip_list],
                                             ["Reset IP List",
                                              self._reset_ip_list],
                                             ["Quit",
                                              self._app_exit]],
                                            [["Create Reports",
                                              self.window_reports.window.show],
                                             ["View & Download Logs",
                                              self.window_sensor_logs.window.show],
                                             ["Add Note to Database",
                                              self.window_sensor_sql_notes.window.show],
                                             ["Send Commands",
                                              self.window_sensor_commands.window.show],
                                             ["Update Configurations",
                                              self.window_sensor_config.window.show]],
                                            [["Open Graph Window",
                                              self.window_graph.window.show]],
                                            [["KootNet Sensors - About",
                                              self.window_about.window.show],
                                             ["KootNet Sensors - Website",
                                              self._app_menu_open_website],
                                             ["Sensor Units - Making a Sensor",
                                              self._app_menu_open_build_sensor],
                                             ["Sensor Units - Help",
                                              self._app_menu_open_sensor_help],
                                             ["Control Center - Help *WIP",
                                              self.window_about.window.show]]])

        self.app_button_check_sensor = PushButton(self.app,
                                                  text="Check Sensors\nStatus",
                                                  command=self.ip_selection.get_verified_ip_list,
                                                  grid=[1, 15, 2, 1],
                                                  align="left")

        self.app_button_download_sql_db = PushButton(self.app,
                                                     text="Download Sensors\nDatabase",
                                                     command=self._app_menu_download_sql_db,
                                                     grid=[4, 15],
                                                     align="right")

    def _app_exit(self):
        """ Closes log handlers & matplotlib before closing the application. """
        app_log_handlers = app_logger.app_logger.handlers[:]
        for handler in app_log_handlers:
            handler.close()
            app_logger.app_logger.removeHandler(handler)

        sensor_log_handlers = app_logger.sensor_logger.handlers[:]
        for handler in sensor_log_handlers:
            handler.close()
            app_logger.sensor_logger.removeHandler(handler)

        pyplot.close()
        self.app.destroy()

    def _app_menu_open_logs(self):
        """ Opens the folder where the logs are kept. """
        if platform.system() == "Windows":
            os.startfile(self.current_config.logs_directory)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", self.current_config.logs_directory])
        else:
            subprocess.Popen(["xdg-open", self.current_config.logs_directory])

    @staticmethod
    def _download_sql_finished_message(threads):
        for thread in threads:
            thread.join()

        info("Downloads", "SQL database downloads complete")

    def _app_menu_download_sql_db(self):
        """ Downloads the Interval SQLite3 database to the chosen location, from the selected sensors. """
        ip_list = self.ip_selection.get_verified_ip_list()
        network_commands = app_sensor_commands.CreateNetworkGetCommands()

        if len(ip_list) >= 1:
            threads = []
            download_to_location = filedialog.askdirectory()
            network_timeout = self.current_config.network_timeout_data

            if download_to_location is not "" and download_to_location is not None:
                for ip in ip_list:
                    senor_command = app_sensor_commands.CreateSensorNetworkCommand(ip,
                                                                                   network_timeout,
                                                                                   network_commands.sensor_sql_database)
                    senor_command.save_to_location = download_to_location

                    threads.append(Thread(target=app_sensor_commands.download_sensor_database,
                                          args=[senor_command]))

                for thread in threads:
                    thread.start()

                download_message_thread = Thread(target=self._download_sql_finished_message, args=[threads])
                download_message_thread.start()
            else:
                warn("Warning", "User Cancelled Download Operation")
        else:
            warn("No IP Selected", "Please Select at least 1 Sensor IP")

    @staticmethod
    def _app_menu_open_website():
        """ Open the program's Website. """
        webbrowser.open_new_tab("http://kootenay-networks.com/?page_id=170")

    def _app_menu_open_build_sensor(self):
        """ Open the help file for building a Sensor Unit. """
        help_file_location = self.current_config.additional_files_directory + "/BuildSensors.html"
        webbrowser.open_new_tab(help_file_location)

    def _app_menu_open_sensor_help(self):
        """ Open the help file for Sensor Units. """
        help_file_location = self.current_config.additional_files_directory + "/SensorUnitHelp.html"
        webbrowser.open_new_tab(help_file_location)

    def _set_ip_list(self):
        self.ip_selection.app_textbox_ip1.value = self.current_config.ip_list[0]
        self.ip_selection.app_textbox_ip2.value = self.current_config.ip_list[1]
        self.ip_selection.app_textbox_ip3.value = self.current_config.ip_list[2]
        self.ip_selection.app_textbox_ip4.value = self.current_config.ip_list[3]
        self.ip_selection.app_textbox_ip5.value = self.current_config.ip_list[4]
        self.ip_selection.app_textbox_ip6.value = self.current_config.ip_list[5]
        self.ip_selection.app_textbox_ip7.value = self.current_config.ip_list[6]
        self.ip_selection.app_textbox_ip8.value = self.current_config.ip_list[7]
        self.ip_selection.app_textbox_ip9.value = self.current_config.ip_list[8]
        self.ip_selection.app_textbox_ip10.value = self.current_config.ip_list[9]
        self.ip_selection.app_textbox_ip11.value = self.current_config.ip_list[10]
        self.ip_selection.app_textbox_ip12.value = self.current_config.ip_list[11]
        self.ip_selection.app_textbox_ip13.value = self.current_config.ip_list[12]
        self.ip_selection.app_textbox_ip14.value = self.current_config.ip_list[13]
        self.ip_selection.app_textbox_ip15.value = self.current_config.ip_list[14]
        self.ip_selection.app_textbox_ip16.value = self.current_config.ip_list[15]

    def _reset_ip_list(self):
        default_config = app_config.CreateDefaultConfigSettings()
        if yesno("Reset IP List to Default", "Are you sure you want to reset the IP list to Defaults?"):
            self.current_config.ip_list = default_config.ip_list
            self._set_ip_list()
