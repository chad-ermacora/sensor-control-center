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
from guizero import Window, PushButton, Text, TextBox, yesno, error as guierror
from app_modules.app_graph import CreateSQLColumnNames
from app_modules.app_graph import adjust_datetime

sql_column_names = CreateSQLColumnNames()


class CreateDataBaseNotesWindow:
    """ Creates a GUI window for generating database information. """

    def __init__(self, app, current_config):
        self.current_config = current_config
        self.db_location = ""

        self.window = Window(app,
                             title="DataBase Notes Editor",
                             width=585,
                             height=555,
                             layout="grid",
                             visible=True)

        self.button_open_database = PushButton(self.window,
                                               text="Open\nDatabase",
                                               command=self._open_database,
                                               grid=[1, 5],
                                               align="left")

        self.button_back_note = PushButton(self.window,
                                           text="Back",
                                           command=self._back_button,
                                           grid=[2, 5],
                                           align="left")

        self.text_note_current = Text(self.window,
                                      text="Current\nNote",
                                      color="blue",
                                      grid=[3, 5],
                                      align="top")

        self.textbox_on_number_notes = TextBox(self.window,
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

        self.text_note_total = Text(self.window,
                                    text="Total\nNotes",
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
                                           command=self._next_button,
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

        self.button_new_note = PushButton(self.window,
                                          text="Add\nNote",
                                          command=self._add_note_button,
                                          grid=[1, 12],
                                          align="left")

        self.button_delete_note = PushButton(self.window,
                                             text="Delete Current\nNote",
                                             command=self._delete_button,
                                             grid=[4, 12],
                                             align="left")

        self.button_save_note = PushButton(self.window,
                                           text="Save\nNote",
                                           command=self._save_note_button,
                                           grid=[6, 12],
                                           align="left")

        # Window Tweaks
        self._disable_notes()
        self.textbox_current_note.bg = "black"
        self.textbox_current_note.text_color = "white"
        self.textbox_current_note.tk.config(insertbackground="red")

    def _open_database(self):
        """ Prompts for Database to open and opens it. """
        self.db_location = filedialog.askopenfilename()

        if str(self.db_location) != "()" and self.db_location != "":
            database_notes = self.get_database_notes()
            database_notes_dates = self.get_database_notes_dates()

            self.textbox_number_of_notes_total.value = str(len(database_notes))

            if len(database_notes) > 0:
                self.textbox_current_note.enable()
                self.textbox_on_number_notes.enable()
                self.textbox_current_note.value = str(database_notes[0])[2:-3]
                self.text_note_date.value = str(database_notes_dates[0])[2:-7]
                self.textbox_on_number_notes.value = "1"

                self.button_next_note.enable()
                self.button_back_note.enable()
                self.button_delete_note.enable()
            else:
                self.textbox_current_note.enable()
                self.textbox_current_note.value = "No Notes Found"
                self._disable_notes()

    def get_database_notes(self):
        sql_query = "SELECT " + \
                    str(sql_column_names.other_notes) + \
                    " FROM " + \
                    str(sql_column_names.sql_other_table)

        database_notes = self._get_sql_data(sql_query)

        return database_notes

    def get_database_notes_dates(self):
        sql_query = "SELECT " + \
                    str(sql_column_names.date_time) + \
                    " FROM " + \
                    str(sql_column_names.sql_other_table)

        database_notes_dates = self._get_sql_data(sql_query)

        return database_notes_dates

    def _next_button(self):
        self._set_note(1)

    def _back_button(self):
        self._set_note(-1)

    def _add_note_button(self):
        pass

    def _delete_button(self):
        try:
            if int(self.textbox_on_number_notes.value) < 1 or int(self.textbox_on_number_notes.value) > len(
                    self.get_database_notes_dates()):
                app_logger.app_logger.warning("Error: Current Note Number is more or less then total")
                guierror("Invalid Current Note Number", (" '" + self.textbox_on_number_notes.value +
                                                         "' is a invalid option\nPlease enter a number between 1 and " +
                                                         str(len(self.get_database_notes_dates()))))
                self._set_note(0)

            elif yesno("Delete Note", "Are you sure you want to Delete Note " +
                                      self.textbox_on_number_notes.value + " out of " + self.textbox_number_of_notes_total.value + "?"):
                note_date_times = self.get_database_notes_dates()
                datetime = str(note_date_times[int(self.textbox_on_number_notes.value) - 1])[2:-3]
                sql_query = "DELETE FROM " + \
                            str(sql_column_names.sql_other_table) + \
                            " WHERE " + \
                            str(sql_column_names.date_time) + \
                            " = '" + datetime + "'"

                self._delete_sql_row(sql_query)
                self._set_note(0)
        except Exception as error:
            app_logger.app_logger.error("Invalid Current Note number: " + str(error))
            guierror("Invalid Current Note Number", (" '" + self.textbox_on_number_notes.value +
                                                     "' is a invalid option\nPlease enter a number between 1 and " +
                                                     str(len(self.get_database_notes_dates()))))
            self._set_note(0)

    def _save_note_button(self):
        pass

    def _set_note(self, plus):
        database_notes = self.get_database_notes()
        database_notes_dates = self.get_database_notes_dates()

        self.textbox_number_of_notes_total.value = str(len(database_notes))

        if len(database_notes) < 1:
            self.textbox_current_note.enable()
            self.textbox_current_note.value = "No Notes Found"
            self._disable_notes()
        else:
            try:
                current_note = int(self.textbox_on_number_notes.value)
                if current_note + plus > int(len(database_notes)):
                    self.textbox_on_number_notes.value = "1"
                    current_note = 1
                elif current_note + plus < 1:
                    self.textbox_on_number_notes.value = str(len(database_notes))
                    current_note = len(database_notes)
                else:
                    current_note += plus
            except Exception as error:
                app_logger.app_logger.error("Unable to convert current Note count: " + str(error))
                current_note = 1

            self.textbox_on_number_notes.value = str(current_note)
            self.textbox_current_note.value = str(database_notes[(current_note - 1)])[2:-3]

            self.text_note_date.value = str(database_notes_dates[(current_note - 1)])[2:-7]

    def _get_sql_data(self, sql_query):
        try:
            database_connection = sqlite3.connect(self.db_location)
            sqlite_database = database_connection.cursor()
            sqlite_database.execute(sql_query)
            sql_column_data = sqlite_database.fetchall()
            sqlite_database.close()
            database_connection.close()
        except Exception as error:
            app_logger.app_logger.error("DB Error: " + str(error))
            sql_column_data = []

        return sql_column_data

    def _delete_sql_row(self, sql_query):
        try:
            database_connection = sqlite3.connect(self.db_location)
            sqlite_database = database_connection.cursor()
            sqlite_database.execute(sql_query)
            database_connection.commit()
            sqlite_database.close()
            database_connection.close()
        except Exception as error:
            app_logger.app_logger.error("DB Error: " + str(error))

    def _disable_notes(self):
        self.button_back_note.disable()
        self.textbox_on_number_notes.value = "0"
        self.textbox_on_number_notes.disable()
        self.textbox_number_of_notes_total.disable()
        self.button_next_note.disable()
        self.textbox_current_note.value = ""
        self.textbox_current_note.disable()

        self.button_new_note.disable()
        self.button_delete_note.disable()
        self.button_save_note.disable()

        self.text_note_date.value = "YYYY-MM-DD hh:mm"
