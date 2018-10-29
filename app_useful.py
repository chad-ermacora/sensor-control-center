import app_logger


def convert_minutes_string(var_minutes):
    try:
        uptime_days = int(float(var_minutes) // 1440)
        uptime_hours = int((float(var_minutes) % 1440) // 60)
        uptime_min = int(float(var_minutes) % 60)
        str_day_hour_min = str(uptime_days) + " Days / " + str(uptime_hours) + "." + str(uptime_min) + " Hours"
    except Exception as error:
        app_logger.app_logger.error("Unable to convert Minutes to days/hours.min: " + str(error))
        str_day_hour_min = var_minutes

    return str_day_hour_min
