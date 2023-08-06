"""
CARPI DASH DAEMON
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""
from datetime import datetime, timedelta
from logging import Logger
from time import sleep

from carpicommons.log import logger
from carpicommons.errors import CarPiExitException
from carpisettings import IniStore, RedisStore, ConfigStore
from daemoncommons.daemon import Daemon
from dashdaemon.keys import LIVE_INPUT_DATA_KEYS, LIVE_OUTPUT_DATA_KEYS, CONFIG_KEYS
from redisdatabus.bus import BusWriter, TypedBusListener

from dashdaemon.work import calculate_fuel_usage, calculate_fuel_efficiency


class DashDaemonError(CarPiExitException):
    DEFAULT_EXIT_CODE = 0xFD00

    REASON_CONFIG_CONNECTION_INVALID = 0xC0
    REASON_CONFIG_WHEREISIT = 0xC1

    def __init__(self, reason=0x0):
        super().__init__(DashDaemonError.DEFAULT_EXIT_CODE + reason)
        self._reason = reason

    @property
    def reason(self):
        return self._reason


class DashDaemon(Daemon):
    ERROR_TIMEOUT = 2

    def __init__(self):
        super().__init__("Dash Daemon")
        self._log: Logger = None
        self._current_values = dict()
        self._running = False
        self._reader: TypedBusListener = None
        self._obd_last_updated: datetime = datetime.now()

    def _build_config_reader(self) -> ConfigStore:
        cfg_type = self._get_config('Config', 'Type', 'Redis')
        if cfg_type.lower() == "ini":
            ini_path = self._get_config('Config', 'Path', None)
            if not ini_path:
                self._log.error("Failed to load configuration because you didn't specify it")
                raise DashDaemonError(DashDaemonError.REASON_CONFIG_WHEREISIT)

            self._log.info("Loading INI configuration from %s ...", ini_path)
            return IniStore(ini_path)
        elif cfg_type.lower() == "redis":
            url = self._get_config('Config', 'URL', None)
            if url:
                self._log.info("Loading Redis configuration from %s ...", url)
                return RedisStore(url=url)
            else:
                host = self._get_config('Config', 'Host', '127.0.0.1')
                port = self._get_config_int('Config', 'Port', 6379)
                db = self._get_config_int('Config', 'DB', 0)

                self._log.info("Loading Redis configuration from %s:%s/%s ...", host, port, db)
                return RedisStore(host=host, port=port, db=db,
                                  password=self._get_config('Config', 'Password', None))
        else:
            self._log.error("Configuration Type %s is unknown or not implemented", cfg_type)
            raise DashDaemonError(DashDaemonError.REASON_CONFIG_CONNECTION_INVALID)

    def _build_bus_writer(self) -> BusWriter:
        self._log.info("Connecting to Data Target Redis instance ...")
        return BusWriter(host=self._get_config('Destination', 'Host', '127.0.0.1'),
                         port=self._get_config_int('Destination', 'Port', 6379),
                         db=self._get_config_int('Destination', 'DB', 0),
                         password=self._get_config('Destination', 'Password', None))

    def _build_bus_reader(self, channels: list) -> TypedBusListener:
        self._log.info("Connecting to Data Source Redis instance ...")
        return TypedBusListener(channels,
                                host=self._get_config('Source', 'Host', '127.0.0.1'),
                                port=self._get_config_int('Source', 'Port', 6379),
                                db=self._get_config_int('Source', 'DB', 0),
                                password=self._get_config('Source', 'Password', None))

    def startup(self):
        self._log = log = logger(self.name)
        log.info("Starting up %s ...", self.name)

        channels = [
            LIVE_INPUT_DATA_KEYS['car_rpm'],
            LIVE_INPUT_DATA_KEYS['car_spd'],
            LIVE_INPUT_DATA_KEYS['car_map'],
            LIVE_INPUT_DATA_KEYS['car_tmp'],
            LIVE_INPUT_DATA_KEYS['car_ful']
        ]

        config = self._build_config_reader()
        reader = self._reader = self._build_bus_reader(channels)
        writer = self._build_bus_writer()

        reader.register_global_callback(self._on_new_value_registered)

        reader.start()
        self._running = True

        log.info("Ready to enter main loop")
        while self._running:
            self._step(config, writer)
            sleep(0.2)

        self._reader.stop()

    def shutdown(self):
        self._running = False
        if self._reader:
            self._reader.stop()

    def _on_new_value_registered(self, channel, value):
        self._log.debug("Reported new value from %s: %s", channel, value)
        self._current_values[channel] = value
        self._obd_last_updated = datetime.now()

    def _step(self, config: ConfigStore, writer: BusWriter):
        vehicle_data = self._process_vehicle_data(config)

        # Write object to Data Bus
        for key, value in vehicle_data.items():
            writer.publish(key, value)

    def _process_vehicle_data(self, config: ConfigStore) -> dict:
        values = self._current_values
        data = {
            LIVE_OUTPUT_DATA_KEYS['fuel_fail_flag']: 0,
            LIVE_OUTPUT_DATA_KEYS['speed']: values.get(LIVE_INPUT_DATA_KEYS['car_spd'], None),

        }

        if datetime.now() - self._obd_last_updated > timedelta(seconds=DashDaemon.ERROR_TIMEOUT):
            data[LIVE_OUTPUT_DATA_KEYS['fuel_fail_flag']] = 1
        else:
            try:
                # Calculate Fuel Efficiency
                rpm = values[LIVE_INPUT_DATA_KEYS['car_rpm']]
                map = values[LIVE_INPUT_DATA_KEYS['car_map']]
                in_tmp = values[LIVE_INPUT_DATA_KEYS['car_tmp']]

                fuel_status = values.get(LIVE_INPUT_DATA_KEYS['car_ful'], 2)

                vol_efficiency = config.read_int_value(CONFIG_KEYS['vol_efficency'], 85) / 100
                eng_volume = config.read_int_value(CONFIG_KEYS['engine_vol']) / 1000
                fuel_density = config.read_int_value(CONFIG_KEYS['fuel_density'], 745)

                lph = calculate_fuel_usage(rpm, map, in_tmp,
                                           vol_efficiency, eng_volume, fuel_density) \
                    if fuel_status != 4 else 0.00

                # The consumer has to calculate l/100km
                data[LIVE_OUTPUT_DATA_KEYS['fuel_usage']] = lph
            except (KeyError, TypeError):
                # If values aren't present, just fail fast
                data[LIVE_OUTPUT_DATA_KEYS['fuel_fail_flag']] = 1

        return data

    def _eval_vehicle_speed(self, config: ConfigStore,
                            car_spd, gps_spd, gps_spd_acc) -> int:
        max_gps_spd_acc = config.read_int_value(CONFIG_KEYS['gps_max_acc'], 5) / 3.6  # km/h => m/s

        if car_spd < 0 and gps_spd_acc < max_gps_spd_acc:
            return gps_spd if gps_spd >= 0 else 0
        elif car_spd >= 0:
            return car_spd

        return 0
