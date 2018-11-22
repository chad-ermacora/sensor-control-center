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
from guizero import Window, Text, TextBox, PushButton, info, MenuBar
from app_sensor_commands import CreateNetworkSendCommands, send_command, CreateCommandData

# import app_logger


class CreateSQLNotesWindow:
    def __init__(self, app, ip_selection, current_config):
        self.current_config = current_config
        self.ip_selection = ip_selection
        self.network_send_commands = CreateNetworkSendCommands()

        self.window = Window(app,
                             title="SQL Notes",
                             width=615,
                             height=405,
                             layout="grid",
                             visible=True)

        self.app_menubar = MenuBar(self.window,
                                   toplevel=[["File"]],
                                   options=[[["Reset DateTime to Now", self.reset_datetime]]])

        self.note_text_warn1 = Text(self.window,
                                    text="Select Sensor IPs in the main window",
                                    color="red",
                                    grid=[1, 1],
                                    align="left")

        self.note_text2 = Text(self.window,
                               text="Enter at Date & Time",
                               color="blue",
                               grid=[3, 1, 2, 1],
                               align="right")

        self.note_datetime_textbox = TextBox(self.window,
                                             text=current_config.get_str_datetime_now(),
                                             grid=[3, 2, 2, 1],
                                             width=21,
                                             align="right")

        self.note_textbox = TextBox(self.window,
                                    text="Press the button in the bottom right to save the note\n" +
                                         "The note is stored in the selected Sensors SQL Database",
                                    grid=[1, 6, 4, 3],
                                    width=75,
                                    height=18,
                                    multiline=True,
                                    align="left")

        self.button_send_note = PushButton(self.window,
                                           text="Attach Note to \nSensor DataBase",
                                           command=self.send_note,
                                           grid=[4, 9],
                                           align="right")

    def send_note(self):
        ip_list = self.ip_selection.get_verified_ip_list()
        datetime = self.note_datetime_textbox.value + ".000"
        command = self.network_send_commands.put_sql_note + datetime + self.note_textbox.value

        for ip in ip_list:
            command_data = CreateCommandData(ip, self.current_config.network_timeout_data, command)
            send_command(command_data)
        info("Added @ " + datetime, "Note sent to " + str(ip_list))

    def reset_datetime(self):
        self.note_datetime_textbox.value = self.current_config.get_str_datetime_now()
