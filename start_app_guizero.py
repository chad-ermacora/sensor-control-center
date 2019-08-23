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
from app_modules import app_logger
from app_modules import program_start_checks
from app_guizero import gui_main
from app_guizero import platform_gui_tweaks


def start_app():
    # Make sure options and such are set right before starting the program
    program_start_checks.run_pre_checks()

    # Create the app
    guizero_app = gui_main.CreateMainWindow()

    # Set app tweaks based on the current system
    platform_gui_tweaks.app_custom_configurations(guizero_app)

    # Start the App after making a note in the log
    app_logger.app_logger.info('KootNet Sensors - Control Center - Started')
    guizero_app.app.display()


if __name__ == '__main__':
    start_app()
