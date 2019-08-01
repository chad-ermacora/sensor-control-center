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

software_version = "Tested on Python 3.5 & 3.7 || Alpha.25.223"


class CreateSQLColumnsReadable:
    """ Creates an object to hold all human readable SQL column names. """

    def __init__(self):
        self.no_sensor = " || No Sensor Detected || "
        self.date_time = "Date & Time"
        self.sensor_name = "Sensor Name"
        self.ip = "IP"
        self.system_uptime = "Sensor Uptime"
        self.cpu_temp = "CPU Temperature"
        self.environmental_temp = "Env Temperature"
        self.pressure = "Pressure"
        self.altitude = "Altitude"
        self.humidity = "Humidity"
        self.distance = "Distance"
        self.gas = "Gas"
        self.particulate_matter = "Particulate Matter"
        self.lumen = "Lumen"
        self.colours = "Colours"
        self.ultra_violet = "Ultra Violet"
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
        self.altitude = "Altitude"
        self.humidity = "Humidity"
        self.distance = "Distance"
        self.gas = ["Gas_Resistance_Index", "Gas_Oxidising", "Gas_Reducing", "Gas_NH3"]
        self.particulate_matter = ["Particulate_Matter_1", "Particulate_Matter_2_5", "Particulate_Matter_10"]
        self.lumen = "Lumen"
        self.rgb = ["Red", "Green", "Blue"]
        self.six_chan_color = ["Red", "Orange", "Yellow", "Green", "Blue", "Violet"]
        self.ultra_violet = ["Ultra_Violet_Index", "Ultra_Violet_A", "Ultra_Violet_B"]
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
        self.altitude = " meters"
        self.humidity = " %RH"
        self.distance = " meters?"
        self.gas = " Resistance"
        self.particulate_matter = " Particulate Matter"
        self.lumen = " Lumen"
        self.rgb = " RGB"
        self.six_chan_color = " ROYGBV"
        self.ultra_violet = " Ultra Violet"
        self.xyz = " XYZ"


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
        self.download_zipped_logs = "DownloadZippedLogs"
        self.sensor_readings = "GetSensorReadings"
        self.sensor_name = "GetHostName"
        self.system_uptime = "GetSystemUptime"
        self.cpu_temp = "GetCPUTemperature"
        self.environmental_temp = "GetEnvTemperature"
        self.env_temp_offset = "GetTempOffsetEnv"
        self.pressure = "GetPressure"
        self.altitude = "GetAltitude"
        self.humidity = "GetHumidity"
        self.distance = "GetDistance"
        self.gas_index = "GetGasResistanceIndex"
        self.gas_oxidised = "GetGasOxidised"
        self.gas_reduced = "GetGasReduced"
        self.gas_nh3 = "GetGasNH3"
        self.pm_1 = "GetParticulateMatter1"
        self.pm_2_5 = "GetParticulateMatter2_5"
        self.pm_10 = "GetParticulateMatter10"
        self.lumen = "GetLumen"
        self.rgb = "GetEMS"
        self.ultra_violet_index = "GetUltraVioletA"
        self.ultra_violet_a = "GetUltraVioletA"
        self.ultra_violet_b = "GetUltraVioletB"
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
        self.reinstall_requirements = "ReInstallRequirements"
        self.upgrade_online = "UpgradeOnline"
        self.upgrade_online_dev = "UpgradeOnlineDev"
        self.upgrade_smb = "UpgradeSMB"
        self.upgrade_smb_dev = "UpgradeSMBDev"
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

        self.display_message = "DisplayText"

        self.delete_primary_log = "DeletePrimaryLog"
        self.delete_network_log = "DeleteNetworkLog"
        self.delete_sensors_log = "DeleteSensorsLog"

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
0 = Pimoroni BMP280
0 = Pimoroni BME680
0 = Pimoroni EnviroPHAT
0 = Pimoroni Enviro+
0 = Pimoroni PMS5003
0 = Pimoroni LSM303D
0 = Pimoroni ICM20948
0 = Pimoroni VL53L1X
0 = Pimoroni LTR-559
0 = Pimoroni VEML6075
0 = Pimoroni 11x7 LED Matrix
0 = Pimoroni 10.96'' SPI Colour LCD (160x80)
0 = Pimoroni 1.12'' Mono OLED (128x128, white/black)
"""

default_sensor_config_text = """
Enable = 1 & Disable = 0 (Recommended: Do not change if you are unsure)
0 = Enable Debug Logging
0 = Enable Display (If present)
1 = Record Interval Sensors to SQL Database
0 = Record Trigger Sensors to SQL Database
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

0 = Enable CPU Temperature
5.0 = CPU Temperature variance
1.0 = Seconds between 'CPU Temperature' readings

0 = Enable Environmental Temperature
5.0 = Environmental Temperature variance
1.0 = Seconds between 'Environmental Temperature' readings

0 = Enable Pressure
10 = Pressure variance
1.0 = Seconds between 'Pressure' readings

0 = Enable Altitude
10 = Altitude variance
1.0 = Seconds between 'Altitude' readings

0 = Enable Humidity
5.0 = Humidity variance
1.0 = Seconds between 'Humidity' readings

0 = Enable Distance
5.0 = Distance variance
1.0 = Seconds between 'Distance' readings

0 = Enable Gas
100.0 = Gas Resistance Index variance
100.0 = Gas Oxidising variance
100.0 = Gas Reducing variance
100.0 = Gas NH3 variance
1.0 = Seconds between 'Gas' readings

0 = Enable Particulate Matter (PM)
1000.0 = Particulate Matter 1 (PM1) variance
1000.0 = Particulate Matter 2.5 (PM2.5) variance
1000.0 = Particulate Matter 10 (PM10) variance
1.0 = Seconds between 'Particulate Matter' readings

0 = Enable Lumen
100.0 = Lumen variance
1.0 = Seconds between 'Lumen' readings

0 = Enable Colour
5.0 = Red variance
5.0 = Orange variance
5.0 = Yellow variance
5.0 = Green variance
5.0 = Blue variance
5.0 = Violet variance
1.0 = Seconds between 'Colour' readings

0 = Enable Ultra Violet
5.0 = Ultra Violet Index variance
5.0 = Ultra Violet A variance
5.0 = Ultra Violet B variance
1.0 = Seconds between 'Ultra Violet' readings

0 = Enable Accelerometer
25.0 = Accelerometer X variance
25.0 = Accelerometer Y variance
25.0 = Accelerometer Z variance
0.25 = Seconds between 'Accelerometer' readings

0 = Enable Magnetometer
25.0 = Magnetometer X variance
25.0 = Magnetometer Y variance
25.0 = Magnetometer Z variance
0.25 = Seconds between 'Magnetometer' readings

0 = Enable Gyroscope
25.0 = Gyroscope X variance
25.0 = Gyroscope Y variance
25.0 = Gyroscope Z variance
0.25 = Seconds between 'Gyroscope' readings
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
