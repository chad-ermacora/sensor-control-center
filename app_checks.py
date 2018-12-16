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
import app_logger
import os
import app_config

current_config = app_config.CreateDefaultConfigSettings()

important_files = []
important_folders = [current_config.save_to,
                     current_config.logs_directory,
                     current_config.config_folder]


def run_pre_checks():
    """ Creates missing folders, files & configuration on program start. """
    if os.path.isfile(current_config.config_file):
        pass
    else:
        app_logger.app_logger.warning("No configuration file found, creating and saving default")
        app_config.save_config_to_file(current_config)

    for folder in important_folders:
        if os.path.isdir(folder):
            pass
        else:
            app_logger.app_logger.warning("Added missing folder: " + folder)
            os.mkdir(folder)

    for file in important_files:
        if os.path.isfile(file):
            pass
        else:
            app_logger.app_logger.warning("Added missing file: " + file)
            open_file = open(file, "w")
            open_file.write("")
            open_file.close()
