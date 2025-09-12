from dataclasses import dataclass

from .util import get_val_from_keys


@dataclass
class Device:
    """
    A helper class to handle value retrieval from a device dictionary.
    Different data widgets may expect different keys in the device dictionary.
    """

    _device: dict

    def get_device_id(self):
        """
        Get the device id from the device dictionary.
        Raise KeyError if the dict does not contain the expected key.
        """
        keys = ["deviceId", "device_id"]
        return get_val_from_keys(self._device, keys, raise_error=True)

    def get_device_code(self) -> str:
        """
        Get the device code from the device dictionary.
        Raise KeyError if the dict does not contain the expected key.
        """
        keys = ["deviceCode", "device_code"]
        return get_val_from_keys(self._device, keys, raise_error=True)

    def get_device_name(self) -> str | None:
        """
        Get the device name from the device dictionary.
        Return None if the dict does not contain the expected key.
        """
        keys = ["deviceName", "device_name"]
        return get_val_from_keys(self._device, keys, raise_error=False)

    def get_file_extensions(self) -> list[str] | None:
        """
        Get the file extension from the device dictionary.
        Return None if the dict does not contain the expected key.
        """
        keys = ["fileExtensions", "file_extensions", "file_extension", "fileExtension"]
        return get_val_from_keys(self._device, keys, raise_error=False)

    def get_device_category_id(self) -> int | str:
        """
        Get the device category id from the device dictionary.
        Raise KeyError if the dict does not contain the expected key.
        """
        keys = ["deviceCategoryId", "device_category_id"]
        return get_val_from_keys(self._device, keys, raise_error=True)

    def get_search_tree_node_id(self) -> int | str:
        """
        Get the search tree node id from the device dictionary.
        Raise KeyError if the dict does not contain the expected key.
        """
        keys = ["searchTreeNodeId", "search_tree_node_id"]
        return get_val_from_keys(self._device, keys, raise_error=True)

    def get_location_code(self) -> str:
        """
        Get the location code from the device dictionary.
        Raise KeyError if the dict does not contain the expected key.
        """
        keys = ["locationCode", "location_code"]
        return get_val_from_keys(self._device, keys, raise_error=True)

    def get_location_name(self) -> str:
        """
        Get the location name from the device dictionary.
        Raise KeyError if the dict does not contain the expected key.
        """
        keys = ["locationName", "location_name"]
        return get_val_from_keys(self._device, keys, raise_error=True)

    def get_device_category_code(self) -> str:
        """
        Get the device category code from the device dictionary.
        Raise KeyError if the dict does not contain the expected key.
        """
        keys = ["deviceCategoryCode", "device_category_code"]
        return get_val_from_keys(self._device, keys, raise_error=True)

    def get_data_preview_options(self) -> list | None:
        """
        Get the data preview options from the device dictionary.
        Return None if the dict does not contain the expected key.
        """
        keys = ["dataPreviewOptions", "data_preview_options"]
        return get_val_from_keys(self._device, keys, raise_error=False, default=None)
