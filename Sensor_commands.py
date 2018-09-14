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
import socket
import pickle
import os
import sys
from tkinter import simpledialog
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:  %(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = RotatingFileHandler('logs/Sensor_commands_log.txt', maxBytes=256000, backupCount=5)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

app_location_directory = str(os.path.dirname(sys.argv[0])) + "/"
config_file = app_location_directory + "config.txt"


def check(ip, net_timeout):
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'checks')
        sensor_status = "Online"
        logger.info("Check " + str(ip) + " Online")
    except Exception as error:
        logger.info("Check " + str(ip) + " Offline: " + str(error))
        sensor_status = "Offline"

    sock_g.close()
    return sensor_status


def get(ip, net_timeout):
    logger.debug("Sensor_commands.get()")
    socket.setdefaulttimeout(net_timeout)
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'datagt')
        var_data = pickle.loads(sock_g.recv(512))
        sensor_data = var_data.split(",")
        sock_g.close()
        logger.info("Getting Sensor Data from " + str(ip) + " - OK")
        return sensor_data
    except Exception as error:
        logger.warning("Getting Sensor Data from " + ip + " - Failed: " + str(error))
        offline_sensor_values = ["N/A", ip, 0, 0, 0, 0, 0, 0, 0, 0, 0, "0000-00-00 00:00:00"]
        return offline_sensor_values


def nas_upgrade(ip):
    logger.debug("Sensor_commands.nas_upgrade()")
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'nasupg')
        logger.info("NAS Upgrade on " + ip + " - OK")
    except Exception as error:
        logger.warning("NAS Upgrade on " + ip + " - Failed: " + str(error))
    sock_g.close()


def online_upgrade(ip):
    logger.debug("Sensor_commands.online_upgrade()")
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'online')
        logger.info("Online Upgrade on " + ip + " - OK")
    except Exception as error:
        logger.warning("Online Upgrade on " + ip + " - Failed: " + str(error))
    sock_g.close()


def reboot(ip):
    logger.debug("Sensor_commands.reboot()")
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'reboot')
        logger.info("Reboot on " + ip + " - OK")
    except Exception as error:
        logger.warning("Reboot on " + ip + " - Failed: " + str(error))
    sock_g.close()


def shutdown(ip):
    logger.debug("Sensor_commands.shutdown()")
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'shutdn')
        logger.info("Shutdown on " + ip + " - OK")
    except Exception as error:
        logger.warning("Shutdown on " + ip + " - Failed: " + str(error))
    sock_g.close()


def kill_progs(ip):
    logger.debug("Sensor_commands.kill_progs()")
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'killpg')
        logger.info("Closing Programs on " + ip + " - OK")
    except Exception as error:
        logger.warning("Closing Programs on " + ip + " - Failed: " + str(error))
    sock_g.close()


def hostname_change(ip):
    logger.debug("Sensor_commands.hostname_change()")
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_hostname = simpledialog.askstring(str(ip), "New Hostname: ")

    if new_hostname is not None:
        if new_hostname is not '':
            print(new_hostname)
            try:
                sock_g.connect((ip, 10065))
                sock_g.send(('hostch' + str(new_hostname)).encode())
                logger.info("Hostname Change on " + ip + " - OK")
            except Exception as error:
                logger.warning("Hostname Change on " + ip + " - Failed: " + str(error))
            sock_g.close()
        else:
            logger.warning("Hostname Blank, Cancelling Name Change on " + ip)
    else:
        logger.warning("Hostname cancelled on " + ip)
