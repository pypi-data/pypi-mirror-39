"""
CARPI GPS DAEMON
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""
from redisdatabus.bus import TypedBusListener

KEY_BASE = 'carpi.gps.'


def build_key(type, name):
    global KEY_BASE
    return "{}{}{}".format(type, KEY_BASE, name)


# Raw GPS JSON String
KEY_RAW = build_key(TypedBusListener.TYPE_PREFIX_STRING, "RAW")
# Fix Mode (0=no mode, 1=no fix, 2=2D, 3=3D)
KEY_FIX_MODE = build_key(TypedBusListener.TYPE_PREFIX_INT, "fixmode")
# GPS Timestamp (UTC)
KEY_TIMESTAMP = build_key(TypedBusListener.TYPE_PREFIX_STRING, "timestamp")

# Latitude [°]
KEY_LATITUDE = build_key(TypedBusListener.TYPE_PREFIX_FLOAT, "latitude")
# Longitude [°]
KEY_LONGITUDE = build_key(TypedBusListener.TYPE_PREFIX_FLOAT, "longitude")
# Altitude [m]
KEY_ALTITUDE = build_key(TypedBusListener.TYPE_PREFIX_INT, "altitude")
# Course / Direction [°]
KEY_TRACK = build_key(TypedBusListener.TYPE_PREFIX_FLOAT, "track")
# Climb rate [m/s]
KEY_CLIMB = build_key(TypedBusListener.TYPE_PREFIX_FLOAT, "climb")

# Speed [m/s]
KEY_SPEED = build_key(TypedBusListener.TYPE_PREFIX_FLOAT, "speed")
# Speed [km/h]
KEY_SPEED_KMH = build_key(TypedBusListener.TYPE_PREFIX_FLOAT, "speed.kmh")
# Speed [mph]
KEY_SPEED_MPH = build_key(TypedBusListener.TYPE_PREFIX_FLOAT, "speed.mph")

# Longitude error [m]
KEY_EPX = build_key(TypedBusListener.TYPE_PREFIX_FLOAT, "epx")
# Latitude error [m]
KEY_EPY = build_key(TypedBusListener.TYPE_PREFIX_FLOAT, "epy")
# Altitude error [m]
KEY_EPV = build_key(TypedBusListener.TYPE_PREFIX_FLOAT, "epv")

# Course / Direction error [°]
KEY_EPD = build_key(TypedBusListener.TYPE_PREFIX_FLOAT, "epd")
# Speed error [m/s]
KEY_EPS = build_key(TypedBusListener.TYPE_PREFIX_FLOAT, "eps")
# Climb rate error [m/s]
KEY_EPC = build_key(TypedBusListener.TYPE_PREFIX_FLOAT, "epc")

# System Timestamp
KEY_SYS_TIMESTAMP = build_key(TypedBusListener.TYPE_PREFIX_STRING, "systimestamp")

# All Keys
ALL_KEYS = [
    KEY_RAW,
    KEY_FIX_MODE,
    KEY_TIMESTAMP,

    KEY_LATITUDE,
    KEY_LONGITUDE,
    KEY_ALTITUDE,
    KEY_TRACK,
    KEY_CLIMB,

    KEY_SPEED,
    KEY_SPEED_KMH,
    KEY_SPEED_MPH,

    KEY_EPX,
    KEY_EPY,
    KEY_EPV,

    KEY_EPD,
    KEY_EPS,
    KEY_EPC,

    KEY_SYS_TIMESTAMP,
]
