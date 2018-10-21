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
from guizero import Window, PushButton, Text, info, MenuBar
import app_sensor_commands
import app_logger


class CreateSensorCommandsWindow:
    def __init__(self, app, ip_selection):
        self.ip_selection = ip_selection
        self.window = Window(app,
                             title="Sensor Commands",
                             width=290,
                             height=285,
                             layout="grid",
                             visible=False)

        self.app_menubar = MenuBar(self.window,
                                   toplevel=[["Advanced"]],
                                   options=[[["Enable Advanced Commands",
                                              self.enable_advanced],
                                             ["Disable Advanced Commands",
                                              self.disable_advanced]]])

        self.text_select = Text(self.window,
                                text="Select Sensor IPs in the main window",
                                grid=[1, 1, 3, 1],
                                color='#CB0000',
                                align="left")

        self.text_upgrade = Text(self.window,
                                 text="Upgrade Commands",
                                 grid=[1, 2, 2, 1],
                                 color='blue',
                                 align="left")

        self.button_lan_Upgrade = PushButton(self.window,
                                             text="Upgrade\nSoftware\nOver SMB",
                                             command=self.upgrade_smb,
                                             grid=[1, 3],
                                             align="left")

        self.button_online_Upgrade = PushButton(self.window,
                                                text="Upgrade\nSoftware\nOver HTTP",
                                                command=self.upgrade_http,
                                                grid=[2, 3],
                                                align="left")

        self.button_os_Upgrade = PushButton(self.window,
                                            text="Upgrade\nOperating\nSystem",
                                            command=self.os_upgrade,
                                            grid=[3, 3],
                                            align="left")

        self.text_power = Text(self.window,
                               text="Power Commands",
                               grid=[1, 4, 3, 1],
                               color='blue',
                               align="left")

        self.button_reboot = PushButton(self.window,
                                        text="Reboot",
                                        command=self.sensor_reboot,
                                        grid=[1, 5],
                                        align="left")

        self.button_shutdown = PushButton(self.window,
                                          text="Shutdown",
                                          command=self.sensor_shutdown,
                                          grid=[2, 5],
                                          align="left")

        self.text_other = Text(self.window,
                               text="Other Commands",
                               grid=[1, 6, 3, 1],
                               color='blue',
                               align="left")

        self.button_terminate = PushButton(self.window,
                                           text="Restart\nServices",
                                           command=self.restart_services,
                                           grid=[1, 7],
                                           align="left")

        self.button_get_config = PushButton(self.window,
                                            text="Change\nNames",
                                            command=self.hostname_change,
                                            grid=[2, 7],
                                            align="left")

        self.button_update_datetime = PushButton(self.window,
                                                 text="Sync DateTime\nwith Computer",
                                                 command=self.datetime_update,
                                                 grid=[3, 7],
                                                 align="left")
        self.disable_advanced()

    def enable_advanced(self):
        self.button_os_Upgrade.enable()
        self.button_shutdown.enable()
        self.button_update_datetime.enable()

    def disable_advanced(self):
        self.button_os_Upgrade.disable()
        self.button_shutdown.disable()
        self.button_update_datetime.disable()

    def upgrade_smb(self):
        """ Sends the upgrade by SMB command to the Sensor Units IP. """
        app_logger.sensor_logger.debug("Sensor Upgrade - SMB")

        ip_list = self.ip_selection.get_verified_ip_list()
        for ip in ip_list:
            app_sensor_commands.upgrade_program_smb(ip)

        info("Sensors Upgrading SMB", "Please Wait up to 30 seconds for the Services to restart")

    def upgrade_http(self):
        """ Sends the upgrade by HTTP command to the Sensor Units IP. """
        app_logger.sensor_logger.debug("Sensor Upgrade - HTTP")

        ip_list = self.ip_selection.get_verified_ip_list()
        for ip in ip_list:
            app_sensor_commands.upgrade_program_online(ip)

        info("Sensors Upgrading HTTP", "Please Wait up to 30 seconds for the Services to restart")

    def os_upgrade(self):
        """ Sends the upgrade Operating System command to the Sensor Units IP. """
        app_logger.sensor_logger.debug("Sensor OS Upgrade")

        ip_list = self.ip_selection.get_verified_ip_list()
        for ip in ip_list:
            app_sensor_commands.upgrade_os_linux(ip)

        info("Sensors Operating System Upgrade Started",
             "Once complete, the Sensors will automatically reboot\n"
             "Sensor should continue to Operate with minor interruptions\n\n"
             "This process can take anywhere from 5 Min to 1 Hour")

    def sensor_reboot(self):
        """ Sends the reboot system command to the Sensor Units IP. """
        app_logger.sensor_logger.debug("Sensor Reboot")

        ip_list = self.ip_selection.get_verified_ip_list()
        for ip in ip_list:
            app_sensor_commands.reboot_sensor(ip)

        info("Sensors Rebooting", "Allow up to 3 Min to reboot")

    def sensor_shutdown(self):
        """ Sends the shutdown system command to the Sensor Units IP. """
        app_logger.sensor_logger.debug("Sensor Shutdown")

        ip_list = self.ip_selection.get_verified_ip_list()
        for ip in ip_list:
            app_sensor_commands.shutdown_sensor(ip)

        info("Sensors Shutting Down", "Allow up to 15 seconds to fully shutdown")

    def restart_services(self):
        """ Sends the restart services command to the Sensor Units IP. """
        app_logger.sensor_logger.info(
            "Sensor(s) Services Restarting - Please allow up to 20 Seconds to restart")

        ip_list = self.ip_selection.get_verified_ip_list()
        for ip in ip_list:
            app_sensor_commands.restart_services(ip)

        info("Sensors Services Restarting", "Please allow up to 20 Seconds to restart")

    def hostname_change(self):
        """ Sends the host name change command to the Sensor Units IP, along with the new host name. """
        app_logger.sensor_logger.debug("Change Sensor Hostname")

        ip_list = self.ip_selection.get_verified_ip_list()
        for ip in ip_list:
            app_sensor_commands.set_hostname(ip)

    def datetime_update(self):
        """ Sends the Date & Time update command to the Sensor Units IP, along with the computers Date & Time. """
        app_logger.sensor_logger.debug("Updating Sensors DateTime")

        ip_list = self.ip_selection.get_verified_ip_list()
        for ip in ip_list:
            app_sensor_commands.set_datetime(ip)

        info("Sensors DateTime Set", "Sensors Date & Time Synchronized with local Computer's")
