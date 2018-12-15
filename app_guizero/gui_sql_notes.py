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
from guizero import Window, Text, TextBox, PushButton, info, CheckBox, warn

import app_logger
import app_sensor_commands
from app_graph import _adjust_datetime
from app_useful import sql_default_textbox_note


class CreateSQLNotesWindow:
    def __init__(self, app, ip_selection, current_config):
        self.current_config = current_config
        self.ip_selection = ip_selection
        self.network_send_commands = app_sensor_commands.CreateNetworkSendCommands()
        self.undo_note = ""

        self.window = Window(app,
                             title="Insert Note into Live Sensors SQL Database",
                             width=615,
                             height=385,
                             layout="grid",
                             visible=False)

        self.text_ip_select = Text(self.window,
                                   text="Select Sensor IPs in the main window",
                                   color="#CB0000",
                                   grid=[1, 1, 3, 1],
                                   align="left")

        self.checkbox_datetime = CheckBox(self.window,
                                          text="Use current Date & Time",
                                          command=self._reset_datetime,
                                          grid=[3, 1, 5, 1],
                                          align="left")

        self.textbox_datetime = TextBox(self.window,
                                        text=current_config.get_str_datetime_now(),
                                        grid=[4, 1, 5, 1],
                                        width=21,
                                        align="right")

        self.textbox_main_note = TextBox(self.window,
                                         text=sql_default_textbox_note.strip(),
                                         grid=[1, 6, 4, 3],
                                         width=75,
                                         height=18,
                                         multiline=True,
                                         align="left")

        self.button_clear_note = PushButton(self.window,
                                            text="Clear Note",
                                            command=self._clear_note,
                                            grid=[1, 9],
                                            align="left")

        self.button_undo_clear_note = PushButton(self.window,
                                                 text="Undo Clear",
                                                 command=self._undue_clear_note,
                                                 grid=[1, 9],
                                                 align="right")

        self.button_send_note = PushButton(self.window,
                                           text="Attach Note to\nSensors DataBase",
                                           command=self._send_note,
                                           grid=[4, 9],
                                           align="right")

        # Window Tweaks
        self.window.tk.resizable(False, False)
        self.checkbox_datetime.value = 1
        self._reset_datetime()
        self.button_undo_clear_note.disable()
        self.textbox_main_note.bg = "black"
        self.textbox_main_note.text_color = "white"
        self.textbox_main_note.tk.config(insertbackground="red")

    def _clear_note(self):
        self.undo_note = self.textbox_main_note.value
        self.textbox_main_note.clear()
        self.button_undo_clear_note.enable()

    def _undue_clear_note(self):
        self.textbox_main_note.value = self.undo_note
        self.button_undo_clear_note.disable()

    def _send_note(self):
        if self.checkbox_datetime.value:
            self._reset_datetime()
        ip_list = self.ip_selection.get_verified_ip_list()
        if len(ip_list) > 0:
            message_ip_addresses = ""
            datetime = self.textbox_datetime.value
            utc_0_datetime = _adjust_datetime(datetime, self.current_config.datetime_offset * -1)
            command = self.network_send_commands.put_sql_note
            command_data = utc_0_datetime + ".000" + self.textbox_main_note.value

            for ip in ip_list:
                message_ip_addresses += ip + ", "
                network_timeout = self.current_config.network_timeout_data
                sensor_command = app_sensor_commands.CreateSensorNetworkCommand(ip, network_timeout, command)
                sensor_command.command_data = command_data
                app_sensor_commands.put_command(sensor_command)

            message_ip_addresses = message_ip_addresses[:-2]

            if message_ip_addresses == "":
                message_ip_addresses = "None"

            info("Note Inserted into Sensors Database", "Inserted with DateTime: " + datetime +
                 "\n\nNote sent to the following sensor IP Addresses\n\n" + message_ip_addresses)
            app_logger.sensor_logger.info("Inserted note into " + str(len(ip_list)) + " sensors with DateTime " + datetime)
        else:
            warn("No Sensor IP", "Please select at least one online sensor IP from the main window")

    def _reset_datetime(self):
        self.textbox_datetime.value = self.current_config.get_str_datetime_now()
        if self.checkbox_datetime.value:
            self.textbox_datetime.disable()
        else:
            self.textbox_datetime.enable()
