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
import app_modules.app_logger as app_logger
from tkinter import filedialog
from guizero import Window, PushButton, Text, TextBox, CheckBox, yesno, error as guierror, warn, info
from app_modules.app_graph import CreateSQLColumnNames
from datetime import datetime, timedelta
from app_modules.app_useful import no_ip_selected_message
from app_modules.app_sensor_commands import CreateNetworkSendCommands, CreateSensorNetworkCommand, \
    CreateNetworkGetCommands, put_command, get_data


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
        self.sensor_return_no_notes = "No Notes"


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
        self.database_note_dates = []

        self.text_variables_generic = CreateGenericNoteVariables()
        self.text_variables_sensor = CreateSensorNoteVariables()
        self.text_variables_database = CreateDatabaseNoteVariables()

        self.sql_column_names = CreateSQLColumnNames()
        self.network_send_commands = CreateNetworkSendCommands()
        self.sensor_get_commands = CreateNetworkGetCommands()

        self.window = Window(app,
                             title=self.text_variables_database.window_title,
                             width=585,
                             height=555,
                             layout="grid",
                             visible=False)

        self.text_connected_to = Text(self.window,
                                      text=self.text_variables_database.text_connected_to,
                                      color="red",
                                      size=8,
                                      grid=[1, 1, 3, 1],
                                      align="left")

        self.checkbox_enable_datetime_change = CheckBox(self.window,
                                                        text=self.text_variables_generic.checkbox_enable_datetime,
                                                        command=self._reset_datetime,
                                                        grid=[4, 1, 5, 1],
                                                        align="left")

        self.button_connect = PushButton(self.window,
                                         text=self.text_variables_database.button_connect,
                                         command=self._open_database,
                                         grid=[1, 5],
                                         align="left")

        self.button_back_note = PushButton(self.window,
                                           text="Back",
                                           command=self._back_button,
                                           grid=[2, 5],
                                           align="left")

        self.text_note_current = Text(self.window,
                                      text=self.text_variables_generic.text_note_current,
                                      color="blue",
                                      grid=[3, 5],
                                      align="top")

        self.textbox_on_number_notes = TextBox(self.window,
                                               text="0",
                                               width=5,
                                               grid=[3, 5],
                                               align="bottom")

        self.text_date_label1 = Text(self.window,
                                     text=self.text_variables_generic.text_date_label1,
                                     color="blue",
                                     grid=[4, 5],
                                     align="top")

        self.textbox_note_date = TextBox(self.window,
                                         text=self.text_variables_generic.textbox_note_date,
                                         grid=[4, 5],
                                         width=23,
                                         align="bottom")

        self.text_total_notes_label = Text(self.window,
                                           text=self.text_variables_generic.text_total_notes_label,
                                           color="blue",
                                           grid=[5, 5],
                                           align="top")

        self.textbox_total_notes = TextBox(self.window,
                                           text="0",
                                           width=5,
                                           grid=[5, 5],
                                           align="bottom")

        self.button_next_note = PushButton(self.window,
                                           text=self.text_variables_generic.button_next_note,
                                           command=self._next_button,
                                           grid=[6, 5],
                                           align="left")

        self.textbox_current_note = TextBox(self.window,
                                            text=self.text_variables_database.textbox_current_note,
                                            width=70,
                                            height=25,
                                            grid=[1, 10, 6, 1],
                                            multiline=True,
                                            scrollbar=True,
                                            align="left")

        self.button_new_note = PushButton(self.window,
                                          text=self.text_variables_generic.button_new_note,
                                          command=self._database_add_note_button,
                                          grid=[1, 12],
                                          align="left")

        self.button_delete_note = PushButton(self.window,
                                             text=self.text_variables_generic.button_delete_note,
                                             command=self._database_delete_button,
                                             grid=[4, 12],
                                             align="left")

        self.button_update_note = PushButton(self.window,
                                             text=self.text_variables_generic.button_update_note,
                                             command=self._database_update_note_button,
                                             grid=[6, 12],
                                             align="left")

        # Window Tweaks
        self.window.tk.resizable(False, False)
        self._disable_notes_window_functions()
        self.checkbox_enable_datetime_change.value = True
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
            sensor_command = CreateSensorNetworkCommand(self.selected_ip, network_timeout, command)

            self.database_notes = get_data(sensor_command).split(",")

            sensor_command.command = self.sensor_get_commands.database_note_dates
            self.database_notes_dates = get_data(sensor_command).split(",")

            if str(self.database_notes)[2:-2] == self.text_variables_generic.sensor_return_no_notes:
                self._no_sql_notes()
            else:
                count = 0
                for date in self.database_notes_dates:
                    new_date = self.adjust_datetime(str(date), self.current_config.datetime_offset)
                    self.database_notes_dates[count] = new_date
                    count += 1

                if len(self.database_notes) > 0:
                    self.database_notes = self.undue_sterilize_notes(self.database_notes)

                    self.textbox_total_notes.value = str(len(self.database_notes))
                    self.checkbox_enable_datetime_change.enable()
                    self.textbox_current_note.enable()
                    self.textbox_on_number_notes.enable()
                    self.textbox_current_note.value = str(self.database_notes[0])
                    self.textbox_note_date.value = str(self.database_notes_dates[0])
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

            no_ip_selected_message()

    def _open_database(self):
        """ Prompts for Database to open and opens it. """
        unchecked_db_location = filedialog.askopenfilename()
        if str(unchecked_db_location) != "()" and unchecked_db_location != "":
            self.db_location = unchecked_db_location
            database_notes = self.get_database_notes()
            database_notes_dates = self.get_database_notes_dates()

            if str(database_notes) == "Bad SQL Execute":
                self._disable_notes_window_functions()
            else:
                self.textbox_current_note.enable()
                if len(database_notes) > 0:
                    self.text_connected_to.value = self.text_variables_database.text_connected_to[:-2] + self.db_location.split("/")[-1]
                    self.database_notes = self.undue_sterilize_notes(database_notes)

                    self.textbox_on_number_notes.enable()
                    self.textbox_current_note.value = str(database_notes[0])
                    self.textbox_note_date.value = str(database_notes_dates[0]).strip()
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
                self.checkbox_enable_datetime_change.enable()
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
            count = 0
            for date in database_notes_dates:
                new_date = self.adjust_datetime(str(date)[2:-7], self.current_config.datetime_offset)
                database_notes_dates[count] = new_date
                count += 1

            return database_notes_dates

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
            warn("Empty Note", "Cannot add a blank Note")
        else:
            if self.checkbox_enable_datetime_change.value:
                self._reset_datetime()

            datetime_var = self.textbox_note_date.value
            utc_0_datetime = self.adjust_datetime(datetime_var, self.current_config.datetime_offset * -1)
            command = self.network_send_commands.put_sql_note
            network_timeout = self.current_config.network_timeout_data

            sensor_command = CreateSensorNetworkCommand(self.selected_ip, network_timeout, command)
            sensor_command.command_data = utc_0_datetime + ".000" + self.sterilize_notes(self.textbox_current_note.value)
            put_command(sensor_command)

            info("Note Inserted into Sensors " + self.selected_ip, "Inserted with DateTime: " + datetime_var)
            app_logger.sensor_logger.info("Inserted note into sensors " + str(self.selected_ip) +
                                          " with DateTime " + datetime_var)
            self._connect_to_sensor()

    def _database_add_note_button(self):
        sql_note_datetime = self.current_config.get_str_datetime_now()
        utc_0_datetime = str(self.adjust_datetime(sql_note_datetime, self.current_config.datetime_offset * -1)) + ".000"
        sql_note = self.sterilize_notes(self.textbox_current_note.value)

        if sql_note == "":
            warn("Empty Note", "Cannot add a blank Note")
        else:
            self.button_delete_note.enable()
            self.button_update_note.enable()
            self.button_back_note.enable()
            self.button_next_note.enable()
            sql_query = "INSERT OR IGNORE INTO " + self.sql_column_names.sql_other_table + " (" + \
                        self.sql_column_names.date_time + "," + self.sql_column_names.other_notes + \
                        ") VALUES ('" + utc_0_datetime + "','" + sql_note + "')"

            self._sql_execute(sql_query)
            self._database_change_to_note_plus(0)

    def _sensor_delete_button(self):
        if yesno("Delete Note", "Are you sure you want to Delete Note " +
                                self.textbox_on_number_notes.value + " out of " +
                                self.textbox_total_notes.value + "?"):
            datetime_var = self.textbox_note_date.value
            utc_0_datetime = self.adjust_datetime(datetime_var, self.current_config.datetime_offset * -1)
            command = self.network_send_commands.delete_sql_note
            network_timeout = self.current_config.network_timeout_data

            sensor_command = CreateSensorNetworkCommand(self.selected_ip, network_timeout, command)
            sensor_command.command_data = utc_0_datetime + ".000"
            put_command(sensor_command)

            info("Note Deleted from sensor " + self.selected_ip, "Deleted note with DateTime: " + datetime_var)
            app_logger.sensor_logger.info("Deleted note from sensor " + self.selected_ip +
                                          " with DateTime " + datetime_var)
            self._connect_to_sensor()

    def _database_delete_button(self):
        try:
            if int(self.textbox_on_number_notes.value) < 1 or \
                    int(self.textbox_on_number_notes.value) > len(self.get_database_notes_dates()):

                app_logger.app_logger.warning("Error: Current Note Number is more or less then total")

                guierror("Invalid Current Note Number", (" '" + self.textbox_on_number_notes.value +
                                                         "' is a invalid option\nPlease enter a number between 1 and " +
                                                         str(len(self.get_database_notes_dates()))))
                self._database_change_to_note_plus(0)

            elif yesno("Delete Note", "Are you sure you want to Delete Note " +
                                      self.textbox_on_number_notes.value + " out of " +
                                      self.textbox_total_notes.value + "?"):

                note_date_times = self.get_database_notes_dates()
                datetime_var = self.adjust_datetime(note_date_times[int(self.textbox_on_number_notes.value) - 1],
                                                    self.current_config.datetime_offset * -1) + ".000"

                sql_query = "DELETE FROM " + \
                            str(self.sql_column_names.sql_other_table) + \
                            " WHERE " + \
                            str(self.sql_column_names.date_time) + \
                            " = '" + datetime_var + "'"

                self._sql_execute(sql_query)
                self._database_change_to_note_plus(0)
        except Exception as error:
            app_logger.app_logger.error("Invalid Current Note number: " + str(error))
            guierror("Invalid Current Note Number", (" '" + self.textbox_on_number_notes.value +
                                                     "' is a invalid option\nPlease enter a number between 1 and " +
                                                     str(len(self.get_database_notes_dates()))))
            self._database_change_to_note_plus(0)

    def _sensor_update_note_button(self):
        sql_note_datetime = self.textbox_note_date.value.strip()
        utc_0_datetime = str(self.adjust_datetime(sql_note_datetime, self.current_config.datetime_offset * -1)) + ".000"
        sql_note = self.sterilize_notes(self.textbox_current_note.value)
        try:
            on_note_number = int(self.textbox_on_number_notes.value.strip()) - 1
            self.database_notes[on_note_number] = self.undue_sterilize_notes(sql_note)

            if sql_note == "":
                warn("Empty Note", "Cannot add a blank Note")
            else:
                command = self.network_send_commands.update_sql_note
                network_timeout = self.current_config.network_timeout_data

                sensor_command = CreateSensorNetworkCommand(self.selected_ip, network_timeout, command)
                sensor_command.command_data = utc_0_datetime + sql_note
                put_command(sensor_command)
        except Exception as error:
            warn("Invalid Note Number", str(error))

    def _database_update_note_button(self):
        sql_note_datetime = self.textbox_note_date.value.strip()
        utc_0_datetime = str(self.adjust_datetime(sql_note_datetime, self.current_config.datetime_offset * -1)) + ".000"
        sql_note = self.sterilize_notes(self.textbox_current_note.value)

        if sql_note == "":
            warn("Empty Note", "Cannot add a blank Note")
        else:
            sql_query = "UPDATE " + self.sql_column_names.sql_other_table + \
                        " SET " + self.sql_column_names.other_notes + \
                        " = '" + sql_note + "' " + \
                        " WHERE " + self.sql_column_names.date_time + \
                        " = '" + utc_0_datetime + "'"

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

            self.textbox_note_date.value = str(self.database_notes_dates[(current_note - 1)])

    def _database_change_to_note_plus(self, plus):
        database_notes = self.undue_sterilize_notes(self.get_database_notes())
        database_notes_dates = self.get_database_notes_dates()

        if len(database_notes) < 1:
            self.textbox_current_note.enable()
            self.textbox_current_note.value = self.text_variables_generic.no_notes_found
            self.textbox_on_number_notes.enable()
            self.textbox_on_number_notes.value = "1"
            self._disable_notes_window_functions()
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

            self.textbox_note_date.value = str(database_notes_dates[(current_note - 1)])

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
        self.selected_ip = ""
        self.textbox_on_number_notes.value = "0"
        self.textbox_note_date.value = self.text_variables_generic.textbox_note_date
        self.textbox_total_notes.value = "0"
        self.textbox_current_note.value = ""
        self.checkbox_enable_datetime_change.disable()
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
        if self.checkbox_enable_datetime_change.value:
            self.textbox_note_date.value = self.current_config.get_str_datetime_now()
            self.textbox_note_date.disable()
        else:
            self.textbox_note_date.enable()

    def _no_sql_notes(self):
        self.textbox_total_notes.value = "0"
        self.checkbox_enable_datetime_change.enable()
        self.checkbox_enable_datetime_change.value = True
        self.textbox_current_note.enable()
        self.textbox_on_number_notes.disable()
        self.textbox_current_note.value = self.text_variables_generic.no_notes_found
        self._reset_datetime()
        self.textbox_on_number_notes.value = "1"

        self.button_next_note.disable()
        self.button_back_note.disable()
        self.button_delete_note.disable()
        self.button_new_note.enable()

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
