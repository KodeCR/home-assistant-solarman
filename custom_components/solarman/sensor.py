"""Platform for SolarMAN logger sensor integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.util.dt import utc_from_timestamp
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components.sensor import (
    SensorEntity,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
)
from homeassistant.const import (
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_TEMPERATURE,
    # DEVICE_CLASS_FREQUENCY,
    DEVICE_CLASS_ENERGY,
    # DEVICE_CLASS_TIME,
    ELECTRIC_POTENTIAL_VOLT,
    ELECTRIC_CURRENT_AMPERE,
    POWER_WATT,
    TEMP_CELSIUS,
    FREQUENCY_HERTZ,
    ENERGY_WATT_HOUR,
    ENERGY_KILO_WATT_HOUR,
    TIME_HOURS,
)

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


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the SolarMAN logger sensor platform."""
    sensors = []
    sensors.append(
        SolarMANSensor(
            SENSOR_VDC1,
            DEVICE_CLASS_VOLTAGE,
            STATE_CLASS_MEASUREMENT,
            ELECTRIC_POTENTIAL_VOLT,
            entry.unique_id,
        )
    )
    sensors.append(
        SolarMANSensor(
            SENSOR_IDC1,
            DEVICE_CLASS_CURRENT,
            STATE_CLASS_MEASUREMENT,
            ELECTRIC_CURRENT_AMPERE,
            entry.unique_id,
        )
    )
    sensors.append(
        SolarMANSensor(
            SENSOR_VDC2,
            DEVICE_CLASS_VOLTAGE,
            STATE_CLASS_MEASUREMENT,
            ELECTRIC_POTENTIAL_VOLT,
            entry.unique_id,
        )
    )
    sensors.append(
        SolarMANSensor(
            SENSOR_IDC2,
            DEVICE_CLASS_CURRENT,
            STATE_CLASS_MEASUREMENT,
            ELECTRIC_CURRENT_AMPERE,
            entry.unique_id,
        )
    )
    sensors.append(
        SolarMANSensor(
            SENSOR_VAC,
            DEVICE_CLASS_VOLTAGE,
            STATE_CLASS_MEASUREMENT,
            ELECTRIC_POTENTIAL_VOLT,
            entry.unique_id,
        )
    )
    sensors.append(
        SolarMANSensor(
            SENSOR_IAC,
            DEVICE_CLASS_CURRENT,
            STATE_CLASS_MEASUREMENT,
            ELECTRIC_CURRENT_AMPERE,
            entry.unique_id,
        )
    )
    sensors.append(
        SolarMANSensor(
            SENSOR_FREQ,
            None,
            STATE_CLASS_MEASUREMENT,
            FREQUENCY_HERTZ,
            entry.unique_id,
        )
    )
    sensors.append(
        SolarMANSensor(
            SENSOR_TEMP,
            DEVICE_CLASS_TEMPERATURE,
            STATE_CLASS_TOTAL_INCREASING,
            TEMP_CELSIUS,
            entry.unique_id,
        )
    )
    sensors.append(
        SolarMANSensor(
            SENSOR_PWR,
            DEVICE_CLASS_POWER,
            STATE_CLASS_MEASUREMENT,
            POWER_WATT,
            entry.unique_id,
        )
    )
    sensors.append(
        SolarMANSensor(
            SENSOR_ENERGY_DAY,
            DEVICE_CLASS_ENERGY,
            STATE_CLASS_TOTAL_INCREASING,
            ENERGY_WATT_HOUR,
            entry.unique_id,
        )
    )
    sensors.append(
        SolarMANSensor(
            SENSOR_ENERGY_TOT,
            DEVICE_CLASS_ENERGY,
            STATE_CLASS_TOTAL_INCREASING,
            ENERGY_KILO_WATT_HOUR,
            entry.unique_id,
        )
    )
    sensors.append(
        SolarMANSensor(
            SENSOR_HRS,
            None,
            STATE_CLASS_TOTAL_INCREASING,
            TIME_HOURS,
            entry.unique_id,
        )
    )
    hass.data[DOMAIN][entry.entry_id].sensors = sensors
    async_add_entities(sensors)


class SolarMANSensor(SensorEntity):
    """Representation of a SolarMAN logger device."""

    def __init__(self, name, device_class, state_class, unit, uid):
        """Initialize the sensor."""
        self._name = name
        self._device_class = device_class
        self._state_class = state_class
        self._unit = unit
        self._uid = uid
        self.online = False
        self.value = 0

    @property
    def unique_id(self):
        """Return unique id."""
        return f"{DOMAIN}_{self._name}"

    @property
    def name(self):
        """Name of this inverter attribute."""
        return self._name

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this device."""
        return {
            "identifiers": {(DOMAIN, self._uid)},
            "name": "SolarMAN",
            "model": "Logger",
            "manufacturer": "IGEN Tech",
        }

    @property
    def device_class(self):
        """State of this inverter attribute."""
        return self._device_class

    @property
    def state_class(self):
        """State of this inverter attribute."""
        return self._state_class

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def native_value(self):
        """State of this inverter attribute."""
        return self.value

    @property
    def should_poll(self) -> bool:
        """No polling needed."""
        return False

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.online
