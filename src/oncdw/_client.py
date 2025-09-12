import os
import warnings
from dataclasses import dataclass

from ._util import now
from .section import Section
from .ui import UI
from .widget import Widget


@dataclass
class ONCDW:
    """
    A wrapper class for Oceans 3.0 data widgets.

    All the client library's functionality is provided as methods of this class's members,
    namely widget, ui, and section.

    Parameters
    ----------
    token : str
        The ONC API token, which could be retrieved at https://data.oceannetworks.ca/Profile once logged in.
        It can be set as a parameter or by using an environment variable called `ONC_TOKEN`.
    env : str, default "PROD"
        Whether the ONC Production server URL is used for service requests. Can be "PROD" or "QA".
    show_info : boolean, default False
        Whether verbose script messages are displayed, such as request url.

    Examples
    --------
    >>> from oncdw import ONCDW
    >>> client = ONCDW()  # Works if the token is set by an env variable ONC_TOKEN
    >>> client2 = ONCDW("YOUR_TOKEN_HERE")
    >>> client3 = ONCDW("YOUR_TOKEN_HERE", show_info=True, env="QA")
    """

    token: str | None = None
    env: str = "PROD"  # "PROD" | "QA"
    show_info: bool = False

    def __post_init__(self):
        if self.token is None:
            self.token = os.environ.get("ONC_TOKEN")
            if self.token is None:
                raise ValueError(
                    "Please set token by passing token to the ONCDW class or by setting the ONC_TOKEN environment variable"
                )

        self.widget = Widget(self)
        self.now = now()
        self.section = Section(self)
        self.ui = UI

    @property
    def hostname(self) -> str:
        if self.env.upper() == "QA":
            return "qa.oceannetworks.ca"
        elif self.env.upper() != "PROD":
            warnings.warn(
                f"Env {self.env} is not in (PROD, QA), default to PROD.", stacklevel=2
            )
        return "data.oceannetworks.ca"
