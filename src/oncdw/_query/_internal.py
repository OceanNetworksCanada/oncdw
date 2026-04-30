from dataclasses import dataclass
from typing import TYPE_CHECKING

import pandas as pd
import requests

if TYPE_CHECKING:
    from .._client import ONCDW


def _estimate_plotpoints(
    date_from: str,
    date_to: str,
    requested_points: int = 800,
) -> int:
    """Estimate a safe ``plotpoints`` value from the requested time span.

    ScalarDataAPIService enables subsampling only when
    ``expectedSampleCount > 3 * plotpoints``. Because the fallback metadata
    path estimates one sample per minute, this helper derives an upper bound
    from duration-in-minutes so the gate is more likely to fire consistently.

    Parameters
    ----------
    date_from : str
        Start datetime in ONC format (ISO 8601, typically with ``Z``).
    date_to : str
        End datetime in ONC format (ISO 8601, typically with ``Z``).
    requested_points : int, default 800
        Maximum preferred number of points for rendering.

    Returns
    -------
    int
        A bounded ``plotpoints`` value in ``[1, requested_points]``. The
        upper bound follows ``floor(duration_minutes / 3) - 1`` to keep
        ``plotpoints < expectedSampleCount / 3`` under the 1-sample/minute
        fallback estimate used by ScalarDataAPIService.
    """
    start = pd.to_datetime(date_from, utc=True)
    end = pd.to_datetime(date_to, utc=True)

    duration_minutes = max((end - start).total_seconds() / 60, 0)
    conservative_upper_bound = int(duration_minutes // 3) - 1

    if conservative_upper_bound < 1:
        return 1

    return min(requested_points, conservative_upper_bound)


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
        plotpoints = _estimate_plotpoints(date_from, date_to)
        params = {
            "datefrom": date_from,
            "dateto": date_to,
            "sensorid": sensor_id,
            "option": 3,
            "isClean": "true",
            "plotpoints": plotpoints,
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
