import streamlit as st

from oncdw import ONCDW

st.set_page_config(layout="wide")
client = ONCDW()

st.title("Sections Demo")

############################################
st.header("1. Links")
with st.echo():
    links = {
        "Oceans 3.0": "https://data.oceannetworks.ca",
        "Marine Traffic": "https://www.marinetraffic.com",
    }
    client.section.links(links, "Useful Links")
st.divider()

############################################
st.header("2. State of the ocean images")
with st.echo():
    client.section.state_of_ocean_images("BACAX")
st.divider()


############################################
st.header("3. Time series section with one sensor")
with st.echo():
    sensor1 = {"sensor_id": 4182, "sensor_name": "Seafloor Pressure"}
    client.section.time_series(sensor1, date_from="-P4D")
st.divider()


############################################
st.header("4. Time series section for two sensors with the same sensor type")
with st.echo():
    sensor1 = {"sensor_id": 4182, "sensor_name": "Seafloor Pressure"}
    sensor2 = {"sensor_id": 7712, "sensor_name": "Uncompensated Seafloor Pressure"}
    sensor = [sensor1, sensor2]
    client.section.time_series(
        sensor,
        date_from="2010-02-18T00:00:00.000Z",
        date_to="2010-02-21T00:00:00.000Z",
    )
st.divider()


############################################
st.header("5. Time series section for two sensors with different sensor types")
with st.echo():
    sensor1 = {"sensor_id": 4176, "sensor_name": "Seafloor Pressure"}
    sensor2 = {"sensor_id": 3016, "sensor_name": "DART Pressure Residual"}
    sensor = [sensor1, sensor2]
    client.section.time_series(
        sensor,
        date_from="-P4D",
    )
st.divider()

############################################
st.header("6. Data preview plots")
with st.echo():
    device = {
        "search_tree_node_id": 450,
        "device_category_id": 72,
        "data_preview_options": [
            {"data_product_format_id": 3, "plot_number": 1},
            {"data_product_format_id": 3, "plot_number": 2},
            {"data_product_format_id": 10, "plot_number": 1},
        ],
    }
    client.section.data_preview(device)
st.divider()


############################################
st.header("7. Location expander")

with st.echo():
    device = {
        "location_code": "BACAX",
        "location_name": "Barkley Canyon Axis",
    }
    client.section.location_expander(device)
st.divider()

############################################
st.header("8. Location sidebar")
with st.echo():
    with st.sidebar:
        device = {"location_code": "BACAX"}
        client.section.location_sidebar(device)
        st.divider()
st.divider()

############################################
st.header("9. Sensor sidebar")
with st.echo():
    with st.sidebar:
        sensor1 = {"sensor_id": 4182, "sensor_name": "Seafloor Pressure"}
        client.section.sensor_sidebar(sensor1)
        st.divider()
st.divider()

############################################
st.header("10. Sensor sidebar with two sensor")
with st.echo():
    with st.sidebar:
        sensor1 = {"sensor_id": 4182, "sensor_name": "Seafloor Pressure"}
        sensor2 = {"sensor_id": 7712, "sensor_name": "Uncompensated Seafloor Pressure"}
        sensor = [sensor1, sensor2]
        client.section.sensor_sidebar(sensor)
        st.divider()
st.divider()

############################################
st.header("11. Map section")
with st.echo():
    client.section.map("BACAX")
st.divider()
