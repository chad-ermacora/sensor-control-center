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
import os
import unittest
from time import sleep

import app_modules.app_config as app_config
import app_modules.app_useful as app_useful
import app_modules.app_graph as app_graph
import app_modules.app_graph_plotly as app_graph_plotly
import app_modules.app_reports as app_reports
import app_modules.app_sensor_commands as app_sensor_commands

config_default = app_config.CreateDefaultConfigSettings()
config_original = app_config.get_from_file()
config_test = app_config.CreateDefaultConfigSettings()

save_to = config_default.script_directory + "/test_files/output/"
sensor_ip = "192.168.10.101"
test_datetime = "2011-11-20 14:45:05"


class TestApp(unittest.TestCase):

    # has _1_ to make sure it runs first
    def test_1_clean_old_test_files(self):
        delete_files = [save_to + "PlotlySensorGraph.html",
                        save_to + "SensorsSystemReport.html",
                        save_to + "SensorsConfigReport.html",
                        save_to + "SensorsReadingsReport.html",
                        save_to + sensor_ip[-3:].replace(".", "_") + "PrimaryLog.txt",
                        save_to + sensor_ip[-3:].replace(".", "_") + "NetworkLog.txt",
                        save_to + sensor_ip[-3:].replace(".", "_") + "SensorsLog.txt"]
        for file in delete_files:
            try:
                os.remove(file)
                print("\nRemoved OK: " + file)
            except FileNotFoundError:
                print("\nFile Not Found: " + file)

        for file in delete_files:
            self.assertFalse(os.path.isfile(file))

    def test_app_config(self):
        # Initial setup complete
        config_test.graph_start = "1984-11-01 11:22:12"
        config_test.graph_end = "3333-04-04 11:22:12"
        config_test.datetime_offset = 4.0
        config_test.sql_queries_skip = 1
        config_test.temperature_offset = -8.0
        config_test.live_refresh = 10
        config_test.network_timeout_sensor_check = 9
        config_test.network_timeout_data = 12
        config_test.allow_config_reset = 1
        config_test.ip_list = ["192.168.77.11", "192.168.77.12", "192.168.77.13", "192.168.77.14",
                               "192.168.77.15", "192.168.77.16", "192.168.77.17", "192.168.77.18",
                               "192.168.77.19", "192.168.77.20", "192.168.77.21", "192.168.77.22",
                               "192.168.77.23", "192.168.77.24", "192.168.77.25", "192.168.77.26"]

        app_config.save_config_to_file(config_test)
        new_config = app_config.get_from_file()

        self.assertEqual(new_config.save_to, config_test.save_to)
        self.assertEqual(new_config.graph_start, config_test.graph_start)
        self.assertEqual(new_config.graph_end, config_test.graph_end)
        self.assertEqual(new_config.live_refresh, config_test.live_refresh)
        self.assertEqual(new_config.datetime_offset, config_test.datetime_offset)
        self.assertEqual(new_config.sql_queries_skip, config_test.sql_queries_skip)
        self.assertEqual(new_config.temperature_offset, config_test.temperature_offset)
        self.assertEqual(new_config.live_refresh, config_test.live_refresh)
        self.assertEqual(new_config.network_timeout_sensor_check, config_test.network_timeout_sensor_check)
        self.assertEqual(new_config.network_timeout_data, config_test.network_timeout_data)
        self.assertEqual(new_config.allow_config_reset, config_test.allow_config_reset)
        self.assertEqual(new_config.ip_list, config_test.ip_list)

        config_test.reset_to_defaults()

        self.assertEqual(config_default.save_to, config_test.save_to)
        self.assertEqual(config_default.graph_start, config_test.graph_start)
        self.assertEqual(config_default.graph_end, config_test.graph_end)
        self.assertEqual(config_default.live_refresh, config_test.live_refresh)
        self.assertEqual(config_default.datetime_offset, config_test.datetime_offset)
        self.assertEqual(config_default.sql_queries_skip, config_test.sql_queries_skip)
        self.assertEqual(config_default.temperature_offset, config_test.temperature_offset)
        self.assertEqual(config_default.live_refresh, config_test.live_refresh)
        self.assertEqual(config_default.network_timeout_sensor_check, config_test.network_timeout_sensor_check)
        self.assertEqual(config_default.network_timeout_data, config_test.network_timeout_data)
        self.assertEqual(config_default.allow_config_reset, config_test.allow_config_reset)
        self.assertEqual(config_default.ip_list, config_test.ip_list)

        app_config.save_config_to_file(config_original)
        print("Configuration tests Complete")

    def test_app_graph(self):
        # Interval & Trigger graph's and functions done.  Only Live Graph left to do.
        print("\nPlease review the opened graph for errors.\n")
        test_graph = app_graph.CreateGraphData()
        test_graph.db_location = config_default.script_directory + "/test_files/SensorRecordingDatabase.sqlite"
        test_graph.save_to = save_to
        test_graph.sql_queries_skip = 0

        test_graph.graph_columns = ["DateTime", "SensorName", "IP", "SensorUpTime", "SystemTemp",
                                    "EnvironmentTemp", "Pressure", "Humidity", "Lumen", "Red", "Green", "Blue",
                                    "Acc_X", "Acc_Y", "Acc_Z", "Mag_X", "Mag_Y", "Mag_Z",
                                    "Gyro_X", "Gyro_Y", "Gyro_Z", "DateTime", "SensorName", "IP"]

        app_graph_plotly.start_plotly_graph(test_graph)

        self.assertTrue(os.path.isfile(save_to + "PlotlySensorGraph.html"))

        self.assertEqual(app_graph.adjust_datetime("1984-10-10 10:00:00", -7), "1984-10-10 03:00:00")
        self.assertEqual(app_graph.adjust_datetime("1984-10-10 10:00:00.111", -7), "1984-10-10 03:00:00.111")

    def test_app_reports(self):
        # # Initial setup complete - Requires a look over the generated reports by human
        print("\nThis REQUIRES an online sensor @ " + sensor_ip + "\nPlease review the 3 opened Reports for errors.")
        self.assertEqual(app_useful.convert_minutes_string(7634), "5 Days, 7 Hours & 14 Min")

        config_test.save_to = save_to

        app_reports.sensor_html_report(app_reports.CreateHTMLSystemData(config_test), [sensor_ip])
        app_reports.sensor_html_report(app_reports.CreateHTMLConfigData(config_test), [sensor_ip])
        app_reports.sensor_html_report(app_reports.CreateHTMLReadingsData(config_test), [sensor_ip])

        sleep(3)

        self.assertTrue(os.path.isfile(save_to + "SensorsSystemReport.html"))
        self.assertTrue(os.path.isfile(save_to + "SensorsConfigReport.html"))
        self.assertTrue(os.path.isfile(save_to + "SensorsReadingsReport.html"))

    def test_app_sensor_commands(self):
        print("\nThis REQUIRES an online sensor @ " + sensor_ip)
        get_network_commands = app_sensor_commands.CreateNetworkGetCommands()
        send_network_commands = app_sensor_commands.CreateNetworkSendCommands()
        network_timeout = config_default.network_timeout_data
        sensor_command = app_sensor_commands.CreateSensorNetworkCommand(sensor_ip, network_timeout, "")

        http_log_download = app_sensor_commands.CreateSensorNetworkCommand(sensor_ip, 2, "")
        http_log_download.save_to_location = save_to

        sensor_status = app_sensor_commands.check_sensor_status(sensor_ip, network_timeout)
        self.assertEqual(sensor_status, "Online")

        app_sensor_commands.download_logs(http_log_download)
        sleep(2)
        self.assertTrue(os.path.isfile(save_to + sensor_ip[-3:].replace(".", "_") + "PrimaryLog.txt"))
        self.assertTrue(os.path.isfile(save_to + sensor_ip[-3:].replace(".", "_") + "NetworkLog.txt"))
        self.assertTrue(os.path.isfile(save_to + sensor_ip[-3:].replace(".", "_") + "SensorsLog.txt"))

        sensor_command.command = get_network_commands.sensor_name
        old_hostname = app_sensor_commands.get_data(sensor_command)

        verified_bad_hostname = app_sensor_commands.get_validated_hostname("^^$##_###This.is$NOT-Good!**")
        self.assertEqual(verified_bad_hostname, "_________This_is_NOT_Good___")

        sensor_command.command = send_network_commands.set_host_name
        sensor_command.command_data = verified_bad_hostname
        app_sensor_commands.put_command(sensor_command)
        sensor_command.command = get_network_commands.sensor_name
        verify_hostname = app_sensor_commands.get_data(sensor_command)
        self.assertEqual(verify_hostname, verified_bad_hostname)

        sensor_command.command = send_network_commands.set_host_name
        sensor_command.command_data = old_hostname
        app_sensor_commands.put_command(sensor_command)
        sensor_command.command = get_network_commands.sensor_name
        verify_hostname = app_sensor_commands.get_data(sensor_command)
        self.assertEqual(verify_hostname, old_hostname)


if __name__ == '__main__':
    unittest.main()
