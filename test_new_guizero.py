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

--------------------------------------------------------------------------
DEBUG - Detailed information, typically of interest only when diagnosing problems. test
INFO - Confirmation that things are working as expected.
WARNING - An indication that something unexpected happened, or indicative of some problem in the near future
ERROR - Due to a more serious problem, the software has not been able to perform some function.
CRITICAL - A serious error, indicating that the program itself may be unable to continue running.
"""
import gui_guizero.main_app
import gui_guizero.control_center_config
import gui_guizero.control_center_about
import gui_guizero.sensor_config
import gui_guizero.reports
import gui_guizero.sensor_commands
import control_center_logger

new_app = gui_guizero.main_app.CreateMainWindow()
program_config_window = gui_guizero.control_center_config.CreateConfigWindow(new_app.app)
about_window = gui_guizero.control_center_about.CreateAboutWindow(new_app.app)
sensor_config_window = gui_guizero.sensor_config.CreateSensorConfigWindow(new_app.app)
reports_window = gui_guizero.reports.CreateReportsWindow(new_app.app)
sensor_commands_window = gui_guizero.sensor_commands.CreateSensorCommandsWindow(new_app.app)

# _app_custom_configurations()

# Start the App
control_center_logger.app_logger.info('KootNet Sensors - PC Control Center - Started')
new_app.app.display()
