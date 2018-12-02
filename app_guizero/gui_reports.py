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
from guizero import Window, PushButton, Text
import app_reports


class CreateReportsWindow:
    def __init__(self, app, ip_selection, current_config):
        self.ip_selection = ip_selection
        self.current_config = current_config
        self.window = Window(app,
                             title="Sensor Reports",
                             width=475,
                             height=100,
                             layout="grid",
                             visible=False)

        self.text_select = Text(self.window,
                                text="Select Sensor IPs in the main window",
                                grid=[1, 1, 3, 1],
                                color='#CB0000',
                                align="top")

        self.text1 = Text(self.window,
                          text="Live Readings Report  |",
                          color='blue',
                          grid=[1, 6],
                          align="top")

        self.button_check_sensor = PushButton(self.window,
                                              text="Create",
                                              command=self.app_sensor_readings_report,
                                              grid=[1, 7],
                                              align="top")

        self.text2 = Text(self.window,
                          text="|  System Report  |",
                          color='blue',
                          grid=[2, 6],
                          align="top")

        self.button_sensor_detail = PushButton(self.window,
                                               text="Create",
                                               command=self.app_sensor_system_report,
                                               grid=[2, 7],
                                               align="top")

        self.text3 = Text(self.window,
                          text="|  Configuration Report",
                          color='blue',
                          grid=[3, 6],
                          align="top")

        self.button_sensor_config = PushButton(self.window,
                                               text="Create",
                                               command=self.app_sensor_config_report,
                                               grid=[3, 7],
                                               align="top")

        # Window Tweaks
        self.window.tk.resizable(False, False)


    def app_sensor_readings_report(self):
        """ Create a HTML sensor Readings Report containing each IP selected and online. """
        sensor_readings_report = app_reports.CreateHTMLReadingsData(self.current_config)
        ip_list = self.ip_selection.get_verified_ip_list()
        app_reports.sensor_html_report(sensor_readings_report, ip_list)

    def app_sensor_system_report(self):
        """ Create a HTML sensor System Report containing each IP selected and online. """
        sensor_system_report = app_reports.CreateHTMLSystemData(self.current_config)
        ip_list = self.ip_selection.get_verified_ip_list()
        app_reports.sensor_html_report(sensor_system_report, ip_list)

    def app_sensor_config_report(self):
        """ Create a HTML sensor Configuration Report containing each IP selected and online. """
        sensor_config_report = app_reports.CreateHTMLConfigData(self.current_config)
        ip_list = self.ip_selection.get_verified_ip_list()
        app_reports.sensor_html_report(sensor_config_report, ip_list)
