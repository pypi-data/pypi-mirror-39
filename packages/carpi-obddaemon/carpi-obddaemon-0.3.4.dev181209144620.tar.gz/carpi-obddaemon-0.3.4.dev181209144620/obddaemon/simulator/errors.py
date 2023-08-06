"""
CARPI OBD II DAEMON
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""
from carpicommons.errors import CarPiExitException


class ObdSimulatorError(CarPiExitException):
    DEFAULT_EXIT_CODE = 0xFD00

    REASON_FILE_NOT_FOUND = 0x01

    def __init__(self, reason_code: int = 0):
        super().__init__(ObdSimulatorError.DEFAULT_EXIT_CODE + reason_code)
        self._reason = reason_code

    @property
    def reason(self):
        return self._reason
