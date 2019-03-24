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

sql_column_names = CreateSQLColumnNames()


class CreateDataBaseInfoWindow:
    """ Creates a GUI window for generating database information. """

    def __init__(self, app, current_config):
        self.current_config = current_config
        self.database_line_width = 45

        self.window = Window(app,
                             title="DataBase Information",
                             width=500,
                             height=500,
                             layout="grid",
                             visible=True)

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

        self.text_db_dates = Text(self.window,
                                  text="Date Range: ",
                                  color='blue',
                                  grid=[1, 4],
                                  align="left")

        self.textbox_db_dates = TextBox(self.window,
                                        text="First Recorded Date || Last Recorded Date",
                                        width=40,
                                        grid=[2, 4],
                                        align="left")

        self.text_db_size = Text(self.window,
                                 text="DB Size: ",
                                 color='blue',
                                 grid=[1, 5],
                                 align="left")

        self.textbox_db_size = TextBox(self.window,
                                       text=" MB",
                                       width=12,
                                       grid=[2, 5],
                                       align="left")

        self.text_db_notes = Text(self.window,
                                  text="Number of DB Notes: ",
                                  color='blue',
                                  grid=[2, 5, 2, 1],
                                  align="top")

        self.textbox_db_notes = TextBox(self.window,
                                        text="",
                                        width=12,
                                        grid=[2, 5, 2, 1],
                                        align="right")

        self.button_select_database = PushButton(self.window,
                                                 text="Select Database",
                                                 command=self._select_database,
                                                 grid=[2, 14],
                                                 align="right")

        # Window Tweaks
        self.textbox_database_name.disable()
        self.textbox_database_location.disable()
        self.textbox_db_dates.disable()
        self.textbox_db_size.disable()
        self.textbox_db_notes.disable()

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

        self._set_first_last_date(db_location)
        self._set_db_size(db_location)

        self._set_db_notes(db_location)

    def _set_first_last_date(self, db_location):
        sql_query = "SELECT Min(" + \
                    str(sql_column_names.date_time) + \
                    ") AS First, Max(" + \
                    str(sql_column_names.date_time) + \
                    ") AS Last FROM " + \
                    str(sql_column_names.sql_interval_table)

        db_datetime_column = str(self._get_sql_data(db_location, sql_query))
        db_datetime_column_list = db_datetime_column.split(",")

        if len(db_datetime_column_list) == 2:
            db_datetime_column_list[0] = db_datetime_column_list[0][3:-5]
            db_datetime_column_list[1] = db_datetime_column_list[1][2:-7]

            self.textbox_db_dates.enable()
            self.textbox_db_dates.value = db_datetime_column_list[0] + " || " + db_datetime_column_list[1]
            self.textbox_db_dates.disable()
        else:
            self.textbox_db_dates.enable()
            self.textbox_db_dates.value = "Invalid DataBase"
            self.textbox_db_dates.disable()

    def _set_db_notes(self, db_location):
        sql_query = "SELECT count(" + \
                    str(sql_column_names.other_notes) + \
                    ") FROM " + \
                    str(sql_column_names.sql_other_table)

        number_of_notes = self._get_sql_data(db_location, sql_query)

        self.textbox_db_notes.enable()
        self.textbox_db_notes.value = str(number_of_notes)[2:-3]
        self.textbox_db_notes.disable()

    def _set_db_size(self, db_location):
        self.textbox_db_size.enable()
        self.textbox_db_size.value = self.get_sql_db_size(db_location)
        self.textbox_db_size.disable()

    @staticmethod
    def _get_sql_data(db_location, sql_query):
        try:
            database_connection = sqlite3.connect(db_location)
            sqlite_database = database_connection.cursor()
            sqlite_database.execute(sql_query)
            sql_column_data = sqlite_database.fetchall()
            sqlite_database.close()
            database_connection.close()
        except Exception as error:
            app_logger.app_logger.error("DB Error: " + str(error))
            sql_column_data = []

        return sql_column_data

    @staticmethod
    def get_sql_db_size(db_location):
        try:
            db_size_mb = os.path.getsize(db_location) / 1024000
            app_logger.app_logger.debug("Database Size - OK")
        except Exception as error:
            app_logger.app_logger.error("Database Size - Failed - " + str(error))
            db_size_mb = 0.0
        return str(round(db_size_mb, 2)) + " MB"
