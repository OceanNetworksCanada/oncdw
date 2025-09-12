from dataclasses import dataclass

from .util import get_val_from_keys


@dataclass
class DataPreviewOption:
    """
    A helper class to handle data preview options for data preview widgets.

    The format of data preview options can be:
    2. A dictionary with keys like 'dataProductFormatId', 'plotNumber', 'sensorCodeId'
    or 'data_product_format_id', 'plot_number', 'sensor_code_id'.

    plot_number (default to be 1) and sensor_code_id (default to be None) are optional.
    """

    _data_preview_option: dict

    def get_data_product_format_id(self) -> int:
        """
        Get the data product format id from the data preview options.
        """
        if isinstance(self._data_preview_option, dict):
            keys = ["dataProductFormatId", "data_product_format_id"]
            return get_val_from_keys(self._data_preview_option, keys)
        else:
            raise ValueError(
                f"Could not get data product format id from {self._data_preview_option}."
            )

    def get_plot_number(self) -> int:
        """
        Get the plot number from the data preview options.
        Defaults to 1 if not specified or the value is None.
        """
        if isinstance(self._data_preview_option, dict):
            keys = ["plotNumber", "plot_number"]
            val = get_val_from_keys(
                self._data_preview_option, keys, raise_error=False, default=1
            )
            return val if val is not None else 1
        else:
            raise ValueError(
                f"Could not get plot number from {self._data_preview_option}."
            )

    def get_sensor_code_id(self) -> int | None:
        """
        Get the sensor code id from the data preview options.
        Defaults to None if not specified or being 0.
        """
        if isinstance(self._data_preview_option, dict):
            keys = ["sensorCodeId", "sensor_code_id"]
            return get_val_from_keys(
                self._data_preview_option, keys, raise_error=False, default=None
            )
        else:
            raise ValueError(
                f"Could not get sensor code id from {self._data_preview_option}."
            )
