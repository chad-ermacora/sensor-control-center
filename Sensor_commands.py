# -*- coding: utf-8 -*-
'''
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
'''
import socket
import pickle
from tkinter import simpledialog
from Sensor_app_imports import config_load_file


def check(ip):
    temp_settings = config_load_file()
    socket.setdefaulttimeout(int(temp_settings[6]))
    sockG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sockG.connect((ip, 10065))
        sockG.send(b'checks')
        sensor_status = "Online"
        colour = "#7CFC00"
        log_message = "Sensor " + ip + " " + sensor_status
        checkbox_value = 1
    except:
        sensor_status = "Offline"
        colour = "red"
        log_message = "Sensor " + ip + " " + sensor_status
        checkbox_value = 0

    sockG.close()
    return sensor_status, colour, log_message, checkbox_value


def get(ip):
    log_print_text = "Sensor_commands.get()"
    temperature_offset = config_load_file()[5]
    socket.setdefaulttimeout(int(config_load_file()[7]))
    sockG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    offline_sensor_values = ["N/A", ip, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             "0000-00-00 00:00:00"]

    try:
        sockG.connect((ip, 10065))
        sockG.send(b'datagt')
        var_data = pickle.loads(sockG.recv(512))
        sensor_data = var_data.split(",")
        sensor_data[4] = round(float(sensor_data[4]) + \
                         float(temperature_offset), 2)
        log_print_text = log_print_text + "\nGetting Sensor Data from " + \
                         str(ip) + " - OK"
        return sensor_data
    except:
        print("\nGetting Sensor Data from " + ip + " - Failed")
        return offline_sensor_values
    sockG.close()


def nas_upgrade(ip):
    log_print_text = "Sensor_commands.nas_upgrade()"
    sockG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sockG.connect((ip, 10065))
        sockG.send(b'nasupg')
        log_print_text = log_print_text + "\nNAS Upgrade on " + ip + " - OK"
    except:
        log_print_text = log_print_text + "\nConnection Failed to " + ip
    sockG.close()
    return log_print_text


def online_upgrade(ip):
    log_print_text = "Sensor_commands.online_upgrade()"
    sockG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sockG.connect((ip, 10065))
        sockG.send(b'online')
        log_print_text = log_print_text + "\nOnline Upgrade on " + ip + " - OK"
    except:
        log_print_text = log_print_text + "\nConnection Failed to " + ip
    sockG.close()
    return log_print_text


def reboot(ip):
    log_print_text = "Sensor_commands.reboot()"
    sockG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sockG.connect((ip, 10065))
        sockG.send(b'reboot')
        log_print_text = log_print_text + "\nReboot on " + ip + " - OK"
    except:
        log_print_text = log_print_text + "\nReboot Failed on " + ip
    sockG.close()
    return log_print_text


def shutdown(ip):
    log_print_text = "Sensor_commands.shutdown()"
    sockG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sockG.connect((ip, 10065))
        sockG.send(b'shutdn')
        log_print_text = log_print_text + "\nShutdown on " + ip + " - OK"
    except:
        log_print_text = log_print_text + "\nShutdown Failed on " + ip
    sockG.close()
    return log_print_text


def kill_progs(ip):
    log_print_text = "Sensor_commands.kill_progs()"
    sockG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sockG.connect((ip, 10065))
        sockG.send(b'killpg')
        log_print_text = log_print_text + "\nPrograms on " + ip + \
                         " - Terminated"
    except:
        log_print_text = log_print_text + "\nPrograms on " + ip + \
                         " - Not running?"
    sockG.close()
    return log_print_text


def hostname_change(ip):
    log_print_text = "Sensor_commands.hostname_change()"
    sockG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sockG.connect((ip, 10065))
        sockG.send(str("hostch" + simpledialog.askstring((str(ip)),
                       "New Hostname: ")).encode())
        log_print_text = log_print_text + "\nHostname on " + ip + " - Updated"
    except:
        log_print_text = log_print_text + "\nPrograms on " + ip + \
                         " - Not running?"
    sockG.close()
    return log_print_text
