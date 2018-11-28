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
from guizero import Window, Text, TextBox, PushButton, info, CheckBox

import app_logger
import app_sensor_commands
from app_graph import _adjust_datetime


class CreateSQLNotesWindow:
    def __init__(self, app, ip_selection, current_config):
        self.current_config = current_config
        self.ip_selection = ip_selection
        self.network_send_commands = app_sensor_commands.CreateNetworkSendCommands()
        self.undo_note = ""

        self.window = Window(app,
                             title="Insert Note into Live Sensors SQL Database",
                             width=615,
                             height=405,
                             layout="grid",
                             visible=False)

        self.note_text_warn1 = Text(self.window,
                                    text="Select Sensor IPs in the main window",
                                    color="red",
                                    grid=[1, 1, 3, 1],
                                    align="left")

        self.note_text2 = Text(self.window,
                               text="Enter at Date & Time",
                               color="blue",
                               grid=[3, 1, 2, 1],
                               align="top")

        self.note_datetime_checkbox = CheckBox(self.window,
                                               text="Use current Date & Time",
                                               command=self.reset_datetime,
                                               grid=[3, 2],
                                               align="right")

        self.note_datetime_textbox = TextBox(self.window,
                                             text=current_config.get_str_datetime_now(),
                                             grid=[4, 2],
                                             width=21,
                                             align="left")

        self.note_textbox = TextBox(self.window,
                                    text="Press the button in the bottom left to clear the note window\n" +
                                         "Press the button in the bottom right to save the note\n\n" +
                                         "The Date & Time you enter in the top right is 'When' the note is entered\n" +
                                         "This is meant to align your notes to the relevant sensor data\n\n" +
                                         "Example Note:\nThe sudden drop of temperature to 0 is actually a sensor\n" +
                                         "malfunction starting from the date & time of this entry and continues\n" +
                                         "for 34.3 hours. Please disregard\n - Chad Ermacora\n",
                                    grid=[1, 6, 4, 3],
                                    width=75,
                                    height=18,
                                    multiline=True,
                                    align="left")

        self.button_clear_note = PushButton(self.window,
                                            text="Clear Note",
                                            command=self.clear_note,
                                            grid=[1, 9],
                                            align="left")

        self.button_undo_clear_note = PushButton(self.window,
                                                 text="Undo Clear Note",
                                                 command=self.undue_clear_note,
                                                 grid=[2, 9],
                                                 align="left")

        self.button_send_note = PushButton(self.window,
                                           text="Attach Note to\nSensor DataBase",
                                           command=self.send_note,
                                           grid=[4, 9],
                                           align="right")

    def clear_note(self):
        self.undo_note = self.note_textbox.value
        self.note_textbox.clear()
        self.button_undo_clear_note.enable()

    def undue_clear_note(self):
        self.note_textbox.value = self.undo_note
        self.button_undo_clear_note.disable()

    def send_note(self):
        if self.note_datetime_checkbox.value:
            self.reset_datetime()
        ip_list = self.ip_selection.get_verified_ip_list()
        message_ip_addresses = ""
        datetime = self.note_datetime_textbox.value
        utc_0_datetime = _adjust_datetime(datetime, self.current_config.datetime_offset * -1)
        command = self.network_send_commands.put_sql_note
        command_data = utc_0_datetime + ".000" + self.note_textbox.value

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

    def reset_datetime(self):
        self.note_datetime_textbox.value = self.current_config.get_str_datetime_now()
        if self.note_datetime_checkbox.value:
            self.note_datetime_textbox.disable()
        else:
            self.note_datetime_textbox.enable()
