import streamlit as st

from ._util import Device, Sensor


def _badge_shields(left: str | int, right: str, color) -> str:
    def _sanitize(input_text):
        return str(input_text).replace(" ", "%20").replace("-", "--").replace("_", "__")

    encoded_left = _sanitize(left)
    encoded_right = _sanitize(right)
    img_alt_text = f"{left} - {right}"
    return f"![{img_alt_text}](https://img.shields.io/badge/{encoded_left}-{encoded_right}-{color})"


class UI:
    @staticmethod
    def import_custom_badge_css(sticky_device=False, sticky_location=False):
        """
        Include a custom css to make badge look bigger.

        Example
        -------
        >>> client = ONCDW()
        >>> client.ui.import_custom_badge_css()
        """
        badge_css = """
            /* Sidebar CSS */
            section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
                gap: 0rem;
            }

            section[data-testid="stSidebar"] h1 img {
                height: 2.25rem;
            }

            section[data-testid="stSidebar"] h2 img {
                height: 2rem;
                padding-left: 0.5rem;
            }

            section[data-testid="stSidebar"] h3 img {
                height: 1.75rem;
                padding-left: 1rem;
            }

            /* Body Badge CSS */
            h1 img {
                height: 2.5rem;
            }

            h2 img {
                height: 2.25rem;
            }

            h3 img {
                height: 2rem;
            }"""
        sticky_devices_css = (
            """
            section[data-testid="stMain"] div[data-testid="stElementContainer"]:has(h2) {
                position: sticky;
                top: 3rem;
                z-index:100;
                background-color: white;
            }"""
            if sticky_device
            else None
        )

        sticky_location_css = (
            """
            section[data-testid="stSidebar"] div[data-testid="stElementContainer"]:has(h1) {
                position: sticky;
                top: 0rem;
                z-index:100;
                padding: 1rem 0;
                background-color: rgb(240, 242, 246);
            }"""
            if sticky_location
            else None
        )

        st.markdown(
            f"""
            <style>
                {badge_css}
                {sticky_devices_css}
                {sticky_location_css}
            </style>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def _badge(
        st_func,
        left: str,
        right: str,
        href: str,
        anchor: str,
        color: str,
    ):
        """
        Basic function to create a badge with an anchor and an optional href link.
        """
        if href:
            assert href.startswith("http") or href.startswith("#")
            return st_func(
                f"[{_badge_shields(left, right, color)}]({href})", anchor=anchor
            )
        else:
            return st_func(f"{_badge_shields(left, right, color)}", anchor=anchor)

    @staticmethod
    def h1_badge(
        left: str,
        right: str,
        href: str = "",
        anchor: str = "",
        color: str = "aqua",
    ):
        return UI._badge(st.title, left, right, href, anchor, color)

    @staticmethod
    def h2_badge(
        left: str,
        right: str,
        href: str = "",
        anchor: str = "",
        color: str = "aqua",
    ):
        return UI._badge(st.header, left, right, href, anchor, color)

    @staticmethod
    def h3_badge(
        left: str,
        right: str,
        href: str = "",
        anchor: str = "",
        color: str = "aqua",
    ):
        return UI._badge(st.subheader, left, right, href, anchor, color)

    @staticmethod
    def location(location: dict):
        """
        Location badge wrapped inside a h1 tag.

        The href is a link to the Data Search page for the location code.
        The anchor is matched with the href of `location_sidebar()`.

        Parameters
        ----------
        location: dict
            A dictionary containing the location code and name.
            Usually it is a device dict that has location info inside.

        Example
        -------
        >>> client = ONCDW()
        >>> device = {
        ...     "location_code": "CODE",
        ...     "location_name": "Location Name",
        ... }
        >>> client.ui.location(device)
        """
        _location = Device(location)
        left = _location.get_location_code()
        right = _location.get_location_name()
        href = f"https://data.oceannetworks.ca/DataSearch?location={left}"
        anchor = f"location-code-{left}"

        return UI.h1_badge(left, right, href=href, anchor=anchor, color="lightblue")

    @staticmethod
    def location_sidebar(location: dict):
        """
        Location badge for the sidebar wrapped inside a h1 tag.

        The href is a link to the anchor of `location()`.

        Parameters
        ----------
        location: dict
            A dictionary containing the location code and name.
            Usually it is a device dict that has location info inside.

        Example
        -------
        >>> client = ONCDW()
        >>> device = {
        ...     "location_code": "CODE",
        ...     "location_name": "Location Name",
        ... }
        >>> client.ui.location_sidebar(device)
        """
        _location = Device(location)
        left = "Site"
        right = _location.get_location_code()
        href = f"#location-code-{right}"
        return UI.h1_badge(left, right, href=href, color="lightblue")

    @staticmethod
    def device(device: dict):
        """
        Device badge wrapped inside a h2 tag.

        The href is a link to the Data Details page for the device id.
        The anchor is matched with the href of `device_sidebar()`.
        Device name is used as the right side of the badge if present, otherwise device code is used.

        Parameters
        ----------
        device: dict
            A dictionary containing the device id, device code and device name.

        Example
        -------
        >>> client = ONCDW()
        >>> device = {
        ...     "device_id": "12345",
        ...     "device_name": "Device Name",
        ... }
        >>> client.ui.device(device)
        """
        _device = Device(device)

        left = str(_device.get_device_id())
        left_sanitized = left.replace(" & ", "--")

        right = _device.get_device_name() or _device.get_device_code()
        anchor = f"device-id-{left_sanitized}"
        if "&" in left:
            # This is a concat two-devices, no href is needed
            return UI.h2_badge(left, right, anchor=anchor, color="lightgreen")
        else:
            href = f"https://data.oceannetworks.ca/DeviceListing?DeviceId={left}"
            return UI.h2_badge(left, right, href, anchor, color="lightgreen")

    @staticmethod
    def device_sidebar(device: dict):
        """
        Device badge for the sidebar wrapped inside a h2 tag.

        The href a link to the anchor of `device()`.

        Parameters
        ----------
        device: dict
            A dictionary containing the device id and device code.

        Example
        -------
        >>> client = ONCDW()
        >>> device = {
        ...     "device_id": "12345",
        ...     "device_code": "CODE"
        ... }
        >>> client.ui.device_sidebar(device)
        """
        _device = Device(device)

        left = str(_device.get_device_id())
        left_sanitized = left.replace(" & ", "--")

        right = _device.get_device_code()
        href = f"#device-id-{left_sanitized}"

        return UI.h2_badge(left, right, href, color="lightgreen")

    @staticmethod
    def sensor(sensor: dict, anchor: str = ""):
        """
        Sensor badge wrapped inside a h3 tag.

        The href is a link to the Sensor Details page for the sensor id.
        The anchor is matched with the href of `sensor_sidebar()`.

        Parameters
        ----------
        sensor: dict
            A dictionary containing the sensor id and sensor name.
        anchor : str
            The anchor link of the badge.

        Example
        -------
        >>> client = ONCDW()
        >>> sensor = {
        ...     "sensor_id": "67900",
        ...     "sensor_name": "Sensor Name"
        ... }
        >>> client.ui.sensor_sidebar(sensor)
        """
        _sensor = Sensor(sensor)
        left = _sensor.get_sensor_id()
        right = _sensor.get_sensor_name()
        href = f"https://data.oceannetworks.ca/SensorListing?SensorId={left}"
        if not anchor:
            anchor = f"sensor-id-{left}"

        return UI.h3_badge(left, right, href, anchor, color="gold")

    @staticmethod
    def sensor_sidebar(sensor: dict, href: str | None = None):
        """
        Sensor badge for the sidebar wrapped inside a h3 tag.

        The href a link to the anchor of `sensor()`.

        Parameters
        ----------
        sensor : dict
            A dictionary containing the sensor id and sensor name.
        href : str or None, optional
            The href link of the badge.

        Example
        -------
        >>> client = ONCDW()
        >>> sensor = {
        ...     "sensor_id": "67900",
        ...     "sensor_name": "Sensor Name"
        ... }
        >>> client.ui.sensor_sidebar(sensor)
        """
        _sensor = Sensor(sensor)
        left = _sensor.get_sensor_id()
        right = _sensor.get_sensor_name()
        if href is None:
            href = f"#sensor-id-{left}"

        return UI.h3_badge(left, right, href, color="gold")

    @staticmethod
    def sensors_two(sensor1: dict, sensor2: dict):
        """
        Two sensor badges for two sensors wrapped inside a h3 tag.

        The href is a link to the Sensor Details page for the individual sensor id.
        The anchor is matched with the href of `sensors_two_sidebar()`.

        Parameters
        ----------
        sensor1, sensor2: dict
            A dictionary containing the sensor id and sensor name.

        Example
        -------
        >>> client = ONCDW()
        >>> sensor1 = {
        ...     "sensor_id": "167900",
        ...     "sensor_name": "Sensor Name 1"
        ... }
        >>> sensor2 = {
        ...     "sensor_id": "267900",
        ...     "sensor_name": "Sensor Name 2"
        ... }
        >>> client.ui.sensor_sidebar(sensor1, sensor2)
        """
        col1, col2 = st.columns(2, gap="large")
        _sensor1 = Sensor(sensor1)
        _sensor2 = Sensor(sensor2)
        anchor = f"sensor-id-{_sensor1.get_sensor_id()},{_sensor2.get_sensor_id()}"
        with col1:
            UI.sensor(sensor1, anchor=anchor)
        with col2:
            UI.sensor(sensor2, anchor=anchor)

    @staticmethod
    def sensors_two_sidebar(sensor1: dict, sensor2: dict):
        """
        One sensor badge for two sensors for the sidebar wrapped inside a h3 tag.

        The href a link to the anchor of `sensors_two()`.

        Parameters
        ----------
        sensor1, sensor2: dict
            A dictionary containing the sensor id and sensor name.

        Example
        -------
        >>> client = ONCDW()
        >>> sensor1 = {
        ...     "sensor_id": "167900",
        ...     "sensor_name": "Sensor Name 1"
        ... }
        >>> sensor2 = {
        ...     "sensor_id": "267900",
        ...     "sensor_name": "Sensor Name 2"
        ... }
        >>> client.ui.sensors_two_sidebar(sensor1, sensor2)
        """
        _sensor1 = Sensor(sensor1)
        _sensor2 = Sensor(sensor2)

        href = f"#sensor-id-{_sensor1.get_sensor_id()},{_sensor2.get_sensor_id()}"
        UI.sensor_sidebar(sensor1, href=href)
        UI.sensor_sidebar(sensor2, href=href)
