import streamlit as st

from ._util import Device, Sensor


def _badge_html(left: str | int, right: str, color: str) -> str:
    safe_left = (
        str(left).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    safe_right = (
        str(right).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    return (
        f'<span class="onc-badge onc-badge-{color}">'
        f'<span class="onc-badge-l">{safe_left}</span>'
        f'<span class="onc-badge-r">{safe_right}</span>'
        f"</span>"
    )


def _location_anchor(location_code: str) -> str:
    return f"location-code-{location_code}"


def _device_anchor(device_id: str) -> str:
    return f"device-id-{device_id.replace(' & ', '--')}"


def _sensor_anchor(sensor_id: str | int) -> str:
    return f"sensor-id-{sensor_id}"


def _sensor_pair_anchor(sensor1_id: str | int, sensor2_id: str | int) -> str:
    return f"{_sensor_anchor(sensor1_id)},{sensor2_id}"


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
            :root {
                --onc-badge-size-main-location: 1.03rem;
                --onc-badge-size-main-device: 0.92rem;
                --onc-badge-size-main-sensor: 0.82rem;
                --onc-badge-size-sidebar-location: 0.93rem;
                --onc-badge-size-sidebar-device: 0.84rem;
                --onc-badge-size-sidebar-sensor: 0.76rem;
            }

            /* Badge pill base */
            .onc-badge {
                display: inline-flex !important;
                align-items: stretch;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                border-radius: 8px;
                overflow: hidden;
                font-family: 'Plus Jakarta Sans', 'Segoe UI', system-ui, sans-serif;
                font-size: 0.85rem;
                line-height: 1;
                box-shadow: 0 1px 4px rgba(0, 0, 0, 0.13);
                white-space: nowrap;
                width: fit-content;
                max-width: 100%;
            }

            .onc-badge-l, .onc-badge-r {
                padding: 0.32em 0.65em;
                font-weight: 600;
                display: flex !important;
                align-items: center;
                flex: 0 0 auto;
                white-space: nowrap;
            }

            section[data-testid="stSidebar"] .onc-heading a {
                display: inline-block;
            }

            /* Site — lightblue */
            .onc-badge-lightblue .onc-badge-l { background: #0f2e4a; color: #cce9f7; }
            .onc-badge-lightblue .onc-badge-r { background: #b8ddf0; color: #0a2035; }

            /* Device — lightgreen */
            .onc-badge-lightgreen .onc-badge-l { background: #0f3020; color: #c8f0d8; }
            .onc-badge-lightgreen .onc-badge-r { background: #b5e8c8; color: #082514; }

            /* Sensor — gold */
            .onc-badge-gold .onc-badge-l { background: #3b2200; color: #fef3c7; }
            .onc-badge-gold .onc-badge-r { background: #fde68a; color: #3b2200; }

            /* Generic / aqua (default) */
            .onc-badge-aqua .onc-badge-l { background: #083344; color: #a5f3fc; }
            .onc-badge-aqua .onc-badge-r { background: #cffafe; color: #083344; }

            /* Hover animation for linked badges */
            a .onc-badge {
                transition: box-shadow 0.15s ease, transform 0.12s ease;
            }
            a:hover .onc-badge {
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
                transform: translateY(-1px);
            }

            /* Badge container element (non-heading to avoid Streamlit auto-slug anchors) */
            .onc-heading {
                font-size: 0;
                margin: 0.25rem 0 0.1rem !important;
                padding: 0 !important;
                border: none !important;
                line-height: 1 !important;
            }

            section[data-testid="stMain"] .onc-heading {
                margin: 0.55rem 0 0.4rem !important;
                padding: 0.05rem 0 0.08rem !important;
            }

            /* Keep custom hash targets visible below Streamlit's fixed top bar */
            .onc-heading[id] {
                scroll-margin-top: 3.75rem;
            }

            /* Body badge sizes */
            .onc-heading-1 .onc-badge { font-size: var(--onc-badge-size-main-location); }
            .onc-heading-2 .onc-badge { font-size: var(--onc-badge-size-main-device); }
            .onc-heading-3 .onc-badge { font-size: var(--onc-badge-size-main-sensor); }

            /* Sidebar: indentation + sizing */
            section[data-testid="stSidebar"] .onc-heading {
                margin: 0.2rem 0 0.08rem !important;
                padding: 0 !important;
            }
            section[data-testid="stSidebar"] .onc-heading-1 .onc-badge { font-size: var(--onc-badge-size-sidebar-location); }
            section[data-testid="stSidebar"] .onc-heading-2 { padding-left: 0.75rem !important; }
            section[data-testid="stSidebar"] .onc-heading-2 .onc-badge { font-size: var(--onc-badge-size-sidebar-device); }
            section[data-testid="stSidebar"] .onc-heading-3 { padding-left: 1.75rem !important; }
            section[data-testid="stSidebar"] .onc-heading-3 .onc-badge { font-size: var(--onc-badge-size-sidebar-sensor); }
        """
        sticky_devices_css = (
            """
            section[data-testid="stMain"] div[data-testid="stElementContainer"]:has(.onc-heading-2) {
                position: sticky;
                top: 3rem;
                z-index: 100;
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px);
            }"""
            if sticky_device
            else ""
        )

        sticky_location_css = (
            """
            section[data-testid="stSidebar"] div[data-testid="stElementContainer"]:has(.onc-heading-1) {
                position: sticky;
                top: 0rem;
                z-index: 100;
                padding: 1rem 0;
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px);
            }"""
            if sticky_location
            else ""
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
    def import_custom_widget_section_css():
        """
        Include custom CSS to make widgets and sections look more modern and beautiful.

        Example
        -------
        >>> client = ONCDW()
        >>> client.ui.import_custom_widget_section_css()
        """
        widget_section_css = """
            /* Typography improvements */
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Plus Jakarta Sans', 'Segoe UI', system-ui, sans-serif;
                letter-spacing: -0.01em;
            }

            h1 {
                font-size: 2rem;
                font-weight: 700;
                margin-bottom: 1.5rem;
            }

            h2 {
                font-size: 1.5rem;
                font-weight: 600;
                margin-top: 2.5rem;
                margin-bottom: 1.2rem;
                padding-bottom: 0.75rem;
                border-bottom: 2px solid rgba(128, 128, 128, 0.3);
            }

            h3 {
                font-size: 1.1rem;
                font-weight: 600;
                margin-top: 1.5rem;
                margin-bottom: 0.75rem;
            }

            /* Divider styling */
            hr {
                margin: 2rem 0;
                border: none;
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(128, 128, 128, 0.3), transparent);
            }

            /* Table styling */
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 1rem 0;
            }

            table th {
                font-weight: 600;
                padding: 0.75rem;
                text-align: left;
                border-bottom: 2px solid rgba(128, 128, 128, 0.3);
                font-family: 'Plus Jakarta Sans', 'Segoe UI', system-ui, sans-serif;
            }

            table td {
                padding: 0.75rem;
                border-bottom: 1px solid rgba(128, 128, 128, 0.15);
            }

            /* Chart container improvements */
            div[data-testid="stArrowVegaLiteChart"],
            div[data-testid="stPlotlyChart"],
            div[data-testid="stAltChart"] {
                border-radius: 8px;
                overflow: hidden;
                border: 1px solid rgba(128, 128, 128, 0.15);
                box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2) !important;
                margin: 1.5rem 0 !important;
                padding: 1rem;
            }

            /* Images in main content — scoped to avoid sidebar icons */
            section[data-testid="stMain"] img {
                border-radius: 8px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            }

            /* Links in main content — scoped to avoid sidebar nav */
            section[data-testid="stMain"] a {
                text-decoration: none;
                transition: opacity 0.15s ease;
            }

            section[data-testid="stMain"] a:hover {
                opacity: 0.8;
                text-decoration: underline;
            }

            /* Alert boxes */
            div[data-testid="stAlert"] {
                border-radius: 8px;
            }

            /* Expander — let Streamlit own the background */
            div[data-testid="stExpander"] {
                border-radius: 8px;
            }

            /* Tab styling */
            div[role="tab"] {
                font-family: 'Plus Jakarta Sans', 'Segoe UI', system-ui, sans-serif;
                font-weight: 500;
            }

            /* Metric styling */
            div[data-testid="stMetricValue"] {
                font-family: 'Plus Jakarta Sans', 'Segoe UI', system-ui, sans-serif;
                font-weight: 600;
            }
        """
        st.markdown(
            f"""
            <style>
                {widget_section_css}
            </style>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def badge(
        level: int,
        left: str,
        right: str,
        href: str = "",
        anchor: str = "",
        color: str = "aqua",
    ):
        """Render a badge row where level controls relative size (1 > 2 > 3)."""
        if level not in (1, 2, 3):
            level = 1
        badge = _badge_html(left, right, color)
        if href:
            assert href.startswith("http") or href.startswith("#")
            href_safe = href.replace('"', "%22")
            target = (
                ' target="_blank" rel="noopener noreferrer"'
                if href.startswith("http")
                else ""
            )
            inner = f'<a href="{href_safe}"{target} style="text-decoration:none">{badge}</a>'
        else:
            inner = badge
        id_attr = f' id="{anchor}"' if anchor else ""
        html = f'<div class="onc-heading onc-heading-{level}"{id_attr}>{inner}</div>'
        st.markdown(html, unsafe_allow_html=True)

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
        anchor = _location_anchor(left)

        return UI.badge(1, left, right, href=href, anchor=anchor, color="lightblue")

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
        href = f"#{_location_anchor(right)}"
        return UI.badge(1, left, right, href=href, anchor="", color="lightblue")

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

        right = _device.get_device_name() or _device.get_device_code()
        anchor = _device_anchor(left)
        if "&" in left:
            # This is a concat two-devices, no href is needed
            return UI.badge(2, left, right, href="", anchor=anchor, color="lightgreen")
        else:
            href = f"https://data.oceannetworks.ca/DeviceListing?DeviceId={left}"
            return UI.badge(
                2, left, right, href=href, anchor=anchor, color="lightgreen"
            )

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

        right = _device.get_device_code()
        href = f"#{_device_anchor(left)}"

        return UI.badge(2, left, right, href=href, anchor="", color="lightgreen")

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
        left = str(_sensor.get_sensor_id())
        right = _sensor.get_sensor_name()
        href = f"https://data.oceannetworks.ca/SensorListing?SensorId={left}"
        if not anchor:
            anchor = _sensor_anchor(left)

        return UI.badge(3, left, right, href=href, anchor=anchor, color="gold")

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
        left = str(_sensor.get_sensor_id())
        right = _sensor.get_sensor_name()
        if href is None:
            href = f"#{_sensor_anchor(left)}"

        return UI.badge(3, left, right, href=href, anchor="", color="gold")

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
        anchor = _sensor_pair_anchor(_sensor1.get_sensor_id(), _sensor2.get_sensor_id())
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

        href = f"#{_sensor_pair_anchor(_sensor1.get_sensor_id(), _sensor2.get_sensor_id())}"
        UI.sensor_sidebar(sensor1, href=href)
        UI.sensor_sidebar(sensor2, href=href)
