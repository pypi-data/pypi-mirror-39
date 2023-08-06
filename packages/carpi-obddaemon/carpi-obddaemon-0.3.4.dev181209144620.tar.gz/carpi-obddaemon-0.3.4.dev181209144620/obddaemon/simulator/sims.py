"""
CARPI OBD II DAEMON
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""
from os.path import dirname, basename
from time import sleep
from typing import TextIO

from obddaemon.custom.daemon import SerialObdDaemon
from .base import BaseFileSimulatorDaemon
from obddaemon.custom.Obd2DataParser import parse_value, ObdPidParserUnknownError
from obddaemon.keys import KEY_STATE_INFO, STATE_SIMULATION, STATE_SIMULATION_ERROR

from re import compile, findall, match
from datetime import datetime, timedelta


class SerialObdLogSimItem(object):
    def __init__(self, pid: str, raw_value: str,
                 timestamp: str = None):
        self._timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f') \
                            if timestamp \
                            else datetime.now()
        self._pid = pid
        self._raw_value = raw_value
        self._value = parse_value(self._pid, self._raw_value)
        self._sleep_for = 0.5

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def pid(self):
        return self._pid

    @property
    def raw_value(self):
        return self._raw_value

    @property
    def parsed_value(self):
        return self._value

    @property
    def sleep_for(self) -> float:
        return self._sleep_for

    @sleep_for.setter
    def sleep_for(self, value: float):
        self._sleep_for = value


class SerialObdLogSimulatorDaemon(BaseFileSimulatorDaemon):
    SEARCH_PATTERN = "^\\[([^\\]]*)\\]\\s\\[([^\\]]*)\\]\\sDEBUG\\s*-\\s\\[([^\\]]*)\\] => ([^\\n]*)$"

    PBMODE_REALTIME = 0
    PBMODE_FIXED = 1

    def __init__(self,
                 file_path: str):
        super().__init__(file_path,
                         u"SerialSim {}".format(basename(file_path)))

        self._playback_mode: int = SerialObdLogSimulatorDaemon.PBMODE_REALTIME
        self._fixed_interval: int = 500
        self._loops: int = -1

    def _configure(self):
        log = self._log

        self._playback_mode = self._get_config_int('Playback', 'Mode',
                                                   SerialObdLogSimulatorDaemon.PBMODE_REALTIME)
        # Load Settings
        if self._playback_mode == SerialObdLogSimulatorDaemon.PBMODE_REALTIME:
            log.debug("Using Real Time playback mode")
        elif self._playback_mode == SerialObdLogSimulatorDaemon.PBMODE_FIXED:
            self._fixed_interval = self._get_config_int('Playback', 'Interval', 500)
            log.debug("Using Fixed Interval playback mode with {}ms interval".format(self._fixed_interval))
        else:
            log.error("Invalid Playback Mode {} (allowed: 0=Realtime, 1=Fixed Interval)".format(self._playback_mode))

        self._loops = self._get_config_int('Playback', 'Loops', -1)

        # Load file
        super()._configure()

        # Parsing Time Deltas (with Realtime Mode)
        if self._playback_mode == SerialObdLogSimulatorDaemon.PBMODE_REALTIME:
            log.debug("Processing items for realtime processing ...")
            last_item = None
            for i in self._file_content:  # type: SerialObdLogSimItem
                if last_item:
                    dif = i.timestamp - last_item.timestamp
                    last_item.sleep_for = dif.total_seconds()
                last_item = i

        elif self._playback_mode == SerialObdLogSimulatorDaemon.PBMODE_FIXED:
            for i in self._file_content:
                i.sleep_for = self._fixed_interval / 1000

        # Calculate an estimated duration and write it to the log
        item_count = len(self._file_content)
        est_duration = sum([i.sleep_for for i in self._file_content])
        log.info("Estimated duration of playback: {:.1f} sec for {} items ({:.1f} items / s)".format(
            est_duration, item_count, (item_count / est_duration)))

    def _parse_file(self, f: TextIO) -> list:
        log = self._log
        vals = []
        r = compile(SerialObdLogSimulatorDaemon.SEARCH_PATTERN)
        for line in f:
            l = findall(r, line.strip())
            if len(l) >= 1 and len(l[0]) == 4:
                pid = l[0][2]
                if pid not in SerialObdDaemon.FETCH_SEQUENCE:
                    continue
                try:
                    vals.append(SerialObdLogSimItem(pid=pid,
                                                    raw_value=l[0][3],
                                                    timestamp=l[0][0]))
                except ObdPidParserUnknownError:
                    log.debug("Cannot parse PID {}, skipped".format(pid))

        log.info("Loaded {} items from {}".format(len(vals),
                                                  dirname(self._file_path)))
        return vals

    def _step(self):
        idx = 0
        last_msg = datetime.min
        size = len(self._file_content)
        log = self._log
        bus = self._bus
        for item in self._file_content:  # type: SerialObdLogSimItem
            now = datetime.now()

            if now - last_msg >= timedelta(seconds=5):
                log.debug("Played back {} / {} items".format(idx, size))
                last_msg = now

            bus.publish(SerialObdDaemon.OBD_MAPPING[item.pid],
                        item.parsed_value[0] if type(item.parsed_value) is tuple else item.parsed_value)
            bus.publish(KEY_STATE_INFO, STATE_SIMULATION)

            idx += 1
            if not self._is_running:
                log.info("Stopping playback ...")
            else:
                sleep(item.sleep_for)
