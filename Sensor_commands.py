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
from tkinter import simpledialog
from Sensor_config import load_file


def check(ip):
    temp_settings = load_file()
    socket.setdefaulttimeout(int(temp_settings[6]))
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'checks')
        sensor_status = "Online"
        colour = "#7CFC00"
        log_message = "Sensor " + ip + " " + sensor_status
        checkbox_value = 1
    except:
        sensor_status = "Offline"
        colour = "red"
        log_message = "Sensor " + ip + " " + sensor_status
        checkbox_value = 0

    sock_g.close()
    return sensor_status, colour, checkbox_value


def get(ip):
    log_print_text = "Sensor_commands.get()"
    temperature_offset = load_file()[5]
    socket.setdefaulttimeout(int(load_file()[7]))
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'datagt')
        var_data = pickle.loads(sock_g.recv(512))
        sensor_data = var_data.split(",")
        sensor_data[4] = round(float(sensor_data[4]) + float(temperature_offset), 2)
        log_print_text = log_print_text + "\nGetting Sensor Data from " + str(ip) + " - OK"
        sock_g.close()
        return sensor_data
    except:
        print("\nGetting Sensor Data from " + ip + " - Failed")
        offline_sensor_values = ["N/A", ip, 0, 0, 0, 0, 0, 0, 0, 0, 0, "0000-00-00 00:00:00"]
        return offline_sensor_values



def nas_upgrade(ip):
    log_print_text = "Sensor_commands.nas_upgrade()"
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'nasupg')
        log_print_text = log_print_text + "\nNAS Upgrade on " + ip + " - OK"
    except:
        log_print_text = log_print_text + "\nConnection Failed to " + ip
    sock_g.close()


def online_upgrade(ip):
    log_print_text = "Sensor_commands.online_upgrade()"
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'online')
        log_print_text = log_print_text + "\nOnline Upgrade on " + ip + " - OK"
    except:
        log_print_text = log_print_text + "\nConnection Failed to " + ip
    sock_g.close()


def reboot(ip):
    log_print_text = "Sensor_commands.reboot()"
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'reboot')
        log_print_text = log_print_text + "\nReboot on " + ip + " - OK"
    except:
        log_print_text = log_print_text + "\nReboot Failed on " + ip
    sock_g.close()


def shutdown(ip):
    log_print_text = "Sensor_commands.shutdown()"
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'shutdn')
        log_print_text = log_print_text + "\nShutdown on " + ip + " - OK"
    except:
        log_print_text = log_print_text + "\nShutdown Failed on " + ip
    sock_g.close()


def kill_progs(ip):
    log_print_text = "Sensor_commands.kill_progs()"
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(b'killpg')
        log_print_text = log_print_text + "\nPrograms on " + ip + " - Terminated"
    except:
        log_print_text = log_print_text + "\nPrograms on " + ip + " - Not running?"
    sock_g.close()


def hostname_change(ip):
    log_print_text = "Sensor_commands.hostname_change()"
    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock_g.connect((ip, 10065))
        sock_g.send(str("hostch" + simpledialog.askstring((str(ip)), "New Hostname: ")).encode())
        log_print_text = log_print_text + "\nHostname on " + ip + " - Updated"
    except:
        log_print_text = log_print_text + "\nPrograms on " + ip + " - Not running?"
    sock_g.close()

