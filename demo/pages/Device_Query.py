import os

import requests as re
import streamlit as st
from onc import ONC

onc = ONC(os.getenv("ONC_TOKEN"))


def combine(device_id, device_data, sensor_data, location_data):
    filter_device_keys = ["deviceName", "deviceCode", "deviceCategory"]
    res = {k: v for k, v in device_data["payload"].items() if k in filter_device_keys}
    res["deviceId"] = device_id
    filter_sensor_keys = ["sensorName", "sensorId"]
    sensors = [
        {k: v for k, v in sensor.items() if k in filter_sensor_keys}
        for sensor in sensor_data["payload"]
    ]
    filter_location_keys = ["locationName", "lat", "lon", "locationCode"]
    locations = [
        {k: v for k, v in location.items() if k in filter_location_keys}
        for location in location_data
    ]
    if sensors:
        res["sensors"] = sensors
    if locations:
        res["locations"] = locations
    return res


device_id = st.number_input("Enter a device ID:", key="device_id", value=None, step=1)

if st.button("Query Device Info"):
    if device_id:
        device_url = f"https://data.oceannetworks.ca/DeviceGeneralTabService?operation=1&deviceId={device_id}"
        sensor_url = (
            f"https://data.oceannetworks.ca/DeviceSensorService?deviceId={device_id}"
        )

        st.toast(f"Querying {device_url}")
        device_response = re.get(device_url)
        st.toast(f"Querying {sensor_url}")
        sensor_response = re.get(sensor_url)

        if device_response.status_code == 200 and sensor_response.status_code == 200:
            device_data = device_response.json()
            sensor_data = sensor_response.json()

            if "payload" not in device_data or "payload" not in sensor_data:
                st.error("No data found for the given device ID.")
                st.stop()

            st.toast("Querying /api/locations service")
            try:
                location_data = onc.getLocations(
                    {"deviceCode": device_data["payload"]["deviceCode"]}
                )
            except Exception:
                location_data = []
            res = combine(device_id, device_data, sensor_data, location_data)
            st.json(res)

        else:
            st.error(
                "Failed to retrieve data. Please check the device ID and try again."
            )
    else:
        st.warning("Please enter a device ID.")
