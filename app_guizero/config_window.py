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
from tkinter import filedialog, simpledialog
from app_modules import app_logger
from app_modules import app_config


class CreateConfigWindow:
    """ Creates a GUI window to configure the program. """

    def __init__(self, app, current_config, ip_selection):
        self.current_config = current_config
        self.ip_selection = ip_selection
        self.window = guizero.Window(app,
                                     title="Control Center Configuration",
                                     width=580,
                                     height=300,
                                     layout="grid",
                                     visible=False)

        self.button_reset = guizero.PushButton(self.window,
                                               text="Reset to\nDefaults",
                                               command=self._reset_to_defaults,
                                               grid=[1, 1],
                                               align="right")

        self.checkbox_power_controls = guizero.CheckBox(self.window,
                                                        text="Enable 'Reset to Defaults'",
                                                        command=self._enable_config_reset,
                                                        grid=[1, 1],
                                                        align="top")

        self.button_save_apply = guizero.PushButton(self.window,
                                                    text="Save",
                                                    command=self._button_save_apply,
                                                    grid=[1, 1],
                                                    align="left")

        self.text3 = guizero.Text(self.window,
                                  text="Save files to",
                                  color='blue',
                                  grid=[1, 2],
                                  align="left")

        self.textbox_save_to = guizero.TextBox(self.window,
                                               text='',
                                               width=50,
                                               grid=[1, 3],
                                               align="bottom")

        self.button_save_dir = guizero.PushButton(self.window,
                                                  text="Choose Folder",
                                                  command=self._button_save_to,
                                                  grid=[1, 4],
                                                  align="left")

        self.button_set_http_auth = guizero.PushButton(self.window,
                                                       text="Set Sensors Authentication",
                                                       command=self._update_http_authentication_credentials,
                                                       grid=[1, 4],
                                                       align="right")

        self.checkbox_enable_open_gl_plotly = guizero.CheckBox(self.window,
                                                               text="Render Plotly with OpenGL",
                                                               grid=[1, 5],
                                                               align="top")

        self.text_info = guizero.Text(self.window,
                                      text="Default graph date range",
                                      color='blue',
                                      grid=[1, 6],
                                      align="top")

        self.text_spacer3 = guizero.Text(self.window,
                                         text="YYYY-MM-DD HH:MM:SS",
                                         size=7,
                                         color='#CB0000',
                                         grid=[1, 7],
                                         align="right")

        self.text_start = guizero.Text(self.window,
                                       text="         Start DateTime: ",
                                       color='green',
                                       grid=[1, 8],
                                       align="left")

        self.textbox_start = guizero.TextBox(self.window,
                                             text="",
                                             width=20,
                                             grid=[1, 8],
                                             align="right")

        self.text_end = guizero.Text(self.window,
                                     text="         End DateTime: ",
                                     color='green',
                                     grid=[1, 9],
                                     align="left")

        self.textbox_end = guizero.TextBox(self.window,
                                           text="",
                                           width=20,
                                           grid=[1, 9],
                                           align="right")

        self.text_live_refresh = guizero.Text(self.window,
                                              text="Live graph refresh in seconds: ",
                                              color='green',
                                              grid=[1, 10],
                                              align="left")

        self.textbox_live_refresh = guizero.TextBox(self.window,
                                                    text="",
                                                    width=5,
                                                    grid=[1, 10],
                                                    align="right")

        self.text_database_time = guizero.Text(self.window,
                                               text="Sensor Databases are\nsaved in UTC 0",
                                               size=10,
                                               grid=[2, 1],
                                               color='#CB0000',
                                               align="top")

        self.text_time_offset2 = guizero.Text(self.window,
                                              text="DateTime offset in hours",
                                              color='blue',
                                              grid=[2, 1],
                                              align="bottom")

        self.textbox_time_offset = guizero.TextBox(self.window,
                                                   text="",
                                                   width="5",
                                                   grid=[2, 2],
                                                   align="bottom")

        self.text_sql_skip = guizero.Text(self.window,
                                          text="Graph sensor data every 'X' entries",
                                          color='blue',
                                          grid=[2, 3],
                                          align="top")

        self.textbox_sql_skip = guizero.TextBox(self.window,
                                                text="",
                                                width="5",
                                                grid=[2, 4],
                                                align="top")

        self.text_temperature_offset = guizero.Text(self.window,
                                                    text="Manual temperature offset in °C",
                                                    color='blue',
                                                    grid=[2, 4],
                                                    align="bottom")

        self.textbox_temperature_offset = guizero.TextBox(self.window,
                                                          text="",
                                                          width="5",
                                                          grid=[2, 5],
                                                          align="bottom")

        self.text_network_timeouts = guizero.Text(self.window,
                                                  text="Network timeouts in seconds",
                                                  color='blue',
                                                  grid=[2, 6],
                                                  align="top")

        self.text_network_timeouts1 = guizero.Text(self.window,
                                                   text="Sensor checks",
                                                   color='green',
                                                   grid=[2, 7],
                                                   align="top")

        self.textbox_network_check = guizero.TextBox(self.window,
                                                     text="",
                                                     width="5",
                                                     grid=[2, 8],
                                                     align="top")

        self.text_network_timeouts2 = guizero.Text(self.window,
                                                   text="Sensor data",
                                                   color='green',
                                                   grid=[2, 9],
                                                   align="top")

        self.textbox_network_details = guizero.TextBox(self.window,
                                                       text="",
                                                       width="5",
                                                       grid=[2, 10],
                                                       align="top")

        # Window Tweaks
        self.window.tk.resizable(False, False)
        self.set_config(self.current_config)
        self.textbox_save_to.disable()
        self._enable_config_reset()

    def get_config(self):
        """ Returns the current set configuration options. """
        new_config = self.current_config

        new_config.save_to = self.textbox_save_to.value
        new_config.graph_start = self.textbox_start.value
        new_config.graph_end = self.textbox_end.value
        new_config.datetime_offset = self.textbox_time_offset.value
        new_config.sql_queries_skip = self.textbox_sql_skip.value
        new_config.temperature_offset = self.textbox_temperature_offset.value
        new_config.network_timeout_sensor_check = self.textbox_network_check.value
        new_config.network_timeout_data = self.textbox_network_details.value
        new_config.allow_config_reset = self.checkbox_power_controls.value
        new_config.enable_plotly_webgl = self.checkbox_enable_open_gl_plotly.value

        return new_config

    def set_config(self, new_config):
        """ Sets the Configuration window to the provided settings. """
        app_config.check_config(new_config)

        self.textbox_save_to.value = new_config.save_to
        self.textbox_start.value = new_config.graph_start
        self.textbox_end.value = new_config.graph_end
        self.textbox_time_offset.value = new_config.datetime_offset
        self.textbox_live_refresh.value = new_config.live_refresh
        self.textbox_sql_skip.value = new_config.sql_queries_skip
        self.textbox_temperature_offset.value = new_config.temperature_offset
        self.textbox_network_check.value = new_config.network_timeout_sensor_check
        self.textbox_network_details.value = new_config.network_timeout_data
        self.checkbox_power_controls.value = new_config.allow_config_reset
        self.checkbox_enable_open_gl_plotly.value = new_config.enable_plotly_webgl

    def _reset_to_defaults(self):
        """ Resets all Control Center Configurations to default. """
        app_logger.app_logger.info("Resetting Configuration to Defaults")
        default_config = app_config.CreateDefaultConfigSettings()
        self.set_config(default_config)
        self._enable_config_reset()

    def save_ip_list(self):
        """ Saves the current configuration, which includes the main window IP addresses. """
        self.current_config.ip_list = self.ip_selection.get_all_ip_list()
        app_config.save_config_to_file(self.current_config)

    def _button_save_apply(self):
        """ Save the programs Configuration and IP list to file """
        app_logger.app_logger.debug("Applying Configuration & Saving to File")

        self.current_config.save_to = self.textbox_save_to.value
        self.current_config.graph_start = self.textbox_start.value
        self.current_config.graph_end = self.textbox_end.value
        self.current_config.datetime_offset = self.textbox_time_offset.value
        self.current_config.sql_queries_skip = self.textbox_sql_skip.value
        self.current_config.temperature_offset = self.textbox_temperature_offset.value
        self.current_config.live_refresh = self.textbox_live_refresh.value
        self.current_config.network_timeout_sensor_check = self.textbox_network_check.value
        self.current_config.network_timeout_data = self.textbox_network_details.value
        self.current_config.allow_config_reset = self.checkbox_power_controls.value
        self.current_config.ip_list = self.ip_selection.get_all_ip_list()
        self.current_config.enable_plotly_webgl = self.checkbox_enable_open_gl_plotly.value

        app_config.check_config(self.current_config)
        app_config.save_config_to_file(self.current_config)
        self.set_config(self.current_config)

    def _button_save_to(self):
        """ Sets where the programs saves HTML graphs and Reports. """
        save_to = filedialog.askdirectory()

        if len(save_to) > 1:
            self.textbox_save_to.value = save_to + "/"
            app_logger.app_logger.debug("Changed Save to Directory")
        else:
            app_logger.app_logger.warning("Invalid Directory Chosen for Save to Directory")

    def _update_http_authentication_credentials(self):
        new_username = simpledialog.askstring("HTTP User Auth", "New Username: ")
        new_password = simpledialog.askstring("HTTP User Auth", "New Password: ")

        if new_username is not None and new_password is not None:
            new_username = new_username.strip()
            new_password = new_password.strip()
            if new_username != "" and new_password != "":
                self.current_config.http_user = new_username
                self.current_config.http_password = new_password
                self._button_save_apply()
                guizero.info("Set HTTP Authentication", "Username & Password Set OK")
            else:
                guizero.warn("Unable to set HTTP Authentication", "Username & Password cannot be blank")
        else:
            guizero.warn("Unable to set HTTP Authentication", "Username & Password Cancelled")

    def _enable_config_reset(self):
        """ Enables disabled buttons in the Control Center application. """
        if self.checkbox_power_controls.value:
            self.button_reset.enable()
        else:
            self.button_reset.disable()
