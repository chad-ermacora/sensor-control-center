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
from sys import path

software_version = "Tested on Python 3.5 & 3.7 || KootNet Sensors - Control Center || Alpha.24.150"


class CreateSQLColumnsReadable:
    """ Creates an object to hold all human readable SQL column names. """

    def __init__(self):
        self.no_sensor = ""
        self.date_time = "Date & Time"
        self.sensor_name = "Sensor Name"
        self.ip = "IP"
        self.system_uptime = "Sensor Uptime"
        self.cpu_temp = "CPU Temperature"
        self.environmental_temp = "Env Temperature"
        self.pressure = "Pressure"
        self.humidity = "Humidity"
        self.lumen = "Lumen"
        self.colours = "Colours"
        self.accelerometer_xyz = "Accelerometer XYZ"
        self.magnetometer_xyz = "Magnetometer XYZ"
        self.gyroscope_xyz = "Gyroscope XYZ"


class CreateSQLColumnNames:
    """ Creates an object to hold all SQL column names. """

    def __init__(self):
        self.sql_interval_table = "IntervalData"
        self.sql_trigger_table = "TriggerData"
        self.sql_other_table = "OtherData"
        self.date_time = "DateTime"
        self.sensor_name = "SensorName"
        self.ip = "IP"
        self.system_uptime = "SensorUpTime"
        self.cpu_temp = "SystemTemp"
        self.environmental_temp = "EnvironmentTemp"
        self.environmental_temp_offset = "EnvTempOffset"
        self.pressure = "Pressure"
        self.humidity = "Humidity"
        self.lumen = "Lumen"
        self.rgb = ["Red", "Green", "Blue"]
        self.six_chan_color = ["Red", "Orange", "Yellow", "Green", "Blue", "Violet"]
        self.accelerometer_xyz = ["Acc_X", "Acc_Y", "Acc_Z"]
        self.magnetometer_xyz = ["Mag_X", "Mag_Y", "Mag_Z"]
        self.gyroscope_xyz = ["Gyro_X", "Gyro_Y", "Gyro_Z"]

        self.other_notes = "Notes"
        self.other_user_datetime = "UserDateTime"


class CreateMeasurementsTypes:
    """ Creates an object to hold all sensor measurement types. """

    def __init__(self):
        self.no_measurement = ""
        self.celsius = " °C"
        self.pressure = " hPa"
        self.humidity = " %RH"
        self.lumen = " Lumen"
        self.rgb = " RGB"
        self.six_chan_color = " ROYGBV"
        self.xyz = " XYZ"


class CreateGraphData:
    """ Creates an object to hold all the data needed for a graph. """

    def __init__(self):
        self.enable_plotly_webgl = False
        self.db_location = ""
        self.graph_table = "IntervalData"
        self.save_to = ""
        self.graph_start = "1111-08-21 00:00:01"
        self.graph_end = "9999-01-01 00:00:01"
        self.datetime_offset = 0.0
        self.sql_queries_skip = 12
        self.bypass_sql_skip = False
        self.enable_custom_temp_offset = True
        self.temperature_offset = 0.0

        self.sub_plots = []
        self.row_count = 0
        self.graph_collection = []

        self.graph_columns = ["DateTime", "SensorName", "SensorUpTime", "IP", "SystemTemp",
                              "EnvironmentTemp", "EnvTempOffset", "Pressure", "Humidity", "Lumen",
                              "Red", "Orange", "Yellow", "Green", "Blue", "Violet"]
        self.max_sql_queries = 200000

        # Graph data holders for SQL DataBase
        self.sql_time = []
        self.sql_ip = []
        self.sql_host_name = []
        self.sql_up_time = []
        self.sql_cpu_temp = []
        self.sql_hat_temp = []
        self.sql_temp_offset = []
        self.sql_pressure = []
        self.sql_humidity = []
        self.sql_lumen = []
        self.sql_red = []
        self.sql_orange = []
        self.sql_yellow = []
        self.sql_green = []
        self.sql_blue = []
        self.sql_violet = []
        self.sql_acc_x = []
        self.sql_acc_y = []
        self.sql_acc_z = []
        self.sql_mg_x = []
        self.sql_mg_y = []
        self.sql_mg_z = []
        self.sql_gyro_x = []
        self.sql_gyro_y = []
        self.sql_gyro_z = []


class CreateNetworkGetCommands:
    """ Create a object instance holding available network "Get" commands (AKA expecting data back). """
    def __init__(self):
        self.sensor_sql_database = "DownloadSQLDatabase"
        self.sensor_configuration = "GetConfigurationReport"
        self.sensor_configuration_file = "GetConfiguration"
        self.installed_sensors_file = "GetInstalledSensors"
        self.wifi_config_file = "GetWifiConfiguration"
        self.variance_config = "GetVarianceConfiguration"
        self.system_data = "GetSystemData"
        self.primary_log = "GetPrimaryLog"
        self.network_log = "GetNetworkLog"
        self.sensors_log = "GetSensorsLog"
        self.download_primary_log = "DownloadPrimaryLog"
        self.download_network_log = "DownloadNetworkLog"
        self.download_sensors_log = "DownloadSensorsLog"
        self.sensor_readings = "GetSensorReadings"
        self.sensor_name = "GetHostName"
        self.system_uptime = "GetSystemUptime"
        self.cpu_temp = "GetCPUTemperature"
        self.environmental_temp = "GetEnvTemperature"
        self.env_temp_offset = "GetTempOffsetEnv"
        self.pressure = "GetPressure"
        self.humidity = "GetHumidity"
        self.lumen = "GetLumen"
        self.rgb = "GetEMS"
        self.accelerometer_xyz = "GetAccelerometerXYZ"
        self.magnetometer_xyz = "GetMagnetometerXYZ"
        self.gyroscope_xyz = "GetGyroscopeXYZ"
        self.database_notes = "GetDatabaseNotes"
        self.database_note_dates = "GetDatabaseNoteDates"
        self.database_user_note_dates = "GetDatabaseNoteUserDates"


class CreateNetworkSendCommands:
    """ Create a object instance holding available network "Send" commands (AKA not expecting data back). """
    def __init__(self):
        self.restart_services = "RestartServices"
        self.shutdown_system = "ShutdownSystem"
        self.reboot_system = "RebootSystem"
        self.upgrade_system_os = "UpgradeSystemOS"
        self.upgrade_online = "UpgradeOnline"
        self.upgrade_smb = "UpgradeSMB"
        self.clean_upgrade_online = "CleanOnline"
        self.clean_upgrade_smb = "CleanSMB"
        self.set_host_name = "SetHostName"
        self.set_datetime = "SetDateTime"
        self.set_configuration = "SetConfiguration"
        self.set_wifi_configuration = "SetWifiConfiguration"
        self.set_variance_configuration = "SetVarianceConfiguration"
        self.set_installed_sensors = "SetInstalledSensors"
        self.put_sql_note = "PutDatabaseNote"
        self.delete_sql_note = "DeleteDatabaseNote"
        self.update_sql_note = "UpdateDatabaseNote"

        self.command_data_separator = "[new_data_section]"


script_directory = str(path[0]).replace("\\", "/")

about_window_text_file_location = script_directory + "/additional_files/about_text.txt"

html_file_output_name_system = "SensorsSystemReport.html"
html_template_system1_location = script_directory + "/additional_files/html_template_system1.html"
html_template_system2_location = script_directory + "/additional_files/html_template_system2.html"
html_template_system3_location = script_directory + "/additional_files/html_template_system3.html"

html_file_output_name_readings = "SensorsReadingsReport.html"
html_template_readings1_location = script_directory + "/additional_files/html_template_readings1.html"
html_template_readings2_location = script_directory + "/additional_files/html_template_readings2.html"
html_template_readings3_location = script_directory + "/additional_files/html_template_readings3.html"

html_file_output_name_config = "SensorsConfigReport.html"
html_template_config1_location = script_directory + "/additional_files/html_template_config1.html"
html_template_config2_location = script_directory + "/additional_files/html_template_config2.html"
html_template_config3_location = script_directory + "/additional_files/html_template_config3.html"

reports_system_replacement_codes = ["{{HostName}}",
                                    "{{IP}}",
                                    "{{DateTime}}",
                                    "{{UpTime}}",
                                    "{{Version}}",
                                    "{{CPUTemp}}",
                                    "{{FreeDisk}}",
                                    "{{SQLDBSize}}",
                                    "{{LastUpdated}}"]

reports_readings_replacement_codes = ["{{SensorTypes}}",
                                      "{{SensorReadings}}"]

reports_config_replacement_codes = ["{{HostName}}",
                                    "{{IP}}",
                                    "{{DateTime}}",
                                    "{{IntervalSQLWriteEnabled}}",
                                    "{{TriggerSQLWriteEnabled}}",
                                    "{{IntervalDuration}}",
                                    "{{CustomTempOffset}}",
                                    "{{TemperatureOffset}}",
                                    "{{InstalledSensors}}"]

reports_local_time_code = ["{{LocalDateTime}}"]

default_installed_sensors_text = """
Change the number in front of each line. Enable = 1 & Disable = 0
1 = Gnu/Linux - Raspbian
0 = Raspberry Pi Zero W
0 = Raspberry Pi 3BPlus
0 = Raspberry Pi Sense HAT
0 = Pimoroni BH1745
0 = Pimoroni AS7262
0 = Pimoroni BME680
0 = Pimoroni EnviroPHAT
0 = Pimoroni LSM303D
0 = Pimoroni VL53L1X
0 = Pimoroni LTR-559
"""

default_sensor_config_text = """
Enable = 1 & Disable = 0 (Recommended: Do not change if you are unsure)
0 = Enable Debug Logging
1 = Record Interval Sensors to SQL Database
1 = Record Trigger Sensors to SQL Database
300.0 = Seconds between Interval recordings
0 = Enable Custom Temperature Offset
0.0 = Custom Temperature Offset
"""

default_wifi_config_text = """
# Update or Add additional wireless network connections as required
# Add your wireless name to the end of 'ssid=' 
# Add the password to the end of 'psk=' in double quotes

ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

# Change 'country' to your country, common codes are included below
# GB (United Kingdom), FR (France), US (United States), CA (Canada)
country=CA

network={
        ssid="SomeOtherNetwork"
        psk="SuperSecurePassword"
        key_mgmt=WPA-PSK
}
"""

default_variance_config_text = """
Enable or Disable & set Variance settings.  0 = Disabled, 1 = Enabled.
1 = Enable Sensor Uptime
1209600.0 = Seconds between SQL Writes of Sensor Uptime

1 = Enable CPU Temperature
10.0 = CPU Temperature variance
99999.99 = Seconds between 'CPU Temperature' readings

1 = Enable Environmental Temperature
10.0 = Environmental Temperature variance
99999.99 = Seconds between 'Environmental Temperature' readings

1 = Enable Pressure
50 = Pressure variance
99999.99 = Seconds between 'Pressure' readings

1 = Enable Humidity
25.0 = Humidity variance
99999.99 = Seconds between 'Humidity' readings

1 = Enable Lumen
600.0 = Lumen variance
99999.99 = Seconds between 'Lumen' readings

1 = Enable Red
10.0 = Red variance
99999.99 = Seconds between 'Red' readings

1 = Enable Orange
10.0 = Orange variance
99999.99 = Seconds between 'Orange' readings

1 = Enable Yellow
10.0 = Yellow variance
99999.99 = Seconds between 'Yellow' readings

1 = Enable Green
10.0 = Green variance
99999.99 = Seconds between 'Green' readings

1 = Enable Blue
10.0 = Blue variance
99999.99 = Seconds between 'Blue' readings

1 = Enable Violet
10.0 = Violet variance
99999.99 = Seconds between 'Violet' readings

1 = Enable Accelerometer
99999.99 = Accelerometer variance
99999.99 = Seconds between 'Accelerometer' readings

1 = Enable Magnetometer
99999.99 = Magnetometer variance
99999.99 = Seconds between 'Magnetometer' readings

1 = Enable Gyroscope
99999.99 = Gyroscope variance
99999.99 = Seconds between 'Gyroscope' readings
"""

sql_default_textbox_note = """
Use this textbox to create a note to enter into one or more sensor
SQL Databases.  Use the Date & Time in the top right to enter the note
beside corresponding sensor data.

Example Notes:
The increase in temperature is due to the approaching wildfire.
  - Generic Worker SN:33942

The increase in lumen at night, may be an indication of the rare 
laser emitting sheep in the area.  
Notice how it only shows in the Near-Infrared spectrum. 
  - Random Zoologist
"""
