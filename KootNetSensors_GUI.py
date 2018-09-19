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
import sys
import platform
import subprocess
import logging
# DEBUG - Detailed information, typically of interest only when diagnosing problems. test
# INFO - Confirmation that things are working as expected.
# WARNING - An indication that something unexpected happened, or indicative of some problem in the near future
#              (e.g. ‘disk space low’). The software is still working as expected.
# ERROR - Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL - A serious error, indicating that the program itself may be unable to continue running.
import Sensor_config
import Sensor_commands
import Sensor_app_imports
import Sensor_graphs
import Sensor_graph_interval
from logging.handlers import RotatingFileHandler
from guizero import App, Window, CheckBox, PushButton, Text, TextBox, MenuBar
from tkinter import filedialog

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:  %(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = RotatingFileHandler('logs/KootNet_GUI_log.txt', maxBytes=256000, backupCount=5)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

app_version = "Tested on Python 3.7 - KootNet Sensors Version Alpha.16.1"
app_location_directory = str(os.path.dirname(sys.argv[0])) + "/"
config_file = app_location_directory + "/config.txt"


def app_graph_open_menu():
    window_graph_interval.show()


def app_sensor_commands_menu():
    window_sensor_commands.show()


def app_log_open_menu():
    logger.debug("Open Logs Folder")
    log_path = app_location_directory + "logs/"
    if platform.system() == "Windows":
        os.startfile(log_path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", log_path])
    else:
        subprocess.Popen(["xdg-open", log_path])


def app_check_all_ip_checkboxes(var_column):
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


# Returns selected IP's from Main App Window & Re-Sets unselected IP background to white
def get_checked_ip():
    ip_list = []

    if app_checkbox_ip1.value == 1:
        ip_list.append(app_textbox_ip1.value)
    else:
        app_textbox_ip1.bg = 'white'

    if app_checkbox_ip2.value == 1:
        ip_list.append(app_textbox_ip2.value)
    else:
        app_textbox_ip2.bg = 'white'

    if app_checkbox_ip3.value == 1:
        ip_list.append(app_textbox_ip3.value)
    else:
        app_textbox_ip3.bg = 'white'

    if app_checkbox_ip4.value == 1:
        ip_list.append(app_textbox_ip4.value)
    else:
        app_textbox_ip4.bg = 'white'

    if app_checkbox_ip5.value == 1:
        ip_list.append(app_textbox_ip5.value)
    else:
        app_textbox_ip5.bg = 'white'

    if app_checkbox_ip6.value == 1:
        ip_list.append(app_textbox_ip6.value)
    else:
        app_textbox_ip6.bg = 'white'

    if app_checkbox_ip7.value == 1:
        ip_list.append(app_textbox_ip7.value)
    else:
        app_textbox_ip7.bg = 'white'

    if app_checkbox_ip8.value == 1:
        ip_list.append(app_textbox_ip8.value)
    else:
        app_textbox_ip8.bg = 'white'

    if app_checkbox_ip9.value == 1:
        ip_list.append(app_textbox_ip9.value)
    else:
        app_textbox_ip9.bg = 'white'

    if app_checkbox_ip10.value == 1:
        ip_list.append(app_textbox_ip10.value)
    else:
        app_textbox_ip10.bg = 'white'

    if app_checkbox_ip11.value == 1:
        ip_list.append(app_textbox_ip11.value)
    else:
        app_textbox_ip11.bg = 'white'

    if app_checkbox_ip12.value == 1:
        ip_list.append(app_textbox_ip12.value)
    else:
        app_textbox_ip12.bg = 'white'

    if app_checkbox_ip13.value == 1:
        ip_list.append(app_textbox_ip13.value)
    else:
        app_textbox_ip13.bg = 'white'

    if app_checkbox_ip14.value == 1:
        ip_list.append(app_textbox_ip14.value)
    else:
        app_textbox_ip14.bg = 'white'

    if app_checkbox_ip15.value == 1:
        ip_list.append(app_textbox_ip15.value)
    else:
        app_textbox_ip15.bg = 'white'

    if app_checkbox_ip16.value == 1:
        ip_list.append(app_textbox_ip16.value)
    else:
        app_textbox_ip16.bg = 'white'

    logger.debug("IP List Generated from Checked Boxes")
    return ip_list


def app_check_sensors_button():
    ip_list = get_checked_ip()
    ip_list_final = []
    net_timeout = int(config_textbox_network_check.value)

    for ip in ip_list:
        sensor_status = Sensor_commands.check(ip, net_timeout)

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

    logger.debug("Checked IP's Processed")
    return ip_list_final


def app_download_interval_db_menu():
    ip_list = app_check_sensors_button()
    Sensor_app_imports.download_interval_db(ip_list)


def app_download_trigger_db_menu():
    ip_list = app_check_sensors_button()
    Sensor_app_imports.download_trigger_db(ip_list)


def app_sensor_details():
    var_ip_list = app_check_sensors_button()
    Sensor_app_imports.sensor_detailed_status(var_ip_list)


def app_open_about():
    window_app_about.show()


def app_open_help():
    help_file_location = app_location_directory + "additional_files/BuildSensors.html"
    Sensor_app_imports.open_html(help_file_location)


def app_open_config():
    window_config.show()


def config_save_apply_button():
    logger.info("Applying Configuration & Saving to File")

    config_settings = Sensor_config.CreateConfigSettings()

    config_settings.save_to = config_textbox_save_to.value
    config_settings.graph_start = config_textbox_start.value
    config_settings.graph_end = config_textbox_end.value
    config_settings.time_offset = config_textbox_time_offset.value
    config_settings.sql_queries_skip = config_textbox_sql_skip.value
    config_settings.temperature_offset = config_textbox_temperature_offset.value
    config_settings.network_check_timeout = config_textbox_network_check.value
    config_settings.network_details_timeout = config_textbox_network_details.value
    config_settings.allow_power_controls = config_checkbox_power_controls.value
    config_settings.allow_reset_config = config_checkbox_reset.value

    Sensor_config.save_file(config_settings)
    set_config(config_settings)


def set_config(config_settings):
    final_config_settings = Sensor_config.check_settings(config_settings)

    try:
        config_textbox_save_to.value = final_config_settings.save_to
        config_textbox_start.value = final_config_settings.graph_start
        graph_textbox_start.value = final_config_settings.graph_start
        config_textbox_end.value = final_config_settings.graph_end
        graph_textbox_end.value = final_config_settings.graph_end
        config_textbox_time_offset.value = final_config_settings.time_offset
        config_textbox_sql_skip.value = final_config_settings.sql_queries_skip
        graph_textbox_sql_skip.value = final_config_settings.sql_queries_skip
        config_textbox_temperature_offset.value = final_config_settings.temperature_offset
        graph_textbox_temperature_offset.value = final_config_settings.temperature_offset
        config_textbox_network_check.value = final_config_settings.network_check_timeout
        config_textbox_network_details.value = final_config_settings.network_details_timeout
        config_checkbox_power_controls.value = final_config_settings.allow_power_controls
        config_checkbox_reset.value = final_config_settings.allow_reset_config
        config_enable_reset()
        config_enable_shutdown()
        logger.info("Configuration Set - OK")
    except Exception as error:
        logger.error("Configuration Set - One or More Items Failed - " + str(error))


def config_save_dir():
    save_to = filedialog.askdirectory()

    if len(save_to) > 1:
        config_textbox_save_to.value = save_to + "/"
        logger.debug("Changed Save to Directory")
    else:
        logger.warning("Invalid Directory Chosen for Save to Directory")


def config_reset_defaults():
    logger.info("Resetting Configuration to Defaults")
    default_settings = Sensor_config.CreateConfigSettings()
    set_config(default_settings)


def config_enable_reset():
    if config_checkbox_reset.value == 1:
        config_button_reset.enable()
    else:
        config_button_reset.disable()


def config_enable_shutdown():
    if config_checkbox_power_controls.value == 1:
        commands_button_reboot.enable()
        commands_button_shutdown.enable()
    else:
        commands_button_reboot.disable()
        commands_button_shutdown.disable()


def commands_upgrade_nas():
    logger.debug("Sensor Upgrade - NAS")
    ip_list = app_check_sensors_button()

    for ip in ip_list:
        logger.info(Sensor_commands.nas_upgrade(ip))


def commands_upgrade_online():
    logger.debug("Sensor Upgrade - Online")
    ip_list = app_check_sensors_button()

    for ip in ip_list:
        logger.info(Sensor_commands.online_upgrade(ip))


def commands_sensor_reboot():
    logger.debug("Sensor Reboot")
    ip_list = app_check_sensors_button()

    for ip in ip_list:
        logger.info(Sensor_commands.reboot(ip))


def commands_sensor_shutdown():
    logger.debug("Sensor Reboot")
    ip_list = app_check_sensors_button()

    for ip in ip_list:
        logger.info(Sensor_commands.shutdown(ip))


def commands_kill_progs():
    logger.debug("Terminate Sensor Programs")
    ip_list = app_check_sensors_button()

    for ip in ip_list:
        logger.info(Sensor_commands.kill_progs(ip))


def commands_hostname_change():
    logger.debug("Change Sensor Hostname")
    ip_list = app_check_sensors_button()

    for ip in ip_list:
        logger.info(Sensor_commands.hostname_change(ip))


def graph_interval_button():
    new_interval_graph = Sensor_graph_interval.CreateGraphIntervalData()
    new_interval_graph.db_location = filedialog.askopenfilename()

    new_interval_graph.save_file_to = config_textbox_save_to.value
    new_interval_graph.skip_sql = graph_textbox_sql_skip.value

    try:
        new_temp_value = float(graph_textbox_temperature_offset.value)
    except Exception as error:
        logger.error("Bad Temperature setting - Using 0: " + str(error))
        new_temp_value = 0.0

    new_interval_graph.temperature_offset = new_temp_value

    new_interval_graph.time_offset = config_textbox_time_offset.value
    new_interval_graph.graph_start = graph_textbox_start.value
    new_interval_graph.graph_end = graph_textbox_end.value
    # new_interval_graph.graph_type = ""
    new_interval_graph.graph_columns = get_column_checkboxes()
    # new_interval_graph.get_sql_entries = ReplaceMe
    Sensor_graph_interval.start_graph(new_interval_graph)


def get_column_checkboxes():
    column_checkboxes = ["Time", "hostName", "ip"]

    if graph_checkbox_up_time.value == 1:
        column_checkboxes.append("uptime")
    if graph_checkbox_temperature.value == 1:
        column_checkboxes.append("cpuTemp")
        column_checkboxes.append("hatTemp")
    if graph_checkbox_pressure.value == 1:
        column_checkboxes.append("pressure")
    if graph_checkbox_humidity.value == 1:
        column_checkboxes.append("humidity")
    if graph_checkbox_lumen.value == 1:
        column_checkboxes.append("lumens")
    if graph_checkbox_colour.value == 1:
        column_checkboxes.append("red")
        column_checkboxes.append("green")
        column_checkboxes.append("blue")
    if graph_checkbox_magnetic.value == 1:
        column_checkboxes.append("mg_X")
        column_checkboxes.append("mg_Y")
        column_checkboxes.append("mg_Z")

    logger.debug(str(column_checkboxes))
    return column_checkboxes


def graph_trigger_button():
    # Need to re-work before pushing to master branch
    mess = Sensor_graphs.motion_graph(graph_textbox_start.value,
                                      graph_textbox_end.value,
                                      config_textbox_save_to.value,
                                      int(config_textbox_time_offset.value),
                                      "scatterT3")


# App & Window Configurations
app = App(title="KootNet Sensors - PC Control Center",
          width=400,
          height=300,
          layout="grid")

window_graph_interval = Window(app,
                               title="Interval Graphing",
                               width=275,
                               height=300,
                               layout="grid",
                               visible=False)

window_graph_trigger = Window(app,
                              title="Trigger Graphing",
                              width=250,
                              height=180,
                              layout="grid",
                              visible=False)

window_sensor_commands = Window(app,
                                title="Sensor Commands",
                                width=275,
                                height=225,
                                layout="grid",
                                visible=False)

window_app_about = Window(app,
                          title="About KootNet Sensors",
                          width=610,
                          height=325,
                          layout="grid",
                          visible=False)

window_config = Window(app,
                       title="Configuration",
                       width=500,
                       height=275,
                       layout="grid",
                       visible=False)

app_menubar = MenuBar(app,
                      toplevel=[["File"],
                                ["Download"],
                                ["Graphing"],
                                ["Help"]],
                      options=[[["Open Logs",
                                 app_log_open_menu],
                                ["Configuration Settings",
                                 app_open_config],
                               ["Sensor Commands",
                                app_sensor_commands_menu]],
                               [["Download Interval Database(s)",
                                 app_download_interval_db_menu],
                                ["Download Trigger Database(s)",
                                 app_download_trigger_db_menu]],
                               [["Graph Interval Database",
                                 app_graph_open_menu]],
                               [["Making a Sensor Unit - WIP",
                                 app_open_help],
                                ["About KootNet Sensors",
                                 app_open_about]]])

app_button_sensor_check = PushButton(app,
                                     text="Check Sensor\nStatus",
                                     command=app_check_sensors_button,
                                     grid=[1, 15, 2, 1],
                                     align="left")

app_button_sensor_details = PushButton(app,
                                       text="View Sensor\nDetails",
                                       command=app_sensor_details,
                                       grid=[2, 15, 2, 1],
                                       align="right")

app_button_sensor_hostname = PushButton(app,
                                        text="Update Sensor(s)\nName",
                                        command=commands_hostname_change,
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
                            text="N/A",
                            grid=[1, 2],
                            align="left")

app_textbox_ip1 = TextBox(app,
                          text="192.168.10.11",
                          width=21,
                          grid=[2, 2],
                          align="left")

app_checkbox_ip2 = CheckBox(app,
                            text="N/A",
                            grid=[1, 3],
                            align="left")

app_textbox_ip2 = TextBox(app,
                          text="192.168.10.12",
                          width=21,
                          grid=[2, 3],
                          align="left")

app_checkbox_ip3 = CheckBox(app,
                            text="N/A",
                            grid=[1, 4],
                            align="left")

app_textbox_ip3 = TextBox(app,
                          text="192.168.10.13",
                          width=21,
                          grid=[2, 4],
                          align="left")

app_checkbox_ip4 = CheckBox(app,
                            text="N/A",
                            grid=[1, 5],
                            align="left")

app_textbox_ip4 = TextBox(app,
                          text="192.168.10.14",
                          width=21,
                          grid=[2, 5],
                          align="left")

app_checkbox_ip5 = CheckBox(app,
                            text="N/A",
                            grid=[1, 6],
                            align="left")

app_textbox_ip5 = TextBox(app,
                          text="192.168.10.15",
                          width=21,
                          grid=[2, 6],
                          align="left")

app_checkbox_ip6 = CheckBox(app,
                            text="N/A",
                            grid=[1, 7],
                            align="left")

app_textbox_ip6 = TextBox(app,
                          text="192.168.10.16",
                          width=21,
                          grid=[2, 7],
                          align="left")

app_checkbox_ip7 = CheckBox(app,
                            text="N/A",
                            grid=[1, 8],
                            align="left")

app_textbox_ip7 = TextBox(app,
                          text="192.168.10.17",
                          width=21,
                          grid=[2, 8],
                          align="left")

app_checkbox_ip8 = CheckBox(app,
                            text="N/A",
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
                            text="N/A",
                            grid=[3, 2],
                            align="left")

app_textbox_ip9 = TextBox(app,
                          text="192.168.10.19",
                          width=21,
                          grid=[4, 2],
                          align="left")

app_checkbox_ip10 = CheckBox(app,
                             text="N/A",
                             grid=[3, 3],
                             align="left")

app_textbox_ip10 = TextBox(app,
                           text="192.168.10.20",
                           width=21,
                           grid=[4, 3],
                           align="left")

app_checkbox_ip11 = CheckBox(app,
                             text="N/A",
                             grid=[3, 4],
                             align="left")

app_textbox_ip11 = TextBox(app,
                           text="192.168.10.21",
                           width=21,
                           grid=[4, 4],
                           align="left")

app_checkbox_ip12 = CheckBox(app,
                             text="N/A",
                             grid=[3, 5],
                             align="left")

app_textbox_ip12 = TextBox(app,
                           text="192.168.10.22",
                           width=21,
                           grid=[4, 5],
                           align="left")

app_checkbox_ip13 = CheckBox(app,
                             text="N/A",
                             grid=[3, 6],
                             align="left")

app_textbox_ip13 = TextBox(app,
                           text="192.168.10.23",
                           width=21,
                           grid=[4, 6],
                           align="left")

app_checkbox_ip14 = CheckBox(app,
                             text="N/A",
                             grid=[3, 7],
                             align="left")

app_textbox_ip14 = TextBox(app,
                           text="192.168.10.24",
                           width=21,
                           grid=[4, 7],
                           align="left")

app_checkbox_ip15 = CheckBox(app,
                             text="N/A",
                             grid=[3, 8],
                             align="left")

app_textbox_ip15 = TextBox(app,
                           text="192.168.10.25",
                           width=21,
                           grid=[4, 8],
                           align="left")

app_checkbox_ip16 = CheckBox(app,
                             text="N/A",
                             grid=[3, 9],
                             align="left")

app_textbox_ip16 = TextBox(app,
                           text="192.168.10.26",
                           width=21,
                           grid=[4, 9],
                           align="left")

# About Window Section
about_text1 = Text(window_app_about,
                   text=app_version,
                   grid=[1, 1],
                   align="right")

about_textbox = TextBox(window_app_about,
                        text="Should of been Replaced with About Text",
                        grid=[1, 2],
                        width=75,
                        height=18,
                        multiline=True,
                        align="left")


# Configuration Window Section
config_button_reset = PushButton(window_config,
                                 text="Reset to\nDefaults",
                                 command=config_reset_defaults,
                                 grid=[1, 1],
                                 align="right")

config_checkbox_power_controls = \
    CheckBox(window_config,
             text="Enable Sensor\nShutdown/Reboot",
             command=config_enable_shutdown,
             grid=[1, 1],
             align="top")

config_checkbox_reset = CheckBox(window_config,
                                 text="Enable Config Reset",
                                 command=config_enable_reset,
                                 grid=[1, 1],
                                 align="bottom")

config_button_save_apply = PushButton(window_config,
                                      text="Save &\nApply",
                                      command=config_save_apply_button,
                                      grid=[1, 1],
                                      align="left")

config_text_database_time = Text(window_config,
                                 text="Database(s) in UTC 0",
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
                                    command=config_save_dir,
                                    grid=[1, 4],
                                    align="bottom")

config_textbox_save_to = TextBox(window_config,
                                 text='',
                                 width=50,
                                 grid=[1, 5, 1, 1],
                                 align="left")

config_text_spacer2 = Text(window_config,
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
                                text="Database Hour(s) Offset",
                                color='blue',
                                grid=[2, 1],
                                align="bottom")

config_textbox_time_offset = TextBox(window_config,
                                     text="",
                                     width="5",
                                     grid=[2, 2],
                                     align="bottom")

config_text_sql_skip = Text(window_config,
                            text="Skip SQL Queries",
                            color='blue',
                            grid=[2, 3],
                            align="top")

config_textbox_sql_skip = TextBox(window_config,
                                  text="",
                                  width="5",
                                  grid=[2, 4],
                                  align="top")

config_text_temperature_offset = Text(window_config,
                                      text="Temperature Offset",
                                      color='blue',
                                      grid=[2, 4],
                                      align="bottom")

config_textbox_temperature_offset = TextBox(window_config,
                                            text="",
                                            width="5",
                                            grid=[2, 5],
                                            align="top")

config_text_network_timeouts = Text(window_config,
                                    text="Network Timeouts",
                                    color='blue',
                                    grid=[2, 6],
                                    align="top")

config_text_network_timeouts1 = Text(window_config,
                                     text="   Sensor Check: ",
                                     color='green',
                                     grid=[2, 7],
                                     align="left")

config_textbox_network_check = TextBox(window_config,
                                       text="",
                                       width="5",
                                       grid=[2, 7],
                                       align="right")

config_text_network_timeouts2 = Text(window_config,
                                     text="   Sensor Details: ",
                                     color='green',
                                     grid=[2, 8],
                                     align="left")

config_textbox_network_details = TextBox(window_config,
                                         text="",
                                         width="5",
                                         grid=[2, 8],
                                         align="right")

# Graph Window Section
graph_text_start = Text(window_graph_interval,
                        text="Start DateTime: ",
                        color='green',
                        grid=[1, 2],
                        align="left")

graph_textbox_start = TextBox(window_graph_interval,
                              text="",
                              width=20,
                              grid=[2, 2],
                              align="left")

graph_text_end = Text(window_graph_interval,
                      text="End DateTime: ",
                      color='green',
                      grid=[1, 3],
                      align="left")

graph_textbox_end = TextBox(window_graph_interval,
                            text="",
                            width=20,
                            grid=[2, 3],
                            align="left")

graph_text_sql_skip = Text(window_graph_interval,
                           text="SQL Skip: ",
                           color='green',
                           grid=[1, 4],
                           align="left")

graph_textbox_sql_skip = TextBox(window_graph_interval,
                                 text="",
                                 width=10,
                                 grid=[2, 4],
                                 align="left")

graph_text_temperature_offset = Text(window_graph_interval,
                                     text="Temp Offset: ",
                                     color='green',
                                     grid=[1, 5],
                                     align="left")

graph_textbox_temperature_offset = TextBox(window_graph_interval,
                                           text="",
                                           width=10,
                                           grid=[2, 5],
                                           align="left")

graph_text_column_selection = Text(window_graph_interval,
                                   text="Sensors to Include",
                                   color='blue',
                                   grid=[1, 6, 2, 1],
                                   align="top")

graph_checkbox_up_time = CheckBox(window_graph_interval,
                                  text="System Uptime",
                                  grid=[1, 7],
                                  align="left")

graph_checkbox_temperature = CheckBox(window_graph_interval,
                                      text="Temperature",
                                      grid=[1, 8],
                                      align="left")

graph_checkbox_pressure = CheckBox(window_graph_interval,
                                   text="Pressure",
                                   grid=[1, 9],
                                   align="left")

graph_checkbox_humidity = CheckBox(window_graph_interval,
                                   text="Humidity",
                                   grid=[1, 10],
                                   align="left")

graph_checkbox_lumen = CheckBox(window_graph_interval,
                                text="Lumen",
                                grid=[2, 7],
                                align="left")

graph_checkbox_colour = CheckBox(window_graph_interval,
                                 text="Colour RGB",
                                 grid=[2, 8],
                                 align="left")

graph_checkbox_magnetic = CheckBox(window_graph_interval,
                                   text="Magnetic XYZ",
                                   grid=[2, 9],
                                   align="left")

graph_button_sensors = PushButton(window_graph_interval,
                                  text="Graph\nSensors",
                                  command=graph_interval_button,
                                  grid=[1, 12, 2, 1],
                                  align="bottom")

# graph_button_motion = PushButton(window_graph_interval,
#                                  text="Graph\nMotion",
#                                  command=graph_trigger_button,
#                                  grid=[3, 8],
#                                  align="right")

# Sensor Commands Window Section
commands_text_select = Text(window_sensor_commands,
                            text="Select Sensors from the Main Window",
                            grid=[1, 1, 3, 1],
                            color='#CB0000',
                            align="left")

commands_text_upgrade = Text(window_sensor_commands,
                             text="Upgrade Selected Sensor",
                             grid=[1, 2, 2, 1],
                             color='blue',
                             align="left")

commands_button_lanUpgrade = PushButton(window_sensor_commands,
                                        text="LAN SMB\nUpgrade",
                                        command=commands_upgrade_nas,
                                        grid=[1, 3],
                                        align="left")

commands_button_onlineUpgrade = PushButton(window_sensor_commands,
                                           text="Online HTTP\nUpgrade",
                                           command=commands_upgrade_online,
                                           grid=[2, 3],
                                           align="left")

commands_text_other = Text(window_sensor_commands,
                           text="Power Commands",
                           grid=[1, 4, 2, 1],
                           color='blue',
                           align="left")

commands_button_terminate = PushButton(window_sensor_commands,
                                       text="Restart\nSensor Unit\nPrograms",
                                       command=commands_kill_progs,
                                       grid=[1, 5],
                                       align="left")

commands_button_reboot = PushButton(window_sensor_commands,
                                    text="Reboot",
                                    command=commands_sensor_reboot,
                                    grid=[2, 5, 2, 1],
                                    align="right")

commands_button_shutdown = PushButton(window_sensor_commands,
                                      text="Shutdown",
                                      command=commands_sensor_shutdown,
                                      grid=[2, 5],
                                      align="left")

# Change Window Configurations before loading app
app_checkbox_all_column1.toggle()
app_check_all_ip_checkboxes(1)
graph_checkbox_up_time.value = 0
graph_checkbox_temperature.value = 1
graph_checkbox_pressure.value = 1
graph_checkbox_humidity.value = 0
graph_checkbox_lumen.value = 0
graph_checkbox_colour.value = 1
graph_checkbox_magnetic.value = 1

about_textbox.value = Sensor_app_imports.get_about_text()
about_textbox.disable()
config_textbox_save_to.disable()

loaded_config_settings = Sensor_config.load_file()
set_config(loaded_config_settings)

# Start the App
app.display()
