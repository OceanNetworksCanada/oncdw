from dataclasses import dataclass

from .util import get_val_from_keys


@dataclass
class Sensor:
    """
    A helper class to handle value retrieval from a sensor dictionary.
    If it is a dict, it should contain keys like 'sensorId' / 'sensor_id' or 'sensorName' / 'sensor_name'.
    If it is an int, it is assumed to be the sensor id.
    """

    _sensor: dict | int

    def get_sensor_id(self):
        """
        Get the sensor id from the sensor.
        """
        if isinstance(self._sensor, dict):
            keys = ["sensor_id", "sensorId"]
            return get_val_from_keys(self._sensor, keys)
        elif isinstance(self._sensor, int):
            return self._sensor
        else:
            raise ValueError(f"Could not get sensor id from {self._sensor}.")

    def get_sensor_name(self) -> str:
        """
        Get the sensor name from the sensor.
        """
        if isinstance(self._sensor, dict):
            keys = ["sensor_name", "sensorName"]
            return get_val_from_keys(self._sensor, keys)
        else:
            raise ValueError(f"Could not get sensor name from {self._sensor}.")
