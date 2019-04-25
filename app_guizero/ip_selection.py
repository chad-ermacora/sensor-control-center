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
from queue import Queue
from threading import Thread
from app_modules import app_logger
from app_modules import sensor_commands as app_sensor_commands


class CreateIPSelector:
    """ Creates the main window IP selections section. """

    def __init__(self, app, current_config):
        self.current_config = current_config
        self.data_queue = Queue()

        # Sensor's Online / Offline IP List Selection 1
        self.app_checkbox_all_column1 = guizero.CheckBox(app,
                                                         text="Check ALL Column 1",
                                                         command=self._app_check_all_ip1,
                                                         grid=[1, 1, 3, 1],
                                                         align="left")

        self.app_checkbox_ip1 = guizero.CheckBox(app,
                                                 text="IP        ",
                                                 grid=[1, 2],
                                                 align="left")

        self.app_textbox_ip1 = guizero.TextBox(app,
                                               text="192.168.10.11",
                                               width=21,
                                               grid=[2, 2],
                                               align="left")

        self.app_checkbox_ip2 = guizero.CheckBox(app,
                                                 text="IP ",
                                                 grid=[1, 3],
                                                 align="left")

        self.app_textbox_ip2 = guizero.TextBox(app,
                                               text="192.168.10.12",
                                               width=21,
                                               grid=[2, 3],
                                               align="left")

        self.app_checkbox_ip3 = guizero.CheckBox(app,
                                                 text="IP ",
                                                 grid=[1, 4],
                                                 align="left")

        self.app_textbox_ip3 = guizero.TextBox(app,
                                               text="192.168.10.13",
                                               width=21,
                                               grid=[2, 4],
                                               align="left")

        self.app_checkbox_ip4 = guizero.CheckBox(app,
                                                 text="IP ",
                                                 grid=[1, 5],
                                                 align="left")

        self.app_textbox_ip4 = guizero.TextBox(app,
                                               text="192.168.10.14",
                                               width=21,
                                               grid=[2, 5],
                                               align="left")

        self.app_checkbox_ip5 = guizero.CheckBox(app,
                                                 text="IP ",
                                                 grid=[1, 6],
                                                 align="left")

        self.app_textbox_ip5 = guizero.TextBox(app,
                                               text="192.168.10.15",
                                               width=21,
                                               grid=[2, 6],
                                               align="left")

        self.app_checkbox_ip6 = guizero.CheckBox(app,
                                                 text="IP ",
                                                 grid=[1, 7],
                                                 align="left")

        self.app_textbox_ip6 = guizero.TextBox(app,
                                               text="192.168.10.16",
                                               width=21,
                                               grid=[2, 7],
                                               align="left")

        self.app_checkbox_ip7 = guizero.CheckBox(app,
                                                 text="IP ",
                                                 grid=[1, 8],
                                                 align="left")

        self.app_textbox_ip7 = guizero.TextBox(app,
                                               text="192.168.10.17",
                                               width=21,
                                               grid=[2, 8],
                                               align="left")

        self.app_checkbox_ip8 = guizero.CheckBox(app,
                                                 text="IP ",
                                                 grid=[1, 9],
                                                 align="left")

        self.app_textbox_ip8 = guizero.TextBox(app,
                                               text="192.168.10.18",
                                               width=21,
                                               grid=[2, 9],
                                               align="left")

        # Sensor's Online / Offline IP List Selection 2
        self.app_checkbox_all_column2 = guizero.CheckBox(app,
                                                         text="Check ALL Column 2",
                                                         command=self._app_check_all_ip2,
                                                         grid=[3, 1, 3, 1],
                                                         align="left")

        self.app_checkbox_ip9 = guizero.CheckBox(app,
                                                 text="IP        ",
                                                 grid=[3, 2],
                                                 align="left")

        self.app_textbox_ip9 = guizero.TextBox(app,
                                               text="192.168.10.19",
                                               width=21,
                                               grid=[4, 2],
                                               align="left")

        self.app_checkbox_ip10 = guizero.CheckBox(app,
                                                  text="IP ",
                                                  grid=[3, 3],
                                                  align="left")

        self.app_textbox_ip10 = guizero.TextBox(app,
                                                text="192.168.10.20",
                                                width=21,
                                                grid=[4, 3],
                                                align="left")

        self.app_checkbox_ip11 = guizero.CheckBox(app,
                                                  text="IP ",
                                                  grid=[3, 4],
                                                  align="left")

        self.app_textbox_ip11 = guizero.TextBox(app,
                                                text="192.168.10.21",
                                                width=21,
                                                grid=[4, 4],
                                                align="left")

        self.app_checkbox_ip12 = guizero.CheckBox(app,
                                                  text="IP ",
                                                  grid=[3, 5],
                                                  align="left")

        self.app_textbox_ip12 = guizero.TextBox(app,
                                                text="192.168.10.22",
                                                width=21,
                                                grid=[4, 5],
                                                align="left")

        self.app_checkbox_ip13 = guizero.CheckBox(app,
                                                  text="IP ",
                                                  grid=[3, 6],
                                                  align="left")

        self.app_textbox_ip13 = guizero.TextBox(app,
                                                text="192.168.10.23",
                                                width=21,
                                                grid=[4, 6],
                                                align="left")

        self.app_checkbox_ip14 = guizero.CheckBox(app,
                                                  text="IP ",
                                                  grid=[3, 7],
                                                  align="left")

        self.app_textbox_ip14 = guizero.TextBox(app,
                                                text="192.168.10.24",
                                                width=21,
                                                grid=[4, 7],
                                                align="left")

        self.app_checkbox_ip15 = guizero.CheckBox(app,
                                                  text="IP ",
                                                  grid=[3, 8],
                                                  align="left")

        self.app_textbox_ip15 = guizero.TextBox(app,
                                                text="192.168.10.25",
                                                width=21,
                                                grid=[4, 8],
                                                align="left")

        self.app_checkbox_ip16 = guizero.CheckBox(app,
                                                  text="IP ",
                                                  grid=[3, 9],
                                                  align="left")

        self.app_textbox_ip16 = guizero.TextBox(app,
                                                text="192.168.10.26",
                                                width=21,
                                                grid=[4, 9],
                                                align="left")

        # Window Tweaks
        self.app_checkbox_all_column1.value = 0
        self.app_checkbox_all_column2.value = 0
        self._app_check_all_ip1()
        self._app_check_all_ip2()
        self.app_checkbox_ip1.value = 1

    def _app_check_all_ip1(self):
        """ Check or uncheck all IP checkboxes on the 1st column. """
        if self.app_checkbox_all_column1.value == 1:
            self.app_checkbox_ip1.value = 1
            self.app_checkbox_ip2.value = 1
            self.app_checkbox_ip3.value = 1
            self.app_checkbox_ip4.value = 1
            self.app_checkbox_ip5.value = 1
            self.app_checkbox_ip6.value = 1
            self.app_checkbox_ip7.value = 1
            self.app_checkbox_ip8.value = 1
        elif self.app_checkbox_all_column1.value == 0:
            self.app_checkbox_ip1.value = 0
            self.app_checkbox_ip2.value = 0
            self.app_checkbox_ip3.value = 0
            self.app_checkbox_ip4.value = 0
            self.app_checkbox_ip5.value = 0
            self.app_checkbox_ip6.value = 0
            self.app_checkbox_ip7.value = 0
            self.app_checkbox_ip8.value = 0

    def _app_check_all_ip2(self):
        """ Check or uncheck all IP checkboxes on the 2nd column. """
        if self.app_checkbox_all_column2.value == 1:
            self.app_checkbox_ip9.value = 1
            self.app_checkbox_ip10.value = 1
            self.app_checkbox_ip11.value = 1
            self.app_checkbox_ip12.value = 1
            self.app_checkbox_ip13.value = 1
            self.app_checkbox_ip14.value = 1
            self.app_checkbox_ip15.value = 1
            self.app_checkbox_ip16.value = 1
        elif self.app_checkbox_all_column2.value == 0:
            self.app_checkbox_ip9.value = 0
            self.app_checkbox_ip10.value = 0
            self.app_checkbox_ip11.value = 0
            self.app_checkbox_ip12.value = 0
            self.app_checkbox_ip13.value = 0
            self.app_checkbox_ip14.value = 0
            self.app_checkbox_ip15.value = 0
            self.app_checkbox_ip16.value = 0

    def set_ip_list(self, new_config):
        """ Sets GUI IP text boxes from the provided configuration file. """
        self.app_textbox_ip1.value = new_config.ip_list[0]
        self.app_textbox_ip2.value = new_config.ip_list[1]
        self.app_textbox_ip3.value = new_config.ip_list[2]
        self.app_textbox_ip4.value = new_config.ip_list[3]
        self.app_textbox_ip5.value = new_config.ip_list[4]
        self.app_textbox_ip6.value = new_config.ip_list[5]
        self.app_textbox_ip7.value = new_config.ip_list[6]
        self.app_textbox_ip8.value = new_config.ip_list[7]
        self.app_textbox_ip9.value = new_config.ip_list[8]
        self.app_textbox_ip10.value = new_config.ip_list[9]
        self.app_textbox_ip11.value = new_config.ip_list[10]
        self.app_textbox_ip12.value = new_config.ip_list[11]
        self.app_textbox_ip13.value = new_config.ip_list[12]
        self.app_textbox_ip14.value = new_config.ip_list[13]
        self.app_textbox_ip15.value = new_config.ip_list[14]
        self.app_textbox_ip16.value = new_config.ip_list[15]

    def get_all_ip_list(self):
        """ Returns a list of all GUI text box IP's """
        checkbox_ip_list = [self.app_textbox_ip1.value,
                            self.app_textbox_ip2.value,
                            self.app_textbox_ip3.value,
                            self.app_textbox_ip4.value,
                            self.app_textbox_ip5.value,
                            self.app_textbox_ip6.value,
                            self.app_textbox_ip7.value,
                            self.app_textbox_ip8.value,
                            self.app_textbox_ip9.value,
                            self.app_textbox_ip10.value,
                            self.app_textbox_ip11.value,
                            self.app_textbox_ip12.value,
                            self.app_textbox_ip13.value,
                            self.app_textbox_ip14.value,
                            self.app_textbox_ip15.value,
                            self.app_textbox_ip16.value]

        app_logger.app_logger.debug("IP List Generated from All Boxes")

        return checkbox_ip_list

    def _worker_sensor_check(self, ip):
        """ Used in Threads.  Socket connects to sensor by IP's in queue. Puts results in a data queue. """
        data = [ip, app_sensor_commands.check_sensor_status(ip, self.current_config.network_timeout_sensor_check)]
        self.data_queue.put(data)

    def get_verified_ip_list(self):
        """
        Checks sensor online status and changes the programs IP textbox depending on the returned results.

        The sensor checks are Threaded by the IP's provided in the IP list.
        """
        ip_list = self._make_ip_list()
        ip_list_final = []
        sensor_data_pool = []
        threads = []

        for ip in ip_list:
            threads.append(Thread(target=self._worker_sensor_check, args=[ip]))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        while not self.data_queue.empty():
            sensor_data_pool.append(self.data_queue.get())
            self.data_queue.task_done()

        sensor_data_pool.sort()

        for data in sensor_data_pool:
            ip = data[0]
            sensor_status = data[1]

            if sensor_status == "Online":
                var_colour = "#7CFC00"
                var_checkbox = 1
            else:
                var_colour = "red"
                var_checkbox = 0

            if var_checkbox == 1:
                ip_list_final.append(ip)

            if ip == self.app_textbox_ip1.value:
                self.app_checkbox_ip1.text = sensor_status
                self.app_textbox_ip1.bg = var_colour
                self.app_checkbox_ip1.value = var_checkbox
            elif ip == self.app_textbox_ip2.value:
                self.app_checkbox_ip2.text = sensor_status
                self.app_textbox_ip2.bg = var_colour
                self.app_checkbox_ip2.value = var_checkbox
            elif ip == self.app_textbox_ip3.value:
                self.app_checkbox_ip3.text = sensor_status
                self.app_textbox_ip3.bg = var_colour
                self.app_checkbox_ip3.value = var_checkbox
            elif ip == self.app_textbox_ip4.value:
                self.app_checkbox_ip4.text = sensor_status
                self.app_textbox_ip4.bg = var_colour
                self.app_checkbox_ip4.value = var_checkbox
            elif ip == self.app_textbox_ip5.value:
                self.app_checkbox_ip5.text = sensor_status
                self.app_textbox_ip5.bg = var_colour
                self.app_checkbox_ip5.value = var_checkbox
            elif ip == self.app_textbox_ip6.value:
                self.app_checkbox_ip6.text = sensor_status
                self.app_textbox_ip6.bg = var_colour
                self.app_checkbox_ip6.value = var_checkbox
            elif ip == self.app_textbox_ip7.value:
                self.app_checkbox_ip7.text = sensor_status
                self.app_textbox_ip7.bg = var_colour
                self.app_checkbox_ip7.value = var_checkbox
            elif ip == self.app_textbox_ip8.value:
                self.app_checkbox_ip8.text = sensor_status
                self.app_textbox_ip8.bg = var_colour
                self.app_checkbox_ip8.value = var_checkbox
            elif ip == self.app_textbox_ip9.value:
                self.app_checkbox_ip9.text = sensor_status
                self.app_textbox_ip9.bg = var_colour
                self.app_checkbox_ip9.value = var_checkbox
            elif ip == self.app_textbox_ip10.value:
                self.app_checkbox_ip10.text = sensor_status
                self.app_textbox_ip10.bg = var_colour
                self.app_checkbox_ip10.value = var_checkbox
            elif ip == self.app_textbox_ip11.value:
                self.app_checkbox_ip11.text = sensor_status
                self.app_textbox_ip11.bg = var_colour
                self.app_checkbox_ip11.value = var_checkbox
            elif ip == self.app_textbox_ip12.value:
                self.app_checkbox_ip12.text = sensor_status
                self.app_textbox_ip12.bg = var_colour
                self.app_checkbox_ip12.value = var_checkbox
            elif ip == self.app_textbox_ip13.value:
                self.app_checkbox_ip13.text = sensor_status
                self.app_textbox_ip13.bg = var_colour
                self.app_checkbox_ip13.value = var_checkbox
            elif ip == self.app_textbox_ip14.value:
                self.app_checkbox_ip14.text = sensor_status
                self.app_textbox_ip14.bg = var_colour
                self.app_checkbox_ip14.value = var_checkbox
            elif ip == self.app_textbox_ip15.value:
                self.app_checkbox_ip15.text = sensor_status
                self.app_textbox_ip15.bg = var_colour
                self.app_checkbox_ip15.value = var_checkbox
            elif ip == self.app_textbox_ip16.value:
                self.app_checkbox_ip16.text = sensor_status
                self.app_textbox_ip16.bg = var_colour
                self.app_checkbox_ip16.value = var_checkbox

        sensor_data_pool.clear()
        app_logger.app_logger.debug("Checked IP's Processed")

        return ip_list_final

    def _make_ip_list(self):
        """ Returns checked IP's skipping duplicates and sets unselected IP backgrounds to white """
        checked_ip_addresses = set()

        if self.app_checkbox_ip1.value:
            checked_ip_addresses.add(self.app_textbox_ip1.value)
        else:
            self.app_textbox_ip1.bg = 'white'

        if self.app_checkbox_ip2.value:
            checked_ip_addresses.add(self.app_textbox_ip2.value)
        else:
            self.app_textbox_ip2.bg = 'white'

        if self.app_checkbox_ip3.value:
            checked_ip_addresses.add(self.app_textbox_ip3.value)
        else:
            self.app_textbox_ip3.bg = 'white'

        if self.app_checkbox_ip4.value:
            checked_ip_addresses.add(self.app_textbox_ip4.value)
        else:
            self.app_textbox_ip4.bg = 'white'

        if self.app_checkbox_ip5.value:
            checked_ip_addresses.add(self.app_textbox_ip5.value)
        else:
            self.app_textbox_ip5.bg = 'white'

        if self.app_checkbox_ip6.value:
            checked_ip_addresses.add(self.app_textbox_ip6.value)
        else:
            self.app_textbox_ip6.bg = 'white'

        if self.app_checkbox_ip7.value:
            checked_ip_addresses.add(self.app_textbox_ip7.value)
        else:
            self.app_textbox_ip7.bg = 'white'

        if self.app_checkbox_ip8.value:
            checked_ip_addresses.add(self.app_textbox_ip8.value)
        else:
            self.app_textbox_ip8.bg = 'white'

        if self.app_checkbox_ip9.value:
            checked_ip_addresses.add(self.app_textbox_ip9.value)
        else:
            self.app_textbox_ip9.bg = 'white'

        if self.app_checkbox_ip10.value:
            checked_ip_addresses.add(self.app_textbox_ip10.value)
        else:
            self.app_textbox_ip10.bg = 'white'

        if self.app_checkbox_ip11.value:
            checked_ip_addresses.add(self.app_textbox_ip11.value)
        else:
            self.app_textbox_ip11.bg = 'white'

        if self.app_checkbox_ip12.value:
            checked_ip_addresses.add(self.app_textbox_ip12.value)
        else:
            self.app_textbox_ip12.bg = 'white'

        if self.app_checkbox_ip13.value:
            checked_ip_addresses.add(self.app_textbox_ip13.value)
        else:
            self.app_textbox_ip13.bg = 'white'

        if self.app_checkbox_ip14.value:
            checked_ip_addresses.add(self.app_textbox_ip14.value)
        else:
            self.app_textbox_ip14.bg = 'white'

        if self.app_checkbox_ip15.value:
            checked_ip_addresses.add(self.app_textbox_ip15.value)
        else:
            self.app_textbox_ip15.bg = 'white'

        if self.app_checkbox_ip16.value:
            checked_ip_addresses.add(self.app_textbox_ip16.value)
        else:
            self.app_textbox_ip16.bg = 'white'

        app_logger.app_logger.debug("IP List Generated from Checked Boxes")

        return checked_ip_addresses
