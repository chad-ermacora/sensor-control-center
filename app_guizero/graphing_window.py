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
from tkinter import filedialog
from app_modules import app_logger
from app_modules import app_variables
from app_modules import app_config
from app_modules import graphing_variables
from app_modules import graphing_live
from app_modules import graphing_offline


class CreateGraphingWindow:
    """ Creates a GUI window for creating Plotly or Live graphs. """

    def __init__(self, app, ip_selection, current_config):
        self.ip_selection = ip_selection
        self.current_config = current_config
        self.readable_column_names = app_variables.CreateSQLColumnsReadable()
        self.sql_columns = app_variables.CreateSQLColumnNames()

        self.window = guizero.Window(app,
                                     title="Graphing",
                                     width=280,
                                     height=580,
                                     layout="grid",
                                     visible=False)

        self.text_sensor_type_name = guizero.Text(self.window,
                                                  text="Data Source",
                                                  color='blue',
                                                  grid=[1, 1, 2, 1],
                                                  align="top")

        self.radio_sensor_type = guizero.ButtonGroup(self.window,
                                                     options=["Live Sensor", "SQL Database"],
                                                     horizontal="True",
                                                     command=self._radio_source_selection,
                                                     grid=[1, 2, 2, 1],
                                                     align="top")

        self.text_space3 = guizero.Text(self.window,
                                        text="SQL Recording Type",
                                        color="blue",
                                        grid=[1, 3, 2, 1],
                                        align="top")

        self.radio_recording_type_selection = guizero.ButtonGroup(self.window,
                                                                  options=["Interval", "Triggers"],
                                                                  horizontal="True",
                                                                  command=self._radio_sql_type_selection,
                                                                  grid=[1, 4, 2, 1],
                                                                  align="top")

        self.text_sensor_type_name = guizero.Text(self.window,
                                                  text="Graph Options",
                                                  color='blue',
                                                  grid=[1, 6, 2, 1],
                                                  align="top")

        self.text_space2 = guizero.Text(self.window,
                                        text="YYYY-MM-DD HH:MM:SS",
                                        size=7,
                                        color='#CB0000',
                                        grid=[2, 7, 2, 1],
                                        align="left")

        self.text_start = guizero.Text(self.window,
                                       text="Start Date & Time: ",
                                       color='green',
                                       grid=[1, 8],
                                       align="left")

        self.textbox_start = guizero.TextBox(self.window,
                                             text="",
                                             width=20,
                                             grid=[2, 8],
                                             align="left")

        self.text_end = guizero.Text(self.window,
                                     text="End Date & Time:",
                                     color='green',
                                     grid=[1, 9],
                                     align="left")

        self.textbox_end = guizero.TextBox(self.window,
                                           text="",
                                           width=20,
                                           grid=[2, 9],
                                           align="left")

        self.text_sql_skip = guizero.Text(self.window,
                                          text="Plot Data - Skip:  ",
                                          color='green',
                                          grid=[1, 10],
                                          align="right")

        self.textbox_sql_skip = guizero.TextBox(self.window,
                                                text="",
                                                width=10,
                                                grid=[2, 10],
                                                align="left")

        self.text_sql_skip2 = guizero.Text(self.window,
                                           text=" Plot 1    ",
                                           color='green',
                                           grid=[2, 10],
                                           align="right")

        self.text_temperature_offset = guizero.Text(self.window,
                                                    text="Env Temp Offset:",
                                                    color='green',
                                                    grid=[1, 11],
                                                    align="left")

        self.textbox_temperature_offset = guizero.TextBox(self.window,
                                                          text="",
                                                          width=5,
                                                          grid=[2, 11],
                                                          align="left")

        self.checkbox_default_offset = guizero.CheckBox(self.window,
                                                        text="Use Sensor\nDefault",
                                                        command=self._click_checkbox_offset,
                                                        grid=[2, 11],
                                                        align="right")

        self.text_refresh_time = guizero.Text(self.window,
                                              text="Live refresh (Sec):",
                                              color='green',
                                              grid=[1, 12],
                                              align="left")

        self.textbox_refresh_time = guizero.TextBox(self.window,
                                                    text="2",
                                                    width=5,
                                                    grid=[2, 12],
                                                    align="left")

        self.checkbox_master = guizero.CheckBox(self.window,
                                                text="All Sensors",
                                                command=self._master_checkbox,
                                                grid=[1, 16, 2, 1],
                                                align="top")

        self.checkbox_up_time = guizero.CheckBox(self.window,
                                                 text=self.readable_column_names.system_uptime,
                                                 command=self._disable_other_checkboxes,
                                                 args=[self.sql_columns.system_uptime],
                                                 grid=[1, 17],
                                                 align="left")

        self.checkbox_cpu_temp = guizero.CheckBox(self.window,
                                                  text=self.readable_column_names.cpu_temp,
                                                  command=self._disable_other_checkboxes,
                                                  args=[self.sql_columns.cpu_temp],
                                                  grid=[1, 18],
                                                  align="left")

        self.checkbox_env_temperature = guizero.CheckBox(self.window,
                                                         text=self.readable_column_names.environmental_temp,
                                                         command=self._disable_other_checkboxes,
                                                         args=[self.sql_columns.environmental_temp],
                                                         grid=[1, 19],
                                                         align="left")

        self.checkbox_pressure = guizero.CheckBox(self.window,
                                                  text=self.readable_column_names.pressure,
                                                  command=self._disable_other_checkboxes,
                                                  args=[self.sql_columns.pressure],
                                                  grid=[1, 20],
                                                  align="left")

        self.checkbox_altitude = guizero.CheckBox(self.window,
                                                  text=self.readable_column_names.altitude,
                                                  command=self._disable_other_checkboxes,
                                                  args=[self.sql_columns.altitude],
                                                  grid=[1, 21],
                                                  align="left")

        self.checkbox_humidity = guizero.CheckBox(self.window,
                                                  text=self.readable_column_names.humidity,
                                                  command=self._disable_other_checkboxes,
                                                  args=[self.sql_columns.humidity],
                                                  grid=[1, 22],
                                                  align="left")

        self.checkbox_distance = guizero.CheckBox(self.window,
                                                  text=self.readable_column_names.distance,
                                                  command=self._disable_other_checkboxes,
                                                  args=[self.sql_columns.distance],
                                                  grid=[1, 23],
                                                  align="left")

        self.checkbox_gas = guizero.CheckBox(self.window,
                                             text=self.readable_column_names.gas,
                                             command=self._disable_other_checkboxes,
                                             args=[self.sql_columns.gas],
                                             grid=[1, 24],
                                             align="left")

        self.checkbox_particulate_matter = guizero.CheckBox(self.window,
                                                            text=self.readable_column_names.particulate_matter,
                                                            command=self._disable_other_checkboxes,
                                                            args=[self.sql_columns.particulate_matter],
                                                            grid=[2, 17],
                                                            align="left")

        self.checkbox_lumen = guizero.CheckBox(self.window,
                                               text=self.readable_column_names.lumen,
                                               command=self._disable_other_checkboxes,
                                               args=[self.sql_columns.lumen],
                                               grid=[2, 18],
                                               align="left")

        self.checkbox_colour = guizero.CheckBox(self.window,
                                                text=self.readable_column_names.colours,
                                                command=self._disable_other_checkboxes,
                                                args=[self.sql_columns.rgb],
                                                grid=[2, 19],
                                                align="left")

        self.checkbox_ultra_violet = guizero.CheckBox(self.window,
                                                      text=self.readable_column_names.ultra_violet,
                                                      command=self._disable_other_checkboxes,
                                                      args=[self.sql_columns.ultra_violet],
                                                      grid=[2, 20],
                                                      align="left")

        self.checkbox_acc = guizero.CheckBox(self.window,
                                             text=self.readable_column_names.accelerometer_xyz,
                                             command=self._disable_other_checkboxes,
                                             args=[self.sql_columns.accelerometer_xyz],
                                             grid=[2, 21],
                                             align="left")

        self.checkbox_mag = guizero.CheckBox(self.window,
                                             text=self.readable_column_names.magnetometer_xyz,
                                             command=self._disable_other_checkboxes,
                                             args=[self.sql_columns.magnetometer_xyz],
                                             grid=[2, 22],
                                             align="left")

        self.checkbox_gyro = guizero.CheckBox(self.window,
                                              text=self.readable_column_names.gyroscope_xyz,
                                              command=self._disable_other_checkboxes,
                                              args=[self.sql_columns.gyroscope_xyz],
                                              grid=[2, 23],
                                              align="left")

        self.text_space4 = guizero.Text(self.window,
                                        text=" ",
                                        grid=[1, 35],
                                        align="right")

        self.button_live = guizero.PushButton(self.window,
                                              text="Create Graph",
                                              command=self._create_graph_button,
                                              grid=[1, 36, 2, 1],
                                              align="top")

        # Window Tweaks
        self.window.tk.resizable(False, False)
        self.checkbox_default_offset.value = 1
        self._set_config()
        self._radio_source_selection()
        self._click_checkbox_offset()
        self.checkbox_up_time.value = 0
        self.checkbox_env_temperature.value = 0
        self.checkbox_pressure.value = 0
        self.checkbox_humidity.value = 0
        self.checkbox_lumen.value = 0
        self.checkbox_colour.value = 0

        # Temp disable radio box until triggers working
        self.radio_recording_type_selection.disable()

    def _master_checkbox(self):
        """ Checks all sensor selection checkboxes. """
        if self.checkbox_master.value:
            self._check_all_sensor_checkboxes()
        else:
            self._uncheck_all_sensor_checkboxes()

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
                guizero.warn("Invalid Temperature Offset", "Please check and correct 'Env Temp Offset'")
                app_logger.app_logger.warning("Invalid Graph 'Env Temp Offset': " + str(error))

    def _set_config(self):
        """ Sets the programs Configuration to the provided settings. """

        self.textbox_start.value = self.current_config.graph_start
        self.textbox_end.value = self.current_config.graph_end
        self.textbox_sql_skip.value = self.current_config.sql_queries_skip
        self.textbox_temperature_offset.value = self.current_config.temperature_offset
        self.textbox_refresh_time.value = self.current_config.live_refresh

    def _radio_source_selection(self):
        """ Enables or disables the Graph Window selections, based on graph type selected. """
        self._enable_all_sensor_checkboxes()
        if self.radio_sensor_type.value_text == "SQL Database":
            self._radio_sql_type_selection()
            self.textbox_refresh_time.disable()

            self.textbox_start.enable()
            self.textbox_end.enable()
            self.radio_recording_type_selection.enable()

            if not self.checkbox_default_offset.value:
                self.textbox_temperature_offset.enable()

            self.checkbox_master.enable()
            self.checkbox_master.value = 1
            self._check_all_sensor_checkboxes()

        if self.radio_sensor_type.value_text == "Live Sensor":
            self.textbox_sql_skip.disable()
            self.textbox_start.disable()
            self.textbox_end.disable()
            self.textbox_refresh_time.enable()
            self.radio_recording_type_selection.disable()

            self.checkbox_master.disable()
            self.checkbox_master.value = 0
            self._uncheck_all_sensor_checkboxes()

    def _radio_sql_type_selection(self):
        """ Enables or disables the SQL Skip, based on graph type selected. """
        if self.radio_recording_type_selection.value_text == "Interval":
            self.textbox_sql_skip.enable()
        else:
            self.textbox_sql_skip.disable()

    def _create_graph_button(self):
        if self.radio_sensor_type.value_text == "Live Sensor":
            self.live_button()
        elif self.radio_sensor_type.value_text == "SQL Database":
            self.plotly_button()

    def plotly_button(self):
        """ Create Plotly offline HTML Graph, based on user selections in the Graph Window. """
        new_data = graphing_variables.CreateGraphData()
        new_data.enable_plotly_webgl = self.current_config.enable_plotly_webgl
        new_data.db_location = filedialog.askopenfilename()

        if str(new_data.db_location) != "()":
            self.current_config.graph_start = self.textbox_start.value
            self.current_config.graph_end = self.textbox_end.value
            self.current_config.sql_queries_skip = self.textbox_sql_skip.value
            self.current_config.temperature_offset = self.textbox_temperature_offset.value

            app_config.check_config(self.current_config)
            self._set_config()

            new_data.save_to = self.current_config.save_to
            if self.radio_recording_type_selection.value_text is "Triggers":
                new_data.graph_table = "TriggerData"
                new_data.bypass_sql_skip = True
            new_data.graph_start = self.current_config.graph_start
            new_data.graph_end = self.current_config.graph_end
            new_data.datetime_offset = self.current_config.datetime_offset
            new_data.sql_queries_skip = self.current_config.sql_queries_skip
            new_data.graph_columns = self._get_column_checkboxes()
            new_data.enable_custom_temp_offset = self.current_config.enable_custom_temp_offset
            new_data.temperature_offset = self.current_config.temperature_offset

            graphing_offline.start_plotly_graph(new_data)
        else:
            app_logger.app_logger.warning("Plotly Graph: No Database Selected")

    def live_button(self):
        """ Creates and starts a 'Live Graph' based on graph selections & the first checked and online IP. """
        graphing_live.pyplot.close()
        try:
            ip = self.ip_selection.get_verified_ip_list()[0]
            sensor_type = self._get_column_checkboxes()[3]
        except IndexError:
            ip = "Invalid"
            sensor_type = "Invalid"

        if ip is not "Invalid":
            self.current_config.live_refresh = self.textbox_refresh_time.value
            self.current_config.temperature_offset = self.textbox_temperature_offset.value
            app_config.check_config(self.current_config)
            self._set_config()
            graphing_live.CreateLiveGraph(sensor_type, ip, self.current_config)
        else:
            guizero.warn("Select Sensor", "Please Select a Sensor IP from the Main window\n"
                                          "& Sensor Type from the Graph window")

    def _get_column_checkboxes(self):
        """ Returns selected SQL Columns from the Graph Window, depending on the Data Source Selected. """
        sql_columns = app_variables.CreateSQLColumnNames()
        column_checkboxes = [sql_columns.date_time, sql_columns.sensor_name, sql_columns.ip]

        if self.checkbox_up_time.value:
            column_checkboxes.append(sql_columns.system_uptime)
        if self.checkbox_cpu_temp.value:
            column_checkboxes.append(sql_columns.cpu_temp)
        if self.checkbox_env_temperature.value:
            column_checkboxes.append(sql_columns.environmental_temp)
        if self.checkbox_pressure.value:
            column_checkboxes.append(sql_columns.pressure)
        if self.checkbox_altitude.value:
            column_checkboxes.append(sql_columns.altitude)
        if self.checkbox_humidity.value:
            column_checkboxes.append(sql_columns.humidity)
        if self.checkbox_distance.value:
            column_checkboxes.append(sql_columns.distance)
        if self.checkbox_gas.value:
            for column in sql_columns.gas:
                column_checkboxes.append(column)
        if self.checkbox_particulate_matter.value:
            for column in sql_columns.particulate_matter:
                column_checkboxes.append(column)
        if self.checkbox_lumen.value:
            column_checkboxes.append(sql_columns.lumen)
        if self.checkbox_colour.value:
            for column in sql_columns.six_chan_color:
                column_checkboxes.append(column)
        if self.checkbox_ultra_violet.value:
            for column in sql_columns.ultra_violet:
                column_checkboxes.append(column)
        if self.checkbox_acc.value:
            for column in sql_columns.accelerometer_xyz:
                column_checkboxes.append(column)
        if self.checkbox_mag.value:
            for column in sql_columns.magnetometer_xyz:
                column_checkboxes.append(column)
        if self.checkbox_gyro.value:
            for column in sql_columns.gyroscope_xyz:
                column_checkboxes.append(column)

        if self.checkbox_gyro.value or self.checkbox_mag.value or self.checkbox_acc.value:
            column_checkboxes.append(sql_columns.date_time)
            column_checkboxes.append(sql_columns.ip)
            column_checkboxes.append(sql_columns.sensor_name)

        app_logger.app_logger.debug(str(column_checkboxes))
        return column_checkboxes

    def _enable_all_sensor_checkboxes(self):
        """ Enables all sensor type checkboxes. """
        self.checkbox_up_time.enable()
        self.checkbox_cpu_temp.enable()
        self.checkbox_env_temperature.enable()
        self.checkbox_pressure.enable()
        self.checkbox_altitude.enable()
        self.checkbox_humidity.enable()
        self.checkbox_distance.enable()
        self.checkbox_gas.enable()
        self.checkbox_particulate_matter.enable()
        self.checkbox_lumen.enable()
        self.checkbox_colour.enable()
        self.checkbox_ultra_violet.enable()
        self.checkbox_acc.enable()
        self.checkbox_mag.enable()
        self.checkbox_gyro.enable()

    def _disable_all_sensor_checkboxes(self):
        """ Disables all sensor type checkboxes. """
        self.checkbox_up_time.disable()
        self.checkbox_cpu_temp.disable()
        self.checkbox_env_temperature.disable()
        self.checkbox_pressure.disable()
        self.checkbox_altitude.disable()
        self.checkbox_humidity.disable()
        self.checkbox_distance.disable()
        self.checkbox_gas.disable()
        self.checkbox_particulate_matter.disable()
        self.checkbox_lumen.disable()
        self.checkbox_colour.disable()
        self.checkbox_ultra_violet.disable()
        self.checkbox_acc.disable()
        self.checkbox_mag.disable()
        self.checkbox_gyro.disable()

    def _check_all_sensor_checkboxes(self):
        """ Checks all sensor type checkboxes. """
        self.checkbox_up_time.value = 1
        self.checkbox_cpu_temp.value = 1
        self.checkbox_env_temperature.value = 1
        self.checkbox_pressure.value = 1
        self.checkbox_altitude.value = 1
        self.checkbox_humidity.value = 1
        self.checkbox_distance.value = 1
        self.checkbox_gas.value = 1
        self.checkbox_particulate_matter.value = 1
        self.checkbox_lumen.value = 1
        self.checkbox_colour.value = 1
        self.checkbox_ultra_violet.value = 1
        self.checkbox_acc.value = 1
        self.checkbox_mag.value = 1
        self.checkbox_gyro.value = 1

    def _uncheck_all_sensor_checkboxes(self):
        """ Unchecks all sensor type checkboxes. """
        self.checkbox_up_time.value = 0
        self.checkbox_cpu_temp.value = 0
        self.checkbox_env_temperature.value = 0
        self.checkbox_pressure.value = 0
        self.checkbox_altitude.value = 0
        self.checkbox_humidity.value = 0
        self.checkbox_distance.value = 0
        self.checkbox_gas.value = 0
        self.checkbox_particulate_matter.value = 0
        self.checkbox_lumen.value = 0
        self.checkbox_colour.value = 0
        self.checkbox_ultra_violet.value = 0
        self.checkbox_acc.value = 0
        self.checkbox_mag.value = 0
        self.checkbox_gyro.value = 0

    def _disable_other_checkboxes(self, var_checkbox):
        """ Disable all unselected sensor type checkboxes. """
        if self.radio_sensor_type.value == "Live Sensor":
            self._disable_all_sensor_checkboxes()

            if var_checkbox is self.sql_columns.system_uptime:
                self.checkbox_up_time.enable()
                if self.checkbox_up_time.value == 0:
                    self._enable_all_sensor_checkboxes()
            elif var_checkbox is self.sql_columns.cpu_temp:
                self.checkbox_cpu_temp.enable()
                if self.checkbox_cpu_temp.value == 0:
                    self._enable_all_sensor_checkboxes()
            elif var_checkbox is self.sql_columns.environmental_temp:
                self.checkbox_env_temperature.enable()
                if self.checkbox_env_temperature.value == 0:
                    self._enable_all_sensor_checkboxes()
            elif var_checkbox is self.sql_columns.pressure:
                self.checkbox_pressure.enable()
                if self.checkbox_pressure.value == 0:
                    self._enable_all_sensor_checkboxes()
            elif var_checkbox is self.sql_columns.altitude:
                self.checkbox_altitude.enable()
                if self.checkbox_altitude.value == 0:
                    self._enable_all_sensor_checkboxes()
            elif var_checkbox is self.sql_columns.humidity:
                self.checkbox_humidity.enable()
                if self.checkbox_humidity.value == 0:
                    self._enable_all_sensor_checkboxes()
            elif var_checkbox is self.sql_columns.distance:
                self.checkbox_distance.enable()
                if self.checkbox_distance.value == 0:
                    self._enable_all_sensor_checkboxes()
            elif var_checkbox is self.sql_columns.gas:
                self.checkbox_gas.enable()
                if self.checkbox_gas.value == 0:
                    self._enable_all_sensor_checkboxes()
            elif var_checkbox is self.sql_columns.particulate_matter:
                self.checkbox_particulate_matter.enable()
                if self.checkbox_particulate_matter.value == 0:
                    self._enable_all_sensor_checkboxes()
            elif var_checkbox is self.sql_columns.lumen:
                self.checkbox_lumen.enable()
                if self.checkbox_lumen.value == 0:
                    self._enable_all_sensor_checkboxes()
            elif var_checkbox is self.sql_columns.rgb or var_checkbox is self.sql_columns.six_chan_color:
                self.checkbox_colour.enable()
                if self.checkbox_colour.value == 0:
                    self._enable_all_sensor_checkboxes()
            elif var_checkbox is self.sql_columns.ultra_violet:
                self.checkbox_ultra_violet.enable()
                if self.checkbox_ultra_violet.value == 0:
                    self._enable_all_sensor_checkboxes()
            elif var_checkbox is self.sql_columns.accelerometer_xyz:
                self.checkbox_acc.enable()
                if self.checkbox_acc.value == 0:
                    self._enable_all_sensor_checkboxes()
            elif var_checkbox is self.sql_columns.magnetometer_xyz:
                self.checkbox_mag.enable()
                if self.checkbox_mag.value == 0:
                    self._enable_all_sensor_checkboxes()
            elif var_checkbox is self.sql_columns.gyroscope_xyz:
                self.checkbox_gyro.enable()
                if self.checkbox_gyro.value == 0:
                    self._enable_all_sensor_checkboxes()
