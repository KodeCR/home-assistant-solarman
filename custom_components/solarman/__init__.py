"""The SolarMAN logger integration."""
from __future__ import annotations
from asyncio.streams import StreamReader, StreamWriter

import logging
import asyncio

from homeassistant.config_entries import ConfigType, ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import (
    DOMAIN,
    SENSOR_VDC1,
    SENSOR_IDC1,
    SENSOR_VDC2,
    SENSOR_IDC2,
    SENSOR_VAC,
    SENSOR_IAC,
    SENSOR_FREQ,
    SENSOR_TEMP,
    SENSOR_PWR,
    SENSOR_ENERGY_DAY,
    SENSOR_ENERGY_TOT,
    SENSOR_HRS,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the SolarMAN logger component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SolarMAN logger from a config entry."""
    inverter = Inverter(hass, entry)
    try:
        inverter.server = await asyncio.start_server(
            inverter.async_refresh, inverter.host, inverter.port
        )
    except OSError:
        pass
    hass.data[DOMAIN][entry.entry_id] = inverter
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(update_listener))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN][entry.entry_id].server.close()
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    hass.data[DOMAIN][entry.entry_id].config(entry)
    entry.title = entry.options[CONF_HOST]


class Inverter:
    """The solar inverter."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Init solar inverter."""
        self._hass = hass
        self.host = ""
        self.port = 0
        self.server = None
        self.data = {}
        self.sensors = []
        self.config(entry)

    def config(self, entry: ConfigEntry) -> None:
        self.host = entry.options[CONF_HOST]
        self.port = entry.options[CONF_PORT]

    def parse_data(self, data, start_byte, num_bytes, div):
        result = int.from_bytes(
            data[start_byte : start_byte + num_bytes], byteorder="big"
        )
        if div != 1:
            result /= div
        return result

    async def async_refresh(self, reader: StreamReader, writer: StreamWriter):
        data = await reader.read()
        if len(data) >= 79:
            self.data[SENSOR_TEMP] = self.parse_data(data, 31, 2, 10)
            self.data[SENSOR_VDC1] = self.parse_data(data, 33, 2, 10)
            self.data[SENSOR_VDC2] = self.parse_data(data, 35, 2, 10)
            self.data[SENSOR_IDC1] = self.parse_data(data, 39, 2, 10)
            self.data[SENSOR_IDC2] = self.parse_data(data, 41, 2, 10)
            self.data[SENSOR_IAC] = self.parse_data(data, 45, 2, 10)
            self.data[SENSOR_VAC] = self.parse_data(data, 51, 2, 10)
            self.data[SENSOR_FREQ] = self.parse_data(data, 57, 2, 100)
            self.data[SENSOR_PWR] = self.parse_data(data, 59, 2, 1)
            self.data[SENSOR_ENERGY_DAY] = 10 * self.parse_data(data, 69, 2, 1)
            self.data[SENSOR_ENERGY_TOT] = self.parse_data(data, 71, 4, 10)
            self.data[SENSOR_HRS] = self.parse_data(data, 75, 4, 1)
            for sensor in self.sensors:
                if sensor.name in self.data:
                    sensor.value = self.data[sensor.name]
                    sensor.online = True
                    sensor.async_schedule_update_ha_state()
