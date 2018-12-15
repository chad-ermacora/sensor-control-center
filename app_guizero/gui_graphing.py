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

import app_config
import app_graph
import app_logger


class CreateGraphingWindow:
    """ Creates a GUI window for creating Plotly or Live graphs. """

    def __init__(self, app, ip_selection, current_config):
        self.ip_selection = ip_selection
        self.current_config = current_config
        self.readable_column_names = app_graph.CreateSQLColumnsReadable()
        self.sql_columns = app_graph.CreateSQLColumnNames()

        self.window = Window(app,
                             title="Graphing",
                             width=275,
                             height=545,
                             layout="grid",
                             visible=False)

        self.text_sensor_type_name = Text(self.window,
                                          text="Data Source",
                                          color='blue',
                                          grid=[1, 1, 2, 1],
                                          align="top")

        self.radio_sensor_type = ButtonGroup(self.window,
                                             options=["Live Sensor", "SQL Database"],
                                             horizontal="True",
                                             command=self._radio_selection,
                                             grid=[1, 2, 2, 1],
                                             align="top")

        self.text_sensor_type_name = Text(self.window,
                                          text="Graph Options",
                                          color='blue',
                                          grid=[1, 4, 2, 1],
                                          align="top")

        self.text_space2 = Text(self.window,
                                text="YYYY-MM-DD HH:MM:SS",
                                size=7,
                                color='#CB0000',
                                grid=[2, 5, 2, 1],
                                align="left")

        self.text_start = Text(self.window,
                               text="Start Date & Time: ",
                               color='green',
                               grid=[1, 6],
                               align="left")

        self.textbox_start = TextBox(self.window,
                                     text="",
                                     width=20,
                                     grid=[2, 6],
                                     align="left")

        self.text_end = Text(self.window,
                             text="End Date & Time:",
                             color='green',
                             grid=[1, 7],
                             align="left")

        self.textbox_end = TextBox(self.window,
                                   text="",
                                   width=20,
                                   grid=[2, 7],
                                   align="left")

        self.text_sql_skip = Text(self.window,
                                  text="Add one every:  ",
                                  color='green',
                                  grid=[1, 8],
                                  align="right")

        self.textbox_sql_skip = TextBox(self.window,
                                        text="",
                                        width=10,
                                        grid=[2, 8],
                                        align="left")

        self.text_sql_skip2 = Text(self.window,
                                   text="entries    ",
                                   color='green',
                                   grid=[2, 8],
                                   align="right")

        self.text_temperature_offset = Text(self.window,
                                            text="Env Temp Offset:",
                                            color='green',
                                            grid=[1, 9],
                                            align="left")

        self.textbox_temperature_offset = TextBox(self.window,
                                                  text="",
                                                  width=5,
                                                  grid=[2, 9],
                                                  align="left")

        self.checkbox_default_offset = CheckBox(self.window,
                                                text="Use Sensor\nDefault",
                                                command=self._click_checkbox_offset,
                                                grid=[2, 9],
                                                align="right")

        self.text_refresh_time = Text(self.window,
                                      text="Live refresh (Sec):",
                                      color='green',
                                      grid=[1, 10],
                                      align="left")

        self.textbox_refresh_time = TextBox(self.window,
                                            text="2",
                                            width=5,
                                            grid=[2, 10],
                                            align="left")

        self.text_space3 = Text(self.window,
                                text=" ",
                                grid=[1, 11],
                                align="right")

        self.checkbox_master = CheckBox(self.window,
                                        text="All",
                                        command=self._master_checkbox,
                                        grid=[1, 15],
                                        align="left")

        self.text_column_selection = Text(self.window,
                                          text="Interval Sensors",
                                          color='blue',
                                          grid=[1, 15, 2, 1],
                                          align="top")

        self.checkbox_up_time = CheckBox(self.window,
                                         text=self.readable_column_names.system_uptime,
                                         command=self._disable_other_checkboxes,
                                         args=[self.sql_columns.system_uptime],
                                         grid=[1, 16],
                                         align="left")

        self.checkbox_cpu_temp = CheckBox(self.window,
                                          text=self.readable_column_names.cpu_temp,
                                          command=self._disable_other_checkboxes,
                                          args=[self.sql_columns.cpu_temp],
                                          grid=[1, 17],
                                          align="left")

        self.checkbox_temperature = CheckBox(self.window,
                                             text=self.readable_column_names.environmental_temp,
                                             command=self._disable_other_checkboxes,
                                             args=[self.sql_columns.environmental_temp],
                                             grid=[1, 18],
                                             align="left")

        self.checkbox_pressure = CheckBox(self.window,
                                          text=self.readable_column_names.pressure,
                                          command=self._disable_other_checkboxes,
                                          args=[self.sql_columns.pressure],
                                          grid=[1, 19],
                                          align="left")

        self.checkbox_humidity = CheckBox(self.window,
                                          text=self.readable_column_names.humidity,
                                          command=self._disable_other_checkboxes,
                                          args=[self.sql_columns.humidity],
                                          grid=[2, 16],
                                          align="left")

        self.checkbox_lumen = CheckBox(self.window,
                                       text=self.readable_column_names.lumen,
                                       command=self._disable_other_checkboxes,
                                       args=[self.sql_columns.lumen],
                                       grid=[2, 17],
                                       align="left")

        self.checkbox_colour = CheckBox(self.window,
                                        text=self.readable_column_names.rgb,
                                        command=self._disable_other_checkboxes,
                                        args=[self.sql_columns.rgb],
                                        grid=[2, 18],
                                        align="left")

        self.text_column_selection2 = Text(self.window,
                                           text="Trigger Sensors",
                                           color='blue',
                                           grid=[1, 24, 2, 1],
                                           align="bottom")

        self.checkbox_acc = CheckBox(self.window,
                                     text=self.readable_column_names.accelerometer_xyz,
                                     command=self._disable_other_checkboxes,
                                     args=[self.sql_columns.accelerometer_xyz],
                                     grid=[1, 25],
                                     align="left")

        self.checkbox_mag = CheckBox(self.window,
                                     text=self.readable_column_names.magnetometer_xyz,
                                     command=self._disable_other_checkboxes,
                                     args=[self.sql_columns.magnetometer_xyz],
                                     grid=[2, 25],
                                     align="left")

        self.checkbox_gyro = CheckBox(self.window,
                                      text=self.readable_column_names.gyroscope_xyz,
                                      command=self._disable_other_checkboxes,
                                      args=[self.sql_columns.gyroscope_xyz],
                                      grid=[1, 26],
                                      align="left")

        self.text_space4 = Text(self.window,
                                text=" ",
                                grid=[1, 35],
                                align="right")

        self.button_database = PushButton(self.window,
                                          text="Open & Graph\nDatabase",
                                          command=self.plotly_button,
                                          grid=[1, 36, 2, 1],
                                          align="left")

        self.button_live = PushButton(self.window,
                                      text="Start Live Graph",
                                      command=self.live_button,
                                      grid=[2, 36],
                                      align="left")

        # Window Tweaks
        self.window.tk.resizable(False, False)
        self.checkbox_default_offset.value = 1
        self._set_config()
        self._radio_selection()
        self._click_checkbox_offset()
        self.checkbox_up_time.value = 0
        self.checkbox_temperature.value = 0
        self.checkbox_pressure.value = 0
        self.checkbox_humidity.value = 0
        self.checkbox_lumen.value = 0
        self.checkbox_colour.value = 0

    def _master_checkbox(self):
        """ Checks all sensor selection checkboxes. """
        if self.checkbox_master.value:
            self._enable_all_checkboxes()
        else:
            self._disable_all_checkboxes()

    def _click_checkbox_offset(self):
        """ Enable or disable custom Env temperature offset for a graph. """
        if self.checkbox_default_offset.value:
            self.textbox_temperature_offset.disable()
            self.current_config.enable_custom_temp_offset = False
        else:
            self.textbox_temperature_offset.enable()
            self.current_config.enable_custom_temp_offset = True
            try:
                self.current_config.temperature_offset = float(self.textbox_temperature_offset.value)
            except Exception as error:
                self.current_config.temperature_offset = 0
                warn("Invalid Temperature Offset", "Please check and correct 'Env Temp Offset'")
                app_logger.app_logger.warning("Invalid Graph 'Env Temp Offset': " + str(error))

    def _set_config(self):
        """ Sets the programs Configuration to the provided settings. """

        self.textbox_start.value = self.current_config.graph_start
        self.textbox_end.value = self.current_config.graph_end
        self.textbox_sql_skip.value = self.current_config.sql_queries_skip
        self.textbox_temperature_offset.value = self.current_config.temperature_offset
        self.textbox_refresh_time.value = self.current_config.live_refresh

    def _radio_selection(self):
        """ Enables or disables the Graph Window selections, based on graph type selected. """
        self._enable_all_for_live()
        if self.radio_sensor_type.get() == "SQL Database":
            self.button_live.disable()
            self.textbox_refresh_time.disable()

            self.textbox_start.enable()
            self.textbox_end.enable()
            self.textbox_sql_skip.enable()

            if not self.checkbox_default_offset.value:
                self.textbox_temperature_offset.enable()

            self.checkbox_master.enable()
            self.checkbox_master.value = 1
            self.checkbox_up_time.enable()
            self.checkbox_up_time.value = 1
            self.checkbox_cpu_temp.enable()
            self.checkbox_cpu_temp.value = 1
            self.checkbox_temperature.enable()
            self.checkbox_temperature.value = 1
            self.checkbox_pressure.enable()
            self.checkbox_pressure.value = 1
            self.checkbox_humidity.enable()
            self.checkbox_humidity.value = 1
            self.checkbox_lumen.enable()
            self.checkbox_lumen.value = 1
            self.checkbox_colour.enable()
            self.checkbox_colour.value = 1
            self.checkbox_acc.enable()
            self.checkbox_acc.value = 1
            self.checkbox_mag.enable()
            self.checkbox_mag.value = 1
            self.checkbox_gyro.enable()
            self.checkbox_gyro.value = 1

            self.button_database.enable()

        if self.radio_sensor_type.get() == "Live Sensor":
            self.button_database.disable()
            self.textbox_sql_skip.disable()
            self.textbox_start.disable()
            self.textbox_end.disable()
            self.textbox_refresh_time.enable()

            self.checkbox_master.disable()
            self.checkbox_master.value = 0
            self.checkbox_up_time.enable()
            self.checkbox_up_time.value = 0
            self.checkbox_cpu_temp.enable()
            self.checkbox_cpu_temp.value = 0
            self.checkbox_temperature.enable()
            self.checkbox_temperature.value = 0
            self.checkbox_pressure.enable()
            self.checkbox_pressure.value = 0
            self.checkbox_humidity.enable()
            self.checkbox_humidity.value = 0
            self.checkbox_lumen.enable()
            self.checkbox_lumen.value = 0
            self.checkbox_colour.enable()
            self.checkbox_colour.value = 0
            self.checkbox_acc.enable()
            self.checkbox_acc.value = 0
            self.checkbox_mag.enable()
            self.checkbox_mag.value = 0
            self.checkbox_gyro.enable()
            self.checkbox_gyro.value = 0

            self.button_live.enable()

    def plotly_button(self):
        """ Create Plotly offline HTML Graph, based on user selections in the Graph Window. """
        new_data = app_graph.CreateGraphData()
        new_data.db_location = filedialog.askopenfilename()

        self.current_config.graph_start = self.textbox_start.value
        self.current_config.graph_end = self.textbox_end.value
        self.current_config.sql_queries_skip = self.textbox_sql_skip.value
        self.current_config.temperature_offset = self.textbox_temperature_offset.value

        app_config.check_config(self.current_config)
        self._set_config()

        new_data.save_to = self.current_config.save_to
        new_data.graph_start = self.current_config.graph_start
        new_data.graph_end = self.current_config.graph_end
        new_data.datetime_offset = self.current_config.datetime_offset
        new_data.sql_queries_skip = self.current_config.sql_queries_skip
        new_data.graph_columns = self._get_column_checkboxes()
        new_data.enable_custom_temp_offset = self.current_config.enable_custom_temp_offset
        new_data.temperature_offset = self.current_config.temperature_offset

        app_graph.start_plotly_graph(new_data)

    def live_button(self):
        """ Creates and starts a 'Live Graph' based on graph selections & the first checked and online IP. """
        app_graph.pyplot.close()
        try:
            ip = self.ip_selection.get_verified_ip_list()[0]
            checkbox = self._get_column_checkboxes()[3]
        except IndexError:
            ip = "Invalid"
            checkbox = "Invalid"

        if ip is not "Invalid":
            self.current_config.live_refresh = self.textbox_refresh_time.value
            self.current_config.temperature_offset = self.textbox_temperature_offset.value
            app_config.check_config(self.current_config)
            self._set_config()
            app_graph.CreateLiveGraph(checkbox, ip, self.current_config)
            # Thread(target=app_graph.CreateLiveGraph, args=[checkbox, ip, self.current_config]).start()
        else:
            warn("Select Sensor", "Please Select a Sensor IP from the Main window\n"
                                  "& Sensor Type from the Graph window")

    def _get_column_checkboxes(self):
        """ Returns selected SQL Columns from the Graph Window, depending on the Data Source Selected. """
        sql_columns = app_graph.CreateSQLColumnNames()
        column_checkboxes = [sql_columns.date_time, sql_columns.sensor_name, sql_columns.ip]

        if self.checkbox_up_time.value:
            column_checkboxes.append(sql_columns.system_uptime)
        if self.checkbox_cpu_temp.value:
            column_checkboxes.append(sql_columns.cpu_temp)
        if self.checkbox_temperature.value:
            column_checkboxes.append(sql_columns.environmental_temp)
        if self.checkbox_pressure.value:
            column_checkboxes.append(sql_columns.pressure)
        if self.checkbox_humidity.value:
            column_checkboxes.append(sql_columns.humidity)
        if self.checkbox_lumen.value:
            column_checkboxes.append(sql_columns.lumen)
        if self.checkbox_colour.value:
            column_checkboxes.append(sql_columns.rgb[0])
            column_checkboxes.append(sql_columns.rgb[1])
            column_checkboxes.append(sql_columns.rgb[2])
        if self.checkbox_acc.value:
            column_checkboxes.append(sql_columns.accelerometer_xyz[0])
            column_checkboxes.append(sql_columns.accelerometer_xyz[1])
            column_checkboxes.append(sql_columns.accelerometer_xyz[2])
        if self.checkbox_mag.value:
            column_checkboxes.append(sql_columns.magnetometer_xyz[0])
            column_checkboxes.append(sql_columns.magnetometer_xyz[1])
            column_checkboxes.append(sql_columns.magnetometer_xyz[2])
        if self.checkbox_gyro.value:
            column_checkboxes.append(sql_columns.gyroscope_xyz[0])
            column_checkboxes.append(sql_columns.gyroscope_xyz[1])
            column_checkboxes.append(sql_columns.gyroscope_xyz[2])

        if self.checkbox_gyro.value or self.checkbox_mag.value or self.checkbox_acc.value:
            column_checkboxes.append(sql_columns.date_time)
            column_checkboxes.append(sql_columns.ip)
            column_checkboxes.append(sql_columns.sensor_name)

        app_logger.app_logger.debug(str(column_checkboxes))
        return column_checkboxes

    def _enable_all_for_live(self):
        """ Uncheck and allows all possible 'Live Graph' sensor type checkboxes. """
        self.checkbox_up_time.enable()
        self.checkbox_up_time.value = 0
        self.checkbox_cpu_temp.enable()
        self.checkbox_cpu_temp.value = 0
        self.checkbox_temperature.enable()
        self.checkbox_temperature.value = 0
        self.checkbox_pressure.enable()
        self.checkbox_pressure.value = 0
        self.checkbox_humidity.enable()
        self.checkbox_humidity.value = 0
        self.checkbox_lumen.enable()
        self.checkbox_lumen.value = 0
        self.checkbox_colour.enable()
        self.checkbox_colour.value = 0
        self.checkbox_acc.enable()
        self.checkbox_acc.value = 0
        self.checkbox_mag.enable()
        self.checkbox_mag.value = 0
        self.checkbox_gyro.enable()
        self.checkbox_gyro.value = 0

    def _enable_all_checkboxes(self):
        """ Check all sensor type checkboxes. """
        self.checkbox_up_time.value = 1
        self.checkbox_cpu_temp.value = 1
        self.checkbox_temperature.value = 1
        self.checkbox_pressure.value = 1
        self.checkbox_humidity.value = 1
        self.checkbox_lumen.value = 1
        self.checkbox_colour.value = 1
        self.checkbox_acc.value = 1
        self.checkbox_mag.value = 1
        self.checkbox_gyro.value = 1

    def _disable_all_checkboxes(self):
        """ Uncheck all sensor type checkboxes. """
        self.checkbox_up_time.value = 0
        self.checkbox_cpu_temp.value = 0
        self.checkbox_temperature.value = 0
        self.checkbox_pressure.value = 0
        self.checkbox_humidity.value = 0
        self.checkbox_lumen.value = 0
        self.checkbox_colour.value = 0
        self.checkbox_acc.value = 0
        self.checkbox_mag.value = 0
        self.checkbox_gyro.value = 0

    def _disable_other_checkboxes(self, var_checkbox):
        """ Disable all unselected sensor type checkboxes. """
        if self.radio_sensor_type.value == "Live Sensor":
            unchecked = False
            if var_checkbox is self.sql_columns.system_uptime:
                if self.checkbox_up_time.value == 0:
                    unchecked = True
            else:
                self.checkbox_up_time.disable()
                self.checkbox_up_time.value = 0
            if var_checkbox is self.sql_columns.cpu_temp:
                if self.checkbox_cpu_temp.value == 0:
                    unchecked = True
            else:
                self.checkbox_cpu_temp.disable()
                self.checkbox_cpu_temp.value = 0
            if var_checkbox is self.sql_columns.environmental_temp:
                if self.checkbox_temperature.value == 0:
                    unchecked = True
            else:
                self.checkbox_temperature.disable()
                self.checkbox_temperature.value = 0
            if var_checkbox is self.sql_columns.pressure:
                if self.checkbox_pressure.value == 0:
                    unchecked = True
            else:
                self.checkbox_pressure.disable()
                self.checkbox_pressure.value = 0
            if var_checkbox is self.sql_columns.humidity:
                if self.checkbox_humidity.value == 0:
                    unchecked = True
            else:
                self.checkbox_humidity.disable()
                self.checkbox_humidity.value = 0
            if var_checkbox is self.sql_columns.lumen:
                if self.checkbox_lumen.value == 0:
                    unchecked = True
            else:
                self.checkbox_lumen.disable()
                self.checkbox_lumen.value = 0
            if var_checkbox is self.sql_columns.rgb:
                if self.checkbox_colour.value == 0:
                    unchecked = True
            else:
                self.checkbox_colour.disable()
                self.checkbox_colour.value = 0
            if var_checkbox is self.sql_columns.accelerometer_xyz:
                if self.checkbox_acc.value == 0:
                    unchecked = True
            else:
                self.checkbox_acc.disable()
                self.checkbox_acc.value = 0
            if var_checkbox is self.sql_columns.magnetometer_xyz:
                if self.checkbox_mag.value == 0:
                    unchecked = True
            else:
                self.checkbox_mag.disable()
                self.checkbox_mag.value = 0
            if var_checkbox is self.sql_columns.gyroscope_xyz:
                if self.checkbox_gyro.value == 0:
                    unchecked = True
            else:
                self.checkbox_gyro.disable()
                self.checkbox_gyro.value = 0

            if unchecked:
                self._enable_all_for_live()
