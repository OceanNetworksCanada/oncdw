from typing import TYPE_CHECKING

import streamlit as st
from onc import ONC

from ._util import Device

if TYPE_CHECKING:
    from ._client import ONCDW


class Section:
    def __init__(self, client: "ONCDW"):
        self._client = client
        self._prev_location_code = None
        self._prev_location_code_sidebar = None

    def links(self, links: dict, header: str = "Links"):
        """
        Display a section with links.

        Parameters
        ----------
        links : dict
            A dictionary of links to be displayed at the top of the page.
            The keys are the link titles, and the values are the URLs.
        header : str
            Header string above the links

        Examples
        --------
        >>> client = ONCDW()
        >>> links = {
        ...     "Oceans 3.0": "https://data.oceannetworks.ca",
        ...     "Marine Traffic": "https://www.marinetraffic.com",
        ... }
        >>> client.section.links(links, "Useful Links")
        """
        st.header(header)
        for title, url in links.items():
            st.subheader(f"[{title}]({url})")

    def state_of_ocean_images(self, location_code: str):
        """
        Display the State of Ocean images for a given location code.

        Also return the information needed to display labels in the sidebar.

        Parameters
        ----------
        location_code : str
            The location code to construct the image URLs.

        Returns
        -------
        labels : list of tuples
            A list of tuples containing the label titles and their corresponding URLs.

        Examples
        --------
        >>> client = ONCDW()
        >>> client.section.state_of_ocean_images("BACAX")

        """
        images = [
            (
                "State of Ocean Climate plot",
                f"https://ftp.oceannetworks.ca/pub/DataProducts/SOO/{location_code}/{location_code}-StateOfOceanEnv-Climate.png",
            ),
            (
                "State of Ocean Anomaly plot",
                f"https://ftp.oceannetworks.ca/pub/DataProducts/SOO/{location_code}/{location_code}-StateOfOceanEnv-Anomaly.png",
            ),
            (
                "State of Ocean Min/Max plot",
                f"https://ftp.oceannetworks.ca/pub/DataProducts/SOO/{location_code}/{location_code}-StateOfOceanEnv_MinMaxAvg1day.png",
            ),
        ]

        for title, url in images:
            st.header(title)
            st.image(url)

        # Format is [(label_left, label_right, href)]
        labels = [
            ("SOOC", "Climate", "#state-of-ocean-climate-plot"),
            ("SOOA", "Anomaly", "#state-of-ocean-anomaly-plot"),
            ("SOOM", "MinMax", "#state-of-ocean-min-max-plot"),
        ]

        return labels

    def time_series(
        self,
        sensor: list | dict,
        date_from: str = "-P7D",
        date_to: str | None = None,
        shade: bool = True,
    ):
        """
        Display time series plots for a given sensor or two sensors, with labels above the plot.

        Parameters
        ----------
        sensor : list
            A list representing a sensor or a pair of sensors.
            The format can be either:
            1. dict: a single sensor, {"sensor_id": sensor_id, "sensor_name": sensor_name}
            2. list: a pair of sensors, [{},{}]. The format of each dict is the same as a single sensor
        date_from : str
            date_from parameter for the web service
        date_to : str or None, optional
            date_to parameter for the web service
        shade : bool, default True
            Whether to show the shaded min-max band around the line.

        Examples
        --------
        >>> client = ONCDW()
        >>> sensor = {
        ...    "sensor_id": 7684,
        ...    "sensor_name": "True Heading",
        ... }
        >>> client.section.time_series(sensor)
        >>> sensor1 = {
        ...     "sensor_id": 4182,
        ...     "sensor_name": "Seafloor Pressure"
        ... }
        >>> sensor2 = {
        ...     "sensor_id": 7712,
        ...     "sensor_name": "Uncompensated Seafloor Pressure"
        ... }
        >>> sensor = [sensor1, sensor2]
        >>> client.section.time_series(sensor)
        """
        if isinstance(sensor, list):
            # The sensor is a pair of sensors
            sensor1, sensor2 = sensor
            self._client.ui.sensors_two(sensor1, sensor2)
            self._client.widget.time_series_two_sensors(
                sensor1, sensor2, date_from=date_from, date_to=date_to, shade=shade
            )
        elif isinstance(sensor, dict):
            # The sensor is a single sensor
            self._client.ui.sensor(sensor)
            self._client.widget.time_series(
                sensor, date_from=date_from, date_to=date_to, shade=shade
            )
        else:
            raise ValueError(
                f"Invalid sensor format: {sensor}. Expected a list or dict."
            )

    def data_preview(self, device: dict):
        """
        Display data preview plots for multiple data preview options.

        Assume data preview plots are placed in two columns,
        and the options are a list of a dict in device["data_preview_options"].

        Parameters
        ----------
        device : dict
            a dict containing search tree node id, device category id
            and data preview options, which is a list of data preview option.
            The dict of data preview option should have the following keys:

            - data_product_format_id
            - plot_number, optional, default 1
            - sensor_code_id, optional

        Examples
        --------
        >>> client = ONCDW()
        >>> device = {
        ...     "search_tree_node_id": 450,
        ...     "device_category_id": 72,
        ...     "data_preview_options": [
        ...         {
        ...             "data_product_format_id": 3,
        ...             "plot_number": 1
        ...         },
        ...         {
        ...             "data_product_format_id": 3,
        ...             "plot_number": 2
        ...         },
        ...     ]
        ... }
        >>> client.section.data_preview(device)
        """
        _device = Device(device)
        data_preview_options = _device.get_data_preview_options()
        if not data_preview_options:
            return

        st.subheader("Data Preview plot")

        # Data preview plots in two columns
        for i in range(0, len(data_preview_options), 2):
            # Get two data preview options for two columns, if available
            options: list[dict] = data_preview_options[i : i + 2]
            if len(options) == 2:
                option1, option2 = options
            else:
                # Deal with odd length of data preview options
                option1 = options[0]
                option2 = None

            cols = st.columns(2)
            with st.container():
                with cols[0]:
                    self._client.widget.data_preview(device, option1)

                with cols[1]:
                    if option2:
                        self._client.widget.data_preview(device, option2)

    def location_expander(self, location: dict):
        """
        Display a location label and information retrieved from /api/location web service.

        This method has a global variable `_prev_location_code` to record the previous location,
        so that it only displays distinct locations.

        Parameters
        ----------
        location : dict
            A dict that contains a location code

        Examples
        --------
        >>> client = ONCDW()
        >>> device = {
        ...     "location_code": "BACAX",
        ...     "location_name": "Barkley Canyon Axis",
        ... }
        >>> client.section.location_expander(device)
        """
        _location = Device(location)
        if self._prev_location_code != _location.get_location_code():
            self._prev_location_code = _location.get_location_code()
            onc = ONC(self._client.token)

            self._client.ui.location(location)
            location_info = onc.getLocations(
                {"locationCode": _location.get_location_code()}
            )
            with st.expander("Location Info", expanded=False):
                st.json(location_info)

    def location_sidebar(self, location: dict):
        """
        Display a location label in the side bar.

        This method has a global variable `_prev_location_code_sidebar` to record the previous location,
        so that it only displays distinct locations.

        Parameters
        ----------
        location : dict
            A dict that contains a location code

        Examples
        --------
        >>> client = ONCDW()
        >>> device = {
        ...     "location_code": "BACAX"
        ... }
        >>> client.section.location_sidebar(device)
        """
        _location = Device(location)
        if self._prev_location_code_sidebar != _location.get_location_code():
            self._prev_location_code_sidebar = _location.get_location_code()
            self._client.ui.location_sidebar(location)

    def sensor_sidebar(self, sensor: list | dict):
        """
        Display a sensor or two sensors label in the sidebar, with the correct href link.

        Parameters
        ----------
        sensor : list
            A list representing a sensor or a pair of sensors.
            The format can be either:
            1. dict: a single sensor, {"sensor_id": sensor_id, "sensor_name": sensor_name}
            2. list: a pair of sensors, [{},{}]. The format of each dict is the same as a single sensor

        Examples
        --------
        >>> client = ONCDW()
        >>> sensor = {
        ...    "sensor_id": 7684,
        ...    "sensor_name": "True Heading",
        ... }
        >>> client.section.sensor_sidebar(sensor)
        >>> sensor1 = {
        ...     "sensor_id": 4182,
        ...     "sensor_name": "Seafloor Pressure"
        ... }
        >>> sensor2 = {
        ...     "sensor_id": 7712,
        ...     "sensor_name": "Uncompensated Seafloor Pressure"
        ... }
        >>> sensor = [sensor1, sensor2]
        >>> client.section.sensor_sidebar(sensor)

        """
        if isinstance(sensor, list):
            # The sensor list contains two sensors
            sensor1, sensor2 = sensor
            self._client.ui.sensors_two_sidebar(sensor1, sensor2)
        else:
            # The sensor dict is a single sensor
            self._client.ui.sensor_sidebar(sensor)

    def map(
        self,
        location_code: str,
        center_lat: float | None = None,
        center_lon: float | None = None,
        zoom: int | None = None,
    ):
        """
        Display a map with a location code.

        It uses `/api/location` web service to query the lat and lon for the location.

        Parameters
        ----------
        location_code : str
            The location code for the location
        center_lat : float or None, optional
            The center latitude for the initial view state of the map widget.
            If not give, it will use the default one
        center_lon : float or None, optional
            The center longitude for the initial view state of the map widget.
            If not give, it will use the default one
        zoom : int or None, optional
            The zoom for the initial view state of the map widget.
            If not give, it will use the default one

        Examples
        --------
        >>> client = ONCDW()
        >>> client.section.map("BACAX")
        """
        onc = ONC(self._client.token)
        location_info = onc.getLocations({"locationCode": location_code})
        self._client.widget.map(
            location_info,
            center_lat=center_lat,
            center_lon=center_lon,
            zoom=zoom,
        )
