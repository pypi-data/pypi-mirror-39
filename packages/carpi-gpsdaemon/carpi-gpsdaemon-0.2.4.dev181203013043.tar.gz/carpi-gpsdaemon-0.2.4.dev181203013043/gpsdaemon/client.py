"""
CARPI GPS DAEMON
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""
from time import sleep
from typing import Any

from gpsdaemon.keys import ALL_KEYS, KEY_RAW
from redis import StrictRedis
from redisdatabus.bus import TypedBusListener


class GpsdClient(TypedBusListener):
    def __init__(self,
                 keys: list = ALL_KEYS,
                 name: str = None,
                 redis: StrictRedis = None,
                 host: str = '127.0.0.1',
                 port: int = 6379,
                 db: int = 0,
                 password: str = None):
        super().__init__(keys,
                         name,
                         redis,
                         host,
                         port,
                         db,
                         password)

    def _process_entry(self, msg: dict) -> (str, Any):
        return super()._process_entry(msg)


if __name__ == '__main__':
    a = ALL_KEYS
    a.remove(KEY_RAW)
    c = GpsdClient(keys=ALL_KEYS,
                   host='127.0.0.1',
                   port=6379,
                   db=0)
    c.start()
    try:
        while True:
            sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Shutdown requested")
    finally:
        c.stop()
