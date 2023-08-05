"""
CARPI GPS DAEMON
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""
from datetime import datetime
from logging import Logger
from time import sleep

from gpsdaemon.keys import *
from daemoncommons.daemon import Daemon
from carpicommons.log import logger
from carpicommons.errors import CarPiExitException
from redisdatabus.bus import BusWriter

from gps3 import agps3


class GpsdConnectionError(CarPiExitException):
    EXIT_CODE = 0xFA00

    def __init__(self):
        super().__init__(GpsdConnectionError.EXIT_CODE)


class GpsDaemon(Daemon):
    def __init__(self):
        super().__init__("GPS Daemon")
        self._log: Logger = None

    def _build_bus_writer(self):
        self._log.info("Connecting to Redis instance ...")
        return BusWriter(host=self._get_config('Redis', 'Host', '127.0.0.1'),
                         port=self._get_config_int('Redis', 'Port', 6379),
                         db=self._get_config_int('Redis', 'DB', 0),
                         password=self._get_config('Redis', 'Password', None))

    def startup(self):
        self._log = log = logger(self.name)
        log.info("Starting up %s ...", self.name)

        retries = 5

        bus = self._build_bus_writer()

        while True:
            sock = agps3.GPSDSocket()
            strm = agps3.DataStream()

            log.info("Connecting to GPSD...")
            sock.connect(self._get_config('GPSD', 'Host', agps3.HOST),
                         self._get_config_int('GPSD', 'Port', agps3.GPSD_PORT))
            sock.watch()

            log.info("Watching for new GPSD packages...")
            try:
                for d in sock:
                    if d:
                        strm.unpack(d)
                        di = self._build_messages(strm, d)
                        self._send_dict(bus, di)
            except OSError:
                if retries > 0:
                    log.error("Failed to fetch data from GPSD! Retrying %s more times", retries)
                    retries -= 1
                else:
                    raise GpsdConnectionError()

            sleep(5)

    def _build_messages(self, strm: agps3.DataStream, raw: str) -> dict:
        return {
            KEY_RAW: raw,
            KEY_FIX_MODE: self._get_int(strm.mode, 0),
            KEY_LATITUDE: self._get_float(strm.lat, None),
            KEY_LONGITUDE: self._get_float(strm.lon, None),
            KEY_TIMESTAMP: strm.time,
            KEY_SPEED: self._get_float(strm.speed),
            KEY_SPEED_KMH: self._get_float(strm.speed) * 3.6,
            KEY_SPEED_MPH: self._get_float(strm.speed) * 2.23694,
            KEY_TRACK: self._get_float(strm.track),
            KEY_CLIMB: self._get_float(strm.climb),
            KEY_EPX: self._get_float(strm.epx),
            KEY_EPY: self._get_float(strm.epy),
            KEY_EPV: self._get_float(strm.epv),
            KEY_EPD: self._get_float(strm.epd),
            KEY_EPS: self._get_float(strm.eps),
            KEY_EPC: self._get_float(strm.epc),
            KEY_SYS_TIMESTAMP: datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        }

    def _get_int(self, v: any, default: int=0):
        return int(v) if v != 'n/a' else default

    def _get_float(self, v: any, default: float=0):
        return float(v) if v != 'n/a' else default

    def _send_dict(self, bus: BusWriter, d: dict):
        for key, value in d.items():
            bus.publish(key, str(value))

    def shutdown(self):
        self._log.info("Shutting down %s...", self.name)
