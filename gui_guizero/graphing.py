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
from guizero import Window, CheckBox, PushButton, Text, TextBox, warn, ButtonGroup
from tkinter import filedialog
from matplotlib import pyplot
import app_config
import app_graph
import control_center_logger


class CreateSensorCommandsWindow:
    def __init__(self, app):
        self.current_config = app_config.get_from_file()
        self.window_graph = Window(app,
                                   title="Graphing",
                                   width=275,
                                   height=505,
                                   layout="grid",
                                   visible=False)

        self.text_sensor_type_name = Text(self.window_graph,
                                          text="Data Source",
                                          color='blue',
                                          grid=[1, 1, 2, 1],
                                          align="top")

        self.radio_sensor_type = ButtonGroup(self.window_graph,
                                             options=["Live", "Interval SQL", "Trigger SQL"],
                                             horizontal="True",
                                             command=self._radio_selection,
                                             grid=[1, 2, 2, 1],
                                             align="top")

        self.text_space1 = Text(self.window_graph,
                                text=" ",
                                grid=[1, 3],
                                align="right")

        self.text_start = Text(self.window_graph,
                               text="Start DateTime: ",
                               color='green',
                               grid=[1, 6],
                               align="left")

        self.textbox_start = TextBox(self.window_graph,
                                     text="",
                                     width=20,
                                     grid=[2, 6],
                                     align="left")

        self.text_end = Text(self.window_graph,
                             text="End DateTime:",
                             color='green',
                             grid=[1, 7],
                             align="left")

        self.textbox_end = TextBox(self.window_graph,
                                   text="",
                                   width=20,
                                   grid=[2, 7],
                                   align="left")

        self.text_sql_skip = Text(self.window_graph,
                                  text="Add row every:",
                                  color='green',
                                  grid=[1, 8],
                                  align="left")

        self.textbox_sql_skip = TextBox(self.window_graph,
                                        text="",
                                        width=10,
                                        grid=[2, 8],
                                        align="left")

        self.text_sql_skip2 = Text(self.window_graph,
                                   text="rows    ",
                                   color='green',
                                   grid=[2, 8],
                                   align="right")

        self.text_temperature_offset = Text(self.window_graph,
                                            text="Environmental:",
                                            color='green',
                                            grid=[1, 9],
                                            align="left")

        self.textbox_temperature_offset = TextBox(self.window_graph,
                                                  text="",
                                                  width=5,
                                                  grid=[2, 9],
                                                  align="left")

        self.text_temperature_offset2 = Text(self.window_graph,
                                             text="Temp Offset",
                                             color='green',
                                             grid=[2, 9],
                                             align="right")

        self.text_refresh_time = Text(self.window_graph,
                                      text="Live refresh (Sec):",
                                      color='green',
                                      grid=[1, 10],
                                      align="left")

        self.textbox_refresh_time = TextBox(self.window_graph,
                                            text="2",
                                            width=5,
                                            grid=[2, 10],
                                            align="left")

        self.text_space2 = Text(self.window_graph,
                                text=" ",
                                grid=[1, 11],
                                align="right")

        self.text_column_selection = Text(self.window_graph,
                                          text="Interval Sensors",
                                          color='blue',
                                          grid=[1, 15, 2, 1],
                                          align="top")

        self.checkbox_up_time = CheckBox(self.window_graph,
                                         text="System Uptime",
                                         command=self._disable_other_checkboxes,
                                         args=["Uptime"],
                                         grid=[1, 16],
                                         align="left")

        self.checkbox_cpu_temp = CheckBox(self.window_graph,
                                          text="CPU Temperature",
                                          command=self._disable_other_checkboxes,
                                          args=["CPUTemperature"],
                                          grid=[1, 17],
                                          align="left")

        self.checkbox_temperature = CheckBox(self.window_graph,
                                             text="Env Temperature",
                                             command=self._disable_other_checkboxes,
                                             args=["Temperature"],
                                             grid=[1, 18],
                                             align="left")

        self.checkbox_pressure = CheckBox(self.window_graph,
                                          text="Pressure",
                                          command=self._disable_other_checkboxes,
                                          args=["Pressure"],
                                          grid=[1, 19],
                                          align="left")

        self.checkbox_humidity = CheckBox(self.window_graph,
                                          text="Humidity",
                                          command=self._disable_other_checkboxes,
                                          args=["Humidity"],
                                          grid=[2, 16],
                                          align="left")

        self.checkbox_lumen = CheckBox(self.window_graph,
                                       text="Lumen",
                                       command=self._disable_other_checkboxes,
                                       args=["Lumen"],
                                       grid=[2, 17],
                                       align="left")

        self.checkbox_colour = CheckBox(self.window_graph,
                                        text="Colour RGB",
                                        command=self._disable_other_checkboxes,
                                        args=["RGB"],
                                        grid=[2, 18],
                                        align="left")

        self.text_column_selection2 = Text(self.window_graph,
                                           text="Trigger Sensors",
                                           color='blue',
                                           grid=[1, 24, 2, 1],
                                           align="bottom")

        self.checkbox_acc = CheckBox(self.window_graph,
                                     text="Accelerometer XYZ",
                                     command=self._disable_other_checkboxes,
                                     args=["Accelerometer"],
                                     grid=[1, 25],
                                     align="left")

        self.checkbox_mag = CheckBox(self.window_graph,
                                     text="Magnetometer XYZ",
                                     command=self._disable_other_checkboxes,
                                     args=["Magnetometer"],
                                     grid=[2, 25],
                                     align="left")

        self.checkbox_gyro = CheckBox(self.window_graph,
                                      text="Gyroscopic XYZ",
                                      command=self._disable_other_checkboxes,
                                      args=["Gyroscopic"],
                                      grid=[1, 26],
                                      align="left")

        self.text_space3 = Text(self.window_graph,
                                text=" ",
                                grid=[1, 35],
                                align="right")

        self.button_database = PushButton(self.window_graph,
                                          text="Open & Graph\nDatabase",
                                          command=self.plotly_button,
                                          grid=[1, 36, 2, 1],
                                          align="left")

        self.button_live = PushButton(self.window_graph,
                                      text="Start Live Graph",
                                      command=self.live_button,
                                      grid=[2, 36],
                                      align="left")

    def set_config(self):
        """ Sets the programs Configuration to the provided settings. """

        self.textbox_start.value = self.current_config.graph_start
        self.textbox_end.value = self.current_config.graph_end
        self.textbox_sql_skip.value = self.current_config.sql_queries_skip
        self.textbox_temperature_offset.value = self.current_config.temperature_offset
        self.textbox_refresh_time.value = self.current_config.live_refresh

    def _radio_selection(self):
        """ Enables or disables the Graph Window selections, based on graph type selected. """
        self._enable_all_checkboxes()
        if self.radio_sensor_type.get() == "Interval SQL":
            self.checkbox_acc.disable()
            self.checkbox_mag.disable()
            self.checkbox_gyro.disable()
            self.button_live.disable()
            self.textbox_refresh_time.disable()

            self.checkbox_cpu_temp.enable()
            self.textbox_temperature_offset.enable()
            self.checkbox_temperature.enable()
            self.checkbox_pressure.enable()
            self.checkbox_humidity.enable()
            self.checkbox_lumen.enable()
            self.checkbox_colour.enable()
            self.checkbox_up_time.enable()
            self.textbox_start.enable()
            self.textbox_end.enable()
            self.textbox_sql_skip.enable()
            self.button_database.enable()

        if self.radio_sensor_type.get() == "Trigger SQL":
            self.textbox_sql_skip.disable()
            self.textbox_temperature_offset.disable()
            self.checkbox_cpu_temp.disable()
            self.checkbox_temperature.disable()
            self.checkbox_pressure.disable()
            self.checkbox_humidity.disable()
            self.checkbox_lumen.disable()
            self.checkbox_colour.disable()
            self.checkbox_up_time.disable()
            self.button_live.disable()
            self.textbox_refresh_time.disable()

            self.checkbox_acc.enable()
            self.checkbox_mag.enable()
            self.checkbox_gyro.enable()
            self.textbox_start.enable()
            self.textbox_end.enable()
            self.textbox_sql_skip.disable()
            self.button_database.enable()

        if self.radio_sensor_type.get() == "Live":
            self.button_database.disable()
            self.textbox_sql_skip.disable()
            self.textbox_start.disable()
            self.textbox_end.disable()

            self.textbox_temperature_offset.enable()
            self.textbox_refresh_time.enable()

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
            self.checkbox_colour.disable()
            self.checkbox_colour.value = 0
            self.checkbox_acc.disable()
            self.checkbox_acc.value = 0
            self.checkbox_mag.disable()
            self.checkbox_mag.value = 0
            self.checkbox_gyro.disable()
            self.checkbox_gyro.value = 0

            self.button_live.enable()

    def plotly_button(self):
        """ Create Plotly offline HTML Graph, based on user selections in the Graph Window. """
        new_data = app_graph.CreateGraphData()
        new_data.db_location = filedialog.askopenfilename()

        self.current_config.start = self.textbox_start.value
        self.current_config.end = self.textbox_end.value
        self.current_config.sql_queries_skip = self.textbox_sql_skip.value
        self.current_config.temperature_offset = self.textbox_temperature_offset.value

        app_config.check_config(self.current_config)
        self.set_config()

        new_data.save_file_to = self.current_config.save_to
        new_data.start = self.current_config.self.start
        new_data.end = self.current_config.self.end
        new_data.time_offset = self.current_config.datetime_offset
        new_data.skip_sql = self.current_config.sql_queries_skip
        new_data.temperature_offset = self.current_config.temperature_offset
        new_data.columns = self._get_column_checkboxes()

        if self.radio_sensor_type.get() == "Interval SQL":
            app_graph.start_graph_interval(new_data)
        elif self.radio_sensor_type.get() == "Trigger SQL":
            app_graph.start_graph_trigger(new_data)

    def live_button(self, ip):
        pyplot.close()
        try:
            checkbox = self._get_column_checkboxes()[3]

            self.current_config.live_refresh = self.textbox_refresh_time.value
            self.current_config.temperature_offset = self.textbox_temperature_offset.value
            app_config.check_config(self.current_config)
            self.set_config()

            app_graph.CreateLiveGraph(checkbox, ip, self.current_config)
        except Exception as error:
            control_center_logger.app_logger.warning("No sensors selected in the main window - " + str(error))
            warn("Select Sensor", "Please Select a Sensor IP from the Main window\n"
                                  "& Sensor Type from the Graph window")

    def _get_column_checkboxes(self):
        """ Returns selected SQL Columns from the Graph Window, depending on the Data Source Selected. """
        column_checkboxes = ["DateTime", "SensorName", "IP"]

        data_source_radio = self.radio_sensor_type.get()
        if data_source_radio == "Interval SQL" or data_source_radio == "Live":
            if self.checkbox_up_time.value:
                column_checkboxes.append("SensorUpTime")
            if self.checkbox_cpu_temp.value:
                column_checkboxes.append("SystemTemp")
            if self.checkbox_temperature.value:
                column_checkboxes.append("EnvironmentTemp")
            if self.checkbox_pressure.value:
                column_checkboxes.append("Pressure")
            if self.checkbox_humidity.value:
                column_checkboxes.append("Humidity")
            if self.checkbox_lumen.value:
                column_checkboxes.append("Lumen")
            if self.checkbox_colour.value:
                column_checkboxes.append("Red")
                column_checkboxes.append("Green")
                column_checkboxes.append("Blue")
        if data_source_radio == "Trigger SQL" or data_source_radio == "Live":
            if self.checkbox_acc.value:
                column_checkboxes.append("Acc_X")
                column_checkboxes.append("Acc_Y")
                column_checkboxes.append("Acc_Z")
            if self.checkbox_mag.value:
                column_checkboxes.append("Mag_X")
                column_checkboxes.append("Mag_Y")
                column_checkboxes.append("Mag_Z")
            if self.checkbox_gyro.value:
                column_checkboxes.append("Gyro_X")
                column_checkboxes.append("Gyro_Y")
                column_checkboxes.append("Gyro_Z")

        control_center_logger.app_logger.debug(str(column_checkboxes))
        return column_checkboxes

    def _enable_all_checkboxes(self):
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

    def _disable_other_checkboxes(self, var_checkbox):
        if self.radio_sensor_type.value == "Live":
            if var_checkbox is "Uptime":
                pass
            else:
                self.checkbox_up_time.disable()
                self.checkbox_up_time.value = 0
            if var_checkbox is "Temperature":
                pass
            else:
                self.checkbox_temperature.disable()
                self.checkbox_temperature.value = 0
            if var_checkbox is "CPUTemperature":
                pass
            else:
                self.checkbox_cpu_temp.disable()
                self.checkbox_cpu_temp.value = 0
            if var_checkbox is "Pressure":
                pass
            else:
                self.checkbox_pressure.disable()
                self.checkbox_pressure.value = 0
            if var_checkbox is "Humidity":
                pass
            else:
                self.checkbox_humidity.disable()
                self.checkbox_humidity.value = 0
            if var_checkbox is "Lumen":
                pass
            else:
                self.checkbox_lumen.disable()
                self.checkbox_lumen.value = 0
            # if var_checkbox is "RGB":
            #     pass
            # else:
            #     self.checkbox_colour.disable()
            #     self.checkbox_colour.value = 0
            # if var_checkbox is "Accelerometer":
            #     pass
            # else:
            #     self.checkbox_acc.disable()
            #     self.checkbox_acc.value = 0
            # if var_checkbox is "Magnetometer":
            #     pass
            # else:
            #     self.checkbox_mag.disable()
            #     self.checkbox_mag.value = 0
            # if var_checkbox is "Gyroscopic":
            #     pass
            # else:
            #     self.checkbox_gyro.disable()
            #     self.checkbox_gyro.value = 0

            if var_checkbox is "Uptime":
                if self.checkbox_up_time.value == 0:
                    self._enable_all_checkboxes()
                else:
                    self.checkbox_up_time.enable()
                    self.checkbox_up_time.value = 1
            elif var_checkbox is "Temperature":
                if self.checkbox_temperature.value == 0:
                    self._enable_all_checkboxes()
                else:
                    self.checkbox_temperature.enable()
                    self.checkbox_temperature.value = 1
            elif var_checkbox is "CPUTemperature":
                if self.checkbox_cpu_temp.value == 0:
                    self._enable_all_checkboxes()
                else:
                    self.checkbox_cpu_temp.enable()
                    self.checkbox_cpu_temp.value = 1
            elif var_checkbox is "Pressure":
                if self.checkbox_pressure.value == 0:
                    self._enable_all_checkboxes()
                else:
                    self.checkbox_pressure.enable()
                    self.checkbox_pressure.value = 1
            elif var_checkbox is "Humidity":
                if self.checkbox_humidity.value == 0:
                    self._enable_all_checkboxes()
                else:
                    self.checkbox_humidity.enable()
                    self.checkbox_humidity.value = 1
            elif var_checkbox is "Lumen":
                if self.checkbox_lumen.value == 0:
                    self._enable_all_checkboxes()
                else:
                    self.checkbox_lumen.enable()
                    self.checkbox_lumen.value = 1
            # elif var_checkbox is "RGB":
            #     if self.checkbox_colour.value == 0:
            #         _self.enable_all_checkboxes()
            #     else:
            #         self.checkbox_colour.enable()
            #         self.checkbox_colour.value = 1
            # elif var_checkbox is "Accelerometer":
            #     if self.checkbox_acc.value == 0:
            #         _self.enable_all_checkboxes()
            #     else:
            #         self.checkbox_acc.enable()
            #         self.checkbox_acc.value = 1
            # elif var_checkbox is "Magnetometer":
            #     if self.checkbox_mag.value == 0:
            #         _self.enable_all_checkboxes()
            #     else:
            #         self.checkbox_mag.enable()
            #         self.checkbox_mag.value = 1
            # elif var_checkbox is "Gyroscopic":
            #     if self.checkbox_gyro.value == 0:
            #         _self.enable_all_checkboxes()
            #     else:
            #         self.checkbox_gyro.enable()
            #         self.checkbox_gyro.value = 1

            self.checkbox_colour.disable()
            self.checkbox_colour.value = 0
            self.checkbox_acc.disable()
            self.checkbox_acc.value = 0
            self.checkbox_mag.disable()
            self.checkbox_mag.value = 0
            self.checkbox_gyro.disable()
            self.checkbox_gyro.value = 0
