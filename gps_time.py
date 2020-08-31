#!/usr/bin/python3
import io
import pynmea2
import serial
from timezonefinder import TimezoneFinder
from datetime import datetime
from pytz import timezone, utc
from sys import platform, argv

if platform == "linux" or platform == "linux2":
    comport = '/dev/ttyUSB0' | argv[1]
elif platform == "win32":
    comport = 'COM5' | argv[1]

ser = serial.Serial(comport, 4800, timeout=5.0)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
tf =TimezoneFinder(in_memory=True)

def get_offset(lat, lng):
    """
    returns a location's time zone offset from UTC in hours.
    """

    today = datetime.now()
    tz_target = timezone(tf.certain_timezone_at(lng=lng, lat=lat))
    # ATTENTION: tz_target could be None! handle error case
    today_target = tz_target.localize(today)
    today_utc = utc.localize(today)
    return (today_utc - today_target).total_seconds() / 3600


def get_loc(reader):
    '''tries to get GPS coordinates from serial device and display location and TZ offset
    '''
    got_coord = False
    msg = ''
    while not got_coord: # need to loop while gps sensor gets a lock
        try:
            msg = pynmea2.parse(sio.readline())
            try: # serial data is messy and often not starting with expected $, raises ParseError mostly
                if msg.latitude:
                    str_lat, str_lon = str(msg.latitude), str(msg.longitude)
                    print('You are at {}, {}'.format(str_lat, str_lon))
                    tz_offset = get_offset(msg.latitude, msg.longitude)
                    print('Your offset is {}.'.format(tz_offset))
                    print('You are in {} timezone.'.format(tf.timezone_at(lng=msg.longitude, lat=msg.latitude)))
                    got_coord = True
            except AttributeError:
                continue
        except serial.SerialException as e: # needed for when gps isn't plugged in or in use by someone else
            print('Device error: {}'.format(e))
            break
        except pynmea2.ParseError: # this is to continue the loop until we get a valid starting character
            continue

if __name__ == '__main__':
    get_loc(sio)