import os

import pytest
from dotenv import load_dotenv

from oncdw import ONCDW

load_dotenv(".streamlit/secrets.toml", override=True)
token = os.getenv("ONC_TOKEN")
env = os.getenv("ONC_ENV", "PROD")


def pytest_configure():
    print("========== Config ==========")
    print(f"Testing environment: {env}")


@pytest.fixture()
def client() -> ONCDW:
    return ONCDW(token, env, show_info=True)


@pytest.fixture()
def sensor1():
    return {"sensor_id": 4182, "sensor_name": "Seafloor Pressure"}


@pytest.fixture()
def sensor2():
    return {"sensor_id": 7712, "sensor_name": "Uncompensated Seafloor Pressure"}


@pytest.fixture()
def device():
    return {
        "device_code": "BPR-Folger-59",
    }
