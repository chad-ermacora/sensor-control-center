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
from tkinter import filedialog

from guizero import Window, CheckBox, PushButton, Text, TextBox, warn, ButtonGroup

import app_modules.app_config as app_config
import app_modules.app_logger as app_logger


class CreateDataBaseInfoWindow:
    """ Creates a GUI window for generating database information. """

    def __init__(self, app, current_config):
        self.current_config = current_config
        self.database_line_width = 45

        self.window = Window(app,
                             title="DataBase Information",
                             width=650,
                             height=500,
                             layout="grid",
                             visible=True)

        self.button_select_database = PushButton(self.window,
                                                 text="Select Database",
                                                 command=self._select_database,
                                                 grid=[1, 1],
                                                 align="top")

        self.text_database_label = Text(self.window,
                                        text="Database: ",
                                        color='blue',
                                        grid=[1, 2],
                                        align="right")

        self.textbox_database_name = TextBox(self.window,
                                             text="Please Select a Database",
                                             width=self.database_line_width,
                                             grid=[2, 2],
                                             align="left")

        self.text_database_location_label = Text(self.window,
                                                 text="Location: ",
                                                 color='blue',
                                                 grid=[1, 3],
                                                 align="right")

        self.textbox_database_location = TextBox(self.window,
                                                 text="Please Select a Database",
                                                 width=self.database_line_width,
                                                 height=2,
                                                 grid=[2, 3],
                                                 multiline=True,
                                                 scrollbar=True,
                                                 align="left")

        # Window Tweaks
        self.textbox_database_name.disable()
        self.textbox_database_location.disable()

    def _select_database(self):
        """ Prompts for Database to open and opens it. """
        str_location = ""
        db_location = filedialog.askopenfilename()
        db_location_list = str(db_location).split("/")

        count = 0
        count2 = 1
        for text in db_location_list:
            if len(str_location) + len(text) > count2 * self.database_line_width:
                str_location += "\n"
                count2 += 1

            if count is not len(db_location_list) - 1:
                str_location += text + "/"
            count += 1

        self.textbox_database_name.value = db_location_list[-1]

        self.textbox_database_location.enable()
        self.textbox_database_location.value = str_location
        self.textbox_database_location.disable()
