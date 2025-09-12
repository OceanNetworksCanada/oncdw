def get_val_from_keys(data: dict, keys: list[str], raise_error=True, default=None):
    """
    Get the value from the dictionary by checking the keys in order.
    If a key is not found, it will either raise a KeyError, or return None.
    """
    for key in keys:
        if key in data:
            return data[key]

    if raise_error:
        raise KeyError(f"None of the keys {keys} found in the dictionary {data}.")
    else:
        return default


def natural_size(size: int) -> str:
    """
    Convert a size in bytes to a human-readable format.
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"  # If size is larger than 1 PB


def get_archive_file_download_link(filename: str, token: str):
    return f"https://data.oceannetworks.ca/api/archivefile/download?filename={filename}&token={token}"  # noqa: E501
