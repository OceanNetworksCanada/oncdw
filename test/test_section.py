import logging

import pytest
from util import _assert_no_logs

# Links tests


def test_links(client, caplog):
    links = {
        "Oceans 3.0": "https://data.oceannetworks.ca",
        "Marine Traffic": "https://www.marinetraffic.com",
    }
    client.section.links(links, "Useful Links")
    _assert_no_logs(caplog, logging.WARNING)


# State of ocean image tests


def test_state_of_ocean_images(client, caplog):
    client.section.state_of_ocean_images("BACAX")
    _assert_no_logs(caplog, logging.WARNING)


# Time series tests


def test_time_series(client, caplog, sensor1):
    client.section.time_series(sensor1)
    _assert_no_logs(caplog, logging.ERROR)


def test_time_series_iso_date_format(client, caplog, sensor1):
    client.section.time_series(
        sensor1,
        date_from="2010-02-18T00:00:00.000Z",
        date_to="2010-02-21T00:00:00.000Z",
    )
    _assert_no_logs(caplog, logging.WARNING)


def test_time_series_two_sensors(client, caplog, sensor1, sensor2):
    sensor = [sensor1, sensor2]
    client.section.time_series(sensor)
    _assert_no_logs(caplog, logging.ERROR)


def test_time_series_two_sensors_iso_date_format(client, caplog, sensor1, sensor2):
    sensor = [sensor1, sensor2]
    client.section.time_series(
        sensor, "2010-02-18T00:00:00.000Z", "2010-02-21T00:00:00.000Z"
    )
    _assert_no_logs(caplog, logging.WARNING)


# Data preview tests


@pytest.fixture
def device_dp():
    return {
        "search_tree_node_id": 450,
        "device_category_id": 72,
        "data_preview_options": [
            {"data_product_format_id": 3, "plot_number": 1},
            {"data_product_format_id": 3, "plot_number": 2},
        ],
    }


def test_data_preview(client, caplog, device_dp):
    client.section.data_preview(device_dp)
    _assert_no_logs(caplog, logging.WARNING)


def test_data_preview_odd_number_of_options(client, caplog, device_dp):
    device_dp["data_preview_options"].append(
        {"data_product_format_id": 10, "plot_number": 1}
    )
    client.section.data_preview(device_dp)
    _assert_no_logs(caplog, logging.WARNING)


def test_data_preview_no_options(client, caplog, device_dp):
    device_dp["data_preview_options"] = []
    client.section.data_preview(device_dp)
    _assert_no_logs(caplog, logging.WARNING)


# Location expander tests


def test_location_expander(client, caplog):
    device = {
        "location_code": "BACAX",
        "location_name": "Barkley Canyon Axis",
    }
    client.section.location_expander(device)
    _assert_no_logs(caplog, logging.WARNING)


# Sidebar tests


def test_location_sidebar(client, caplog):
    device = {
        "location_code": "BACAX",
    }
    client.section.location_sidebar(device)
    _assert_no_logs(caplog, logging.WARNING)


def test_sensor_sidebar(client, caplog, sensor1):
    client.section.sensor_sidebar(sensor1)
    _assert_no_logs(caplog, logging.WARNING)


def test_sensor_sidebar_two_sensors(client, caplog, sensor1, sensor2):
    sensor = [sensor1, sensor2]
    client.section.sensor_sidebar(sensor)
    _assert_no_logs(caplog, logging.WARNING)


# Map tests


def test_map(client, caplog):
    client.section.map("BACAX")
    _assert_no_logs(caplog, logging.WARNING)
