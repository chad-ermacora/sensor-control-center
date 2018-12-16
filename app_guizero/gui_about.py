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

import app_modules.app_logger as app_logger
from app_modules.app_config import app_version


class CreateAboutWindow:
    """ Creates a GUI window for program & license information. """

    def __init__(self, app, current_config):
        self.current_config = current_config
        self.about_text = self.current_config.additional_files_directory + "/about_text.txt"

        self.window = Window(app,
                             title="About KootNet Sensors - Control Center",
                             width=610,
                             height=325,
                             layout="grid",
                             visible=False)

        self.about_text1 = Text(self.window,
                                text=app_version,
                                grid=[1, 1],
                                align="right")

        self.about_textbox = TextBox(self.window,
                                     text="About",
                                     grid=[1, 2],
                                     width=75,
                                     height=18,
                                     multiline=True,
                                     align="left")

        # Window Tweaks
        self.window.tk.resizable(False, False)
        self._set_about_text()
        self.about_textbox.disable()
        self.about_textbox.bg = "black"
        self.about_textbox.text_color = "white"

    def _set_about_text(self):
        """ Loads and sets the about text from file. """
        try:
            local_file = open(self.about_text, 'r')
            new_text = local_file.read()
            local_file.close()
            self.about_textbox.value = new_text
            app_logger.app_logger.debug("About Text Load - OK")
        except Exception as error:
            app_logger.app_logger.error("About Text Load - Failed: " + str(error))
