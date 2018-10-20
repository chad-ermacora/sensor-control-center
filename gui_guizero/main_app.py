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
from guizero import App, PushButton, MenuBar, info, warn
from tkinter import filedialog
from threading import Thread
import sensor_commands
import control_center_logger
import app_config
import gui_guizero.control_center_config
import gui_guizero.control_center_about
import gui_guizero.sensor_config
import gui_guizero.reports
import gui_guizero.sensor_commands
import gui_guizero.graphing
import gui_guizero.ip_selection


class CreateMainWindow:
    def __init__(self):
        self.current_config = app_config.get_from_file()

        self.app = App(title="KootNet Sensors - PC Control Center",
                       width=405,
                       height=295,
                       layout="grid")

        self.ip_selection = gui_guizero.ip_selection.CreateIPSelector(self.app)

        self.window_control_center_config = gui_guizero.control_center_config.CreateConfigWindow(self.app)
        self.window_sensor_commands = gui_guizero.sensor_commands.CreateSensorCommandsWindow(self.app, self.ip_selection)
        self.window_sensor_config = gui_guizero.sensor_config.CreateSensorConfigWindow(self.app, self.ip_selection)
        self.window_reports = gui_guizero.reports.CreateReportsWindow(self.app, self.ip_selection)
        self.window_graph = gui_guizero.graphing.CreateGraphingWindow(self.app, self.ip_selection)
        self.window_about = gui_guizero.control_center_about.CreateAboutWindow(self.app)

        self.app_menubar = MenuBar(self.app,
                                   toplevel=[["File"],
                                             ["Sensors"],
                                             ["Graphing"],
                                             ["Help"]],
                                   options=[[["Open Logs",
                                              self.app_menu_open_logs],
                                             ["Save ALL Configurations & IP's",
                                              self.save_ip_list],
                                             ["Control Center Configuration",
                                              self.window_control_center_config.window.show],
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
                                              self.app_menu_open_website],
                                             ["Sensor Units - DIY",
                                              self.app_menu_open_build_sensor],
                                             ["Sensor Units - Help",
                                              self.app_menu_open_sensor_help],
                                             ["PC Control Center - Help *WIP",
                                              self.window_about.window.show]]])

        self.app_button_check_sensor = PushButton(self.app,
                                                  text="Check Sensors\nStatus",
                                                  command=self.ip_selection.get_verified_ip_list,
                                                  grid=[1, 15, 2, 1],
                                                  align="left")

        self.app_button_sensor_detail = PushButton(self.app,
                                                   text="Download Sensor\nInterval Databases",
                                                   command=self.app_menu_download_interval_db,
                                                   grid=[2, 15, 2, 1],
                                                   align="right")

        self.app_button_sensor_config = PushButton(self.app,
                                                   text="Download Sensor\nTrigger Databases",
                                                   command=self.app_menu_download_trigger_db,
                                                   grid=[4, 15],
                                                   align="right")

        self._app_custom_configurations()

    def save_ip_list(self):
        self.current_config.ip_list = self.ip_selection.get_all_ip_list()
        app_config.save_config_to_file(self.current_config)

    def _app_custom_configurations(self):
        """ Apply system & user specific settings to application.  Used just before application start. """
        # Add extra tk options to guizero windows
        self.app.on_close(self._app_exit)
        self.app.tk.resizable(False, False)
        self.window_sensor_commands.window.tk.resizable(False, False)
        self.window_sensor_config.window.tk.resizable(False, False)
        self.window_reports.window.tk.resizable(False, False)
        self.window_graph.window.tk.resizable(False, False)
        self.window_about.window.tk.resizable(False, False)

        # # Add custom selections and GUI settings
        # self.app_checkbox_all_column1.value = 0
        # self.app_checkbox_all_column2.value = 0
        # self.graph_checkbox_up_time.value = 1
        # self.graph_checkbox_temperature.value = 1
        # self.graph_checkbox_pressure.value = 0
        # self.graph_checkbox_humidity.value = 0
        # self.graph_checkbox_lumen.value = 0
        # self.graph_checkbox_colour.value = 0
        # self.sensor_config_checkbox_db_record.value = 1
        # self.sensor_config_checkbox_custom.value = 0
        #
        # self._app_check_all_ip1()
        # self._app_check_all_ip2()
        # self._graph_radio_selection()
        # self.sensor_config_enable_recording()
        # self.sensor_config_enable_custom()
        #
        # self.about_textbox.disable()
        # self.config_textbox_save_to.disable()
        # self.sensor_config_button_set_config.disable()
        # self.commands_button_os_Upgrade.disable()

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

        self.set_config()
        if not os.path.isfile(self.current_config.config_file):
            control_center_logger.app_logger.info('No Configuration File Found - Saving Default')
            app_config.save_config_to_file(self.current_config)

    def _app_exit(self):
        """ Closes log handlers & matplotlib before closing the application. """
        app_log_handlers = control_center_logger.app_logger.handlers[:]
        for handler in app_log_handlers:
            handler.close()
            control_center_logger.app_logger.removeHandler(handler)

        sensor_log_handlers = control_center_logger.sensor_logger.handlers[:]
        for handler in sensor_log_handlers:
            handler.close()
            control_center_logger.sensor_logger.removeHandler(handler)

        gui_guizero.graphing.pyplot.close()
        self.app.destroy()

    def app_menu_open_logs(self):
        """ Opens the folder where the logs are kept. """
        if platform.system() == "Windows":
            os.startfile(self.current_config.logs_directory)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", self.current_config.logs_directory])
        else:
            subprocess.Popen(["xdg-open", self.current_config.logs_directory])

    def app_menu_download_interval_db(self):
        """ Downloads the Interval SQLite3 database to the chosen location, from the selected sensors. """
        ip_list = self.ip_selection.get_verified_ip_list()
        if len(ip_list) >= 1:
            threads = []
            download_to_location = filedialog.askdirectory()

            if download_to_location is not "" and download_to_location is not None:
                for ip in ip_list:
                    threads.append(Thread(target=sensor_commands.download_interval_db,
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

    def app_menu_download_trigger_db(self):
        """ Downloads the Trigger SQLite3 database to the chosen location, from the selected sensors. """
        ip_list = self.ip_selection.get_verified_ip_list()
        if len(ip_list) >= 1:
            threads = []
            download_to_location = filedialog.askdirectory()

            if download_to_location is not "" and download_to_location is not None:
                for ip in ip_list:
                    threads.append(Thread(target=sensor_commands.download_trigger_db,
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
    def app_menu_open_website():
        """ Open the program's Website. """
        webbrowser.open_new_tab("http://kootenay-networks.com/?page_id=170")

    def app_menu_open_build_sensor(self):
        """ Open the help file for building a Sensor Unit. """
        help_file_location = self.current_config.additional_files_directory + "/BuildSensors.html"
        webbrowser.open_new_tab(help_file_location)

    def app_menu_open_sensor_help(self):
        """ Open the help file for Sensor Units. """
        help_file_location = self.current_config.additional_files_directory + "/SensorUnitHelp.html"
        webbrowser.open_new_tab(help_file_location)

    def config_button_save(self):
        """ Save the programs Configuration and IP list to file """
        control_center_logger.app_logger.debug("Applying Configuration & Saving to File")

        # self.current_config.save_to = self.config_textbox_save_to.value
        # self.current_config.graph_start = self.config_textbox_start.value
        # self.current_config.graph_end = self.config_textbox_end.value
        # self.current_config.datetime_offset = self.config_textbox_time_offset.value
        # self.current_config.sql_queries_skip = self.config_textbox_sql_skip.value
        # self.current_config.temperature_offset = self.config_textbox_temperature_offset.value
        # self.current_config.live_refresh = graph_textbox_refresh_time.value
        # self.current_config.network_timeout_sensor_check = self.config_textbox_network_check.value
        # self.current_config.network_timeout_data = self.config_textbox_network_details.value
        # self.current_config.allow_advanced_controls = self.config_checkbox_power_controls.value
        self.current_config.ip_list = self.ip_selection.get_all_ip_list()

        app_config.save_config_to_file(self.current_config)
        self.set_config()

    def set_config(self):
        """ Sets the programs Configuration to the provided settings. """

        # self.graph_textbox_start.value = self.current_config.graph_start
        # self.graph_textbox_end.value = self.current_config.graph_end
        # self.graph_textbox_sql_skip.value = self.current_config.sql_queries_skip
        # self.graph_textbox_temperature_offset.value = self.current_config.temperature_offset
        # self.graph_textbox_refresh_time.value = self.current_config.live_refresh

        # self.ip_selection.set_ip_list(self.current_config)

        # self.config_checkbox_enable_advanced()
