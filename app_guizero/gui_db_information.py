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


class CreateDataBaseInfoWindow:
    """ Creates a GUI window for generating database information. """

    def __init__(self, app, current_config):
        self.current_config = current_config
        self.database_line_width = 46

        self.window = Window(app,
                             title="DataBase Information",
                             width=570,
                             height=680,
                             layout="grid",
                             visible=True)

        self.text_database_label = Text(self.window,
                                        text="Database:   ",
                                        color='blue',
                                        grid=[1, 2],
                                        align="right")

        self.textbox_database_name = TextBox(self.window,
                                             text="Please Select a Database",
                                             width=self.database_line_width,
                                             grid=[1, 2, 2, 1],
                                             align="right")

        self.text_database_location_label = Text(self.window,
                                                 text="Location:   ",
                                                 color='blue',
                                                 grid=[1, 3],
                                                 align="right")

        self.textbox_database_location = TextBox(self.window,
                                                 text="Please Select a Database",
                                                 width=self.database_line_width,
                                                 height=2,
                                                 grid=[1, 3, 2, 1],
                                                 multiline=True,
                                                 scrollbar=True,
                                                 align="right")

        self.text_db_dates = Text(self.window,
                                  text="Date Range: ",
                                  color='blue',
                                  grid=[1, 4],
                                  align="right")

        self.textbox_db_dates = TextBox(self.window,
                                        text="First Recorded Date || Last Recorded Date",
                                        width=self.database_line_width,
                                        grid=[2, 4],
                                        align="left")

        self.text_db_size = Text(self.window,
                                 text="Database Misc. Info: ",
                                 color='blue',
                                 grid=[1, 5],
                                 align="right")

        self.textbox_misc_db_info = TextBox(self.window,
                                            text="DB Size:  MB || Notes: XX || Reboots: XX",
                                            width=self.database_line_width,
                                            grid=[2, 5, 2, 1],
                                            align="left")

        self.text_name_changes = Text(self.window,
                                      text="\nRecorded Name Changes\n",
                                      color='purple',
                                      grid=[2, 6, 2, 2],
                                      align="left")

        self.text_name_date = Text(self.window,
                                   text="Date of Change",
                                   color='blue',
                                   grid=[1, 10],
                                   align="left")

        self.textbox_name_date = TextBox(self.window,
                                         text="1. Date: Date",
                                         width=21,
                                         height=10,
                                         grid=[1, 11],
                                         multiline=True,
                                         scrollbar=True,
                                         align="left")

        self.text_name_new = Text(self.window,
                                  text="New Name",
                                  color='blue',
                                  grid=[2, 10, 2, 1],
                                  align="left")

        self.textbox_name_new = TextBox(self.window,
                                        text="1. New: New Name",
                                        width=21,
                                        height=10,
                                        grid=[2, 11, 2, 1],
                                        multiline=True,
                                        scrollbar=True,
                                        align="left")

        self.text_name_old = Text(self.window,
                                  text="                     Old Name",
                                  color='blue',
                                  grid=[2, 10],
                                  align="top")

        self.textbox_name_old = TextBox(self.window,
                                        text="1. Old: Old Name",
                                        width=21,
                                        height=10,
                                        grid=[2, 11, 2, 1],
                                        multiline=True,
                                        scrollbar=True,
                                        align="right")

        self.text_ip_changes = Text(self.window,
                                    text="\nRecorded IP Changes\n",
                                    color='purple',
                                    grid=[2, 12, 2, 2],
                                    align="left")

        self.text_ip_date = Text(self.window,
                                 text="Date of Change",
                                 color='blue',
                                 grid=[1, 16],
                                 align="left")

        self.textbox_ip_date = TextBox(self.window,
                                       text="1. Date: Date",
                                       width=21,
                                       height=10,
                                       grid=[1, 17],
                                       multiline=True,
                                       scrollbar=True,
                                       align="left")

        self.text_ip_new = Text(self.window,
                                text="New IP",
                                color='blue',
                                grid=[2, 16, 2, 1],
                                align="left")

        self.textbox_ip_new = TextBox(self.window,
                                      text="1. New: New IP",
                                      width=21,
                                      height=10,
                                      grid=[2, 17, 2, 1],
                                      multiline=True,
                                      scrollbar=True,
                                      align="left")

        self.text_ip_old = Text(self.window,
                                text="                     Old IP",
                                color='blue',
                                grid=[2, 16],
                                align="top")

        self.textbox_ip_old = TextBox(self.window,
                                      text="1. Old: Old IP",
                                      width=21,
                                      height=10,
                                      grid=[2, 17, 2, 1],
                                      multiline=True,
                                      scrollbar=True,
                                      align="right")

        self.button_select_database = PushButton(self.window,
                                                 text="Select Database",
                                                 command=self._select_database,
                                                 grid=[2, 24],
                                                 align="right")

        # Window Tweaks
        self.window.tk.resizable(False, False)
        self.textbox_database_name.disable()
        self.textbox_database_location.disable()
        self.textbox_db_dates.disable()
        self.textbox_misc_db_info.disable()

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

        self._set_misc_db_info(db_location)

    def _set_misc_db_info(self, db_location):
        db_size = self.get_sql_db_size(db_location)
        db_number_notes = self._get_db_notes(db_location)
        reboot_count = self._get_sensor_reboot_count(db_location)

        db_info_str = "Size: " + db_size + " || Notes: " + db_number_notes + " || Reboots: " + reboot_count

        self.textbox_misc_db_info.enable()
        self.textbox_misc_db_info.value = db_info_str
        self.textbox_misc_db_info.disable()

    def _set_first_last_date(self, db_location):
        sql_query = "SELECT Min(" + \
                    str(sql_column_names.date_time) + \
                    ") AS First, Max(" + \
                    str(sql_column_names.date_time) + \
                    ") AS Last FROM " + \
                    str(sql_column_names.sql_interval_table)

        db_datetime_column = str(self._get_sql_data(db_location, sql_query))

        try:
            db_datetime_column_list = db_datetime_column.split(",")
        except Exception as error:
            app_logger.app_logger.error("Database get First & Last DateTime - Failed - " + str(error))
            db_datetime_column_list = ["---NA-----", "--NA-------"]

        if len(db_datetime_column_list) == 2:
            db_datetime_column_list[0] = adjust_datetime(db_datetime_column_list[0][3:-5],
                                                         self.current_config.datetime_offset)
            db_datetime_column_list[1] = adjust_datetime(db_datetime_column_list[1][2:-7],
                                                         self.current_config.datetime_offset)

            self.textbox_db_dates.enable()
            self.textbox_db_dates.value = db_datetime_column_list[0] + " || " + db_datetime_column_list[1]
            self.textbox_db_dates.disable()
        else:
            self.textbox_db_dates.enable()
            self.textbox_db_dates.value = "Invalid DataBase"
            self.textbox_db_dates.disable()

    def _get_db_notes(self, db_location):
        sql_query = "SELECT count(" + \
                    str(sql_column_names.other_notes) + \
                    ") FROM " + \
                    str(sql_column_names.sql_other_table)

        number_of_notes = str(self._get_sql_data(db_location, sql_query))
        if len(number_of_notes) > 5:
            return_notes_count = number_of_notes[2:-3]
        else:
            app_logger.app_logger.error("Unable to get DB Notes count")
            return_notes_count = "NA"

        return return_notes_count

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
            return str(round(db_size_mb, 2)) + " MB"
        except Exception as error:
            app_logger.app_logger.error("Database Size - Failed - " + str(error))
            return "NA"

    @staticmethod
    def _get_sensor_reboot_count(db_location):
        sql_query = "SELECT " + \
                    str(sql_column_names.system_uptime) + \
                    " FROM " + \
                    str(sql_column_names.sql_interval_table)

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

        reboot_count = 0
        previous_entry = 0
        for entry in sql_column_data:
            entry_int = int(str(entry)[2:-3])
            if entry_int < previous_entry:
                reboot_count += 1
                previous_entry = entry_int
            else:
                previous_entry = entry_int
        if reboot_count is 0:
            return "NA"
        else:
            return str(reboot_count)
