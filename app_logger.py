import os
import logging
from logging.handlers import RotatingFileHandler

script_directory = str(os.path.dirname(os.path.realpath(__file__))).replace("\\", "/")

if not os.path.exists(os.path.dirname(script_directory + "/logs/")):
    os.makedirs(os.path.dirname(script_directory + "/logs/"))

# Main App Log
app_logger = logging.getLogger("MainLog")
app_logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s:  %(message)s', '%Y-%m-%d %H:%M:%S')

file_handler_kootnet = RotatingFileHandler(script_directory + '/logs/KootNet_log.txt', maxBytes=256000, backupCount=5)
file_handler_kootnet.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

app_logger.addHandler(file_handler_kootnet)
app_logger.addHandler(stream_handler)

# Sensor Commands Log
sensor_logger = logging.getLogger("SensorLog")
sensor_logger.setLevel(logging.INFO)

formatter_sensor = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:  %(message)s', '%Y-%m-%d %H:%M:%S')

file_handler_sensor = RotatingFileHandler(script_directory + '/logs/Sensor_Commands_log.txt', maxBytes=256000, backupCount=5)
file_handler_sensor.setFormatter(formatter_sensor)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter_sensor)

sensor_logger.addHandler(file_handler_sensor)
sensor_logger.addHandler(stream_handler)
