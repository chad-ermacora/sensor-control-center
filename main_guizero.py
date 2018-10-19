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
import app_config
import sensor_commands
import app_reports
import app_graph
import os
import platform
import subprocess
import webbrowser
from guizero import App, Window, CheckBox, PushButton, Text, TextBox, MenuBar, info, warn, ButtonGroup
from tkinter import filedialog
from matplotlib import pyplot
from threading import Thread
from queue import Queue
import logging
from logging.handlers import RotatingFileHandler

script_directory = str(os.path.dirname(os.path.realpath(__file__))).replace("\\", "/")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(script_directory + '/logs/KootNet_log.txt',
                                   maxBytes=256000,
                                   backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                              '%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

current_config = app_config.get_from_file()
data_queue = Queue()


def _app_custom_configurations():
    """ Apply system & user specific settings to application.  Used just before application start. """
    # Add extra tk options to guizero windows
    app.on_close(_app_exit)
    app.tk.resizable(False, False)
    window_graph.tk.resizable(False, False)
    window_sensor_commands.tk.resizable(False, False)
    window_sensor_config.tk.resizable(False, False)
    window_sensor_reports.tk.resizable(False, False)
    window_app_about.tk.resizable(False, False)
    window_config.tk.resizable(False, False)

    # Add custom selections and GUI settings
    app_checkbox_all_column1.value = 0
    app_checkbox_all_column2.value = 0
    graph_checkbox_up_time.value = 1
    graph_checkbox_temperature.value = 1
    graph_checkbox_pressure.value = 0
    graph_checkbox_humidity.value = 0
    graph_checkbox_lumen.value = 0
    graph_checkbox_colour.value = 0
    sensor_config_checkbox_db_record.value = 1
    sensor_config_checkbox_custom.value = 0

    _set_about_text()
    app_check_all_ip_checkboxes(1)
    app_check_all_ip_checkboxes(2)
    _graph_radio_selection()
    sensor_config_enable_recording()
    sensor_config_enable_custom()

    about_textbox.disable()
    config_textbox_save_to.disable()
    sensor_config_button_set_config.disable()
    commands_button_os_Upgrade.disable()

    # Platform specific adjustments
    if platform.system() == "Windows":
        app.tk.iconbitmap(current_config.additional_files_directory + "/icon.ico")
    elif platform.system() == "Linux":
        app.width = 490
        app.height = 250
        window_config.width = 675
        window_config.height = 275
        window_graph.width = 325
        window_graph.height = 440
        window_sensor_config.width = 365
        window_sensor_config.height = 240
        window_sensor_commands.width = 300
        window_sensor_commands.height = 260
        window_app_about.width = 555
        window_app_about.height = 290

    set_config()
    if not os.path.isfile(current_config.config_file):
        logger.info('No Configuration File Found - Saving Default')
        app_config.save_config_to_file(current_config)


def _app_exit():
    """ Clean ups before application closes. """
    log_handlers = logger.handlers[:]
    for handler in log_handlers:
        handler.close()
        logger.removeHandler(handler)

    pyplot.close()
    app.destroy()


def _set_about_text():
    """ Loads and sets the about text from file. """
    try:
        local_file = open(current_config.about_text, 'r')
        new_text = local_file.read()
        local_file.close()
        about_textbox.value = new_text
        logger.debug("About Text Load - OK")
    except Exception as error:
        logger.error("About Text Load - Failed: " + str(error))


def app_menu_open_logs():
    """ Opens the folder where the logs are kept. """
    logger.debug("Open Logs Folder")
    if platform.system() == "Windows":
        os.startfile(current_config.logs_directory)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", current_config.logs_directory])
    else:
        subprocess.Popen(["xdg-open", current_config.logs_directory])


def app_menu_download_interval_db():
    """ Downloads the Interval SQLite3 database to the chosen location, from the selected sensors. """
    ip_list = get_verified_ip_list()
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


def app_menu_download_trigger_db():
    """ Downloads the Trigger SQLite3 database to the chosen location, from the selected sensors. """
    ip_list = get_verified_ip_list()
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


def app_menu_open_website():
    """ Open the program's Website. """
    webbrowser.open_new_tab("http://kootenay-networks.com/?page_id=170")


def app_menu_open_build_sensor():
    """ Open the help file for building a Sensor Unit. """
    help_file_location = current_config.additional_files_directory + "/BuildSensors.html"
    webbrowser.open_new_tab(help_file_location)


def app_menu_open_sensor_help():
    """ Open the help file for Sensor Units. """
    help_file_location = current_config.additional_files_directory + "/SensorUnitHelp.html"
    webbrowser.open_new_tab(help_file_location)


def app_check_all_ip_checkboxes(var_column):
    """ Check or uncheck all IP checkboxes on the column provided. """
    if var_column == 1:
        if app_checkbox_all_column1.value == 1:
            app_checkbox_ip1.value = 1
            app_checkbox_ip2.value = 1
            app_checkbox_ip3.value = 1
            app_checkbox_ip4.value = 1
            app_checkbox_ip5.value = 1
            app_checkbox_ip6.value = 1
            app_checkbox_ip7.value = 1
            app_checkbox_ip8.value = 1
        elif app_checkbox_all_column1.value == 0:
            app_checkbox_ip1.value = 0
            app_checkbox_ip2.value = 0
            app_checkbox_ip3.value = 0
            app_checkbox_ip4.value = 0
            app_checkbox_ip5.value = 0
            app_checkbox_ip6.value = 0
            app_checkbox_ip7.value = 0
            app_checkbox_ip8.value = 0

    elif var_column == 2:
        if app_checkbox_all_column2.value == 1:
            app_checkbox_ip9.value = 1
            app_checkbox_ip10.value = 1
            app_checkbox_ip11.value = 1
            app_checkbox_ip12.value = 1
            app_checkbox_ip13.value = 1
            app_checkbox_ip14.value = 1
            app_checkbox_ip15.value = 1
            app_checkbox_ip16.value = 1
        elif app_checkbox_all_column2.value == 0:
            app_checkbox_ip9.value = 0
            app_checkbox_ip10.value = 0
            app_checkbox_ip11.value = 0
            app_checkbox_ip12.value = 0
            app_checkbox_ip13.value = 0
            app_checkbox_ip14.value = 0
            app_checkbox_ip15.value = 0
            app_checkbox_ip16.value = 0


def _worker_sensor_check(ip):
    """ Used in Threads.  Socket connects to sensor by IP's in queue. Puts results in a data queue. """
    data = [ip, sensor_commands.check_sensor_status(ip, current_config.network_timeout_sensor_check)]
    data_queue.put(data)


def get_verified_ip_list():
    """
    Checks sensor online status and changes the programs IP textbox depending on the returned results.

    The sensor checks are Threaded by the IP's provided in the IP list.
    """
    ip_list = _make_ip_list()
    ip_list_final = []
    sensor_data_pool = []
    threads = []

    for ip in ip_list:
        threads.append(Thread(target=_worker_sensor_check, args=[ip]))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    while not data_queue.empty():
        sensor_data_pool.append(data_queue.get())
        data_queue.task_done()

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

        if ip == app_textbox_ip1.value:
            app_checkbox_ip1.text = sensor_status
            app_textbox_ip1.bg = var_colour
            app_checkbox_ip1.value = var_checkbox
        elif ip == app_textbox_ip2.value:
            app_checkbox_ip2.text = sensor_status
            app_textbox_ip2.bg = var_colour
            app_checkbox_ip2.value = var_checkbox
        elif ip == app_textbox_ip3.value:
            app_checkbox_ip3.text = sensor_status
            app_textbox_ip3.bg = var_colour
            app_checkbox_ip3.value = var_checkbox
        elif ip == app_textbox_ip4.value:
            app_checkbox_ip4.text = sensor_status
            app_textbox_ip4.bg = var_colour
            app_checkbox_ip4.value = var_checkbox
        elif ip == app_textbox_ip5.value:
            app_checkbox_ip5.text = sensor_status
            app_textbox_ip5.bg = var_colour
            app_checkbox_ip5.value = var_checkbox
        elif ip == app_textbox_ip6.value:
            app_checkbox_ip6.text = sensor_status
            app_textbox_ip6.bg = var_colour
            app_checkbox_ip6.value = var_checkbox
        elif ip == app_textbox_ip7.value:
            app_checkbox_ip7.text = sensor_status
            app_textbox_ip7.bg = var_colour
            app_checkbox_ip7.value = var_checkbox
        elif ip == app_textbox_ip8.value:
            app_checkbox_ip8.text = sensor_status
            app_textbox_ip8.bg = var_colour
            app_checkbox_ip8.value = var_checkbox
        elif ip == app_textbox_ip9.value:
            app_checkbox_ip9.text = sensor_status
            app_textbox_ip9.bg = var_colour
            app_checkbox_ip9.value = var_checkbox
        elif ip == app_textbox_ip10.value:
            app_checkbox_ip10.text = sensor_status
            app_textbox_ip10.bg = var_colour
            app_checkbox_ip10.value = var_checkbox
        elif ip == app_textbox_ip11.value:
            app_checkbox_ip11.text = sensor_status
            app_textbox_ip11.bg = var_colour
            app_checkbox_ip11.value = var_checkbox
        elif ip == app_textbox_ip12.value:
            app_checkbox_ip12.text = sensor_status
            app_textbox_ip12.bg = var_colour
            app_checkbox_ip12.value = var_checkbox
        elif ip == app_textbox_ip13.value:
            app_checkbox_ip13.text = sensor_status
            app_textbox_ip13.bg = var_colour
            app_checkbox_ip13.value = var_checkbox
        elif ip == app_textbox_ip14.value:
            app_checkbox_ip14.text = sensor_status
            app_textbox_ip14.bg = var_colour
            app_checkbox_ip14.value = var_checkbox
        elif ip == app_textbox_ip15.value:
            app_checkbox_ip15.text = sensor_status
            app_textbox_ip15.bg = var_colour
            app_checkbox_ip15.value = var_checkbox
        elif ip == app_textbox_ip16.value:
            app_checkbox_ip16.text = sensor_status
            app_textbox_ip16.bg = var_colour
            app_checkbox_ip16.value = var_checkbox

    sensor_data_pool.clear()
    logger.debug("Checked IP's Processed")
    return ip_list_final


# Returns selected IP's from Main App Window & Re-Sets unselected IP background to white
def _make_ip_list():
    """ Returns a list of all checked IP's, skipping duplicates """
    checkbox_ip_list = []

    if app_checkbox_ip1.value == 1 and app_textbox_ip1.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip1.value)
    else:
        app_textbox_ip1.bg = 'white'

    if app_checkbox_ip2.value == 1 and app_textbox_ip2.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip2.value)
    else:
        app_textbox_ip2.bg = 'white'

    if app_checkbox_ip3.value == 1 and app_textbox_ip3.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip3.value)
    else:
        app_textbox_ip3.bg = 'white'

    if app_checkbox_ip4.value == 1 and app_textbox_ip4.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip4.value)
    else:
        app_textbox_ip4.bg = 'white'

    if app_checkbox_ip5.value == 1 and app_textbox_ip5.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip5.value)
    else:
        app_textbox_ip5.bg = 'white'

    if app_checkbox_ip6.value == 1 and app_textbox_ip6.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip6.value)
    else:
        app_textbox_ip6.bg = 'white'

    if app_checkbox_ip7.value == 1 and app_textbox_ip7.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip7.value)
    else:
        app_textbox_ip7.bg = 'white'

    if app_checkbox_ip8.value == 1 and app_textbox_ip8.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip8.value)
    else:
        app_textbox_ip8.bg = 'white'

    if app_checkbox_ip9.value == 1 and app_textbox_ip9.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip9.value)
    else:
        app_textbox_ip9.bg = 'white'

    if app_checkbox_ip10.value == 1 and app_textbox_ip10.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip10.value)
    else:
        app_textbox_ip10.bg = 'white'

    if app_checkbox_ip11.value == 1 and app_textbox_ip11.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip11.value)
    else:
        app_textbox_ip11.bg = 'white'

    if app_checkbox_ip12.value == 1 and app_textbox_ip12.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip12.value)
    else:
        app_textbox_ip12.bg = 'white'

    if app_checkbox_ip13.value == 1 and app_textbox_ip13.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip13.value)
    else:
        app_textbox_ip13.bg = 'white'

    if app_checkbox_ip14.value == 1 and app_textbox_ip14.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip14.value)
    else:
        app_textbox_ip14.bg = 'white'

    if app_checkbox_ip15.value == 1 and app_textbox_ip15.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip15.value)
    else:
        app_textbox_ip15.bg = 'white'

    if app_checkbox_ip16.value == 1 and app_textbox_ip16.value not in checkbox_ip_list:
        checkbox_ip_list.append(app_textbox_ip16.value)
    else:
        app_textbox_ip16.bg = 'white'

    logger.debug("IP List Generated from Checked Boxes")
    return checkbox_ip_list


def app_sensor_readings_report():
    """ Create a HTML sensor Readings Report containing each IP selected and online. """
    var_ip_list = get_verified_ip_list()
    readings_config = app_reports.HTMLReadings()
    app_reports.sensor_html_report(readings_config, var_ip_list)


def app_sensor_system_report():
    """ Create a HTML sensor System Report containing each IP selected and online. """
    var_ip_list = get_verified_ip_list()
    system_config = app_reports.HTMLSystem()
    app_reports.sensor_html_report(system_config, var_ip_list)


def app_sensor_config_report():
    """ Create a HTML sensor Configuration Report containing each IP selected and online. """
    var_ip_list = get_verified_ip_list()
    sensor_config_config = app_reports.HTMLConfig()
    app_reports.sensor_html_report(sensor_config_config, var_ip_list)


def config_button_save():
    """ Save the programs Configuration and IP list to file """
    logger.debug("Applying Configuration & Saving to File")

    current_config.save_to = config_textbox_save_to.value
    current_config.graph_start = config_textbox_start.value
    current_config.graph_end = config_textbox_end.value
    current_config.datetime_offset = config_textbox_time_offset.value
    current_config.sql_queries_skip = config_textbox_sql_skip.value
    current_config.temperature_offset = config_textbox_temperature_offset.value
    current_config.live_refresh = graph_textbox_refresh_time.value
    current_config.network_timeout_sensor_check = config_textbox_network_check.value
    current_config.network_timeout_data = config_textbox_network_details.value
    current_config.allow_advanced_controls = config_checkbox_power_controls.value
    current_config.ip_list[0] = app_textbox_ip1.value
    current_config.ip_list[1] = app_textbox_ip2.value
    current_config.ip_list[2] = app_textbox_ip3.value
    current_config.ip_list[3] = app_textbox_ip4.value
    current_config.ip_list[4] = app_textbox_ip5.value
    current_config.ip_list[5] = app_textbox_ip6.value
    current_config.ip_list[6] = app_textbox_ip7.value
    current_config.ip_list[7] = app_textbox_ip8.value
    current_config.ip_list[8] = app_textbox_ip9.value
    current_config.ip_list[9] = app_textbox_ip10.value
    current_config.ip_list[10] = app_textbox_ip11.value
    current_config.ip_list[11] = app_textbox_ip12.value
    current_config.ip_list[12] = app_textbox_ip13.value
    current_config.ip_list[13] = app_textbox_ip14.value
    current_config.ip_list[14] = app_textbox_ip15.value
    current_config.ip_list[15] = app_textbox_ip16.value

    app_config.save_config_to_file(current_config)
    set_config()


def set_config():
    """ Sets the programs Configuration to the provided settings. """
    try:
        config_textbox_save_to.value = current_config.save_to
        config_textbox_start.value = current_config.graph_start
        config_textbox_end.value = current_config.graph_end
        config_textbox_time_offset.value = current_config.datetime_offset
        config_textbox_sql_skip.value = current_config.sql_queries_skip
        config_textbox_temperature_offset.value = current_config.temperature_offset
        config_textbox_network_check.value = current_config.network_timeout_sensor_check
        config_textbox_network_details.value = current_config.network_timeout_data
        config_checkbox_power_controls.value = current_config.allow_advanced_controls

        graph_textbox_start.value = current_config.graph_start
        graph_textbox_end.value = current_config.graph_end
        graph_textbox_sql_skip.value = current_config.sql_queries_skip
        graph_textbox_temperature_offset.value = current_config.temperature_offset
        graph_textbox_refresh_time.value = current_config.live_refresh

        app_textbox_ip1.value = current_config.ip_list[0]
        app_textbox_ip2.value = current_config.ip_list[1]
        app_textbox_ip3.value = current_config.ip_list[2]
        app_textbox_ip4.value = current_config.ip_list[3]
        app_textbox_ip5.value = current_config.ip_list[4]
        app_textbox_ip6.value = current_config.ip_list[5]
        app_textbox_ip7.value = current_config.ip_list[6]
        app_textbox_ip8.value = current_config.ip_list[7]
        app_textbox_ip9.value = current_config.ip_list[8]
        app_textbox_ip10.value = current_config.ip_list[9]
        app_textbox_ip11.value = current_config.ip_list[10]
        app_textbox_ip12.value = current_config.ip_list[11]
        app_textbox_ip13.value = current_config.ip_list[12]
        app_textbox_ip14.value = current_config.ip_list[13]
        app_textbox_ip15.value = current_config.ip_list[14]
        app_textbox_ip16.value = current_config.ip_list[15]

        config_checkbox_enable_advanced()

        logger.debug("Configuration Set - OK")
    except Exception as error:
        logger.error("Configuration Set - One or More Items Failed - " + str(error))


def config_button_save_directory():
    """ Sets where the programs saves HTML graphs and Reports. """
    save_to = filedialog.askdirectory()

    if len(save_to) > 1:
        config_textbox_save_to.value = save_to + "/"
        logger.debug("Changed Save to Directory")
    else:
        logger.warning("Invalid Directory Chosen for Save to Directory")


def config_button_reset_defaults():
    """ Resets all Control Center Configurations to default. """
    logger.info("Resetting Configuration to Defaults")
    current_config.reset_to_defaults()
    set_config()


def config_checkbox_enable_advanced():
    """ Enables disabled buttons in the Control Center application. """
    if config_checkbox_power_controls.value == 1:
        config_button_reset.enable()
        commands_button_shutdown.enable()
        commands_button_os_Upgrade.enable()
        sensor_config_button_update_datetime.enable()
        sensor_config_button_set_config.enable()
    else:
        config_button_reset.disable()
        commands_button_shutdown.disable()
        commands_button_os_Upgrade.disable()
        sensor_config_button_update_datetime.disable()
        sensor_config_button_set_config.disable()


def commands_upgrade_smb():
    """ Sends the upgrade by SMB command to the Sensor Units IP. """
    logger.debug("Sensor Upgrade - SMB")
    ip_list = get_verified_ip_list()

    for ip in ip_list:
        sensor_commands.upgrade_program_smb(ip)

    info("Sensors Upgrading SMB", "Please Wait up to 30 seconds for the Services to restart")


def commands_upgrade_http():
    """ Sends the upgrade by HTTP command to the Sensor Units IP. """
    logger.debug("Sensor Upgrade - HTTP")
    ip_list = get_verified_ip_list()

    for ip in ip_list:
        sensor_commands.upgrade_program_online(ip)

    info("Sensors Upgrading HTTP", "Please Wait up to 30 seconds for the Services to restart")


def commands_os_upgrade():
    """ Sends the upgrade Operating System command to the Sensor Units IP. """
    logger.debug("Sensor OS Upgrade")
    ip_list = get_verified_ip_list()

    for ip in ip_list:
        sensor_commands.upgrade_os_linux(ip)

    info("Sensors Operating System Upgrade Started",
         "Once complete, the Sensors will automatically reboot\n"
         "Sensor should continue to Operate with minor interruptions\n\n"
         "This process can take anywhere from 5 Min to 1 Hour")


def commands_sensor_reboot():
    """ Sends the reboot system command to the Sensor Units IP. """
    logger.debug("Sensor Reboot")
    ip_list = get_verified_ip_list()

    for ip in ip_list:
        sensor_commands.reboot_sensor(ip)

    info("Sensors Rebooting", "Allow up to 3 Min to reboot")


def commands_sensor_shutdown():
    """ Sends the shutdown system command to the Sensor Units IP. """
    logger.debug("Sensor Shutdown")
    ip_list = get_verified_ip_list()

    for ip in ip_list:
        sensor_commands.shutdown_sensor(ip)

    info("Sensors Shutting Down", "Allow up to 15 seconds to fully shutdown")


def commands_restart_services():
    """ Sends the restart services command to the Sensor Units IP. """
    logger.info("Sensor(s) Services Restarting - Please allow up to 20 Seconds to restart")
    ip_list = get_verified_ip_list()

    for ip in ip_list:
        sensor_commands.restart_services(ip)

    info("Sensors Services Restarting", "Please allow up to 20 Seconds to restart")


def commands_hostname_change():
    """ Sends the host name change command to the Sensor Units IP, along with the new host name. """
    logger.debug("Change Sensor Hostname")
    ip_list = get_verified_ip_list()

    for ip in ip_list:
        sensor_commands.set_hostname(ip)


def commands_datetime_update():
    """ Sends the Date & Time update command to the Sensor Units IP, along with the computers Date & Time. """
    logger.debug("Updating Sensors DateTime")
    ip_list = get_verified_ip_list()

    for ip in ip_list:
        sensor_commands.set_datetime(ip)

    info("Sensors DateTime Set", "Sensors Date & Time Synchronized with local Computer's")


def sensor_config_enable_recording():
    """ Enables or disables the timing Sensor Configuration Window text boxes. """
    if sensor_config_checkbox_db_record.value:
        sensor_config_textbox_interval.enable()
        sensor_config_textbox_trigger.enable()
    else:
        sensor_config_textbox_interval.disable()
        sensor_config_textbox_trigger.disable()


def sensor_config_enable_custom():
    """ Enables or disables the custom Sensor Configuration Window text boxes. """
    if sensor_config_checkbox_custom.value:
        sensor_config_textbox_custom_acc.enable()
        sensor_config_textbox_custom_mag.enable()
        sensor_config_textbox_custom_gyro.enable()
    else:
        sensor_config_textbox_custom_acc.disable()
        sensor_config_textbox_custom_mag.disable()
        sensor_config_textbox_custom_gyro.disable()


def sensor_config_set():
    """ Sends the update configuration command to the Sensor Units IP, along with the new configuration. """
    logger.debug("Setting Sensor Config")
    ip_list = get_verified_ip_list()
    config_settings_str = "," + str(sensor_config_checkbox_db_record.value) + "," + \
        str(sensor_config_textbox_interval.value) + "," + \
        str(sensor_config_textbox_trigger.value) + "," + \
        str(sensor_config_checkbox_custom.value) + "," + \
        str(sensor_config_textbox_custom_acc.value) + "," + \
        str(sensor_config_textbox_custom_mag.value) + "," + \
        str(sensor_config_textbox_custom_gyro.value)

    for ip in ip_list:
        sensor_commands.set_sensor_config(ip, config_settings_str)

    info("Sensors Configuration Set", "Configurations Set")


def _graph_radio_selection():
    """ Enables or disables the Graph Window selections, based on graph type selected. """
    _graph_enable_all_checkboxes()
    if graph_radio_sensor_type.get() == "Interval SQL":
        graph_checkbox_acc.disable()
        graph_checkbox_mag.disable()
        graph_checkbox_gyro.disable()
        graph_button_live.disable()
        graph_textbox_refresh_time.disable()

        graph_checkbox_cpu_temp.enable()
        graph_textbox_temperature_offset.enable()
        graph_checkbox_temperature.enable()
        graph_checkbox_pressure.enable()
        graph_checkbox_humidity.enable()
        graph_checkbox_lumen.enable()
        graph_checkbox_colour.enable()
        graph_checkbox_up_time.enable()
        graph_textbox_start.enable()
        graph_textbox_end.enable()
        graph_textbox_sql_skip.enable()
        graph_button_database.enable()

    if graph_radio_sensor_type.get() == "Trigger SQL":
        graph_textbox_sql_skip.disable()
        graph_textbox_temperature_offset.disable()
        graph_checkbox_cpu_temp.disable()
        graph_checkbox_temperature.disable()
        graph_checkbox_pressure.disable()
        graph_checkbox_humidity.disable()
        graph_checkbox_lumen.disable()
        graph_checkbox_colour.disable()
        graph_checkbox_up_time.disable()
        graph_button_live.disable()
        graph_textbox_refresh_time.disable()

        graph_checkbox_acc.enable()
        graph_checkbox_mag.enable()
        graph_checkbox_gyro.enable()
        graph_textbox_start.enable()
        graph_textbox_end.enable()
        graph_textbox_sql_skip.disable()
        graph_button_database.enable()

    if graph_radio_sensor_type.get() == "Live":
        graph_button_database.disable()
        graph_textbox_sql_skip.disable()
        graph_textbox_start.disable()
        graph_textbox_end.disable()

        graph_textbox_temperature_offset.enable()
        graph_textbox_refresh_time.enable()

        graph_checkbox_up_time.enable()
        graph_checkbox_up_time.value = 0
        graph_checkbox_cpu_temp.enable()
        graph_checkbox_cpu_temp.value = 0
        graph_checkbox_temperature.enable()
        graph_checkbox_temperature.value = 0
        graph_checkbox_pressure.enable()
        graph_checkbox_pressure.value = 0
        graph_checkbox_humidity.enable()
        graph_checkbox_humidity.value = 0
        graph_checkbox_lumen.enable()
        graph_checkbox_lumen.value = 0
        graph_checkbox_colour.disable()
        graph_checkbox_colour.value = 0
        graph_checkbox_acc.disable()
        graph_checkbox_acc.value = 0
        graph_checkbox_mag.disable()
        graph_checkbox_mag.value = 0
        graph_checkbox_gyro.disable()
        graph_checkbox_gyro.value = 0

        graph_button_live.enable()


def graph_plotly_button():
    """ Create Plotly offline HTML Graph, based on user selections in the Graph Window. """
    new_graph_data = app_graph.CreateGraphData()
    new_graph_data.db_location = filedialog.askopenfilename()

    current_config.graph_start = graph_textbox_start.value
    current_config.graph_end = graph_textbox_end.value
    current_config.sql_queries_skip = graph_textbox_sql_skip.value
    current_config.temperature_offset = graph_textbox_temperature_offset.value

    app_config.check_config(current_config)
    set_config()

    new_graph_data.save_file_to = current_config.save_to
    new_graph_data.graph_start = current_config.graph_start
    new_graph_data.graph_end = current_config.graph_end
    new_graph_data.time_offset = current_config.datetime_offset
    new_graph_data.skip_sql = current_config.sql_queries_skip
    new_graph_data.temperature_offset = current_config.temperature_offset
    new_graph_data.graph_columns = _graph_get_column_checkboxes()

    if graph_radio_sensor_type.get() == "Interval SQL":
        app_graph.start_graph_interval(new_graph_data)
    elif graph_radio_sensor_type.get() == "Trigger SQL":
        app_graph.start_graph_trigger(new_graph_data)


def graph_live_button():
    pyplot.close()
    try:
        graph_checkbox = _graph_get_column_checkboxes()[3]
        ip_list = get_verified_ip_list()

        current_config.live_refresh = graph_textbox_refresh_time.value
        current_config.temperature_offset = graph_textbox_temperature_offset.value
        app_config.check_config(current_config)
        set_config()

        app_graph.CreateLiveGraph(graph_checkbox, ip_list[0], current_config)
    except Exception as error:
        logger.warning("No sensors selected in the main window - " + str(error))
        warn("Select Sensor", "Please Select a Sensor IP from the Main window\n"
                              "& Sensor Type from the Graph window")


def _graph_get_column_checkboxes():
    """ Returns selected SQL Columns from the Graph Window, depending on the Data Source Selected. """
    column_checkboxes = ["DateTime", "SensorName", "IP"]

    data_source_radio = graph_radio_sensor_type.get()
    if data_source_radio == "Interval SQL" or data_source_radio == "Live":
        if graph_checkbox_up_time.value:
            column_checkboxes.append("SensorUpTime")
        if graph_checkbox_cpu_temp.value:
            column_checkboxes.append("SystemTemp")
        if graph_checkbox_temperature.value:
            column_checkboxes.append("EnvironmentTemp")
        if graph_checkbox_pressure.value:
            column_checkboxes.append("Pressure")
        if graph_checkbox_humidity.value:
            column_checkboxes.append("Humidity")
        if graph_checkbox_lumen.value:
            column_checkboxes.append("Lumen")
        if graph_checkbox_colour.value:
            column_checkboxes.append("Red")
            column_checkboxes.append("Green")
            column_checkboxes.append("Blue")
    if data_source_radio == "Trigger SQL" or data_source_radio == "Live":
        if graph_checkbox_acc.value:
            column_checkboxes.append("Acc_X")
            column_checkboxes.append("Acc_Y")
            column_checkboxes.append("Acc_Z")
        if graph_checkbox_mag.value:
            column_checkboxes.append("Mag_X")
            column_checkboxes.append("Mag_Y")
            column_checkboxes.append("Mag_Z")
        if graph_checkbox_gyro.value:
            column_checkboxes.append("Gyro_X")
            column_checkboxes.append("Gyro_Y")
            column_checkboxes.append("Gyro_Z")

    logger.debug(str(column_checkboxes))
    return column_checkboxes


def _graph_enable_all_checkboxes():
    graph_checkbox_up_time.enable()
    graph_checkbox_up_time.value = 0
    graph_checkbox_cpu_temp.enable()
    graph_checkbox_cpu_temp.value = 0
    graph_checkbox_temperature.enable()
    graph_checkbox_temperature.value = 0
    graph_checkbox_pressure.enable()
    graph_checkbox_pressure.value = 0
    graph_checkbox_humidity.enable()
    graph_checkbox_humidity.value = 0
    graph_checkbox_lumen.enable()
    graph_checkbox_lumen.value = 0
    graph_checkbox_colour.enable()
    graph_checkbox_colour.value = 0
    graph_checkbox_acc.enable()
    graph_checkbox_acc.value = 0
    graph_checkbox_mag.enable()
    graph_checkbox_mag.value = 0
    graph_checkbox_gyro.enable()
    graph_checkbox_gyro.value = 0


def _graph_disable_other_checkboxes(var_checkbox):
    if graph_radio_sensor_type.value == "Live":
        if var_checkbox is "Uptime":
            pass
        else:
            graph_checkbox_up_time.disable()
            graph_checkbox_up_time.value = 0
        if var_checkbox is "Temperature":
            pass
        else:
            graph_checkbox_temperature.disable()
            graph_checkbox_temperature.value = 0
        if var_checkbox is "CPUTemperature":
            pass
        else:
            graph_checkbox_cpu_temp.disable()
            graph_checkbox_cpu_temp.value = 0
        if var_checkbox is "Pressure":
            pass
        else:
            graph_checkbox_pressure.disable()
            graph_checkbox_pressure.value = 0
        if var_checkbox is "Humidity":
            pass
        else:
            graph_checkbox_humidity.disable()
            graph_checkbox_humidity.value = 0
        if var_checkbox is "Lumen":
            pass
        else:
            graph_checkbox_lumen.disable()
            graph_checkbox_lumen.value = 0
        # if var_checkbox is "RGB":
        #     pass
        # else:
        #     graph_checkbox_colour.disable()
        #     graph_checkbox_colour.value = 0
        # if var_checkbox is "Accelerometer":
        #     pass
        # else:
        #     graph_checkbox_acc.disable()
        #     graph_checkbox_acc.value = 0
        # if var_checkbox is "Magnetometer":
        #     pass
        # else:
        #     graph_checkbox_mag.disable()
        #     graph_checkbox_mag.value = 0
        # if var_checkbox is "Gyroscopic":
        #     pass
        # else:
        #     graph_checkbox_gyro.disable()
        #     graph_checkbox_gyro.value = 0

        if var_checkbox is "Uptime":
            if graph_checkbox_up_time.value == 0:
                _graph_enable_all_checkboxes()
            else:
                graph_checkbox_up_time.enable()
                graph_checkbox_up_time.value = 1
        elif var_checkbox is "Temperature":
            if graph_checkbox_temperature.value == 0:
                _graph_enable_all_checkboxes()
            else:
                graph_checkbox_temperature.enable()
                graph_checkbox_temperature.value = 1
        elif var_checkbox is "CPUTemperature":
            if graph_checkbox_cpu_temp.value == 0:
                _graph_enable_all_checkboxes()
            else:
                graph_checkbox_cpu_temp.enable()
                graph_checkbox_cpu_temp.value = 1
        elif var_checkbox is "Pressure":
            if graph_checkbox_pressure.value == 0:
                _graph_enable_all_checkboxes()
            else:
                graph_checkbox_pressure.enable()
                graph_checkbox_pressure.value = 1
        elif var_checkbox is "Humidity":
            if graph_checkbox_humidity.value == 0:
                _graph_enable_all_checkboxes()
            else:
                graph_checkbox_humidity.enable()
                graph_checkbox_humidity.value = 1
        elif var_checkbox is "Lumen":
            if graph_checkbox_lumen.value == 0:
                _graph_enable_all_checkboxes()
            else:
                graph_checkbox_lumen.enable()
                graph_checkbox_lumen.value = 1
        # elif var_checkbox is "RGB":
        #     if graph_checkbox_colour.value == 0:
        #         _graph_enable_all_checkboxes()
        #     else:
        #         graph_checkbox_colour.enable()
        #         graph_checkbox_colour.value = 1
        # elif var_checkbox is "Accelerometer":
        #     if graph_checkbox_acc.value == 0:
        #         _graph_enable_all_checkboxes()
        #     else:
        #         graph_checkbox_acc.enable()
        #         graph_checkbox_acc.value = 1
        # elif var_checkbox is "Magnetometer":
        #     if graph_checkbox_mag.value == 0:
        #         _graph_enable_all_checkboxes()
        #     else:
        #         graph_checkbox_mag.enable()
        #         graph_checkbox_mag.value = 1
        # elif var_checkbox is "Gyroscopic":
        #     if graph_checkbox_gyro.value == 0:
        #         _graph_enable_all_checkboxes()
        #     else:
        #         graph_checkbox_gyro.enable()
        #         graph_checkbox_gyro.value = 1

        graph_checkbox_colour.disable()
        graph_checkbox_colour.value = 0
        graph_checkbox_acc.disable()
        graph_checkbox_acc.value = 0
        graph_checkbox_mag.disable()
        graph_checkbox_mag.value = 0
        graph_checkbox_gyro.disable()
        graph_checkbox_gyro.value = 0


# GUI Window Setup
app = App(title="KootNet Sensors - PC Control Center",
          width=405,
          height=295,

          layout="grid")

window_app_about = Window(app,
                          title="About KootNet Sensors - PC Control Center",
                          width=610,
                          height=325,
                          layout="grid",
                          visible=False)

window_config = Window(app,
                       title="Control Center Configuration",
                       width=580,
                       height=300,
                       layout="grid",
                       visible=False)

window_sensor_commands = Window(app,
                                title="Sensor Commands",
                                width=290,
                                height=285,
                                layout="grid",
                                visible=False)

window_sensor_config = Window(app,
                              title="Sensors Configuration Updater",
                              width=340,
                              height=265,
                              layout="grid",
                              visible=False)

window_sensor_reports = Window(app,
                               title="Sensor Reports",
                               width=475,
                               height=100,
                               layout="grid",
                               visible=False)

window_graph = Window(app,
                      title="Graphing",
                      width=275,
                      height=505,
                      layout="grid",
                      visible=False)

app_menubar = MenuBar(app,
                      toplevel=[["File"],
                                ["Sensors"],
                                ["Graphing"],
                                ["Help"]],
                      options=[[["Open Logs",
                                 app_menu_open_logs],
                                ["Save IP's",
                                 config_button_save],
                                ["Control Center Configuration",
                                 window_config.show]],
                               [["Send Commands",
                                window_sensor_commands.show],
                                ["Update Configurations",
                                window_sensor_config.show],
                                ["Create Reports",
                                window_sensor_reports.show]],
                               [["Open Graph Window",
                                 window_graph.show]],
                               [["KootNet Sensors - About",
                                 window_app_about.show],
                                ["KootNet Sensors - Website",
                                 app_menu_open_website],
                                ["Sensor Units - DIY",
                                 app_menu_open_build_sensor],
                                ["Sensor Units - Help",
                                 app_menu_open_sensor_help],
                                ["PC Control Center - Help *WIP",
                                 window_app_about.show]]])

app_button_check_sensor = PushButton(app,
                                     text="Check Sensors\nStatus",
                                     command=get_verified_ip_list,
                                     grid=[1, 15, 2, 1],
                                     align="left")

app_button_sensor_detail = PushButton(app,
                                      text="Download Sensor\nInterval Databases",
                                      command=app_menu_download_interval_db,
                                      grid=[2, 15, 2, 1],
                                      align="right")

app_button_sensor_config = PushButton(app,
                                      text="Download Sensor\nTrigger Databases",
                                      command=app_menu_download_trigger_db,
                                      grid=[4, 15],
                                      align="right")

# Sensor's Online / Offline IP List Selection 1
app_checkbox_all_column1 = CheckBox(app,
                                    text="Check ALL Column 1",
                                    command=app_check_all_ip_checkboxes,
                                    args=[1],
                                    grid=[1, 1, 3, 1],
                                    align="left")

app_checkbox_ip1 = CheckBox(app,
                            text="IP        ",
                            grid=[1, 2],
                            align="left")

app_textbox_ip1 = TextBox(app,
                          text="192.168.10.11",
                          width=21,
                          grid=[2, 2],
                          align="left")

app_checkbox_ip2 = CheckBox(app,
                            text="IP ",
                            grid=[1, 3],
                            align="left")

app_textbox_ip2 = TextBox(app,
                          text="192.168.10.12",
                          width=21,
                          grid=[2, 3],
                          align="left")

app_checkbox_ip3 = CheckBox(app,
                            text="IP ",
                            grid=[1, 4],
                            align="left")

app_textbox_ip3 = TextBox(app,
                          text="192.168.10.13",
                          width=21,
                          grid=[2, 4],
                          align="left")

app_checkbox_ip4 = CheckBox(app,
                            text="IP ",
                            grid=[1, 5],
                            align="left")

app_textbox_ip4 = TextBox(app,
                          text="192.168.10.14",
                          width=21,
                          grid=[2, 5],
                          align="left")

app_checkbox_ip5 = CheckBox(app,
                            text="IP ",
                            grid=[1, 6],
                            align="left")

app_textbox_ip5 = TextBox(app,
                          text="192.168.10.15",
                          width=21,
                          grid=[2, 6],
                          align="left")

app_checkbox_ip6 = CheckBox(app,
                            text="IP ",
                            grid=[1, 7],
                            align="left")

app_textbox_ip6 = TextBox(app,
                          text="192.168.10.16",
                          width=21,
                          grid=[2, 7],
                          align="left")

app_checkbox_ip7 = CheckBox(app,
                            text="IP ",
                            grid=[1, 8],
                            align="left")

app_textbox_ip7 = TextBox(app,
                          text="192.168.10.17",
                          width=21,
                          grid=[2, 8],
                          align="left")

app_checkbox_ip8 = CheckBox(app,
                            text="IP ",
                            grid=[1, 9],
                            align="left")

app_textbox_ip8 = TextBox(app,
                          text="192.168.10.18",
                          width=21,
                          grid=[2, 9],
                          align="left")

# Sensor's Online / Offline IP List Selection 2
app_checkbox_all_column2 = CheckBox(app,
                                    text="Check ALL Column 2",
                                    command=app_check_all_ip_checkboxes,
                                    args=[2],
                                    grid=[3, 1, 3, 1],
                                    align="left")

app_checkbox_ip9 = CheckBox(app,
                            text="IP        ",
                            grid=[3, 2],
                            align="left")

app_textbox_ip9 = TextBox(app,
                          text="192.168.10.19",
                          width=21,
                          grid=[4, 2],
                          align="left")

app_checkbox_ip10 = CheckBox(app,
                             text="IP ",
                             grid=[3, 3],
                             align="left")

app_textbox_ip10 = TextBox(app,
                           text="192.168.10.20",
                           width=21,
                           grid=[4, 3],
                           align="left")

app_checkbox_ip11 = CheckBox(app,
                             text="IP ",
                             grid=[3, 4],
                             align="left")

app_textbox_ip11 = TextBox(app,
                           text="192.168.10.21",
                           width=21,
                           grid=[4, 4],
                           align="left")

app_checkbox_ip12 = CheckBox(app,
                             text="IP ",
                             grid=[3, 5],
                             align="left")

app_textbox_ip12 = TextBox(app,
                           text="192.168.10.22",
                           width=21,
                           grid=[4, 5],
                           align="left")

app_checkbox_ip13 = CheckBox(app,
                             text="IP ",
                             grid=[3, 6],
                             align="left")

app_textbox_ip13 = TextBox(app,
                           text="192.168.10.23",
                           width=21,
                           grid=[4, 6],
                           align="left")

app_checkbox_ip14 = CheckBox(app,
                             text="IP ",
                             grid=[3, 7],
                             align="left")

app_textbox_ip14 = TextBox(app,
                           text="192.168.10.24",
                           width=21,
                           grid=[4, 7],
                           align="left")

app_checkbox_ip15 = CheckBox(app,
                             text="IP ",
                             grid=[3, 8],
                             align="left")

app_textbox_ip15 = TextBox(app,
                           text="192.168.10.25",
                           width=21,
                           grid=[4, 8],
                           align="left")

app_checkbox_ip16 = CheckBox(app,
                             text="IP ",
                             grid=[3, 9],
                             align="left")

app_textbox_ip16 = TextBox(app,
                           text="192.168.10.26",
                           width=21,
                           grid=[4, 9],
                           align="left")

# About Window Section
about_text1 = Text(window_app_about,
                   text=current_config.app_version,
                   grid=[1, 1],
                   align="right")

about_textbox = TextBox(window_app_about,
                        text="Should of been Replaced with About Text",
                        grid=[1, 2],
                        width=75,
                        height=18,
                        multiline=True,
                        align="right")

# Configuration Window Section
config_button_reset = PushButton(window_config,
                                 text="Reset to\nDefaults",
                                 command=config_button_reset_defaults,
                                 grid=[1, 1],
                                 align="right")

config_checkbox_power_controls = CheckBox(window_config,
                                          text="Enable Advanced\nSensor Commands &\nConfiguration Options",
                                          command=config_checkbox_enable_advanced,
                                          grid=[1, 1],
                                          align="top")

config_button_save_apply = PushButton(window_config,
                                      text="Save &\nApply",
                                      command=config_button_save,
                                      grid=[1, 1],
                                      align="left")

config_text_database_time = Text(window_config,
                                 text="Sensor Databases\nSaved in UTC 0",
                                 size=10,
                                 grid=[2, 1],
                                 color='#CB0000',
                                 align="top")

config_text_spacer1 = Text(window_config,
                           text=" ",
                           grid=[1, 2],
                           align="left")

config_text3 = Text(window_config,
                    text="Save Files To",
                    color='blue',
                    grid=[1, 3],
                    align="top")

config_button_save_dir = PushButton(window_config,
                                    text="Choose Folder",
                                    command=config_button_save_directory,
                                    grid=[1, 5],
                                    align="bottom")

config_textbox_save_to = TextBox(window_config,
                                 text='',
                                 width=50,
                                 grid=[1, 4],
                                 align="bottom")

config_text_spacer3 = Text(window_config,
                           text=" ",
                           grid=[1, 6],
                           align="left")

config_text_info = Text(window_config,
                        text="Default Graph Date Range",
                        color='blue',
                        grid=[1, 7],
                        align="top")

config_text_start = Text(window_config,
                         text="         Start DateTime: ",
                         color='green',
                         grid=[1, 8],
                         align="left")

config_textbox_start = TextBox(window_config,
                               text="",
                               width=20,
                               grid=[1, 8],
                               align="right")

config_text_end = Text(window_config,
                       text="         End DateTime: ",
                       color='green',
                       grid=[1, 9],
                       align="left")

config_textbox_end = TextBox(window_config,
                             text="",
                             width=20,
                             grid=[1, 9],
                             align="right")

config_text_time_offset2 = Text(window_config,
                                text="Graph DateTime Offset in Hours",
                                color='blue',
                                grid=[2, 1],
                                align="bottom")

config_textbox_time_offset = TextBox(window_config,
                                     text="",
                                     width="5",
                                     grid=[2, 2],
                                     align="bottom")

config_text_sql_skip = Text(window_config,
                            text="Add SQL row to Graph every 'X' rows",
                            color='blue',
                            grid=[2, 3],
                            align="top")

config_textbox_sql_skip = TextBox(window_config,
                                  text="",
                                  width="5",
                                  grid=[2, 4],
                                  align="top")

config_text_temperature_offset = Text(window_config,
                                      text="Environment Temperature Offset in °C",
                                      color='blue',
                                      grid=[2, 5],
                                      align="top")

config_textbox_temperature_offset = TextBox(window_config,
                                            text="",
                                            width="5",
                                            grid=[2, 5],
                                            align="bottom")

config_text_network_timeouts = Text(window_config,
                                    text="Network Timeouts in Seconds",
                                    color='blue',
                                    grid=[2, 6],
                                    align="top")

config_text_network_timeouts1 = Text(window_config,
                                     text="Sensor Status",
                                     color='green',
                                     grid=[2, 7],
                                     align="top")

config_textbox_network_check = TextBox(window_config,
                                       text="",
                                       width="5",
                                       grid=[2, 8],
                                       align="top")

config_text_network_timeouts2 = Text(window_config,
                                     text="Sensor Reports",
                                     color='green',
                                     grid=[2, 9],
                                     align="top")

config_textbox_network_details = TextBox(window_config,
                                         text="",
                                         width="5",
                                         grid=[2, 10],
                                         align="top")

# Sensor Reports Window Section
reports_text_select = Text(window_sensor_reports,
                           text="Check Sensor IPs from The Main Window",
                           grid=[1, 1, 3, 1],
                           color='#CB0000',
                           align="top")

reports_text1 = Text(window_sensor_reports,
                     text="Live Readings Report  |",
                     color='blue',
                     grid=[1, 6],
                     align="top")

reports_button_check_sensor = PushButton(window_sensor_reports,
                                         text="Create",
                                         command=app_sensor_readings_report,
                                         grid=[1, 7],
                                         align="top")

reports_text2 = Text(window_sensor_reports,
                     text="|  System Report  |",
                     color='blue',
                     grid=[2, 6],
                     align="top")

reports_button_sensor_detail = PushButton(window_sensor_reports,
                                          text="Create",
                                          command=app_sensor_system_report,
                                          grid=[2, 7],
                                          align="top")

reports_text3 = Text(window_sensor_reports,
                     text="|  Configuration Report",
                     color='blue',
                     grid=[3, 6],
                     align="top")

reports_button_sensor_config = PushButton(window_sensor_reports,
                                          text="Create",
                                          command=app_sensor_config_report,
                                          grid=[3, 7],
                                          align="top")

# Graph Window Section
graph_text_sensor_type_name = Text(window_graph,
                                   text="Data Source",
                                   color='blue',
                                   grid=[1, 1, 2, 1],
                                   align="top")

graph_radio_sensor_type = ButtonGroup(window_graph,
                                      options=["Live", "Interval SQL", "Trigger SQL"],
                                      horizontal="True",
                                      command=_graph_radio_selection,
                                      grid=[1, 2, 2, 1],
                                      align="top")

graph_text_space1 = Text(window_graph,
                         text=" ",
                         grid=[1, 3],
                         align="right")

graph_text_start = Text(window_graph,
                        text="Start DateTime: ",
                        color='green',
                        grid=[1, 6],
                        align="left")

graph_textbox_start = TextBox(window_graph,
                              text="",
                              width=20,
                              grid=[2, 6],
                              align="left")

graph_text_end = Text(window_graph,
                      text="End DateTime:",
                      color='green',
                      grid=[1, 7],
                      align="left")

graph_textbox_end = TextBox(window_graph,
                            text="",
                            width=20,
                            grid=[2, 7],
                            align="left")

graph_text_sql_skip = Text(window_graph,
                           text="Add row every:",
                           color='green',
                           grid=[1, 8],
                           align="left")

graph_textbox_sql_skip = TextBox(window_graph,
                                 text="",
                                 width=10,
                                 grid=[2, 8],
                                 align="left")

graph_text_sql_skip2 = Text(window_graph,
                            text="rows    ",
                            color='green',
                            grid=[2, 8],
                            align="right")

graph_text_temperature_offset = Text(window_graph,
                                     text="Environmental:",
                                     color='green',
                                     grid=[1, 9],
                                     align="left")

graph_textbox_temperature_offset = TextBox(window_graph,
                                           text="",
                                           width=5,
                                           grid=[2, 9],
                                           align="left")

graph_text_temperature_offset2 = Text(window_graph,
                                      text="Temp Offset",
                                      color='green',
                                      grid=[2, 9],
                                      align="right")

graph_text_refresh_time = Text(window_graph,
                               text="Live refresh (Sec):",
                               color='green',
                               grid=[1, 10],
                               align="left")

graph_textbox_refresh_time = TextBox(window_graph,
                                     text="2",
                                     width=5,
                                     grid=[2, 10],
                                     align="left")

graph_text_space2 = Text(window_graph,
                         text=" ",
                         grid=[1, 11],
                         align="right")

graph_text_column_selection = Text(window_graph,
                                   text="Interval Sensors",
                                   color='blue',
                                   grid=[1, 15, 2, 1],
                                   align="top")

graph_checkbox_up_time = CheckBox(window_graph,
                                  text="System Uptime",
                                  command=_graph_disable_other_checkboxes,
                                  args=["Uptime"],
                                  grid=[1, 16],
                                  align="left")

graph_checkbox_cpu_temp = CheckBox(window_graph,
                                   text="CPU Temperature",
                                   command=_graph_disable_other_checkboxes,
                                   args=["CPUTemperature"],
                                   grid=[1, 17],
                                   align="left")

graph_checkbox_temperature = CheckBox(window_graph,
                                      text="Env Temperature",
                                      command=_graph_disable_other_checkboxes,
                                      args=["Temperature"],
                                      grid=[1, 18],
                                      align="left")

graph_checkbox_pressure = CheckBox(window_graph,
                                   text="Pressure",
                                   command=_graph_disable_other_checkboxes,
                                   args=["Pressure"],
                                   grid=[1, 19],
                                   align="left")

graph_checkbox_humidity = CheckBox(window_graph,
                                   text="Humidity",
                                   command=_graph_disable_other_checkboxes,
                                   args=["Humidity"],
                                   grid=[2, 16],
                                   align="left")

graph_checkbox_lumen = CheckBox(window_graph,
                                text="Lumen",
                                command=_graph_disable_other_checkboxes,
                                args=["Lumen"],
                                grid=[2, 17],
                                align="left")

graph_checkbox_colour = CheckBox(window_graph,
                                 text="Colour RGB",
                                 command=_graph_disable_other_checkboxes,
                                 args=["RGB"],
                                 grid=[2, 18],
                                 align="left")

graph_text_column_selection2 = Text(window_graph,
                                    text="Trigger Sensors",
                                    color='blue',
                                    grid=[1, 24, 2, 1],
                                    align="bottom")

graph_checkbox_acc = CheckBox(window_graph,
                              text="Accelerometer XYZ",
                              command=_graph_disable_other_checkboxes,
                              args=["Accelerometer"],
                              grid=[1, 25],
                              align="left")

graph_checkbox_mag = CheckBox(window_graph,
                              text="Magnetometer XYZ",
                              command=_graph_disable_other_checkboxes,
                              args=["Magnetometer"],
                              grid=[2, 25],
                              align="left")

graph_checkbox_gyro = CheckBox(window_graph,
                               text="Gyroscopic XYZ",
                               command=_graph_disable_other_checkboxes,
                               args=["Gyroscopic"],
                               grid=[1, 26],
                               align="left")

graph_text_space3 = Text(window_graph,
                         text=" ",
                         grid=[1, 35],
                         align="right")

graph_button_database = PushButton(window_graph,
                                   text="Open & Graph\nDatabase",
                                   command=graph_plotly_button,
                                   grid=[1, 36, 2, 1],
                                   align="left")

graph_button_live = PushButton(window_graph,
                               text="Start Live Graph",
                               command=graph_live_button,
                               grid=[2, 36],
                               align="left")

# Sensor Commands Window
commands_text_select = Text(window_sensor_commands,
                            text="Check Sensor IPs from the Main Window",
                            grid=[1, 1, 3, 1],
                            color='#CB0000',
                            align="left")

commands_text_upgrade = Text(window_sensor_commands,
                             text="Upgrade Commands",
                             grid=[1, 2, 2, 1],
                             color='blue',
                             align="left")

commands_button_lan_Upgrade = PushButton(window_sensor_commands,
                                         text="Upgrade\nSoftware\nOver SMB",
                                         command=commands_upgrade_smb,
                                         grid=[1, 3],
                                         align="left")

commands_button_online_Upgrade = PushButton(window_sensor_commands,
                                            text="Upgrade\nSoftware\nOver HTTP",
                                            command=commands_upgrade_http,
                                            grid=[2, 3],
                                            align="left")

commands_button_os_Upgrade = PushButton(window_sensor_commands,
                                        text="Upgrade\nOperating\nSystem",
                                        command=commands_os_upgrade,
                                        grid=[3, 3],
                                        align="left")

commands_text_power = Text(window_sensor_commands,
                           text="Power Commands",
                           grid=[1, 4, 3, 1],
                           color='blue',
                           align="left")

commands_button_reboot = PushButton(window_sensor_commands,
                                    text="Reboot",
                                    command=commands_sensor_reboot,
                                    grid=[1, 5],
                                    align="left")

commands_button_shutdown = PushButton(window_sensor_commands,
                                      text="Shutdown",
                                      command=commands_sensor_shutdown,
                                      grid=[2, 5],
                                      align="left")

commands_text_other = Text(window_sensor_commands,
                           text="Other Commands",
                           grid=[1, 6, 3, 1],
                           color='blue',
                           align="left")

commands_button_terminate = PushButton(window_sensor_commands,
                                       text="Restart\nServices",
                                       command=commands_restart_services,
                                       grid=[1, 7],
                                       align="left")

sensor_config_button_get_config = PushButton(window_sensor_commands,
                                             text="Change\nNames",
                                             command=commands_hostname_change,
                                             grid=[2, 7],
                                             align="left")

sensor_config_button_update_datetime = PushButton(window_sensor_commands,
                                                  text="Sync DateTime\nwith Computer",
                                                  command=commands_datetime_update,
                                                  grid=[3, 7],
                                                  align="left")

# Update Sensor Configuration Section
sensor_config_text_select = Text(window_sensor_config,
                                 text="Check Sensor IPs from the Main Window",
                                 grid=[1, 1, 3, 1],
                                 color='#CB0000',
                                 align="left")

sensor_config_checkbox_db_record = CheckBox(window_sensor_config,
                                            text="Enable Database Recording",
                                            command=sensor_config_enable_recording,
                                            grid=[1, 2, 2, 1],
                                            align="left")

sensor_config_textbox_interval = TextBox(window_sensor_config,
                                         text='300',
                                         width=10,
                                         grid=[1, 3],
                                         align="left")

sensor_config_text_interval = Text(window_sensor_config,
                                   text="Seconds Between Interval Recording",
                                   color='green',
                                   grid=[2, 3],
                                   align="left")

sensor_config_textbox_trigger = TextBox(window_sensor_config,
                                        text='0.15',
                                        width=10,
                                        grid=[1, 4],
                                        align="left")

sensor_config_text_trigger = Text(window_sensor_config,
                                  text="Seconds Between Trigger Readings",
                                  color='green',
                                  grid=[2, 4],
                                  align="left")

sensor_config_checkbox_custom = CheckBox(window_sensor_config,
                                         text="Enable Custom Settings",
                                         command=sensor_config_enable_custom,
                                         grid=[1, 5, 2, 1],
                                         align="left")

sensor_config_textbox_custom_acc = TextBox(window_sensor_config,
                                           text='0.05',
                                           width=10,
                                           grid=[1, 6],
                                           align="left")

sensor_config_text_custom_acc = Text(window_sensor_config,
                                     text="Accelerometer Variance",
                                     color='green',
                                     grid=[2, 6],
                                     align="left")

sensor_config_textbox_custom_mag = TextBox(window_sensor_config,
                                           text='300',
                                           width=10,
                                           grid=[1, 7],
                                           align="left")

sensor_config_text_custom_mag = Text(window_sensor_config,
                                     text="Magnetometer Variance",
                                     color='green',
                                     grid=[2, 7],
                                     align="left")

sensor_config_textbox_custom_gyro = TextBox(window_sensor_config,
                                            text='0.05',
                                            width=10,
                                            grid=[1, 8],
                                            align="left")

sensor_config_text_custom_gyro = Text(window_sensor_config,
                                      text="Gyroscopic Variance",
                                      color='green',
                                      grid=[2, 8],
                                      align="left")

sensor_config_button_set_config = PushButton(window_sensor_config,
                                             text="Apply Sensor\nConfiguration",
                                             command=sensor_config_set,
                                             grid=[2, 14],
                                             align="right")

# Set custom app configurations
_app_custom_configurations()

# Start the App
logger.info('KootNet Sensors - PC Control Center - Started')
app.display()
