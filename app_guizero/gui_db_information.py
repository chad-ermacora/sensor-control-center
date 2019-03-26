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
        self.database_line_width = 40
        self.textbox_table_width = 21

        self.window = Window(app,
                             title="DataBase Information",
                             width=565,
                             height=635,
                             layout="grid",
                             visible=False)

        self.button_open_database = PushButton(self.window,
                                               text="Open\nDatabase",
                                               command=self._open_database,
                                               grid=[1, 1, 1, 2],
                                               align="left")

        self.text_database_label = Text(self.window,
                                        text="Database: ",
                                        color='blue',
                                        grid=[1, 1],
                                        align="right")

        self.textbox_database_name = TextBox(self.window,
                                             text="Please Open a Database",
                                             width=self.database_line_width,
                                             grid=[2, 1, 2, 1],
                                             align="left")

        self.text_database_location_label = Text(self.window,
                                                 text="Location: ",
                                                 color='blue',
                                                 grid=[1, 2],
                                                 align="right")

        self.textbox_database_location = TextBox(self.window,
                                                 text="Please Open a Database",
                                                 width=self.database_line_width,
                                                 height=2,
                                                 grid=[2, 2, 2, 1],
                                                 multiline=True,
                                                 scrollbar=True,
                                                 align="left")

        self.text_db_dates = Text(self.window,
                                  text="Date Range: ",
                                  color='blue',
                                  grid=[1, 3],
                                  align="right")

        self.textbox_db_dates = TextBox(self.window,
                                        text="First Recorded Date || Last Recorded Date",
                                        width=self.database_line_width,
                                        grid=[2, 3, 2, 1],
                                        align="left")

        self.text_db_size = Text(self.window,
                                 text="Database Misc. Info: ",
                                 color='blue',
                                 grid=[1, 4],
                                 align="right")

        self.textbox_misc_db_info = TextBox(self.window,
                                            text="DB Size:  MB || Notes: XX || Reboots: XX",
                                            width=self.database_line_width,
                                            grid=[2, 4, 2, 1],
                                            align="left")

        self.text_name_changes = Text(self.window,
                                      text="\nRecorded Name Changes\n",
                                      color='purple',
                                      grid=[2, 7, 2, 1],
                                      align="left")

        self.text_name_date = Text(self.window,
                                   text="Date of Change",
                                   color='blue',
                                   grid=[1, 10],
                                   align="left")

        self.textbox_name_dates = TextBox(self.window,
                                          text="1. Date",
                                          width=self.textbox_table_width,
                                          height=10,
                                          grid=[1, 11],
                                          multiline=True,
                                          scrollbar=True,
                                          align="left")

        self.text_name_new = Text(self.window,
                                  text="New Name",
                                  color='blue',
                                  grid=[2, 10],
                                  align="left")

        self.textbox_new_names = TextBox(self.window,
                                         text="1. NewName",
                                         width=self.textbox_table_width,
                                         height=10,
                                         grid=[2, 11],
                                         multiline=True,
                                         scrollbar=True,
                                         align="left")

        self.text_name_old = Text(self.window,
                                  text="Old Name",
                                  color='blue',
                                  grid=[3, 10],
                                  align="left")

        self.textbox_old_names = TextBox(self.window,
                                         text="1. OldName",
                                         width=self.textbox_table_width,
                                         height=10,
                                         grid=[3, 11],
                                         multiline=True,
                                         scrollbar=True,
                                         align="left")

        self.text_ip_changes = Text(self.window,
                                    text="\nRecorded IP Changes\n",
                                    color='purple',
                                    grid=[2, 12],
                                    align="left")

        self.text_ip_date = Text(self.window,
                                 text="Date of Change",
                                 color='blue',
                                 grid=[1, 16],
                                 align="left")

        self.textbox_ip_dates = TextBox(self.window,
                                        text="1. Date",
                                        width=self.textbox_table_width,
                                        height=10,
                                        grid=[1, 17],
                                        multiline=True,
                                        scrollbar=True,
                                        align="left")

        self.text_ip_new = Text(self.window,
                                text="New IP",
                                color='blue',
                                grid=[2, 16],
                                align="left")

        self.textbox_new_ips = TextBox(self.window,
                                       text="1. NewIP",
                                       width=self.textbox_table_width,
                                       height=10,
                                       grid=[2, 17],
                                       multiline=True,
                                       scrollbar=True,
                                       align="left")

        self.text_ip_old = Text(self.window,
                                text="Old IP",
                                color='blue',
                                grid=[3, 16],
                                align="left")

        self.textbox_old_ips = TextBox(self.window,
                                       text="1. OldIP",
                                       width=self.textbox_table_width,
                                       height=10,
                                       grid=[3, 17],
                                       multiline=True,
                                       scrollbar=True,
                                       align="left")

        self.text_spacer = Text(self.window,
                                text="",
                                grid=[1, 18],
                                align="left")

        # Window Tweaks
        self.window.tk.resizable(False, False)
        self.textbox_database_name.disable()
        self.textbox_database_location.disable()
        self.textbox_db_dates.disable()
        self.textbox_misc_db_info.disable()

        self.textbox_name_dates.bg = "black"
        self.textbox_name_dates.text_color = "white"
        self.textbox_name_dates.tk.config(insertbackground="red")

        self.textbox_new_names.bg = "black"
        self.textbox_new_names.text_color = "white"
        self.textbox_new_names.tk.config(insertbackground="red")

        self.textbox_old_names.bg = "black"
        self.textbox_old_names.text_color = "white"
        self.textbox_old_names.tk.config(insertbackground="red")

        self.textbox_ip_dates.bg = "black"
        self.textbox_ip_dates.text_color = "white"
        self.textbox_ip_dates.tk.config(insertbackground="red")

        self.textbox_new_ips.bg = "black"
        self.textbox_new_ips.text_color = "white"
        self.textbox_new_ips.tk.config(insertbackground="red")

        self.textbox_old_ips.bg = "black"
        self.textbox_old_ips.text_color = "white"
        self.textbox_old_ips.tk.config(insertbackground="red")

    def _open_database(self):
        """ Prompts for Database to open and opens it. """
        str_location = ""
        db_location = filedialog.askopenfilename()
        db_location_list = str(db_location).split("/")

        if str(db_location) != "()" and db_location != "":
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

            self.set_all_name_ip_columns(db_location)

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

    def _get_sensor_reboot_count(self, db_location):
        sql_query = "SELECT " + \
                    str(sql_column_names.system_uptime) + \
                    " FROM " + \
                    str(sql_column_names.sql_interval_table)

        sql_column_data = self._get_sql_data(db_location, sql_query)

        reboot_count = 0
        previous_entry = 0
        bad_entries = 0
        for entry in sql_column_data:
            try:
                entry_int = int(str(entry)[2:-3])
            except Exception as error:
                app_logger.app_logger.debug("DB Error: " + str(error))
                bad_entries += 1
                entry_int = previous_entry

            if entry_int < previous_entry:
                reboot_count += 1
                previous_entry = entry_int
            else:
                previous_entry = entry_int

        if bad_entries:
            app_logger.app_logger.error("One or more bad entries in DB reboot column")

        if reboot_count:
            return str(reboot_count)
        else:
            app_logger.app_logger.error("Database get reboot count - Failed")
            return "NA"

    def set_all_name_ip_columns(self, db_location):
        var_columns = [sql_column_names.date_time,
                       sql_column_names.sensor_name,
                       sql_column_names.ip]

        var_column_data = []

        for column in var_columns:
            sql_query = "SELECT " + \
                        column + \
                        " FROM " + \
                        sql_column_names.sql_interval_table

            var_column_data.append(self._get_sql_data(db_location, sql_query))

        self._set_recorded_changes(var_column_data)

    def _set_recorded_changes(self, var_column_data):
        bad_sql_entry = False

        if len(var_column_data[0]) > 0:
            count = 0
            while count < len(var_column_data[0]):
                try:
                    var_column_data[0][count] = str(var_column_data[0][count])[2:-10]
                    var_column_data[1][count] = str(var_column_data[1][count])[2:-3]
                    var_column_data[2][count] = str(var_column_data[2][count])[2:-3]
                except Exception as error:
                    bad_sql_entry = True
                    app_logger.app_logger.debug("Bad SQL Entry: " + str(error))
                count += 1

            if bad_sql_entry:
                app_logger.app_logger.error("One or more Bad SQL Entries")

            self._set_changed_names(var_column_data)
            self._set_changed_ips(var_column_data)
        else:
            self.textbox_ip_dates.value = "NA"
            self.textbox_old_ips.value = "NA"
            self.textbox_new_ips.value = "NA"

            self.textbox_name_dates.value = "NA"
            self.textbox_new_names.value = "NA"
            self.textbox_old_names.value = "NA"

    def _set_changed_names(self, var_column_data):
        name_dates = []
        new_names = []
        old_names = []

        previous_name = var_column_data[1][0]
        count = 0
        for name in var_column_data[1]:
            if str(name) != str(previous_name):
                name_dates.append(var_column_data[0][count])
                new_names.append(name)
                old_names.append(previous_name)
                previous_name = name
            count += 1

        if len(name_dates) == 0:
            self.textbox_name_dates.value = "No Changes Found"
        else:
            self.textbox_name_dates.value = self._get_change_textbox_str(name_dates)

        if len(new_names) == 0:
            self.textbox_new_names.value = "No Changes Found"
        else:
            self.textbox_new_names.value = self._get_change_textbox_str(new_names)

        if len(old_names) == 0:
            self.textbox_old_names.value = "No Changes Found"
        else:
            self.textbox_old_names.value = self._get_change_textbox_str(old_names)

    def _set_changed_ips(self, var_column_data):

        ip_dates = []
        new_ips = []
        old_ips = []

        previous_ip = var_column_data[2][0]
        count = 0
        for ip in var_column_data[2]:
            if str(ip) != str(previous_ip):
                ip_dates.append(var_column_data[0][count])
                new_ips.append(ip)
                old_ips.append(previous_ip)
                previous_ip = ip
            count += 1

        if len(ip_dates) == 0:
            self.textbox_ip_dates.value = "No Changes Found"
        else:
            self.textbox_ip_dates.value = self._get_change_textbox_str(ip_dates)

        if len(new_ips) == 0:
            self.textbox_new_ips.value = "No Changes Found"
        else:
            self.textbox_new_ips.value = self._get_change_textbox_str(new_ips)

        if len(old_ips) == 0:
            self.textbox_old_ips.value = "No Changes Found"
        else:
            self.textbox_old_ips.value = self._get_change_textbox_str(old_ips)

    @staticmethod
    def _get_change_textbox_str(sql_list):
        return_str = ""

        count = 1
        for name in sql_list:
            return_str += str(count) + ". " + name + "\n"
            count += 1

        return return_str
