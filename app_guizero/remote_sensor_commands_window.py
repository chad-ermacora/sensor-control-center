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
import guizero
from threading import Thread
from tkinter import simpledialog
from app_modules import app_logger
from app_modules import app_variables
from app_modules import app_useful_functions
from app_modules import sensor_commands

network_commands = app_variables.CreateNetworkSendCommands()


class CreateSensorCommandsWindow:
    """ Creates a GUI window for sending sensor commands. """

    def __init__(self, app, ip_selection, current_config):
        self.ip_selection = ip_selection
        self.current_config = current_config

        self.text_upgrades_smb = "Regular SMB"
        self.text_upgrades_http = "Regular HTTP"
        self.text_upgrades_smb_dev = "Development SMB"
        self.text_upgrades_http_dev = "Development HTTP"
        self.text_upgrades_os = "Operating System"

        self.text_power_restart_services = "Restart Services"
        self.text_power_reboot = "Reboot"
        self.text_power_shutdown = "Shutdown"

        self.text_system_change_name = "Change Sensors Names"
        self.text_system_check_dependencies = "Check Dependencies"
        self.text_system_sync_clock = "Sync Date & Time"
        self.text_system_clear_log_primary = "Clear Primary Log"
        self.text_system_clear_log_network = "Clear Network Log"
        self.text_system_clear_log_sensors = "Clear Sensors Log"

        self.window = guizero.Window(app,
                                     title="Sensor Commands",
                                     width=295,
                                     height=440,
                                     layout="grid",
                                     visible=False)

        self.text_select = guizero.Text(self.window,
                                        text="Select Sensor IPs in the main window",
                                        grid=[1, 1],
                                        color='#CB0000',
                                        align="left")

        self.text_upgrade = guizero.Text(self.window,
                                         text="Upgrade Commands",
                                         grid=[1, 2],
                                         color='blue',
                                         align="left")

        self.upgrade_dropdown_selection = guizero.Combo(self.window,
                                                        options=[self.text_upgrades_http,
                                                                 self.text_upgrades_smb,
                                                                 self.text_upgrades_http_dev,
                                                                 self.text_upgrades_smb_dev,
                                                                 self.text_upgrades_os],
                                                        grid=[1, 3],
                                                        align="left")

        self.button_upgrade_proceed = guizero.PushButton(self.window,
                                                         text="Proceed",
                                                         command=self._proceed_upgrade,
                                                         grid=[1, 3],
                                                         align="right")

        self.text_power = guizero.Text(self.window,
                                       text="Power Commands",
                                       grid=[1, 24],
                                       color='blue',
                                       align="left")

        self.power_dropdown_selection = guizero.Combo(self.window,
                                                      options=[self.text_power_restart_services,
                                                               self.text_power_reboot,
                                                               self.text_power_shutdown],
                                                      grid=[1, 25],
                                                      align="left")

        self.button_power_proceed = guizero.PushButton(self.window,
                                                       text="Proceed",
                                                       command=self._proceed_power,
                                                       grid=[1, 25],
                                                       align="right")

        self.text_other = guizero.Text(self.window,
                                       text="System Commands",
                                       grid=[1, 36],
                                       color='blue',
                                       align="left")

        self.system_dropdown_selection = guizero.Combo(self.window,
                                                       options=[self.text_system_change_name,
                                                                self.text_system_check_dependencies,
                                                                self.text_system_sync_clock,
                                                                self.text_system_clear_log_primary,
                                                                self.text_system_clear_log_network,
                                                                self.text_system_clear_log_sensors],
                                                       grid=[1, 37],
                                                       align="left")

        self.button_system_proceed = guizero.PushButton(self.window,
                                                        text="Proceed",
                                                        command=self._proceed_system,
                                                        grid=[1, 37],
                                                        align="right")

        # Window Tweaks
        self.window.tk.resizable(False, False)

    def _proceed_upgrade(self):
        if self.upgrade_dropdown_selection.value == self.text_upgrades_http:
            self.send_commands(network_commands.upgrade_online)
        elif self.upgrade_dropdown_selection.value == self.text_upgrades_http_dev:
            self.send_commands(network_commands.upgrade_online_dev)
        elif self.upgrade_dropdown_selection.value == self.text_upgrades_smb:
            self.send_commands(network_commands.upgrade_smb)
        elif self.upgrade_dropdown_selection.value == self.text_upgrades_smb_dev:
            self.send_commands(network_commands.upgrade_smb_dev)
        elif self.upgrade_dropdown_selection.value == self.text_upgrades_os:
            self.send_commands(network_commands.upgrade_system_os)

    def _proceed_power(self):
        if self.power_dropdown_selection.value == self.text_power_restart_services:
            self.send_commands(network_commands.restart_services)
        elif self.power_dropdown_selection.value == self.text_power_reboot:
            self.send_commands(network_commands.reboot_system)
        elif self.power_dropdown_selection.value == self.text_power_shutdown:
            self.send_commands(network_commands.shutdown_system)

    def _proceed_system(self):
        if self.system_dropdown_selection.value == self.text_system_change_name:
            self.hostname_change()
        elif self.system_dropdown_selection.value == self.text_system_check_dependencies:
            self.send_commands(network_commands.reinstall_requirements)
        elif self.system_dropdown_selection.value == self.text_system_sync_clock:
            self.datetime_update()
        elif self.system_dropdown_selection.value == self.text_system_clear_log_primary:
            self.send_commands(network_commands.delete_primary_log)
        elif self.system_dropdown_selection.value == self.text_system_clear_log_network:
            self.send_commands(network_commands.delete_network_log)
        elif self.system_dropdown_selection.value == self.text_system_clear_log_sensors:
            self.send_commands(network_commands.delete_sensors_log)

    def send_commands(self, command):
        """ Sends provided command to the Sensor Units IP's. """
        threads = []

        ip_list = self.ip_selection.get_verified_ip_list()
        network_timeout = self.current_config.network_timeout_data

        for ip in ip_list:
            sensor_command = sensor_commands.CreateSensorNetworkCommand(ip, network_timeout, command)
            threads.append(Thread(target=sensor_commands.send_command, args=[sensor_command]))

        for thread in threads:
            thread.daemon = True
            thread.start()

        if len(ip_list) > 0:
            message = command + " sent to " + str(len(ip_list))
            if len(ip_list) is 1:
                message += " sensor"
            else:
                message += " sensors"

            guizero.info("Sensor Command Sent", message)
        else:
            app_useful_functions.no_ip_selected_message()

    def hostname_change(self):
        """ Sends the host name change command to the Sensor Units IP, along with the new host name. """
        app_logger.sensor_logger.debug("Change Sensor Hostname")
        threads = []

        network_timeout = self.current_config.network_timeout_data
        ip_list = self.ip_selection.get_verified_ip_list()
        if len(ip_list) > 0:
            for ip in ip_list:
                new_hostname = simpledialog.askstring(ip, "New Hostname: ")
                app_logger.sensor_logger.debug("Sent Hostname: " + str(new_hostname))
                validated_hostname = sensor_commands.get_validated_hostname(new_hostname)
                app_logger.sensor_logger.debug("Validated Hostname: " + validated_hostname)

                if validated_hostname is not "Cancelled":
                    command = network_commands.set_host_name
                    sensor_command = sensor_commands.CreateSensorNetworkCommand(ip, network_timeout, command)
                    sensor_command.command_data = validated_hostname
                    threads.append(Thread(target=sensor_commands.put_command, args=[sensor_command]))
                else:
                    guizero.info(ip, "Hostname Cancelled or blank for " + ip)

            for thread in threads:
                thread.start()
        else:
            app_useful_functions.no_ip_selected_message()

    def datetime_update(self):
        """ Sends the Date & Time update command to the Sensor Units IP, along with the computers Date & Time. """
        app_logger.sensor_logger.debug("Updating Sensors DateTime")
        threads = []

        network_timeout = self.current_config.network_timeout_data
        ip_list = self.ip_selection.get_verified_ip_list()
        if len(ip_list) > 0:
            command = network_commands.set_datetime
            for ip in ip_list:
                sensor_command = sensor_commands.CreateSensorNetworkCommand(ip, network_timeout, command)
                sensor_command.command_data = self.current_config.get_str_datetime_now()
                threads.append(Thread(target=sensor_commands.put_command, args=[sensor_command]))

            for thread in threads:
                thread.start()

            guizero.info("Sensors DateTime Set", "Sensors Date & Time synchronized with local computer's")
        else:
            app_useful_functions.no_ip_selected_message()
