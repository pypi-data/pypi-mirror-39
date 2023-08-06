"""
CARPI OBD II DAEMON
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""
from configparser import ConfigParser
from logging import Logger
from os.path import dirname, basename
from sys import argv
from typing import TextIO, Union

from carpicommons.log import logger
from daemoncommons.daemon import Daemon
from redisdatabus.bus import BusWriter

from obddaemon.simulator.errors import ObdSimulatorError


class BaseSimulatorDaemon(Daemon):
    def __init__(self, name):
        super().__init__(name)
        self._bus: BusWriter = None
        self._log: Logger = None
        self._is_running = False

    def _get_config_from_argv(self, section: str, key: str) -> Union[str, None]:
        argv_key = "--{}.{}=".format(section, key)
        for arg in argv:  # type: str
            if arg.startswith(argv_key):
                return arg[arg.index('=') + 1:]
        return None

    def _get_config(self, section: str, key: str, fallback: str = None) -> str:
        argv_val = self._get_config_from_argv(section, key)
        if argv_val is not None:
            return argv_val
        else:
            return super()._get_config(section, key, fallback)

    def _get_config_float(self, section: str, key: str, fallback: float = None) -> float:
        argv_val = self._get_config_from_argv(section, key)
        if argv_val is not None:
            return float(argv_val)
        else:
            return super()._get_config_float(section, key, fallback)

    def _get_config_int(self, section: str, key: str, fallback: int = None) -> int:
        argv_val = self._get_config_from_argv(section, key)
        if argv_val is not None:
            return int(argv_val)
        else:
            return super()._get_config_int(section, key, fallback)

    def _get_config_bool(self, section: str, key: str, fallback: bool = False) -> bool:
        argv_key = "--{}{}.{}".format("no-" if fallback else "",
                                      section, key)
        if argv_key in argv:
            return not fallback
        else:
            return super()._get_config_bool(section, key, fallback)

    def startup(self):
        log = self._log = logger(self.name)
        self._bus = self._build_bus_writer()

        log.info("Configuring Simulator Daemon ...")
        self._configure()

        log.info("Configuration completed, starting simulation ...")
        self._is_running = True
        while self._is_running:
            self._step()

    def _build_bus_writer(self) -> BusWriter:
        self._log.info("Connecting to Redis instance ...")
        return BusWriter(host=self._get_config('Redis', 'Host', '127.0.0.1'),
                         port=self._get_config_int('Redis', 'Port', 6379),
                         db=self._get_config_int('Redis', 'DB', 0),
                         password=self._get_config('Redis', 'Password', None))

    def _configure(self):
        raise NotImplemented

    def _step(self):
        raise NotImplemented

    def shutdown(self):
        self._is_running = False


class BaseFileSimulatorDaemon(BaseSimulatorDaemon):
    def __init__(self,
                 file_path: str,
                 daemon_name: str=None):
        super().__init__(daemon_name if daemon_name
                         else u"FileSim {}".format(basename(file_path)))
        self._file_path = file_path
        self._file_content = []

    def _configure(self):
        try:
            with open(self._file_path, 'r') as f:
                self._file_content = self._parse_file(f)
        except FileNotFoundError:
            raise ObdSimulatorError(ObdSimulatorError.REASON_FILE_NOT_FOUND)

    def _parse_file(self, f: TextIO) -> list:
        raise NotImplemented
