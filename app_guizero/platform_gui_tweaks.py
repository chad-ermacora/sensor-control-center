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
from platform import system
from app_modules import app_logger


def app_custom_configurations(main_app):
    """ Apply system & user specific settings to application.  Used just before application start. """

    if system() == "Windows":
        main_app.app.tk.iconbitmap(main_app.current_config.additional_files_directory + "/icon.ico")

    elif system() == "Linux":
        if check_pi_model()[:12] == "Raspberry Pi":
            main_app.app.width = 490
            main_app.app.height = 240
            main_app.window_control_center_config.window.width = 675
            main_app.window_control_center_config.window.height = 275
            main_app.window_reports.window.width = 460
            main_app.window_reports.window.height = 85
            main_app.window_sensor_logs.window.width = 850
            main_app.window_sensor_logs.window.height = 395
            main_app.window_sensor_notes.window.width = 555
            main_app.window_sensor_notes.window.height = 460
            main_app.window_sensor_notes.textbox_current_note.width = 76
            main_app.window_sensor_notes.textbox_note_date.width = 21
            main_app.window_sensor_commands.window.width = 295
            main_app.window_sensor_commands.window.height = 255
            main_app.window_sensor_config.window.width = 550
            main_app.window_sensor_config.window.height = 340
            main_app.window_graph.window.width = 320
            main_app.window_graph.window.height = 435
            main_app.window_db_info.window.width = 520
            main_app.window_db_info.window.height = 545
            main_app.window_db_notes.window.width = 555
            main_app.window_db_notes.window.height = 460
            main_app.window_db_notes.textbox_current_note.width = 76
            main_app.window_db_notes.textbox_note_date.width = 21
            main_app.window_about.window.width = 540
            main_app.window_about.window.height = 285
        else:
            # Configured for Ubuntu 18.04
            main_app.app.width = 500
            main_app.app.height = 275
            main_app.window_control_center_config.window.width = 675
            main_app.window_control_center_config.window.height = 300
            main_app.window_reports.window.width = 485
            main_app.window_reports.window.height = 95
            main_app.window_sensor_logs.window.width = 970
            main_app.window_sensor_logs.window.height = 470
            main_app.window_sensor_notes.window.width = 585
            main_app.window_sensor_notes.window.height = 545
            main_app.window_sensor_notes.textbox_current_note.width = 70
            main_app.window_sensor_notes.textbox_note_date.width = 20
            main_app.window_sensor_commands.window.width = 315
            main_app.window_sensor_commands.window.height = 275
            main_app.window_sensor_config.window.width = 625
            main_app.window_sensor_config.window.height = 405
            main_app.window_graph.window.width = 325
            main_app.window_graph.window.height = 485
            main_app.window_db_notes.window.width = 585
            main_app.window_db_notes.window.height = 545
            main_app.window_db_notes.textbox_current_note.width = 70
            main_app.window_db_notes.textbox_note_date.width = 20
            main_app.window_about.window.width = 610
            main_app.window_about.window.height = 340


def check_pi_model():
    try:
        system_model_file = open("/proc/device-tree/model", "r")
        system_model = system_model_file.read()
        system_model_file.close()
        return str(system_model)
    except Exception as error:
        app_logger.app_logger.debug("Unable to get Raspberry model: " + str(error))
        return ""
