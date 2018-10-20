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
from guizero import Window, Text, TextBox
import app_config

app_version = "Tested on Python 3.7 / KootNet Sensors - PC Control Center / Ver. Alpha.20.1"


class CreateAboutWindow:
    def __init__(self, app):
        self.current_config = app_config.get_from_file()
        self.about_text = self.current_config.additional_files_directory + "/about_text.txt"

        self.window_app_about = Window(app,
                                       title="About KootNet Sensors - PC Control Center",
                                       width=610,
                                       height=325,
                                       layout="grid",
                                       visible=True)
        # About Window Section
        self.about_text1 = Text(self.window_app_about,
                                text=app_version,
                                grid=[1, 1],
                                align="right")

        self.about_textbox = TextBox(self.window_app_about,
                                     text="About",
                                     grid=[1, 2],
                                     width=75,
                                     height=18,
                                     multiline=True,
                                     align="right")
        self._set_about_text()

    def _set_about_text(self):
        """ Loads and sets the about text from file. """
        # try:
        local_file = open(self.about_text, 'r')
        new_text = local_file.read()
        local_file.close()
        self.about_textbox.value = new_text
        #     logger.debug("About Text Load - OK")
        # except Exception as error:
        #     logger.error("About Text Load - Failed: " + str(error))
