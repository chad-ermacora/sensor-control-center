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
    # Add extra tk options to guizero windows
    main_app.app.tk.resizable(False, False)
    main_app.window_control_center_config.window.tk.resizable(False, False)
    main_app.window_sensor_commands.window.tk.resizable(False, False)
    main_app.window_sensor_config.window.tk.resizable(False, False)
    main_app.window_reports.window.tk.resizable(False, False)
    main_app.window_sensor_logs.window.tk.resizable(False, False)
    main_app.window_sensor_sql_notes.window.tk.resizable(False, False)
    main_app.window_graph.window.tk.resizable(False, False)
    main_app.window_about.window.tk.resizable(False, False)

    # Add custom selections and GUI settings
    main_app.ip_selection.app_checkbox_all_column1.value = 0
    main_app.ip_selection.app_checkbox_all_column2.value = 0
    main_app.ip_selection.app_check_all_ip1()
    main_app.ip_selection.app_check_all_ip2()
    main_app.ip_selection.app_checkbox_ip1.value = 1

    main_app.window_graph.checkbox_up_time.value = 0
    main_app.window_graph.checkbox_temperature.value = 0
    main_app.window_graph.checkbox_pressure.value = 0
    main_app.window_graph.checkbox_humidity.value = 0
    main_app.window_graph.checkbox_lumen.value = 0
    main_app.window_graph.checkbox_colour.value = 0

    main_app.window_sensor_config.checkbox_db_record.value = 1
    main_app.window_sensor_config.checkbox_custom.value = 0
    main_app.window_sensor_config.recording_checkbox()
    main_app.window_sensor_config.custom_checkbox()

    main_app.window_sensor_logs.textbox_log.bg = "black"
    main_app.window_sensor_logs.textbox_log.text_color = "white"
    main_app.window_sensor_logs.textbox_log.tk.config(insertbackground="red")
    main_app.window_about.about_textbox.bg = "black"
    main_app.window_about.about_textbox.text_color = "white"
    main_app.window_sensor_sql_notes.note_textbox.bg = "black"
    main_app.window_sensor_sql_notes.note_textbox.text_color = "white"
    main_app.window_sensor_sql_notes.note_textbox.tk.config(insertbackground="red")
    main_app.window_sensor_sql_notes.note_datetime_checkbox.value = 1
    main_app.window_sensor_sql_notes.reset_datetime()
    main_app.window_sensor_sql_notes.button_undo_clear_note.disable()

    # Platform specific adjustments
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
        main_app.window_graph.window.height = 420
        main_app.window_sensor_config.window.width = 350
        main_app.window_sensor_config.window.height = 230
        main_app.window_sensor_commands.window.width = 295
        main_app.window_sensor_commands.window.height = 255
        main_app.window_sensor_logs.window.width = 850
        main_app.window_sensor_logs.window.height = 395
        main_app.window_about.window.width = 575
        main_app.window_about.window.height = 285

    # If no config file, create and save it
    if not os.path.isfile(main_app.current_config.config_file):
        app_logger.app_logger.info('No Configuration File Found - Saving Default')
        app_config.save_config_to_file(main_app.current_config)
