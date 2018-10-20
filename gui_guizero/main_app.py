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
from guizero import App, CheckBox, PushButton, TextBox, MenuBar, info, warn
from tkinter import filedialog
from queue import Queue
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


class CreateMainWindow:
    def __init__(self):
        self.current_config = app_config.get_from_file()
        self.data_queue = Queue()

        self.app = App(title="KootNet Sensors - PC Control Center",
                       width=405,
                       height=295,
                       layout="grid")

        self.window_control_center_config = gui_guizero.control_center_config.CreateConfigWindow(self.app)
        self.window_sensor_commands = gui_guizero.sensor_commands.CreateSensorCommandsWindow(self.app)
        self.window_sensor_config = gui_guizero.sensor_config.CreateSensorConfigWindow(self.app)
        self.window_reports = gui_guizero.reports.CreateReportsWindow(self.app)
        self.window_graph = gui_guizero.graphing.CreateGraphingWindow(self.app)
        self.window_about = gui_guizero.control_center_about.CreateAboutWindow(self.app)

        self.app_menubar = MenuBar(self.app,
                                   toplevel=[["File"],
                                             ["Sensors"],
                                             ["Graphing"],
                                             ["Help"]],
                                   options=[[["Open Logs",
                                              self.app_menu_open_logs],
                                             ["Save ALL Configurations & IP's",
                                              app_config.save_config_to_file(self.current_config)],
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
                                                  command=self.get_verified_ip_list,
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

        # Sensor's Online / Offline IP List Selection 1
        self.app_checkbox_all_column1 = CheckBox(self.app,
                                                 text="Check ALL Column 1",
                                                 command=self.app_check_all_ip1,
                                                 grid=[1, 1, 3, 1],
                                                 align="left")

        self.app_checkbox_ip1 = CheckBox(self.app,
                                         text="IP        ",
                                         grid=[1, 2],
                                         align="left")

        self.app_textbox_ip1 = TextBox(self.app,
                                       text="192.168.10.11",
                                       width=21,
                                       grid=[2, 2],
                                       align="left")

        self.app_checkbox_ip2 = CheckBox(self.app,
                                         text="IP ",
                                         grid=[1, 3],
                                         align="left")

        self.app_textbox_ip2 = TextBox(self.app,
                                       text="192.168.10.12",
                                       width=21,
                                       grid=[2, 3],
                                       align="left")

        self.app_checkbox_ip3 = CheckBox(self.app,
                                         text="IP ",
                                         grid=[1, 4],
                                         align="left")

        self.app_textbox_ip3 = TextBox(self.app,
                                       text="192.168.10.13",
                                       width=21,
                                       grid=[2, 4],
                                       align="left")

        self.app_checkbox_ip4 = CheckBox(self.app,
                                         text="IP ",
                                         grid=[1, 5],
                                         align="left")

        self.app_textbox_ip4 = TextBox(self.app,
                                       text="192.168.10.14",
                                       width=21,
                                       grid=[2, 5],
                                       align="left")

        self.app_checkbox_ip5 = CheckBox(self.app,
                                         text="IP ",
                                         grid=[1, 6],
                                         align="left")

        self.app_textbox_ip5 = TextBox(self.app,
                                       text="192.168.10.15",
                                       width=21,
                                       grid=[2, 6],
                                       align="left")

        self.app_checkbox_ip6 = CheckBox(self.app,
                                         text="IP ",
                                         grid=[1, 7],
                                         align="left")

        self.app_textbox_ip6 = TextBox(self.app,
                                       text="192.168.10.16",
                                       width=21,
                                       grid=[2, 7],
                                       align="left")

        self.app_checkbox_ip7 = CheckBox(self.app,
                                         text="IP ",
                                         grid=[1, 8],
                                         align="left")

        self.app_textbox_ip7 = TextBox(self.app,
                                       text="192.168.10.17",
                                       width=21,
                                       grid=[2, 8],
                                       align="left")

        self.app_checkbox_ip8 = CheckBox(self.app,
                                         text="IP ",
                                         grid=[1, 9],
                                         align="left")

        self.app_textbox_ip8 = TextBox(self.app,
                                       text="192.168.10.18",
                                       width=21,
                                       grid=[2, 9],
                                       align="left")

        # Sensor's Online / Offline IP List Selection 2
        self.app_checkbox_all_column2 = CheckBox(self.app,
                                                 text="Check ALL Column 2",
                                                 command=self.app_check_all_ip2,
                                                 grid=[3, 1, 3, 1],
                                                 align="left")

        self.app_checkbox_ip9 = CheckBox(self.app,
                                         text="IP        ",
                                         grid=[3, 2],
                                         align="left")

        self.app_textbox_ip9 = TextBox(self.app,
                                       text="192.168.10.19",
                                       width=21,
                                       grid=[4, 2],
                                       align="left")

        self.app_checkbox_ip10 = CheckBox(self.app,
                                          text="IP ",
                                          grid=[3, 3],
                                          align="left")

        self.app_textbox_ip10 = TextBox(self.app,
                                        text="192.168.10.20",
                                        width=21,
                                        grid=[4, 3],
                                        align="left")

        self.app_checkbox_ip11 = CheckBox(self.app,
                                          text="IP ",
                                          grid=[3, 4],
                                          align="left")

        self.app_textbox_ip11 = TextBox(self.app,
                                        text="192.168.10.21",
                                        width=21,
                                        grid=[4, 4],
                                        align="left")

        self.app_checkbox_ip12 = CheckBox(self.app,
                                          text="IP ",
                                          grid=[3, 5],
                                          align="left")

        self.app_textbox_ip12 = TextBox(self.app,
                                        text="192.168.10.22",
                                        width=21,
                                        grid=[4, 5],
                                        align="left")

        self.app_checkbox_ip13 = CheckBox(self.app,
                                          text="IP ",
                                          grid=[3, 6],
                                          align="left")

        self.app_textbox_ip13 = TextBox(self.app,
                                        text="192.168.10.23",
                                        width=21,
                                        grid=[4, 6],
                                        align="left")

        self.app_checkbox_ip14 = CheckBox(self.app,
                                          text="IP ",
                                          grid=[3, 7],
                                          align="left")

        self.app_textbox_ip14 = TextBox(self.app,
                                        text="192.168.10.24",
                                        width=21,
                                        grid=[4, 7],
                                        align="left")

        self.app_checkbox_ip15 = CheckBox(self.app,
                                          text="IP ",
                                          grid=[3, 8],
                                          align="left")

        self.app_textbox_ip15 = TextBox(self.app,
                                        text="192.168.10.25",
                                        width=21,
                                        grid=[4, 8],
                                        align="left")

        self.app_checkbox_ip16 = CheckBox(self.app,
                                          text="IP ",
                                          grid=[3, 9],
                                          align="left")

        self.app_textbox_ip16 = TextBox(self.app,
                                        text="192.168.10.26",
                                        width=21,
                                        grid=[4, 9],
                                        align="left")

        self._app_custom_configurations()

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
        # self.app_check_all_ip1()
        # self.app_check_all_ip2()
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
        ip_list = self.get_verified_ip_list()
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
        ip_list = self.get_verified_ip_list()
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

    def app_check_all_ip1(self):
        """ Check or uncheck all IP checkboxes on the 1st column. """
        if self.app_checkbox_all_column1.value == 1:
            self.app_checkbox_ip1.value = 1
            self.app_checkbox_ip2.value = 1
            self.app_checkbox_ip3.value = 1
            self.app_checkbox_ip4.value = 1
            self.app_checkbox_ip5.value = 1
            self.app_checkbox_ip6.value = 1
            self.app_checkbox_ip7.value = 1
            self.app_checkbox_ip8.value = 1
        elif self.app_checkbox_all_column1.value == 0:
            self.app_checkbox_ip1.value = 0
            self.app_checkbox_ip2.value = 0
            self.app_checkbox_ip3.value = 0
            self.app_checkbox_ip4.value = 0
            self.app_checkbox_ip5.value = 0
            self.app_checkbox_ip6.value = 0
            self.app_checkbox_ip7.value = 0
            self.app_checkbox_ip8.value = 0

    def app_check_all_ip2(self):
        """ Check or uncheck all IP checkboxes on the 2nd column. """
        if self.app_checkbox_all_column2.value == 1:
            self.app_checkbox_ip9.value = 1
            self.app_checkbox_ip10.value = 1
            self.app_checkbox_ip11.value = 1
            self.app_checkbox_ip12.value = 1
            self.app_checkbox_ip13.value = 1
            self.app_checkbox_ip14.value = 1
            self.app_checkbox_ip15.value = 1
            self.app_checkbox_ip16.value = 1
        elif self.app_checkbox_all_column2.value == 0:
            self.app_checkbox_ip9.value = 0
            self.app_checkbox_ip10.value = 0
            self.app_checkbox_ip11.value = 0
            self.app_checkbox_ip12.value = 0
            self.app_checkbox_ip13.value = 0
            self.app_checkbox_ip14.value = 0
            self.app_checkbox_ip15.value = 0
            self.app_checkbox_ip16.value = 0

    def _worker_sensor_check(self, ip):
        """ Used in Threads.  Socket connects to sensor by IP's in queue. Puts results in a data queue. """
        data = [ip, sensor_commands.check_sensor_status(ip, self.current_config.network_timeout_sensor_check)]
        self.data_queue.put(data)

    def get_verified_ip_list(self):
        """
        Checks sensor online status and changes the programs IP textbox depending on the returned results.

        The sensor checks are Threaded by the IP's provided in the IP list.
        """
        ip_list = self._make_ip_list()
        ip_list_final = []
        sensor_data_pool = []
        threads = []

        for ip in ip_list:
            threads.append(Thread(target=self._worker_sensor_check, args=[ip]))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        while not self.data_queue.empty():
            sensor_data_pool.append(self.data_queue.get())
            self.data_queue.task_done()

        sensor_data_pool.sort()

        for data in sensor_data_pool:
            ip = data[0]
            sensor_status = data[1]

            if sensor_status == "Online":
                var_colour = "#7CFC00"
                var_checkbox = 1
            else:
                var_colour = "red"
                var_checkbox = 0

            if var_checkbox == 1:
                ip_list_final.append(ip)

            if ip == self.app_textbox_ip1.value:
                self.app_checkbox_ip1.text = sensor_status
                self.app_textbox_ip1.bg = var_colour
                self.app_checkbox_ip1.value = var_checkbox
            elif ip == self.app_textbox_ip2.value:
                self.app_checkbox_ip2.text = sensor_status
                self.app_textbox_ip2.bg = var_colour
                self.app_checkbox_ip2.value = var_checkbox
            elif ip == self.app_textbox_ip3.value:
                self.app_checkbox_ip3.text = sensor_status
                self.app_textbox_ip3.bg = var_colour
                self.app_checkbox_ip3.value = var_checkbox
            elif ip == self.app_textbox_ip4.value:
                self.app_checkbox_ip4.text = sensor_status
                self.app_textbox_ip4.bg = var_colour
                self.app_checkbox_ip4.value = var_checkbox
            elif ip == self.app_textbox_ip5.value:
                self.app_checkbox_ip5.text = sensor_status
                self.app_textbox_ip5.bg = var_colour
                self.app_checkbox_ip5.value = var_checkbox
            elif ip == self.app_textbox_ip6.value:
                self.app_checkbox_ip6.text = sensor_status
                self.app_textbox_ip6.bg = var_colour
                self.app_checkbox_ip6.value = var_checkbox
            elif ip == self.app_textbox_ip7.value:
                self.app_checkbox_ip7.text = sensor_status
                self.app_textbox_ip7.bg = var_colour
                self.app_checkbox_ip7.value = var_checkbox
            elif ip == self.app_textbox_ip8.value:
                self.app_checkbox_ip8.text = sensor_status
                self.app_textbox_ip8.bg = var_colour
                self.app_checkbox_ip8.value = var_checkbox
            elif ip == self.app_textbox_ip9.value:
                self.app_checkbox_ip9.text = sensor_status
                self.app_textbox_ip9.bg = var_colour
                self.app_checkbox_ip9.value = var_checkbox
            elif ip == self.app_textbox_ip10.value:
                self.app_checkbox_ip10.text = sensor_status
                self.app_textbox_ip10.bg = var_colour
                self.app_checkbox_ip10.value = var_checkbox
            elif ip == self.app_textbox_ip11.value:
                self.app_checkbox_ip11.text = sensor_status
                self.app_textbox_ip11.bg = var_colour
                self.app_checkbox_ip11.value = var_checkbox
            elif ip == self.app_textbox_ip12.value:
                self.app_checkbox_ip12.text = sensor_status
                self.app_textbox_ip12.bg = var_colour
                self.app_checkbox_ip12.value = var_checkbox
            elif ip == self.app_textbox_ip13.value:
                self.app_checkbox_ip13.text = sensor_status
                self.app_textbox_ip13.bg = var_colour
                self.app_checkbox_ip13.value = var_checkbox
            elif ip == self.app_textbox_ip14.value:
                self.app_checkbox_ip14.text = sensor_status
                self.app_textbox_ip14.bg = var_colour
                self.app_checkbox_ip14.value = var_checkbox
            elif ip == self.app_textbox_ip15.value:
                self.app_checkbox_ip15.text = sensor_status
                self.app_textbox_ip15.bg = var_colour
                self.app_checkbox_ip15.value = var_checkbox
            elif ip == self.app_textbox_ip16.value:
                self.app_checkbox_ip16.text = sensor_status
                self.app_textbox_ip16.bg = var_colour
                self.app_checkbox_ip16.value = var_checkbox

        sensor_data_pool.clear()
        control_center_logger.app_logger.debug("Checked IP's Processed")
        return ip_list_final

    # Returns selected IP's from Main App Window & Re-Sets unselected IP background to white
    def _make_ip_list(self):
        """ Returns a list of all checked IP's, skipping duplicates """
        checkbox_ip_list = []

        if self.app_checkbox_ip1.value == 1 and self.app_textbox_ip1.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip1.value)
        else:
            self.app_textbox_ip1.bg = 'white'

        if self.app_checkbox_ip2.value == 1 and self.app_textbox_ip2.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip2.value)
        else:
            self.app_textbox_ip2.bg = 'white'

        if self.app_checkbox_ip3.value == 1 and self.app_textbox_ip3.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip3.value)
        else:
            self.app_textbox_ip3.bg = 'white'

        if self.app_checkbox_ip4.value == 1 and self.app_textbox_ip4.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip4.value)
        else:
            self.app_textbox_ip4.bg = 'white'

        if self.app_checkbox_ip5.value == 1 and self.app_textbox_ip5.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip5.value)
        else:
            self.app_textbox_ip5.bg = 'white'

        if self.app_checkbox_ip6.value == 1 and self.app_textbox_ip6.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip6.value)
        else:
            self.app_textbox_ip6.bg = 'white'

        if self.app_checkbox_ip7.value == 1 and self.app_textbox_ip7.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip7.value)
        else:
            self.app_textbox_ip7.bg = 'white'

        if self.app_checkbox_ip8.value == 1 and self.app_textbox_ip8.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip8.value)
        else:
            self.app_textbox_ip8.bg = 'white'

        if self.app_checkbox_ip9.value == 1 and self.app_textbox_ip9.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip9.value)
        else:
            self.app_textbox_ip9.bg = 'white'

        if self.app_checkbox_ip10.value == 1 and self.app_textbox_ip10.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip10.value)
        else:
            self.app_textbox_ip10.bg = 'white'

        if self.app_checkbox_ip11.value == 1 and self.app_textbox_ip11.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip11.value)
        else:
            self.app_textbox_ip11.bg = 'white'

        if self.app_checkbox_ip12.value == 1 and self.app_textbox_ip12.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip12.value)
        else:
            self.app_textbox_ip12.bg = 'white'

        if self.app_checkbox_ip13.value == 1 and self.app_textbox_ip13.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip13.value)
        else:
            self.app_textbox_ip13.bg = 'white'

        if self.app_checkbox_ip14.value == 1 and self.app_textbox_ip14.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip14.value)
        else:
            self.app_textbox_ip14.bg = 'white'

        if self.app_checkbox_ip15.value == 1 and self.app_textbox_ip15.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip15.value)
        else:
            self.app_textbox_ip15.bg = 'white'

        if self.app_checkbox_ip16.value == 1 and self.app_textbox_ip16.value not in checkbox_ip_list:
            checkbox_ip_list.append(self.app_textbox_ip16.value)
        else:
            self.app_textbox_ip16.bg = 'white'

        control_center_logger.app_logger.debug("IP List Generated from Checked Boxes")
        return checkbox_ip_list

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
        self.current_config.ip_list[0] = self.app_textbox_ip1.value
        self.current_config.ip_list[1] = self.app_textbox_ip2.value
        self.current_config.ip_list[2] = self.app_textbox_ip3.value
        self.current_config.ip_list[3] = self.app_textbox_ip4.value
        self.current_config.ip_list[4] = self.app_textbox_ip5.value
        self.current_config.ip_list[5] = self.app_textbox_ip6.value
        self.current_config.ip_list[6] = self.app_textbox_ip7.value
        self.current_config.ip_list[7] = self.app_textbox_ip8.value
        self.current_config.ip_list[8] = self.app_textbox_ip9.value
        self.current_config.ip_list[9] = self.app_textbox_ip10.value
        self.current_config.ip_list[10] = self.app_textbox_ip11.value
        self.current_config.ip_list[11] = self.app_textbox_ip12.value
        self.current_config.ip_list[12] = self.app_textbox_ip13.value
        self.current_config.ip_list[13] = self.app_textbox_ip14.value
        self.current_config.ip_list[14] = self.app_textbox_ip15.value
        self.current_config.ip_list[15] = self.app_textbox_ip16.value

        app_config.save_config_to_file(self.current_config)
        self.set_config()

    def set_config(self):
        """ Sets the programs Configuration to the provided settings. """

        # self.graph_textbox_start.value = self.current_config.graph_start
        # self.graph_textbox_end.value = self.current_config.graph_end
        # self.graph_textbox_sql_skip.value = self.current_config.sql_queries_skip
        # self.graph_textbox_temperature_offset.value = self.current_config.temperature_offset
        # self.graph_textbox_refresh_time.value = self.current_config.live_refresh

        self.app_textbox_ip1.value = self.current_config.ip_list[0]
        self.app_textbox_ip2.value = self.current_config.ip_list[1]
        self.app_textbox_ip3.value = self.current_config.ip_list[2]
        self.app_textbox_ip4.value = self.current_config.ip_list[3]
        self.app_textbox_ip5.value = self.current_config.ip_list[4]
        self.app_textbox_ip6.value = self.current_config.ip_list[5]
        self.app_textbox_ip7.value = self.current_config.ip_list[6]
        self.app_textbox_ip8.value = self.current_config.ip_list[7]
        self.app_textbox_ip9.value = self.current_config.ip_list[8]
        self.app_textbox_ip10.value = self.current_config.ip_list[9]
        self.app_textbox_ip11.value = self.current_config.ip_list[10]
        self.app_textbox_ip12.value = self.current_config.ip_list[11]
        self.app_textbox_ip13.value = self.current_config.ip_list[12]
        self.app_textbox_ip14.value = self.current_config.ip_list[13]
        self.app_textbox_ip15.value = self.current_config.ip_list[14]
        self.app_textbox_ip16.value = self.current_config.ip_list[15]

        # self.config_checkbox_enable_advanced()
