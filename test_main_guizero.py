import unittest

import app_config
import app_graph
import app_reports


class TestAppConfig(unittest.TestCase):

    def test_app_config(self):
        # This test section should be complete
        config_default = app_config.CreateDefaultConfigSettings()
        config_file = app_config.CreateDefaultConfigSettings()

        config_file.save_to = "C:/Users/OO-Dragon/Desktop/test"
        config_file.graph_start = "1984-11-01 11:22:12"
        config_file.graph_end = "3333-04-04 11:22:12"
        config_file.datetime_offset = 4.0
        config_file.sql_queries_skip = 1
        config_file.temperature_offset = -8.0
        config_file.live_refresh = 10
        config_file.network_timeout_sensor_check = 9
        config_file.network_timeout_data = 12
        config_file.allow_config_reset = 1
        config_file.ip_list = ["192.168.77.11", "192.168.77.12", "192.168.77.13", "192.168.77.14",
                               "192.168.77.15", "192.168.77.16", "192.168.77.17", "192.168.77.18",
                               "192.168.77.19", "192.168.77.20", "192.168.77.21", "192.168.77.22",
                               "192.168.77.23", "192.168.77.24", "192.168.77.25", "192.168.77.26"]

        app_config.save_config_to_file(config_file)
        new_config = app_config.get_from_file()

        self.assertEqual(new_config.save_to, config_file.save_to)
        self.assertEqual(new_config.graph_start, config_file.graph_start)
        self.assertEqual(new_config.graph_end, config_file.graph_end)
        self.assertEqual(new_config.live_refresh, config_file.live_refresh)
        self.assertEqual(new_config.datetime_offset, config_file.datetime_offset)
        self.assertEqual(new_config.sql_queries_skip, config_file.sql_queries_skip)
        self.assertEqual(new_config.temperature_offset, config_file.temperature_offset)
        self.assertEqual(new_config.live_refresh, config_file.live_refresh)
        self.assertEqual(new_config.network_timeout_sensor_check, config_file.network_timeout_sensor_check)
        self.assertEqual(new_config.network_timeout_data, config_file.network_timeout_data)
        self.assertEqual(new_config.allow_config_reset, config_file.allow_config_reset)
        self.assertEqual(new_config.ip_list, config_file.ip_list)

        config_file.reset_to_defaults()
        self.assertEqual(config_default.save_to, config_file.save_to)
        self.assertEqual(config_default.graph_start, config_file.graph_start)
        self.assertEqual(config_default.graph_end, config_file.graph_end)
        self.assertEqual(config_default.live_refresh, config_file.live_refresh)
        self.assertEqual(config_default.datetime_offset, config_file.datetime_offset)
        self.assertEqual(config_default.sql_queries_skip, config_file.sql_queries_skip)
        self.assertEqual(config_default.temperature_offset, config_file.temperature_offset)
        self.assertEqual(config_default.live_refresh, config_file.live_refresh)
        self.assertEqual(config_default.network_timeout_sensor_check, config_file.network_timeout_sensor_check)
        self.assertEqual(config_default.network_timeout_data, config_file.network_timeout_data)
        self.assertEqual(config_default.allow_config_reset, config_file.allow_config_reset)
        self.assertEqual(config_default.ip_list, config_file.ip_list)

        app_config.save_config_to_file(config_default)

    def test_app_graph(self):
        # This test section needs work
        self.assertEqual(app_graph._adjust_interval_datetime("1984-10-10 10:00:00", -7), "1984-10-10 03:00:00")
        self.assertEqual(app_graph._adjust_trigger_datetime("1984-10-10 10:00:00.111", -7), "1984-10-10 03:00:00.111")

    def test_app_logger(self):
        # This test section needs work
        pass

    def test_app_reports(self):
        # This test section needs work
        self.assertEqual(app_reports.convert_minutes_string(7634), "5 Days / 7.14 Hours")

    def test_app_sensor_commands(self):
        # This test section needs work
        pass


if __name__ == '__main__':
    unittest.main()
