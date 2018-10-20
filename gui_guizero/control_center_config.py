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
from guizero import Window, CheckBox, PushButton, Text, TextBox
from tkinter import filedialog
import app_config
import control_center_logger


class CreateConfigWindow:
    def __init__(self, app):
        self.current_config = app_config.get_from_file()
        self.window_config = Window(app,
                                    title="Control Center Configuration",
                                    width=580,
                                    height=300,
                                    layout="grid",
                                    visible=True)

        # Configuration Window Section
        self.button_reset = PushButton(self.window_config,
                                       text="Reset to\nDefaults",
                                       command=self.reset_to_defaults,
                                       grid=[1, 1],
                                       align="right")

        self.checkbox_power_controls = CheckBox(self.window_config,
                                                text="Enable Advanced\nSensor Commands &\nConfiguration Options",
                                                command=self._advanced_checkbox,
                                                grid=[1, 1],
                                                align="top")

        self.button_save_apply = PushButton(self.window_config,
                                            text="Save &\nApply",
                                            command=self._button_save_apply,
                                            grid=[1, 1],
                                            align="left")

        self.text_database_time = Text(self.window_config,
                                       text="Sensor Databases\nSaved in UTC 0",
                                       size=10,
                                       grid=[2, 1],
                                       color='#CB0000',
                                       align="top")

        self.text_spacer1 = Text(self.window_config,
                                 text=" ",
                                 grid=[1, 2],
                                 align="left")

        self.text3 = Text(self.window_config,
                          text="Save Files To",
                          color='blue',
                          grid=[1, 3],
                          align="top")

        self.button_save_dir = PushButton(self.window_config,
                                          text="Choose Folder",
                                          command=self._button_save_to,
                                          grid=[1, 5],
                                          align="bottom")

        self.textbox_save_to = TextBox(self.window_config,
                                       text='',
                                       width=50,
                                       grid=[1, 4],
                                       align="bottom")

        self.text_spacer3 = Text(self.window_config,
                                 text=" ",
                                 grid=[1, 6],
                                 align="left")

        self.text_info = Text(self.window_config,
                              text="Default Graph Date Range",
                              color='blue',
                              grid=[1, 7],
                              align="top")

        self.text_start = Text(self.window_config,
                               text="         Start DateTime: ",
                               color='green',
                               grid=[1, 8],
                               align="left")

        self.textbox_start = TextBox(self.window_config,
                                     text="",
                                     width=20,
                                     grid=[1, 8],
                                     align="right")

        self.text_end = Text(self.window_config,
                             text="         End DateTime: ",
                             color='green',
                             grid=[1, 9],
                             align="left")

        self.textbox_end = TextBox(self.window_config,
                                   text="",
                                   width=20,
                                   grid=[1, 9],
                                   align="right")

        self.text_time_offset2 = Text(self.window_config,
                                      text="Graph DateTime Offset in Hours",
                                      color='blue',
                                      grid=[2, 1],
                                      align="bottom")

        self.textbox_time_offset = TextBox(self.window_config,
                                           text="",
                                           width="5",
                                           grid=[2, 2],
                                           align="bottom")

        self.text_sql_skip = Text(self.window_config,
                                  text="Add SQL row to Graph every 'X' rows",
                                  color='blue',
                                  grid=[2, 3],
                                  align="top")

        self.textbox_sql_skip = TextBox(self.window_config,
                                        text="",
                                        width="5",
                                        grid=[2, 4],
                                        align="top")

        self.text_temperature_offset = Text(self.window_config,
                                            text="Environment Temperature Offset in °C",
                                            color='blue',
                                            grid=[2, 5],
                                            align="top")

        self.textbox_temperature_offset = TextBox(self.window_config,
                                                  text="",
                                                  width="5",
                                                  grid=[2, 5],
                                                  align="bottom")

        self.text_network_timeouts = Text(self.window_config,
                                          text="Network Timeouts in Seconds",
                                          color='blue',
                                          grid=[2, 6],
                                          align="top")

        self.text_network_timeouts1 = Text(self.window_config,
                                           text="Sensor Status",
                                           color='green',
                                           grid=[2, 7],
                                           align="top")

        self.textbox_network_check = TextBox(self.window_config,
                                             text="",
                                             width="5",
                                             grid=[2, 8],
                                             align="top")

        self.text_network_timeouts2 = Text(self.window_config,
                                           text="Sensor Reports",
                                           color='green',
                                           grid=[2, 9],
                                           align="top")

        self.textbox_network_details = TextBox(self.window_config,
                                               text="",
                                               width="5",
                                               grid=[2, 10],
                                               align="top")

    def set_config(self):
        """ Sets the Configuration window to the provided settings. """
        self.textbox_save_to.value = self.current_config.save_to
        self.textbox_start.value = self.current_config.graph_start
        self.textbox_end.value = self.current_config.graph_end
        self.textbox_time_offset.value = self.current_config.datetime_offset
        self.textbox_sql_skip.value = self.current_config.sql_queries_skip
        self.textbox_temperature_offset.value = self.current_config.temperature_offset
        self.textbox_network_check.value = self.current_config.network_timeout_sensor_check
        self.textbox_network_details.value = self.current_config.network_timeout_data
        self.checkbox_power_controls.value = self.current_config.allow_advanced_controls

    def reset_to_defaults(self):
        """ Resets all Control Center Configurations to default. """
        control_center_logger.app_logger.info("Resetting Configuration to Defaults")
        self.current_config.reset_to_defaults()
        self.set_config()

    def _button_save_apply(self):
        pass

    def _button_save_to(self):
        """ Sets where the programs saves HTML graphs and Reports. """
        save_to = filedialog.askdirectory()

        if len(save_to) > 1:
            self.textbox_save_to.value = save_to + "/"
            control_center_logger.app_logger.debug("Changed Save to Directory")
        else:
            control_center_logger.app_logger.warning("Invalid Directory Chosen for Save to Directory")

    def _advanced_checkbox(self):
        """ Enables disabled buttons in the Control Center application. """
        if self.checkbox_power_controls.value == 1:
            self.button_reset.enable()
        else:
            self.button_reset.disable()
