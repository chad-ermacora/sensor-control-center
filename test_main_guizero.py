import unittest

import app_config
import app_graph
import app_reports

config_default = app_config.CreateDefaultConfigSettings()
config_original = app_config.get_from_file()
config_test = app_config.CreateDefaultConfigSettings()

save_to = config_default.script_directory + "/test_files/"
sensor_ip = "192.168.10.101"


class TestAppConfig(unittest.TestCase):

    def test_app_config(self):
        # This test section should be complete
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

    def test_app_graph(self):
        # Interval & Trigger graph's and functions done.  Only Live Graph left to do.
        # Test Plotly graphs
        test_graph_interval = app_graph.CreateGraphData()
        test_graph_interval.db_location = config_default.script_directory + "/test_files/SensorIntervalDatabase.sqlite"
        test_graph_interval.save_to = save_to
        test_graph_interval.sql_queries_skip = 0

        app_graph.start_graph_interval(test_graph_interval)

        test_graph_trigger = app_graph.CreateGraphData()
        test_graph_trigger.save_to = save_to
        test_graph_trigger.db_location = config_default.script_directory + "/test_files/SensorTriggerDatabase.sqlite"
        test_graph_trigger.graph_columns = ["DateTime", "SensorName", "IP", "Acc_X", "Acc_Y", "Acc_Z",
                                            "Mag_X", "Mag_Y", "Mag_Z", "Gyro_X", "Gyro_Y", "Gyro_Z"]

        app_graph.start_graph_trigger(test_graph_trigger)

        self.assertEqual(app_graph._adjust_interval_datetime("1984-10-10 10:00:00", -7), "1984-10-10 03:00:00")
        self.assertEqual(app_graph._adjust_trigger_datetime("1984-10-10 10:00:00.111", -7), "1984-10-10 03:00:00.111")

    def test_app_reports(self):
        # Done, but requires an online sensor at provided IP & a quick glance at the generated reports and Graphs
        print("This REQUIRES an online sensor @ " + sensor_ip)
        self.assertEqual(app_reports.convert_minutes_string(7634), "5 Days / 7.14 Hours")

        config_test.save_to = save_to

        app_reports.sensor_html_report(app_reports.CreateHTMLSystemData(config_test), [sensor_ip])
        app_reports.sensor_html_report(app_reports.CreateHTMLConfigData(config_test), [sensor_ip])
        app_reports.sensor_html_report(app_reports.CreateHTMLReadingsData(config_test), [sensor_ip])

    def test_app_sensor_commands(self):
        # I need to figure out how to create a "Virtual" sensor, as I don't want to run all commands on a live one...
        pass


if __name__ == '__main__':
    unittest.main()
