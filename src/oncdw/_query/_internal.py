from dataclasses import dataclass
from typing import TYPE_CHECKING

import pandas as pd
import requests

if TYPE_CHECKING:
    from .._client import ONCDW


@dataclass
class Internal:
    _client: "ONCDW"

    def get_scalar_data(
        self, sensor_id: int | str, date_from: str, date_to: str
    ) -> tuple[pd.DataFrame, str, int]:
        """
        Return scalar data in a pd.DataFrame by calling internal `ScalarDataAPIService`,
        together with label (combination of sensor id, name and uofm) and sensor type id.

        The dataframe would have no empty cells, and have following columns:
        - datetime
        - min
        - max
        - avg
        - qaqcflag
        """
        base_url = f"https://{self._client.hostname}/ScalarDataAPIService"
        params = {
            "datefrom": date_from,
            "dateto": date_to,
            "sensorid": sensor_id,
            "option": 3,
            "isClean": "true",
            "plotpoints": 1500,
        }

        r = requests.get(base_url, params)
        if self._client.show_info:
            print(f"Requesting scalar data from {r.url}")

        payload = r.json()["payload"]

        if not payload:
            # This usually means the sensor id is invalid, or there are malformed parameters
            raise ValueError(f"No data returned for sensor {sensor_id}.")

        ylabel = f"{sensor_id} - {payload['name']} ({payload['uofm']})"
        sensor_type_id = payload["sensortypeid"]

        df = pd.DataFrame(
            payload["data"], columns=["datetime", "min", "max", "avg", "qaqcflag"]
        )
        df.mask(df == "", inplace=True)
        df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")

        return df, ylabel, sensor_type_id

    def get_data_preview(
        self,
        sensor_code_id: int | None,
        device_category_id: int,
        search_tree_node_id: int,
        data_product_format_id: int,
        plot_number: int,
    ) -> str:
        base_url = f"https://{self._client.hostname}/DataPreviewService"
        params = {
            "searchTreeNodeId": search_tree_node_id,
            "deviceCategoryId": device_category_id,
            "sensorCodeId": sensor_code_id,
            "timeConfigId": 2,  # Week
            "dataProductFormatId": data_product_format_id,
            "plotNumber": plot_number,
            "operation": 5,  # GET_DATA_PREVIEW_PLOT
        }

        r = requests.get(base_url, params)
        if self._client.show_info:
            print(f"Requesting data preview from {r.url}")

        response_json = r.json()

        if response_json:
            return response_json["payload"].get("filePath", "")
        else:
            return ""
