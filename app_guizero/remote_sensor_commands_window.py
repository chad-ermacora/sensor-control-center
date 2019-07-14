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
        self.window = guizero.Window(app,
                                     title="Sensor Commands",
                                     width=285,
                                     height=310,
                                     layout="grid",
                                     visible=False)

        self.app_menubar = guizero.MenuBar(self.window,
                                           toplevel=[["Advanced"]],
                                           options=[[["Enable Advanced Commands",
                                                      self.enable_advanced],
                                                     ["Disable Advanced Commands",
                                                      self.disable_advanced]]])

        self.text_select = guizero.Text(self.window,
                                        text="Select Sensor IPs in the main window",
                                        grid=[1, 1, 3, 1],
                                        color='#CB0000',
                                        align="left")

        self.text_upgrade = guizero.Text(self.window,
                                         text="Upgrade Commands",
                                         grid=[1, 2, 2, 1],
                                         color='blue',
                                         align="left")

        self.button_lan_Upgrade = guizero.PushButton(self.window,
                                                     text="Upgrade\nSoftware\nOver SMB",
                                                     command=self.send_commands,
                                                     args=[network_commands.upgrade_smb],
                                                     grid=[1, 3],
                                                     align="top")

        self.button_online_Upgrade = guizero.PushButton(self.window,
                                                        text="Upgrade\nSoftware\nOver HTTP",
                                                        command=self.send_commands,
                                                        args=[network_commands.upgrade_online],
                                                        grid=[2, 3],
                                                        align="top")

        self.button_os_Upgrade = guizero.PushButton(self.window,
                                                    text="Upgrade\nOperating\nSystem",
                                                    command=self.send_commands,
                                                    args=[network_commands.upgrade_system_os],
                                                    grid=[3, 3],
                                                    align="top")

        self.button_lan_Upgrade_dev = guizero.PushButton(self.window,
                                                         text="Dev SMB\nUpgrade",
                                                         command=self.send_commands,
                                                         args=[network_commands.upgrade_smb_dev],
                                                         grid=[1, 4],
                                                         align="top")

        self.button_online_Upgrade_dev = guizero.PushButton(self.window,
                                                            text="Dev HTTP\nUpgrade",
                                                            command=self.send_commands,
                                                            args=[network_commands.upgrade_online_dev],
                                                            grid=[2, 4],
                                                            align="top")

        self.text_power = guizero.Text(self.window,
                                       text="Power Commands",
                                       grid=[1, 24, 3, 1],
                                       color='blue',
                                       align="left")

        self.button_terminate = guizero.PushButton(self.window,
                                                   text="Restart\nServices",
                                                   command=self.send_commands,
                                                   args=[network_commands.restart_services],
                                                   grid=[1, 25],
                                                   align="top")

        self.button_reboot = guizero.PushButton(self.window,
                                                text="Reboot",
                                                command=self.send_commands,
                                                args=[network_commands.reboot_system],
                                                grid=[2, 25],
                                                align="top")

        self.button_shutdown = guizero.PushButton(self.window,
                                                  text="Shutdown",
                                                  command=self.send_commands,
                                                  args=[network_commands.shutdown_system],
                                                  grid=[3, 25],
                                                  align="top")

        self.text_other = guizero.Text(self.window,
                                       text="System Commands",
                                       grid=[1, 36, 3, 1],
                                       color='blue',
                                       align="left")

        self.button_get_config = guizero.PushButton(self.window,
                                                    text="Change\nNames",
                                                    command=self.hostname_change,
                                                    grid=[1, 37],
                                                    align="top")

        self.button_update_datetime = guizero.PushButton(self.window,
                                                         text="Sync Clock\nwith\nComputer",
                                                         command=self.datetime_update,
                                                         grid=[3, 37],
                                                         align="top")

        self.button_reinstall_python_requirements = guizero.PushButton(self.window,
                                                                       text="Check/Install\nDependencies",
                                                                       command=self.send_commands,
                                                                       args=[network_commands.reinstall_requirements],
                                                                       grid=[2, 37],
                                                                       align="top")

        self.text_display_commands = guizero.Text(self.window,
                                                  text="Clear Sensor Logs",
                                                  grid=[1, 48, 3, 1],
                                                  color='blue',
                                                  align="left")

        self.button_delete_primary_log = guizero.PushButton(self.window,
                                                            text="Primary Log",
                                                            command=self.send_commands,
                                                            args=[network_commands.delete_primary_log],
                                                            grid=[1, 49],
                                                            align="top")

        self.button_delete_network_log = guizero.PushButton(self.window,
                                                            text="Network Log",
                                                            command=self.send_commands,
                                                            args=[network_commands.delete_network_log],
                                                            grid=[2, 49],
                                                            align="top")

        self.button_delete_sensor_log = guizero.PushButton(self.window,
                                                           text="Sensors Log",
                                                           command=self.send_commands,
                                                           args=[network_commands.delete_sensors_log],
                                                           grid=[3, 49],
                                                           align="top")

        # Window Tweaks
        self.window.tk.resizable(False, False)
        self.disable_advanced()

    def enable_advanced(self):
        """ Enables advanced commands & changes software upgrades to 'Clean' upgrades. """
        self.button_os_Upgrade.enable()
        self.button_shutdown.enable()
        self.button_update_datetime.enable()
        self.button_reinstall_python_requirements.enable()
        self.button_delete_primary_log.enable()
        self.button_delete_network_log.enable()
        self.button_delete_sensor_log.enable()
        self.button_lan_Upgrade_dev.enable()
        self.button_online_Upgrade_dev.enable()
        self.button_lan_Upgrade.text = "Clean\nUpgrade\nOver SMB"
        self.button_online_Upgrade.text = "Clean\nUpgrade\nOver HTTP"
        self.button_online_Upgrade.update_command(self.send_commands, [network_commands.clean_upgrade_online])
        self.button_lan_Upgrade.update_command(self.send_commands, [network_commands.clean_upgrade_smb])

    def disable_advanced(self):
        """ Disables advanced commands & changes software upgrades to normal upgrades. """
        self.button_os_Upgrade.disable()
        self.button_shutdown.disable()
        self.button_update_datetime.disable()
        self.button_reinstall_python_requirements.disable()
        self.button_delete_primary_log.disable()
        self.button_delete_network_log.disable()
        self.button_delete_sensor_log.disable()
        self.button_lan_Upgrade_dev.disable()
        self.button_online_Upgrade_dev.disable()
        self.button_lan_Upgrade.text = "Upgrade\nSoftware\nOver SMB"
        self.button_online_Upgrade.text = "Upgrade\nSoftware\nOver HTTP"
        self.button_online_Upgrade.update_command(self.send_commands, [network_commands.upgrade_online])
        self.button_lan_Upgrade.update_command(self.send_commands, [network_commands.upgrade_smb])

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
