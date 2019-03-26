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
import sqlite3
import os.path
import app_modules.app_logger as app_logger
from tkinter import filedialog
from guizero import Window, PushButton, Text, TextBox
from app_modules.app_graph_plotly import CreateSQLColumnNames
from app_modules.app_graph import adjust_datetime

sql_column_names = CreateSQLColumnNames()


class CreateDataBaseNotesWindow:
    """ Creates a GUI window for generating database information. """

    def __init__(self, app, current_config):
        self.current_config = current_config

        self.window = Window(app,
                             title="DataBase Notes Editor",
                             width=585,
                             height=500,
                             layout="grid",
                             visible=True)

        # self.text_top_spacer1 = Text(self.window,
        #                              text="",
        #                              grid=[1, 1],
        #                              align="left")

        self.button_open_database = PushButton(self.window,
                                               text="Open\nDatabase",
                                               command=self._open_database,
                                               grid=[1, 5],
                                               align="left")

        self.button_back_note = PushButton(self.window,
                                           text="Back",
                                           command=self._open_database,
                                           grid=[2, 5],
                                           align="left")

        self.text_note_date = Text(self.window,
                                   text="Current",
                                   color="blue",
                                   grid=[3, 5],
                                   align="top")

        self.textbox_number_of_notes = TextBox(self.window,
                                               text="0",
                                               width=5,
                                               grid=[3, 5],
                                               align="bottom")

        self.text_label1 = Text(self.window,
                                text="Current Note's\nDate",
                                color="blue",
                                grid=[4, 5],
                                align="top")

        self.text_note_date = Text(self.window,
                                   text="YYYY-MM-DD hh:mm",
                                   grid=[4, 5],
                                   align="bottom")

        self.text_note_date = Text(self.window,
                                   text="Total",
                                   color="blue",
                                   grid=[5, 5],
                                   align="top")

        self.textbox_number_of_notes_total = TextBox(self.window,
                                                     text="0",
                                                     width=5,
                                                     grid=[5, 5],
                                                     align="bottom")

        self.button_next_note = PushButton(self.window,
                                           text="Next",
                                           command=self._open_database,
                                           grid=[6, 5],
                                           align="left")

        self.textbox_current_note = TextBox(self.window,
                                            text="Please Open a Database to view Notes",
                                            width=70,
                                            height=25,
                                            grid=[1, 10, 6, 1],
                                            multiline=True,
                                            scrollbar=True,
                                            align="left")

        # Window Tweaks
        self.button_back_note.disable()
        self.textbox_number_of_notes.disable()
        self.textbox_number_of_notes_total.disable()
        self.button_next_note.disable()
        self.textbox_current_note.disable()
        self.textbox_current_note.bg = "black"
        self.textbox_current_note.text_color = "white"
        self.textbox_current_note.tk.config(insertbackground="red")

    def _open_database(self):
        pass
