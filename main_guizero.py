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
import app_guizero.gui_main
import app_modules.app_logger as app_logger
import app_guizero.gui_platform_tweaks
import app_modules.app_checks as app_checks

# Make sure options and such are set right before starting the program
app_checks.run_pre_checks()

# Create the app
guizero_app = app_guizero.gui_main.CreateMainWindow()

# Set app tweaks based on the current system
app_guizero.gui_platform_tweaks.app_custom_configurations(guizero_app)

# Start the App after making a note in the log
app_logger.app_logger.info('KootNet Sensors - Control Center - Started')
guizero_app.app.display()
