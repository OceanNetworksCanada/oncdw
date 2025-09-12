import streamlit as st

from oncdw import ONCDW


def _delete_none(_dict):
    """Delete None values recursively from all of the dictionaries"""
    for key, value in list(_dict.items()):
        if isinstance(value, dict):
            _delete_none(value)
        elif value is None:
            del _dict[key]
        elif isinstance(value, list):
            for v_i in value:
                if isinstance(v_i, dict):
                    _delete_none(v_i)


def int_or_none(str_value):
    return int(str_value) if str_value else None


client = ONCDW()
# The format is (label, default_value, placeholder)
labels = {
    "Time series": [
        ("sensor_id :red[*]", "4182", None),
        ("date_from :red[*]", "-P4D", "e.g. -P4D, 2025-08-17T00:00:00.000Z"),
        ("date_to", None, "Optional, e.g. 2025-08-18T00:00:00.000Z"),
    ],
    "Time series two sensors": [
        ("sensor_id1 :red[*]", "4181", None),
        ("sensor_id2 :red[*]", "4182", None),
        ("date_from :red[*]", "-P4D", "e.g. -P4D, 2025-08-17T00:00:00.000Z"),
        ("date_to", None, "Optional, e.g. 2025-08-18T00:00:00.000Z"),
    ],
    "Table archive file": [
        ("device_code :red[*]", "ICLISTENHF6329", None),
        ("file_extensions", "fft, flac", "Optional"),
        (
            "date_from :red[*]",
            "-P1D",
            "e.g. -P1D, -PT23H, 2025-08-17T00:00:00.000Z",
        ),
        ("date_to", "-PT23H", "Optional, e.g. -P1D, -PT23H, 2025-08-17T01:00:00.000Z"),
    ],
    "Data Preview": [
        ("device_category_id :red[*]", 20, None),
        ("search_tree_node_id :red[*]", 172, None),
        ("sensor_code_id", "611", "optional"),
        ("data_product_format_id :red[*]", 149, None),
        ("plot_number", "", "Optional, default to 1"),
    ],
    "Heatmap archive file": [
        ("device_code :red[*]", "CODAR25VATK", None),
        ("file_extensions", "tar, zip", "Optional"),
        (
            "date_from :red[*]",
            "-P4D",
            "e.g. -P1D, -PT23H, 2025-08-17T00:00:00.000Z",
        ),
        ("date_to", "", "Optional, e.g. -P1D, -PT23H, 2025-08-17T01:00:00.000Z"),
    ],
    "Scatter plot": [
        ("location_code :red[*]", "BACAX", None),
        ("device_category_code :red[*]", "CTD", None),
        ("sensor_category_codes :red[*]", "salinity,temperature", None),
        ("date_from :red[*]", "-P1D", "e.g. -P1D, 2025-08-17T00:00:00.000Z"),
        ("date_to", None, "Optional"),
        ("resample_period", None, "Optional, default to 60"),
    ],
    "Map": [
        ("coordinates :red[*]", "48.314627, -126.058106; 50.54427, -126.84264", None),
        ("zoom", "6", None),
    ],
}

cols = st.columns(2)
with cols[0]:
    st.subheader("Choose a widget")
    option = st.radio("", labels.keys(), index=None)
    generate_button = st.button("Generate")


if option:
    with cols[1]:
        st.subheader("Parameters")
        for label, default_value, placeholder in labels[option]:
            if label in ["sensor_ids", "sensor_names"]:
                st.text_area(
                    label,
                    key=label.replace(" :red[*]", ""),
                    value=default_value,
                    placeholder=placeholder,
                )
            else:
                st.text_input(
                    label,
                    key=label.replace(" :red[*]", ""),
                    value=default_value,
                    placeholder=placeholder,
                )

    if generate_button:
        st.divider()
        st.subheader("Widget")
        if option == "Time series":
            sensor_id = st.session_state.sensor_id
            date_from = st.session_state.date_from
            date_to = st.session_state.date_to

            container = st.container()

            sensor = {
                "sensor_id": int(sensor_id),
            }

            with st.echo():
                client.widget.time_series(
                    sensor,
                    date_from=date_from,
                    date_to=date_to,
                )

            with container.expander("sensor", expanded=True):
                st.json(sensor)

        elif option == "Time series two sensors":
            sensor_id1 = st.session_state.sensor_id1
            sensor_id2 = st.session_state.sensor_id2
            date_from = st.session_state.date_from
            date_to = st.session_state.date_to

            container = st.container()

            sensor1 = {
                "sensor_id": int(sensor_id1),
            }

            sensor2 = {
                "sensor_id": int(sensor_id2),
            }

            with st.echo():
                client.widget.time_series_two_sensors(
                    sensor1,
                    sensor2,
                    date_from=date_from,
                    date_to=date_to,
                )

            with container.expander("sensors", expanded=True):
                st.code("sensor1")
                st.json(sensor1)
                st.code("sensor2")
                st.json(sensor2)

        elif option == "Table archive file":
            device_code = st.session_state.device_code
            file_extensions_text = st.session_state.file_extensions
            file_extensions = (
                [x.strip() for x in file_extensions_text.split(",")]
                if file_extensions_text
                else None
            )

            date_from = st.session_state.date_from
            date_to = st.session_state.date_to

            container = st.container()

            device = {
                "device_code": device_code,
                "file_extensions": file_extensions,
            }

            _delete_none(device)

            with st.echo():
                client.widget.table_archive_files(
                    device,
                    date_from=date_from,
                    date_to=date_to,
                )

            with container.expander("device", expanded=True):
                st.json(device)

        elif option == "Data Preview":
            deviceCategoryId = st.session_state.device_category_id
            searchTreeNodeId = st.session_state.search_tree_node_id
            sensor_code_id = st.session_state.sensor_code_id
            data_product_format_id = st.session_state.data_product_format_id
            plot_number = st.session_state.plot_number

            container = st.container()

            device = {
                "device_category_id": int(deviceCategoryId),
                "search_tree_node_id": int(searchTreeNodeId),
                "data_preview_options": [
                    {
                        "data_product_format_id": int(data_product_format_id),
                        "plot_number": int_or_none(plot_number),
                        "sensor_code_id": int_or_none(sensor_code_id),
                    }
                ],
            }

            _delete_none(device)

            with st.echo():
                option = device["data_preview_options"]

                client.widget.data_preview(device, option[0])

            with container.expander("device", expanded=True):
                st.json(device)

        elif option == "Heatmap archive file":
            device_code = st.session_state.device_code
            file_extensions_text = st.session_state.file_extensions
            file_extensions = (
                [x.strip() for x in file_extensions_text.split(",")]
                if file_extensions_text
                else None
            )

            date_from = st.session_state.date_from
            date_to = st.session_state.date_to

            container = st.container()

            device = {
                "device_code": device_code,
                "file_extensions": file_extensions,
            }

            _delete_none(device)

            with st.echo():
                client.widget.heatmap_archive_files(
                    device,
                    date_from=date_from,
                    date_to=date_to,
                )

            with container.expander("device", expanded=True):
                st.json(device)

        elif option == "Scatter plot":
            location_code = st.session_state.location_code
            device_category_Code = st.session_state.device_category_code
            sensor_category_codes = st.session_state.sensor_category_codes
            resample_period = st.session_state.resample_period

            container = st.container()

            device = {
                "location_code": location_code,
                "device_category_code": device_category_Code,
                "sensor_category_codes": sensor_category_codes,
            }

            if resample_period:
                with st.echo():
                    sensor_category_codes = device["sensor_category_codes"]
                    client.widget.scatter_plot_two_sensors(
                        device,
                        sensor_category_codes,
                        resample_period=resample_period,
                    )
            else:
                with st.echo():
                    sensor_category_codes = device["sensor_category_codes"]
                    client.widget.scatter_plot_two_sensors(
                        device,
                        sensor_category_codes,
                    )

            with container.expander("device", expanded=True):
                st.json(device)

        elif option == "Map":
            coordinates = st.session_state.coordinates
            zoom = int_or_none(st.session_state.zoom)

            devices = []
            for coordinate in coordinates.split(";"):
                lat, lon = coordinate.split(",")
                device = {"lat": float(lat), "lon": float(lon)}
                devices.append(device)

            container = st.container()

            if zoom:
                with st.echo():
                    client.widget.map(devices, zoom=zoom)
            else:
                with st.echo():
                    client.widget.map(devices)

            with container.expander("devices", expanded=True):
                st.json(devices)
