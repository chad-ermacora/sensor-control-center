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
import webbrowser
import plotly
import sqlite3
import plotly.graph_objs as go
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta
from tkinter import filedialog
from plotly import tools

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:  %(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = RotatingFileHandler('logs/Sensor_graph_interval_log.txt', maxBytes=256000, backupCount=5)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class GraphIntervalData:

    def __init__(self):
        self.db_location = ""
        self.save_file_to = ""
        self.skip_sql = 0
        self.temperature_offset = 0
        self.time_offset = 0
        self.graph_start = ""
        self.graph_end = ""
        self.graph_type = ""
        self.graph_columns = []
        self.get_sql_entries = 200000


def open_html(outfile):
    try:
        file_var = "file:///" + outfile
        webbrowser.open(file_var, new=2)
        logger.info("open_html OK")
    except Exception as error:
        logger.error("open_html Failed: " + str(error))


def check_sql_end(var_date_end, var_date_now, var_date_old):
    now_year = str(var_date_now)[0:4]
    now_month = str(var_date_now)[5:7]
    now_day = str(var_date_now)[8:10]
    now_hour = str(var_date_now)[11:13]
    now_min = str(var_date_now)[14:16]
    now_sec = str(var_date_now)[17:19]
    now_date = int(now_year + now_month + now_day
                   + now_hour + now_min + now_sec)

    end_year = str(var_date_end)[0:4]
    end_month = str(var_date_end)[5:7]
    end_day = str(var_date_end)[8:10]
    end_hour = str(var_date_end)[11:13]
    end_min = str(var_date_end)[14:16]
    end_sec = str(var_date_end)[17:19]
    end_date = int(end_year + end_month + end_day +
                   end_hour + end_min + end_sec)

    old_year = str(var_date_old)[0:4]
    old_month = str(var_date_old)[5:7]
    old_day = str(var_date_old)[8:10]
    old_hour = str(var_date_old)[11:13]
    old_min = str(var_date_old)[14:16]
    old_sec = str(var_date_old)[17:19]
    old_date = int(old_year + old_month + old_day +
                   old_hour + old_min + old_sec)

    if now_date > end_date:
        var_do = "end"
        logger.debug("now_date end")
        logger.debug("now_date " + str(now_date))
        logger.debug("old_date " + str(old_date))
        logger.debug("end_date " + str(end_date))

    else:
        var_do = "proceed"

    if var_do != "end":
        if old_year > now_year:
            var_do = "skip"
            logger.debug("old_year is newer then now_year - skip")
            logger.debug("now_date " + str(now_date))
            logger.debug("old_date " + str(old_date))
            logger.debug("end_date " + str(end_date))

    return var_do


def get_sql_data(var_column, var_table, var_start, var_end, conn_db):
    var_sql_data = []
    logger.debug("\nvar_column " + str(var_column))
    logger.debug("var_table " + str(var_table))
    logger.debug("var_start " + str(var_start))
    logger.debug("var_end " + str(var_end))
    logger.debug("conn_db " + str(conn_db))

    var_sql_query = "SELECT " + \
        str(var_column) + \
        " FROM " + \
        str(var_table) + \
        " WHERE Time BETWEEN date('" + \
        str(var_start) + \
        "') AND date('" + \
        str(var_end) + \
        "') LIMIT " + \
        str(get_sql_entries)

    try:
        conn = sqlite3.connect(str(conn_db))
        c = conn.cursor()
        try:
            c.execute(var_sql_query)
            var_sql_data = c.fetchall()
            count = 0
            for i in var_sql_data:
                var_sql_data[count] = str(i)[2:-3]
                count = count + 1

            c.close()
            conn.close()
        except Exception as error:
            logger.error("Failed SQL Query Failed: " + str(error))
    except Exception as error:
        logger.error("Failed DB Connection: " + str(error))

    return var_sql_data
