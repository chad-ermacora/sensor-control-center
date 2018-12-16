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

import app_config
import app_logger


def app_custom_configurations(main_app):
    """ Apply system & user specific settings to application.  Used just before application start. """

    if platform.system() == "Windows":
        main_app.app.tk.iconbitmap(main_app.current_config.additional_files_directory + "/icon.ico")
    elif platform.system() == "Linux":
        main_app.app.width = 490
        main_app.app.height = 240
        main_app.window_control_center_config.window.width = 675
        main_app.window_control_center_config.window.height = 275
        main_app.window_reports.window.width = 460
        main_app.window_reports.window.height = 85
        main_app.window_graph.window.width = 320
        main_app.window_graph.window.height = 465
        main_app.window_sensor_config.window.width = 535
        main_app.window_sensor_config.window.height = 340
        main_app.window_sensor_commands.window.width = 295
        main_app.window_sensor_commands.window.height = 255
        main_app.window_sensor_logs.window.width = 850
        main_app.window_sensor_logs.window.height = 395
        main_app.window_sensor_sql_notes.window.height = 340
        main_app.window_sensor_sql_notes.window.width = 750
        main_app.window_sensor_sql_notes.textbox_main_note.width = 105
        main_app.window_about.window.width = 540
        main_app.window_about.window.height = 285
