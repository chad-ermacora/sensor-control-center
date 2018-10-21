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
import platform
import os
import subprocess
from guizero import App, PushButton, MenuBar, info, warn, yesno
from tkinter import filedialog
from threading import Thread
import app_sensor_commands
import app_logger
import app_config
import app_guizero.gui_config
import app_guizero.gui_about
import app_guizero.gui_sensor_config
import app_guizero.gui_reports
import app_guizero.gui_sensor_commands
import app_guizero.gui_graphing
import app_guizero.gui_ip_selection


class CreateMainWindow:
    def __init__(self):
        self.current_config = app_config.get_from_file()

        self.app = App(title="KootNet Sensors - PC Control Center",
                       width=405,
                       height=295,
                       layout="grid")

        self.ip_selection = app_guizero.gui_ip_selection.CreateIPSelector(self.app, self.current_config)

        self.window_control_center_config = app_guizero.gui_config.CreateConfigWindow(self.app,
                                                                                      self.current_config,
                                                                                      self.ip_selection)
        self.window_sensor_commands = app_guizero.gui_sensor_commands.CreateSensorCommandsWindow(self.app,
                                                                                                 self.ip_selection)
        self.window_sensor_config = app_guizero.gui_sensor_config.CreateSensorConfigWindow(self.app, self.ip_selection)
        self.window_reports = app_guizero.gui_reports.CreateReportsWindow(self.app, self.ip_selection)
        self.window_graph = app_guizero.gui_graphing.CreateGraphingWindow(self.app, self.ip_selection,
                                                                          self.current_config)
        self.window_about = app_guizero.gui_about.CreateAboutWindow(self.app, self.current_config)

        self.app_menubar = MenuBar(self.app,
                                   toplevel=[["File"],
                                             ["Sensors"],
                                             ["Graphing"],
                                             ["Help"]],
                                   options=[[["Control Center Configuration",
                                              self.window_control_center_config.window.show],
                                             ["Open Logs",
                                              self._app_menu_open_logs],
                                             ["Save ALL Configurations & IP's",
                                              self.window_control_center_config.save_ip_list],
                                             ["Reset ALL IP List",
                                              self._reset_ip_list],
                                             ["Quit",
                                              self._app_exit]],
                                            [["Send Commands",
                                              self.window_sensor_commands.window.show],
                                             ["Update Configurations",
                                              self.window_sensor_config.window.show],
                                             ["Create Reports",
                                              self.window_reports.window.show]],
                                            [["Open Graph Window",
                                              self.window_graph.window.show]],
                                            [["KootNet Sensors - About",
                                              self.window_about.window.show],
                                             ["KootNet Sensors - Website",
                                              self._app_menu_open_website],
                                             ["Sensor Units - DIY",
                                              self._app_menu_open_build_sensor],
                                             ["Sensor Units - Help",
                                              self._app_menu_open_sensor_help],
                                             ["PC Control Center - Help *WIP",
                                              self.window_about.window.show]]])

        self.app_button_check_sensor = PushButton(self.app,
                                                  text="Check Sensors\nStatus",
                                                  command=self.ip_selection.get_verified_ip_list,
                                                  grid=[1, 15, 2, 1],
                                                  align="left")

        self.app_button_sensor_detail = PushButton(self.app,
                                                   text="Download Sensor\nInterval Databases",
                                                   command=self._app_menu_download_interval_db,
                                                   grid=[2, 15, 2, 1],
                                                   align="right")

        self.app_button_sensor_config = PushButton(self.app,
                                                   text="Download Sensor\nTrigger Databases",
                                                   command=self._app_menu_download_trigger_db,
                                                   grid=[4, 15],
                                                   align="right")

    def app_custom_configurations(self):
        """ Apply system & user specific settings to application.  Used just before application start. """
        # Add extra tk options to guizero windows
        self.app.tk.resizable(False, False)
        self.window_control_center_config.window.tk.resizable(False, False)
        self.window_sensor_commands.window.tk.resizable(False, False)
        self.window_sensor_config.window.tk.resizable(False, False)
        self.window_reports.window.tk.resizable(False, False)
        self.window_graph.window.tk.resizable(False, False)
        self.window_about.window.tk.resizable(False, False)

        # Add custom selections and GUI settings
        self.app.on_close(self._app_exit)

        self.ip_selection.app_checkbox_all_column1.value = 0
        self.ip_selection.app_checkbox_all_column2.value = 0
        self.ip_selection.app_check_all_ip1()
        self.ip_selection.app_check_all_ip2()

        self.window_graph.checkbox_up_time.value = 0
        self.window_graph.checkbox_temperature.value = 0
        self.window_graph.checkbox_pressure.value = 0
        self.window_graph.checkbox_humidity.value = 0
        self.window_graph.checkbox_lumen.value = 0
        self.window_graph.checkbox_colour.value = 0

        self.window_sensor_config.checkbox_db_record.value = 1
        self.window_sensor_config.checkbox_custom.value = 0
        self.window_sensor_config.recording_checkbox()
        self.window_sensor_config.custom_checkbox()

        # Platform specific adjustments
        if platform.system() == "Windows":
            self.app.tk.iconbitmap(self.current_config.additional_files_directory + "/icon.ico")
        elif platform.system() == "Linux":
            self.app.width = 490
            self.app.height = 250
            self.window_control_center_config.window.width = 675
            self.window_control_center_config.window.height = 275
            self.window_graph.window.width = 325
            self.window_graph.window.height = 440
            self.window_sensor_config.window.width = 365
            self.window_sensor_config.window.height = 240
            self.window_sensor_commands.window.width = 300
            self.window_sensor_commands.window.height = 260
            self.window_about.window.width = 555
            self.window_about.window.height = 290

        # If no config file, create and save it
        if not os.path.isfile(self.current_config.config_file):
            app_logger.app_logger.info('No Configuration File Found - Saving Default')
            app_config.save_config_to_file(self.current_config)
        else:
            self._set_ip_list()

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

        app_guizero.gui_graphing.pyplot.close()
        self.app.destroy()

    def _app_menu_open_logs(self):
        """ Opens the folder where the logs are kept. """
        if platform.system() == "Windows":
            os.startfile(self.current_config.logs_directory)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", self.current_config.logs_directory])
        else:
            subprocess.Popen(["xdg-open", self.current_config.logs_directory])

    def _app_menu_download_interval_db(self):
        """ Downloads the Interval SQLite3 database to the chosen location, from the selected sensors. """
        ip_list = self.ip_selection.get_verified_ip_list()
        if len(ip_list) >= 1:
            threads = []
            download_to_location = filedialog.askdirectory()

            if download_to_location is not "" and download_to_location is not None:
                for ip in ip_list:
                    threads.append(Thread(target=app_sensor_commands.download_interval_db,
                                          args=[ip, download_to_location]))

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()

                info("Downloads", "Interval Database Downloads Complete")
            else:
                warn("Warning", "User Cancelled Download Operation")
        else:
            warn("No IP Selected", "Please Select at least 1 Sensor IP")

    def _app_menu_download_trigger_db(self):
        """ Downloads the Trigger SQLite3 database to the chosen location, from the selected sensors. """
        ip_list = self.ip_selection.get_verified_ip_list()
        if len(ip_list) >= 1:
            threads = []
            download_to_location = filedialog.askdirectory()

            if download_to_location is not "" and download_to_location is not None:
                for ip in ip_list:
                    threads.append(Thread(target=app_sensor_commands.download_trigger_db,
                                          args=[ip, download_to_location]))

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()

                info("Downloads", "Trigger Database Downloads Complete")
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
