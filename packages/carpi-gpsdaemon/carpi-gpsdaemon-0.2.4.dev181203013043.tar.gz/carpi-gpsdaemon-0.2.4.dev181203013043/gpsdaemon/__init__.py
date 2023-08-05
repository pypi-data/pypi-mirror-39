"""
CARPI GPS DAEMON
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""
from daemoncommons.daemon import DaemonRunner

from gpsdaemon.daemon import GpsDaemon

if __name__ == '__main__':
    d = DaemonRunner('GPS_DAEMON_CFG', ['gps.ini', '/etc/carpi/gps.ini'])
    d.run(GpsDaemon())
