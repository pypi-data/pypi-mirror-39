"""
CARPI OBD II DAEMON
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""
from redisdatabus.bus import TypedBusListener

KEY_BASE = 'carpi.obd.'


def build_key(type, name):
    global KEY_BASE
    return "{}{}{}".format(type, KEY_BASE, name)


KEY_VOLTAGE = build_key(TypedBusListener.TYPE_PREFIX_FLOAT, "voltage")
KEY_FUEL_STATUS = build_key(TypedBusListener.TYPE_PREFIX_INT, "fuel_status")
KEY_COOLANT_TEMP = build_key(TypedBusListener.TYPE_PREFIX_INT, "coolant_temp")
KEY_INTAKE_PRESSURE = build_key(TypedBusListener.TYPE_PREFIX_INT, "intake_pressure")
KEY_RPM = build_key(TypedBusListener.TYPE_PREFIX_INT, "rpm")
KEY_SPEED = build_key(TypedBusListener.TYPE_PREFIX_INT, "speed")
KEY_INTAKE_TEMP = build_key(TypedBusListener.TYPE_PREFIX_INT, "temperature")

KEY_STATE_INFO = build_key(TypedBusListener.TYPE_PREFIX_INT, "state")

ALL_KEYS = [
    KEY_VOLTAGE,
    KEY_FUEL_STATUS,
    KEY_COOLANT_TEMP,
    KEY_INTAKE_PRESSURE,
    KEY_RPM,
    KEY_SPEED,
    KEY_INTAKE_TEMP,
    KEY_STATE_INFO
]

# ### State Codes ######################################
STATE_UNKNOWN = 0x00
STATE_OK = 0x01
STATE_SIMULATION = 0x02

STATE_ERROR_UNKNOWN = 0x10
STATE_ERROR_UNSPECIFIED = 0x11
STATE_SIMULATION_ERROR = 0x12
STATE_SERIAL_CON_ERROR = 0x13
STATE_SERIAL_OBD_ERROR = 0x14
STATE_NO_DATA_ERROR = 0x15


STATES = {
    'UNKNOWN': STATE_UNKNOWN,
    'OK': STATE_OK,
    'SIMULATION': STATE_SIMULATION,

    'ERR_UNKNOWN': STATE_ERROR_UNKNOWN,
    'ERR_UNSPECIFIED': STATE_ERROR_UNSPECIFIED,
    'ERR_SIMULATION': STATE_SIMULATION_ERROR,
    'ERR_SERIAL_CON': STATE_SERIAL_CON_ERROR,
    'ERR_SERIAL_OBD': STATE_SERIAL_OBD_ERROR,
    'ERR_NO_DATA': STATE_NO_DATA_ERROR
}


def state_str(state: int):
    for k, v in STATES.items():
        if state == v:
            return state
    return 'None'
