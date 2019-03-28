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
from guizero import Window, PushButton, Text, TextBox, yesno, info, CheckBox, warn
from app_modules.app_graph import CreateSQLColumnNames
from app_modules.app_useful import no_ip_selected_message
from app_modules.app_sensor_commands import CreateNetworkSendCommands, CreateSensorNetworkCommand, \
    CreateNetworkGetCommands, put_command, get_data
from datetime import datetime, timedelta


class CreateSensorNotesWindow:
    """ Creates a GUI window for generating database information. """

    def __init__(self, app, ip_selection, current_config):
        self.current_config = current_config
        self.ip_selection = ip_selection
        self.db_location = ""
        self.database_notes = []
        self.database_note_dates = []

        self.sql_column_names = CreateSQLColumnNames()
        self.network_send_commands = CreateNetworkSendCommands()
        self.sensor_get_commands = CreateNetworkGetCommands()

        self.window = Window(app,
                             title="Online Notes Editor",
                             width=585,
                             height=575,
                             layout="grid",
                             visible=False)

        self.checkbox_enable_datetime_change = CheckBox(self.window,
                                                        text="Use current Date & Time",
                                                        command=self._reset_datetime,
                                                        grid=[4, 1, 5, 1],
                                                        align="left")

        self.button_open_database = PushButton(self.window,
                                               text="Connect to Sensor",
                                               command=self._connect_to_sensor,
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

        self.textbox_note_date = TextBox(self.window,
                                         text="YYYY-MM-DD hh:mm:ss",
                                         grid=[4, 5],
                                         width=21,
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
                                            text="Please Connect to a Sensor to view Notes",
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
                                             text="Delete Note\nfrom\nSensor",
                                             command=self._delete_button,
                                             grid=[4, 12],
                                             align="left")

        self.button_update_note = PushButton(self.window,
                                             text="Update\nCurrent\nNote",
                                             command=self._save_note_button,
                                             grid=[6, 12],
                                             align="left")

        # Window Tweaks
        self._disable_notes_window_functions()
        self.checkbox_enable_datetime_change.value = True
        self.textbox_current_note.bg = "black"
        self.textbox_current_note.text_color = "white"
        self.textbox_current_note.tk.config(insertbackground="red")

    def _connect_to_sensor(self):
        """ Prompts for Database to open and opens it. """
        ip_list = self.ip_selection.get_verified_ip_list()

        if len(ip_list) > 0:
            command = self.sensor_get_commands.database_notes
            network_timeout = self.current_config.network_timeout_data
            sensor_command = CreateSensorNetworkCommand(ip_list[0], network_timeout, command)

            self.database_notes = get_data(sensor_command).split(",")
            sensor_command.command = self.sensor_get_commands.database_note_dates
            self.database_notes_dates = get_data(sensor_command).split(",")

            count = 0
            for date in self.database_notes_dates:
                new_date = self.adjust_datetime(str(date), self.current_config.datetime_offset)
                self.database_notes_dates[count] = new_date
                count += 1

            if len(self.database_notes) > 0:
                count = 0
                for entry in self.database_notes:
                    self.database_notes[count] = entry.replace("[replaced_comma]", ",")
                    count += 1

                count = 0
                for entry in self.database_note_dates:
                    self.database_note_dates[count] = entry.replace("[replaced_comma]", ",")
                    count += 1

                self.textbox_number_of_notes_total.value = str(len(self.database_notes))
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
            else:
                self.textbox_current_note.enable()
                self.textbox_current_note.value = "No Notes Found"
                self._disable_notes_window_functions()

    def _next_button(self):
        self._change_to_note_plus(1)

    def _back_button(self):
        self._change_to_note_plus(-1)

    def _add_note_button(self):
        """ Send the note to selected sensor. """
        if self.textbox_current_note.value.strip() == "":
            warn("Empty Note", "Cannot add a blank Note")
        else:
            if self.checkbox_enable_datetime_change.value:
                self._reset_datetime()

            ip_list = self.ip_selection.get_verified_ip_list()

            if len(ip_list) > 0:
                datetime_var = self.textbox_note_date.value
                utc_0_datetime = self.adjust_datetime(datetime_var, self.current_config.datetime_offset * -1)
                command = self.network_send_commands.put_sql_note
                network_timeout = self.current_config.network_timeout_data

                sensor_command = CreateSensorNetworkCommand(ip_list[0], network_timeout, command)
                sensor_command.command_data = utc_0_datetime + ".000" + self.textbox_current_note.value
                put_command(sensor_command)

                info("Note Inserted into Sensors " + ip_list[0], "Inserted with DateTime: " + datetime_var)
                app_logger.sensor_logger.info("Inserted note into sensors " + str(ip_list[0]) +
                                              " with DateTime " + datetime_var)
                self._connect_to_sensor()
            else:
                no_ip_selected_message()

    def _delete_button(self):
        ip_list = self.ip_selection.get_verified_ip_list()

        if len(ip_list) > 0:
            if yesno("Delete Note", "Are you sure you want to Delete Note " +
                                    self.textbox_on_number_notes.value + " out of " +
                                    self.textbox_number_of_notes_total.value + "?"):
                datetime_var = self.textbox_note_date.value
                utc_0_datetime = self.adjust_datetime(datetime_var, self.current_config.datetime_offset * -1)
                command = self.network_send_commands.delete_sql_note
                network_timeout = self.current_config.network_timeout_data

                sensor_command = CreateSensorNetworkCommand(ip_list[0], network_timeout, command)
                sensor_command.command_data = utc_0_datetime + ".000"
                put_command(sensor_command)

                info("Note Deleted from sensor " + ip_list[0], "Deleted note with DateTime: " + datetime_var)
                app_logger.sensor_logger.info("Deleted note from sensor " + str(ip_list[0]) +
                                              " with DateTime " + datetime_var)
                self._connect_to_sensor()
        else:
            no_ip_selected_message()

    def _save_note_button(self):
        # note_datetime = str(self.textbox_note_date.value).strip()
        pass

    def _change_to_note_plus(self, plus):
        self.textbox_number_of_notes_total.value = str(len(self.database_notes))

        if len(self.database_notes) < 1:
            self.textbox_current_note.enable()
            self.textbox_current_note.value = "No Notes Found"
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
            sql_column_data = []

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
        self.checkbox_enable_datetime_change.disable()
        self.button_back_note.disable()
        self.textbox_on_number_notes.value = "0"
        self.textbox_on_number_notes.disable()
        self.textbox_note_date.value = "YYYY-MM-DD hh:mm:ss"
        self.textbox_note_date.disable()
        self.textbox_number_of_notes_total.disable()
        self.button_next_note.disable()
        self.textbox_current_note.value = ""
        self.textbox_current_note.disable()

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
