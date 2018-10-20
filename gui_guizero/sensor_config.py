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
from guizero import Window, CheckBox, PushButton, Text, TextBox, info
from sensor_commands import set_sensor_config


class CreateSensorConfigWindow:
    def __init__(self, app):
        self.window_sensor_config = Window(app,
                                           title="Sensors Configuration Updater",
                                           width=340,
                                           height=265,
                                           layout="grid",
                                           visible=True)

        self.text_select = Text(self.window_sensor_config,
                                text="Check Sensor IPs from the Main Window",
                                grid=[1, 1, 3, 1],
                                color='#CB0000',
                                align="left")

        self.checkbox_db_record = CheckBox(self.window_sensor_config,
                                           text="Enable Database Recording",
                                           command=self._recording_checkbox,
                                           grid=[1, 2, 2, 1],
                                           align="left")

        self.textbox_interval = TextBox(self.window_sensor_config,
                                        text='300',
                                        width=10,
                                        grid=[1, 3],
                                        align="left")

        self.text_interval = Text(self.window_sensor_config,
                                  text="Seconds Between Interval Recording",
                                  color='green',
                                  grid=[2, 3],
                                  align="left")

        self.textbox_trigger = TextBox(self.window_sensor_config,
                                       text='0.15',
                                       width=10,
                                       grid=[1, 4],
                                       align="left")

        self.text_trigger = Text(self.window_sensor_config,
                                 text="Seconds Between Trigger Readings",
                                 color='green',
                                 grid=[2, 4],
                                 align="left")

        self.checkbox_custom = CheckBox(self.window_sensor_config,
                                        text="Enable Custom Variances",
                                        command=self._custom_checkbox,
                                        grid=[1, 5, 2, 1],
                                        align="left")

        self.textbox_custom_acc = TextBox(self.window_sensor_config,
                                          text='0.05',
                                          width=10,
                                          grid=[1, 6],
                                          align="left")

        self.text_custom_acc = Text(self.window_sensor_config,
                                    text="Accelerometer Variance",
                                    color='green',
                                    grid=[2, 6],
                                    align="left")

        self.textbox_custom_mag = TextBox(self.window_sensor_config,
                                          text='300',
                                          width=10,
                                          grid=[1, 7],
                                          align="left")

        self.text_custom_mag = Text(self.window_sensor_config,
                                    text="Magnetometer Variance",
                                    color='green',
                                    grid=[2, 7],
                                    align="left")

        self.textbox_custom_gyro = TextBox(self.window_sensor_config,
                                           text='0.05',
                                           width=10,
                                           grid=[1, 8],
                                           align="left")

        self.text_custom_gyro = Text(self.window_sensor_config,
                                     text="Gyroscopic Variance",
                                     color='green',
                                     grid=[2, 8],
                                     align="left")

        self.button_set_config = PushButton(self.window_sensor_config,
                                            text="Apply Sensor\nConfiguration",
                                            command=self.config_set,
                                            grid=[2, 14],
                                            align="right")

    def _recording_checkbox(self):
        """ Enables or disables the timing Sensor Configuration Window text boxes. """
        if self.checkbox_db_record.value:
            self.textbox_interval.enable()
            self.textbox_trigger.enable()
        else:
            self.textbox_interval.disable()
            self.textbox_trigger.disable()

    def _custom_checkbox(self):
        """ Enables or disables the custom Sensor Configuration Window text boxes. """
        if self.checkbox_custom.value:
            self.textbox_custom_acc.enable()
            self.textbox_custom_mag.enable()
            self.textbox_custom_gyro.enable()
        else:
            self.textbox_custom_acc.disable()
            self.textbox_custom_mag.disable()
            self.textbox_custom_gyro.disable()

    def config_set(self, ip_list):
        """ Sends the update configuration command to the Sensor Units IP, along with the new configuration. """
        config_settings_str = "," + str(self.checkbox_db_record.value) + "," + \
                              str(self.textbox_interval.value) + "," + \
                              str(self.textbox_trigger.value) + "," + \
                              str(self.checkbox_custom.value) + "," + \
                              str(self.textbox_custom_acc.value) + "," + \
                              str(self.textbox_custom_mag.value) + "," + \
                              str(self.textbox_custom_gyro.value)

        for ip in ip_list:
            set_sensor_config(ip, config_settings_str)

        info("Sensors Configuration Set", "Configurations Set")

    def enable_set_config_button(self):
        self.button_set_config.enable()

    def disable_set_config_button(self):
        self.button_set_config.disable()
