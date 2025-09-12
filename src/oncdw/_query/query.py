from typing import TYPE_CHECKING

import pandas as pd

from ._internal import Internal
from ._openapi import OpenAPI

if TYPE_CHECKING:
    from .._client import ONCDW


class Query:

    def __init__(self, client: "ONCDW"):
        self._internal = Internal(client)
        self._openapi = OpenAPI(client)

    def _get_service(self, source: str) -> Internal | OpenAPI:
        match source.lower():
            case "internal":
                return self._internal
            case "openapi":
                return self._openapi
            case _:
                raise ValueError(
                    f"Source {source} is not supported! Please choose from (internal, openapi)"
                )

    def get_scalar_data(
        self, source="internal", **kwargs
    ) -> tuple[pd.DataFrame, str, int]:
        return self._get_service(source).get_scalar_data(**kwargs)

    def get_archive_files(self, source="openapi", **kwargs) -> pd.DataFrame:
        return self._get_service(source).get_archive_files(**kwargs)

    def get_data_preview(self, source="internal", **kwargs) -> str:
        return self._get_service(source).get_data_preview(**kwargs)

    def get_scalar_data_two_sensors(self, source="openapi", **kwargs) -> pd.DataFrame:
        return self._get_service(source).get_scalar_data_two_sensors(**kwargs)
