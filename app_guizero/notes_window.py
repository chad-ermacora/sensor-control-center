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
import guizero
import sqlite3
from tkinter import filedialog
from datetime import datetime, timedelta
from app_modules import app_logger
from app_modules import app_variables
from app_modules import app_useful_functions
from app_modules import sensor_commands


class CreateGenericNoteVariables:
    """ Holds generic text variables for notes window """

    def __init__(self):
        self.checkbox_enable_datetime = "Use current Date & Time"
        self.button_back_note = "Back"
        self.text_note_current = "Current"
        self.text_date_label1 = "Note's Date"
        self.textbox_note_date = "YYYY-MM-DD hh:mm:ss"
        self.text_total_notes_label = "Total"
        self.button_next_note = "Next"
        self.button_new_note = "Add Note"
        self.button_delete_note = "Delete Note"
        self.button_update_note = "Update Note"

        self.sensor_notes_verification = "sensor"
        self.no_notes_found = "No Notes Found"
        self.replace_comma = "[replaced_comma]"
        self.replace_new_line = "[new_line]"
        self.replace_back_slash = "[clean_slash]"
        self.sensor_return_no_notes = "No Data"


class CreateSensorNoteVariables:
    """ Holds text variables for notes window connecting to a Sensor """

    def __init__(self):
        self.window_title = "Online Notes Editor"
        self.text_connected_to = "Sensor: IP"
        self.button_connect = "Connect to Sensor"
        self.textbox_current_note = "Please Connect to a Sensor to view Notes"


class CreateDatabaseNoteVariables:
    """ Holds text variables for notes window connecting to a Database """

    def __init__(self):
        self.window_title = "Offline Notes Editor"
        self.text_connected_to = "Database: Database_file_name"
        self.button_connect = "Open Database"
        self.textbox_current_note = "Please Open a Database to view Notes"


class CreateDataBaseNotesWindow:
    """ Creates a GUI window for generating database information. """

    def __init__(self, app, ip_selection, current_config, database_or_sensor):
        self.database_or_sensor = database_or_sensor
        self.current_config = current_config
        self.ip_selection = ip_selection
        self.selected_ip = ""
        self.db_location = ""
        self.database_notes = []
        self.database_notes_dates = []
        self.database_user_note_dates = []

        self.text_variables_generic = CreateGenericNoteVariables()
        self.text_variables_sensor = CreateSensorNoteVariables()
        self.text_variables_database = CreateDatabaseNoteVariables()

        self.sql_column_names = app_variables.CreateSQLColumnNames()
        self.network_send_commands = app_variables.CreateNetworkSendCommands()
        self.sensor_get_commands = app_variables.CreateNetworkGetCommands()

        self.window = guizero.Window(app,
                                     title=self.text_variables_database.window_title,
                                     width=580,
                                     height=525,
                                     layout="grid",
                                     visible=False)

        self.text_connected_to = guizero.Text(self.window,
                                              text=self.text_variables_database.text_connected_to,
                                              color="red",
                                              size=8,
                                              grid=[1, 1, 3, 1],
                                              align="left")

        self.checkbox_use_current_datetime = guizero.CheckBox(self.window,
                                                              text=self.text_variables_generic.checkbox_enable_datetime,
                                                              command=self._reset_datetime,
                                                              grid=[4, 1, 5, 1],
                                                              align="left")

        self.button_connect = guizero.PushButton(self.window,
                                                 text=self.text_variables_database.button_connect,
                                                 command=self._open_database,
                                                 grid=[1, 5],
                                                 align="left")

        self.button_back_note = guizero.PushButton(self.window,
                                                   text="Back",
                                                   command=self._back_button,
                                                   grid=[2, 5],
                                                   align="left")

        self.text_note_current = guizero.Text(self.window,
                                              text=self.text_variables_generic.text_note_current,
                                              color="blue",
                                              grid=[3, 5],
                                              align="top")

        self.textbox_on_number_notes = guizero.TextBox(self.window,
                                                       text="0",
                                                       width=5,
                                                       grid=[3, 5],
                                                       align="bottom")

        self.text_date_label1 = guizero.Text(self.window,
                                             text=self.text_variables_generic.text_date_label1,
                                             color="blue",
                                             grid=[4, 5],
                                             align="top")

        self.textbox_note_date = guizero.TextBox(self.window,
                                                 text=self.text_variables_generic.textbox_note_date,
                                                 grid=[4, 5],
                                                 width=23,
                                                 align="bottom")

        self.text_total_notes_label = guizero.Text(self.window,
                                                   text=self.text_variables_generic.text_total_notes_label,
                                                   color="blue",
                                                   grid=[5, 5],
                                                   align="top")

        self.textbox_total_notes = guizero.TextBox(self.window,
                                                   text="0",
                                                   width=5,
                                                   grid=[5, 5],
                                                   align="bottom")

        self.button_next_note = guizero.PushButton(self.window,
                                                   text=self.text_variables_generic.button_next_note,
                                                   command=self._next_button,
                                                   grid=[6, 5],
                                                   align="left")

        self.textbox_current_note = guizero.TextBox(self.window,
                                                    text=self.text_variables_database.textbox_current_note,
                                                    width=70,
                                                    height=25,
                                                    grid=[1, 10, 6, 1],
                                                    multiline=True,
                                                    scrollbar=True,
                                                    align="left")

        self.button_new_note = guizero.PushButton(self.window,
                                                  text=self.text_variables_generic.button_new_note,
                                                  command=self._database_add_note_button,
                                                  grid=[1, 12],
                                                  align="left")

        self.button_delete_note = guizero.PushButton(self.window,
                                                     text=self.text_variables_generic.button_delete_note,
                                                     command=self._database_delete_button,
                                                     grid=[4, 12],
                                                     align="left")

        self.button_update_note = guizero.PushButton(self.window,
                                                     text=self.text_variables_generic.button_update_note,
                                                     command=self._database_update_note_button,
                                                     grid=[5, 12, 2, 1],
                                                     align="left")

        # Window Tweaks
        self.window.tk.resizable(False, False)
        self._disable_notes_window_functions()
        self.checkbox_use_current_datetime.value = True
        self.textbox_current_note.bg = "black"
        self.textbox_current_note.text_color = "white"
        self.textbox_current_note.tk.config(insertbackground="red")

        if database_or_sensor == self.text_variables_generic.sensor_notes_verification:
            self._change_for_sensor()

    def _connect_to_sensor(self):
        """ Prompts for Database to open and opens it. """
        ip_list = self.ip_selection.get_verified_ip_list()

        if len(ip_list) > 0:
            self.selected_ip = ip_list[0]
            self.text_connected_to.value = self.text_variables_sensor.text_connected_to[:-2] + self.selected_ip
            command = self.sensor_get_commands.database_notes
            network_timeout = self.current_config.network_timeout_data
            sensor_command = sensor_commands.CreateSensorNetworkCommand(self.selected_ip, network_timeout, command)

            test_database_notes = sensor_commands.get_data(sensor_command).split(",")

            if str(test_database_notes)[2:-2] == self.text_variables_generic.sensor_return_no_notes:
                self._no_sql_notes()
            else:
                self.database_notes = test_database_notes

                sensor_command.command = self.sensor_get_commands.database_note_dates
                self.database_notes_dates = sensor_commands.get_data(sensor_command).split(",")
                sensor_command.command = self.sensor_get_commands.database_user_note_dates
                self.database_user_note_dates = sensor_commands.get_data(sensor_command).split(",")

                count = 0
                datetime_offset = self.current_config.datetime_offset
                for date in self.database_user_note_dates:
                    new_date = self.adjust_datetime(date, datetime_offset)
                    self.database_user_note_dates[count] = new_date
                    count += 1

                if len(self.database_notes) > 0:
                    self.database_notes = self.undue_sterilize_notes(self.database_notes)

                    self.textbox_total_notes.value = str(len(self.database_notes))
                    self.checkbox_use_current_datetime.enable()
                    self.textbox_current_note.enable()
                    self.textbox_on_number_notes.enable()
                    self.textbox_current_note.value = self.database_notes[0]
                    self.textbox_note_date.value = self.database_user_note_dates[0]
                    self.textbox_on_number_notes.value = "1"

                    self.button_next_note.enable()
                    self.button_back_note.enable()
                    self.button_delete_note.enable()
                    self.button_new_note.enable()
                    self.button_update_note.enable()
                else:
                    self.textbox_current_note.enable()
                    self.textbox_current_note.value = self.text_variables_generic.no_notes_found
                    self._disable_notes_window_functions()
        else:
            self._disable_notes_window_functions()
            self.text_connected_to.value = self.text_variables_sensor.text_connected_to

            app_useful_functions.no_ip_selected_message()

    def _open_database(self):
        """ Prompts for Database to open and opens it. """
        unchecked_db_location = filedialog.askopenfilename()
        if str(unchecked_db_location) != "()" and unchecked_db_location != "":
            self.db_location = unchecked_db_location
            database_notes = self.get_database_notes()

            if str(database_notes) == "Bad SQL Execute":
                self._disable_notes_window_functions()
                self.text_connected_to.value = self.text_variables_database.text_connected_to
            else:
                self.textbox_current_note.enable()
                new_text = self.text_variables_database.text_connected_to[:-18] + self.db_location.split("/")[-1]
                self.text_connected_to.value = new_text

                if len(database_notes) > 0:
                    self.database_notes = self.undue_sterilize_notes(database_notes)
                    self.database_notes_dates = self.get_database_notes_dates()
                    self.database_user_note_dates = self.get_database_notes_dates_user()

                    self.textbox_on_number_notes.enable()
                    self.textbox_current_note.value = str(database_notes[0])
                    self.textbox_note_date.value = str(self.database_user_note_dates[0]).strip()
                    self.button_delete_note.enable()
                    self.button_next_note.enable()
                    self.button_back_note.enable()
                    self.button_update_note.enable()
                    self.textbox_total_notes.value = str(len(database_notes))
                else:
                    self.textbox_on_number_notes.value = "1"
                    self.textbox_total_notes.value = "0"
                    self.textbox_current_note.value = self.text_variables_generic.no_notes_found
                    self._reset_datetime()
                    self.textbox_on_number_notes.disable()
                    self.button_delete_note.disable()
                    self.button_update_note.disable()
                    self.button_back_note.disable()
                    self.button_next_note.disable()

                self.button_new_note.enable()
                self.checkbox_use_current_datetime.enable()
                self.textbox_on_number_notes.value = "1"

    def get_database_notes(self):
        sql_query = "SELECT " + \
                    str(self.sql_column_names.other_notes) + \
                    " FROM " + \
                    str(self.sql_column_names.sql_other_table)

        database_notes = self._sql_execute_get_data(sql_query)

        if database_notes == "Bad SQL Execute":
            return "Bad SQL Execute"
        else:
            count = 0
            for note in database_notes:
                new_note = self.undue_sterilize_notes(str(note)[2:-3].strip())
                database_notes[count] = new_note
                count += 1

            return database_notes

    def get_database_notes_dates(self):
        sql_query = "SELECT " + \
                    str(self.sql_column_names.date_time) + \
                    " FROM " + \
                    str(self.sql_column_names.sql_other_table)

        database_notes_dates = self._sql_execute_get_data(sql_query)

        if database_notes_dates == "Bad SQL Execute":
            return "Bad SQL Execute"
        else:
            for index, date in enumerate(database_notes_dates):
                database_notes_dates[index] = str(date)[2:-3].strip()

            return database_notes_dates

    def get_database_notes_dates_user(self):
        sql_query = "SELECT " + \
                    str(self.sql_column_names.other_user_datetime) + \
                    " FROM " + \
                    str(self.sql_column_names.sql_other_table)

        database_notes_dates_user = self._sql_execute_get_data(sql_query)

        if database_notes_dates_user == "Bad SQL Execute":
            return "Bad SQL Execute"
        else:
            count = 0
            for date in database_notes_dates_user:
                try:
                    new_date = self.adjust_datetime(str(date)[2:-3], self.current_config.datetime_offset)
                    if new_date == "":
                        database_notes_dates_user[count] = "No-DateTime"
                    else:
                        database_notes_dates_user[count] = new_date

                    count += 1
                except Exception as error:
                    app_logger.app_logger.error("Unable to convert current Note's User DateTime: " + str(error))
                    database_notes_dates_user[count] = "Bad-DateTime"
                    count += 1

        return database_notes_dates_user

    def _next_button(self):
        if self.database_or_sensor == self.text_variables_generic.sensor_notes_verification:
            self._sensor_change_to_note_plus(1)
        else:
            self._database_change_to_note_plus(1)

    def _back_button(self):
        if self.database_or_sensor == self.text_variables_generic.sensor_notes_verification:
            self._sensor_change_to_note_plus(-1)
        else:
            self._database_change_to_note_plus(-1)

    def _sensor_add_note_button(self):
        """ Send the note to selected sensor. """
        if self.textbox_current_note.value.strip() == "":
            guizero.warn("Empty Note", "Cannot add a blank Note")
        else:
            if self.checkbox_use_current_datetime.value:
                self._reset_datetime()

            try:
                user_datetime_var = self.adjust_datetime(self.textbox_note_date.value,
                                                         self.current_config.datetime_offset * -1)
            except Exception as error:
                user_datetime_var = self.textbox_note_date.value
                app_logger.sensor_logger.error("Unable to convert user entered DateTime: " + str(error))

            command = self.network_send_commands.put_sql_note
            network_timeout = self.current_config.network_timeout_data

            sensor_command = sensor_commands.CreateSensorNetworkCommand(self.selected_ip, network_timeout, command)
            sensor_command.command_data = user_datetime_var + \
                                          self.network_send_commands.command_data_separator + \
                                          self.sterilize_notes(self.textbox_current_note.value)
            sensor_commands.put_command(sensor_command)

            guizero.info("Note Inserted into Sensors " + self.selected_ip,
                         "Inserted with DateTime: " + user_datetime_var)
            app_logger.sensor_logger.info("Inserted note into sensors " + str(self.selected_ip) +
                                          " with DateTime " + user_datetime_var)
            self._connect_to_sensor()

    def _database_add_note_button(self):
        sql_note_datetime = self.current_config.get_str_datetime_now()
        utc_0_datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        sql_note = self.sterilize_notes(self.textbox_current_note.value)

        if self.checkbox_use_current_datetime.value:
            sql_note_user_datetime = sql_note_datetime
        else:
            sql_note_user_datetime = self.textbox_note_date.value.strip()

        self.database_notes.append(sql_note)
        self.database_notes_dates.append(utc_0_datetime)
        self.database_user_note_dates.append(sql_note_user_datetime)

        datetime_offset = self.current_config.datetime_offset
        sql_note_user_datetime_utc_0 = self.adjust_datetime(sql_note_user_datetime, datetime_offset * -1)

        if sql_note == "":
            guizero.warn("Empty Note", "Cannot add a blank Note")
        else:
            self.button_delete_note.enable()
            self.button_update_note.enable()
            self.button_back_note.enable()
            self.button_next_note.enable()
            sql_query = "INSERT OR IGNORE INTO " + \
                        self.sql_column_names.sql_other_table + " (" + \
                        self.sql_column_names.date_time + "," + \
                        self.sql_column_names.other_notes + "," + \
                        self.sql_column_names.other_user_datetime + \
                        ") VALUES ('" + utc_0_datetime + "','" + sql_note + "','" + sql_note_user_datetime_utc_0 + "')"

            self._sql_execute(sql_query)
            self._database_change_to_note_plus(0)

    def _sensor_delete_button(self):
        current_note_on = int(self.textbox_on_number_notes.value) - 1

        if guizero.yesno("Delete Note", "Are you sure you want to Delete Note " +
                                        self.textbox_on_number_notes.value + " out of " +
                                        self.textbox_total_notes.value + "?\n\n"):
            utc_0_datetime = self.database_notes_dates[current_note_on]
            command = self.network_send_commands.delete_sql_note
            network_timeout = self.current_config.network_timeout_data

            sensor_command = sensor_commands.CreateSensorNetworkCommand(self.selected_ip, network_timeout, command)
            sensor_command.command_data = utc_0_datetime
            sensor_commands.put_command(sensor_command)

            app_logger.sensor_logger.info("Deleted note from sensor " + self.selected_ip)
            self._connect_to_sensor()

    def _database_delete_button(self):
        on_note_number = int(self.textbox_on_number_notes.value)
        number_of_notes = len(self.database_notes)
        try:
            if on_note_number < 1 or on_note_number > number_of_notes:
                app_logger.app_logger.warning("Error: Current Note Number is more or less then total")

                guizero.error("Invalid Current Note Number", (" '" + str(on_note_number) + "' is a invalid option\n" +
                                                              "Please enter a number between 1 and " +
                                                              str(number_of_notes)))
                self._database_change_to_note_plus(0)

            elif guizero.yesno("Delete Note", "Are you sure you want to Delete Note " +
                                              self.textbox_on_number_notes.value + " out of " +
                                              self.textbox_total_notes.value + "?"):

                note_date_times = self.get_database_notes_dates()
                datetime_var = str(note_date_times[on_note_number - 1])

                sql_query = "DELETE FROM " + \
                            str(self.sql_column_names.sql_other_table) + \
                            " WHERE " + \
                            str(self.sql_column_names.date_time) + \
                            " = '" + datetime_var + "'"

                self._sql_execute(sql_query)

                self.database_notes.pop(on_note_number - 1)
                self.database_notes_dates.pop(on_note_number - 1)
                self.database_user_note_dates.pop(on_note_number - 1)

                self._database_change_to_note_plus(0)
        except Exception as error:
            app_logger.app_logger.error("Invalid Current Note number: " + str(error))
            guizero.error("Invalid Current Note Number", (" '" + self.textbox_on_number_notes.value +
                                                          "' is a invalid option\nPlease enter a number between 1 and " +
                                                          str(len(self.get_database_notes_dates()))))
            self._database_change_to_note_plus(0)

    def _sensor_update_note_button(self):
        current_note_number = int(self.textbox_on_number_notes.value.strip()) - 1
        utc_0_datetime_current = self.database_notes_dates[current_note_number]
        reverse_datetime_offset = self.current_config.datetime_offset * -1

        if self.checkbox_use_current_datetime.value:
            datetime_var = self.current_config.get_str_datetime_now()
        else:
            datetime_var = self.textbox_note_date.value.strip()

        self.database_user_note_dates[current_note_number] = datetime_var
        self.textbox_note_date.value = datetime_var

        utc_0_datetime_user = str(self.adjust_datetime(datetime_var, reverse_datetime_offset))
        sql_note = self.sterilize_notes(self.textbox_current_note.value)

        try:
            on_note_number = int(self.textbox_on_number_notes.value.strip()) - 1
            self.database_notes[on_note_number] = self.undue_sterilize_notes(sql_note)

            if sql_note == "":
                guizero.warn("Empty Note", "Cannot add a blank Note")
            else:
                command = self.network_send_commands.update_sql_note
                network_timeout = self.current_config.network_timeout_data

                sensor_command = sensor_commands.CreateSensorNetworkCommand(self.selected_ip, network_timeout, command)
                sensor_command.command_data = utc_0_datetime_current + \
                                              self.network_send_commands.command_data_separator + \
                                              utc_0_datetime_user + \
                                              self.network_send_commands.command_data_separator + \
                                              sql_note
                sensor_commands.put_command(sensor_command)
        except Exception as error:
            guizero.warn("Invalid Note Number", str(error))

    def _database_update_note_button(self):
        current_note_number = int(self.textbox_on_number_notes.value.strip()) - 1
        datetime_offset = self.current_config.datetime_offset

        user_note_datetime = self.textbox_note_date.value.strip()
        try:
            if self.checkbox_use_current_datetime.value:
                current_datetime = self.current_config.get_str_datetime_now()
                user_note_datetime_utc = str(self.adjust_datetime(current_datetime, datetime_offset * -1))
            else:
                user_note_datetime_utc = self.adjust_datetime(user_note_datetime, datetime_offset * -1)
        except Exception as error:
            app_logger.app_logger.error("Unable to convert current Note's user set DateTime: " + str(error))
            user_note_datetime_utc = user_note_datetime

        current_note_datetime_utc = self.database_notes_dates[current_note_number]
        self.database_user_note_dates[current_note_number] = user_note_datetime

        sql_note = self.sterilize_notes(self.textbox_current_note.value)

        if sql_note == "":
            guizero.warn("Empty Note", "Cannot add a blank Note")
        else:
            sql_query = "UPDATE " + self.sql_column_names.sql_other_table + \
                        " SET " + self.sql_column_names.other_notes + \
                        " = '" + sql_note + \
                        "', " + self.sql_column_names.other_user_datetime + \
                        " = '" + user_note_datetime_utc + \
                        "' WHERE " + self.sql_column_names.date_time + \
                        " = '" + current_note_datetime_utc + "'"

            self._sql_execute(sql_query)
            self._database_change_to_note_plus(0)

    def _sensor_change_to_note_plus(self, plus):
        self.textbox_total_notes.value = str(len(self.database_notes))

        if len(self.database_notes) < 1:
            self.textbox_current_note.enable()
            self.textbox_current_note.value = self.text_variables_generic.no_notes_found
            self._disable_notes_window_functions()
        else:
            try:
                current_note = int(self.textbox_on_number_notes.value)
                if current_note + plus > int(len(self.database_notes)):
                    self.textbox_on_number_notes.value = "1"
                    current_note = 1
                elif current_note + plus < 1:
                    self.textbox_on_number_notes.value = str(len(self.database_notes))
                    current_note = len(self.database_notes)
                else:
                    current_note += plus
            except Exception as error:
                app_logger.app_logger.error("Unable to convert current Note count: " + str(error))
                current_note = 1

            self.textbox_on_number_notes.value = str(current_note)
            self.textbox_current_note.value = str(self.database_notes[(current_note - 1)])

            self.textbox_note_date.value = str(self.database_user_note_dates[(current_note - 1)])

    def _database_change_to_note_plus(self, plus):
        database_notes = self.undue_sterilize_notes(self.get_database_notes())

        if len(database_notes) < 1:
            connected_to_db = self.text_connected_to.value

            self.textbox_current_note.enable()
            self.textbox_current_note.value = self.text_variables_generic.no_notes_found
            self.textbox_on_number_notes.enable()
            self.textbox_on_number_notes.value = "1"
            self._disable_notes_window_functions()
            self.text_connected_to.value = connected_to_db
            self.checkbox_use_current_datetime.enable()
            self.textbox_current_note.enable()
            self.button_new_note.enable()
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

            self.textbox_on_number_notes.enable()
            self.textbox_on_number_notes.value = str(current_note)
            self.textbox_current_note.value = str(database_notes[(current_note - 1)])

            self.textbox_note_date.value = str(self.database_user_note_dates[(current_note - 1)])

        self.textbox_total_notes.value = str(len(database_notes))

    def _sql_execute_get_data(self, sql_query):
        try:
            database_connection = sqlite3.connect(self.db_location)
            sqlite_database = database_connection.cursor()
            sqlite_database.execute(sql_query)
            sql_column_data = sqlite_database.fetchall()
            sqlite_database.close()
            database_connection.close()
        except Exception as error:
            app_logger.app_logger.error("SQL Execute Get Data Error: " + str(error))
            sql_column_data = "Bad SQL Execute"

        return sql_column_data

    def _sql_execute(self, sql_query):
        try:
            database_connection = sqlite3.connect(self.db_location)
            sqlite_database = database_connection.cursor()
            sqlite_database.execute(sql_query)
            database_connection.commit()
            sqlite_database.close()
            database_connection.close()
        except Exception as error:
            app_logger.app_logger.error("SQL Execute Error: " + str(error))

    def _disable_notes_window_functions(self):
        self.text_connected_to.value = self.text_variables_database.text_connected_to
        self.selected_ip = ""
        self.textbox_on_number_notes.value = "0"
        self.textbox_note_date.value = self.text_variables_generic.textbox_note_date
        self.textbox_total_notes.value = "0"
        self.textbox_current_note.value = ""
        self.checkbox_use_current_datetime.disable()
        self.textbox_on_number_notes.disable()
        self.textbox_note_date.disable()
        self.textbox_total_notes.disable()
        self.textbox_current_note.disable()

        self.button_back_note.disable()
        self.button_next_note.disable()
        self.button_new_note.disable()
        self.button_delete_note.disable()
        self.button_update_note.disable()

    @staticmethod
    def adjust_datetime(var_datetime, datetime_offset):
        """
        Adjusts the provided datetime by the provided hour offset and returns the result as a string.
        """
        try:
            new_var_datetime = datetime.strptime(var_datetime, "%Y-%m-%d %H:%M:%S")
            new_time = new_var_datetime + timedelta(hours=datetime_offset)
        except Exception as error:
            app_logger.app_logger.debug("Unable to Convert Interval datetime string to datetime format - " + str(error))
            new_time = var_datetime

        app_logger.app_logger.debug("Adjusted datetime: " + str(new_time))
        return str(new_time)

    def _reset_datetime(self):
        """ Reset note Date & Time stamp. """
        if self.checkbox_use_current_datetime.value:
            self.textbox_note_date.value = self.current_config.get_str_datetime_now()
            self.textbox_note_date.disable()
        else:
            self.textbox_note_date.enable()

    def _no_sql_notes(self):
        self.textbox_total_notes.value = "0"
        self.checkbox_use_current_datetime.enable()
        self.checkbox_use_current_datetime.value = True
        self.textbox_current_note.enable()
        self.textbox_on_number_notes.disable()
        self.textbox_current_note.value = self.text_variables_generic.no_notes_found
        self._reset_datetime()
        self.textbox_on_number_notes.value = "1"

        self.button_next_note.disable()
        self.button_back_note.disable()
        self.button_delete_note.disable()
        self.button_new_note.enable()
        self.button_update_note.disable()

    def _change_for_sensor(self):
        self.window.title = self.text_variables_sensor.window_title
        self.text_connected_to.value = self.text_variables_sensor.text_connected_to
        self.button_connect.text = self.text_variables_sensor.button_connect
        self.button_connect.update_command(self._connect_to_sensor)
        self.button_new_note.update_command(self._sensor_add_note_button)
        self.button_delete_note.update_command(self._sensor_delete_button)
        self.button_update_note.update_command(self._sensor_update_note_button)

    def sterilize_notes(self, notes):
        if type(notes) == str:
            notes = notes.strip()
            notes = notes.replace(",", self.text_variables_generic.replace_comma)
            notes = notes.replace("\n", self.text_variables_generic.replace_new_line)
            notes = notes.replace("\\", self.text_variables_generic.replace_back_slash)
        else:
            count = 0
            for note in notes:
                note = note.strip()
                note = note.replace(",", self.text_variables_generic.replace_comma)
                note = note.replace("\n", self.text_variables_generic.replace_new_line)
                note = note.replace("\\", self.text_variables_generic.replace_back_slash)
                notes[count] = note
                count += 1

        return notes

    def undue_sterilize_notes(self, notes):
        if type(notes) == str:
            notes = notes.strip()
            notes = notes.replace(self.text_variables_generic.replace_comma, ",")
            notes = notes.replace(self.text_variables_generic.replace_new_line, "\n")
            notes = notes.replace(self.text_variables_generic.replace_back_slash, "\\")
        else:
            count = 0
            for note in notes:
                note = note.strip()
                note = note.replace(self.text_variables_generic.replace_comma, ",")
                note = note.replace(self.text_variables_generic.replace_new_line, "\n")
                note = note.replace(self.text_variables_generic.replace_back_slash, "\\")
                notes[count] = note
                count += 1

        return notes
