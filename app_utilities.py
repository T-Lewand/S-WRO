import math
from datetime import datetime
import Dataset
import utilities as util
import numpy as np
import pandas as pd

def calc_zoom(data):
    """
    Calculate zoom value to fit data in map boundaries
    :param data: data to fit
    :return: zoom value
    """
    max_lat = max(data['Latitude'])
    min_lat = min(data['Latitude'])
    max_lon = max(data['Longitude'])
    min_lon = min(data['Longitude'])

    height = max_lat - min_lat
    width = max_lon - min_lon

    X = []
    val = 360 * 2
    for i in range(24):
        val = val / 2
        X.append(val)

    X.sort()
    min_extent = max([height*3, width]) * 1.5
    zoom = round(np.interp(min_extent, np.array(X), range(24, 0, -1)), 1)

    return zoom

def to_time(value, date):
    """
    Recalculates decimal format of time H into H:M:S
    :param value:
    :param date:
    :return:
    """
    minutes, hour = math.modf(value)

    minutes = round(round(minutes, 4)*60)
    if minutes == 60:
        minutes = 0
        hour = hour + 1
    hour = int(hour)
    if hour == 24:
        hour = hour - 1
        minutes = 59
    time_string = f'{hour}:{minutes:02}:00'
    time = datetime.strptime('{} {}'.format(date, time_string), '%Y-%m-%d %H:%M:%S')
    return time
