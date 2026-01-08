import streamlit as st

from oncdw import ONCDW

st.set_page_config(layout="wide")
client = ONCDW()

st.title("Widgets Demo")

headers = [
    "Data Preview png data product",
    "Data Preview gif data product",
    "Table for latest archive files (with hyperlink to download data)",
    "Heatmap for latest archive files (with hyperlink to download data)",
    "Time series scalar data plot from one sensor",
    "Time series scalar data plot with two sensors of the same type",
    "Time series scalar data plot with two sensors of different types",
    "Scalar data plot with two sensors of different type on separate axis",
    "Map widget",
    "Time series multiple",
]

with st.sidebar:
    for header in headers:
        st.markdown(f"- [{header}](#{header.lower().replace(' ', '-').replace('(', '').replace(')', '')})")

############################################
st.header("Data Preview png data product")
with st.echo():
    device = {"device_category_id": 20, "search_tree_node_id": 172}
    data_preview_option = {"data_product_format_id": 149, "sensor_code_id": 611}

    client.widget.data_preview(device, data_preview_option)
st.divider()

############################################
st.header("Data Preview gif data product")
with st.echo():
    device = {"device_category_id": 65, "search_tree_node_id": 429}
    data_preview_options = {"data_product_format_id": 178}

    client.widget.data_preview(device, data_preview_options)
st.divider()


############################################
st.header("Table for latest archive files (with hyperlink to download data)")
with st.echo():
    client.widget.table_archive_files({"device_code": "BPR_BC"}, date_from="-P7D")
    client.widget.table_archive_files(
        {"device_code": "CODAR25VATK", "file_extensions": ["png", "ruv"]},
        date_from="-P1D",
        date_to="-PT22H",
    )
st.divider()


############################################
st.header("Heatmap for latest archive files (with hyperlink to download data)")
with st.echo():
    device = {
        "device_code": "CODAR25VATK",
        "file_extensions": ["tar", "zip"],
    }
    client.widget.heatmap_archive_files(device, date_from="-P3D")
st.divider()


############################################
st.header("Time series scalar data plot from one sensor")
with st.echo():
    client.widget.time_series(
        {"sensor_id": 4182},
        date_from="2010-02-18T00:00:00.000Z",
        date_to="2010-02-21T00:00:00.000Z",
    )
st.divider()


############################################
st.header("Time series scalar data plot with two sensors of the same type")
with st.echo():
    client.widget.time_series_two_sensors(4182, 7712, date_from="-P2D")
    client.widget.time_series_two_sensors(4182, 7712, date_from="-P2D", shade=False)
st.divider()


############################################
st.header("Time series scalar data plot with two sensors of different types")

with st.echo():
    sensor1 = {"sensor_id": 4176}
    sensor2 = {"sensor_id": 3016}
    client.widget.time_series_two_sensors(sensor1, sensor2, date_from="-P2D")
    client.widget.time_series_two_sensors(sensor1, sensor2, date_from="-P2D", shade=False)
st.divider()


############################################
st.header("Scalar data plot with two sensors of different type on separate axis")
with st.echo():
    device = {"location_code": "BACAX", "device_category_code": "CTD"}
    sensor_category_codes = "salinity,temperature"
    client.widget.scatter_plot_two_sensors(
        device, sensor_category_codes, date_from="-P1D"
    )
st.divider()


############################################
st.header("Map widget")
with st.echo():
    devices = [
        {
            "lat": 48.314627,
            "lon": -126.058106,
            "location_name": "Location X",
            "location_code": "LocationX",
            "device_name": "Device X",
            "device_code": "DeviceX",
        },
        {
            "lat": 50.54427,
            "lon": -126.84264,
            "location_name": "Location Y",
            "location_code": "LocationY",
            "device_name": "Device Y",
            "device_code": "DeviceY",
        },
    ]
    # Hover over the point to show the tooltip
    client.widget.map(devices, zoom=6)

st.divider()
st.title("Experimental Widget Demo")

############################################
st.header("Time series multiple")
with st.echo():
    sensors = [{"sensor_id": 16688}, {"sensor_id": 16689}, {"sensor_id": 13331}, {"sensor_id": 13329}]
    client.widget.time_series_multiple(sensors, date_from="-P1D")