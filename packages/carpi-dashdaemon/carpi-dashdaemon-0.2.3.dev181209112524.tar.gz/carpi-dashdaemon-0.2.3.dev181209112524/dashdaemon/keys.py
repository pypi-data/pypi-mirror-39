"""
CARPI DASH DAEMON
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""

from redisdatabus.bus import TypedBusListener as Types
import gpsdaemon.keys as gpskeys
import obddaemon.keys as obdkeys


SETTINGS_KEY_BASE = 'carpi.settings.'
PERSIST_KEY_BASE = 'carpi.persist.'
DASH_KEY_BASE = 'carpi.dashboard.'


def _build_key(type, key_base, name):
    return "{}{}{}".format(type if type else "", key_base, name)


CONFIG_KEYS = {
    'engine_vol': _build_key(Types.TYPE_PREFIX_INT, SETTINGS_KEY_BASE, 'car.enginevolume'),
    'vol_efficency': _build_key(Types.TYPE_PREFIX_INT, SETTINGS_KEY_BASE, 'car.efficency'),
    'fuel_density': _build_key(Types.TYPE_PREFIX_INT, SETTINGS_KEY_BASE, 'car.fueldensity'),
    'gps_max_acc': _build_key(Types.TYPE_PREFIX_INT, SETTINGS_KEY_BASE, 'gps.maxerror')
}

CONFIG_DEFAULT_VALUES = {
    CONFIG_KEYS['engine_vol']: 1000,
    CONFIG_KEYS['vol_efficency']: 85,
    CONFIG_KEYS['fuel_density']: 745,
    CONFIG_KEYS['gps_max_acc']: 5
}

PERSIST_KEYS = {
    'used_fuel': _build_key(Types.TYPE_PREFIX_FLOAT, PERSIST_KEY_BASE, 'fuel.used')
}

LIVE_INPUT_DATA_KEYS = {
    'car_rpm': obdkeys.KEY_RPM,
    'car_map': obdkeys.KEY_INTAKE_PRESSURE,
    'car_tmp': obdkeys.KEY_INTAKE_TEMP,
    'car_spd': obdkeys.KEY_SPEED,
    'car_ful': obdkeys.KEY_FUEL_STATUS,
    'gps_spd': gpskeys.KEY_SPEED,
    'gps_acc_lng': gpskeys.KEY_EPX,
    'gps_acc_lat': gpskeys.KEY_EPY,
    'gps_acc_spd': gpskeys.KEY_EPS
}

LIVE_OUTPUT_DATA_KEYS = {
    'speed': _build_key(Types.TYPE_PREFIX_INT, DASH_KEY_BASE, 'speed'),
    'fuel_usage': _build_key(Types.TYPE_PREFIX_FLOAT, DASH_KEY_BASE, 'fuelusage'),
    'fuel_efficiency': _build_key(Types.TYPE_PREFIX_FLOAT, DASH_KEY_BASE, 'fuelefficiency'),
    'fuel_fail_flag': _build_key(Types.TYPE_PREFIX_BOOL, DASH_KEY_BASE, 'fuelfailflag')
}
