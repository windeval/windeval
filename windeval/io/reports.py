import xarray as xr
from typing import Any, Dict


def report(wndpr: Dict[str, xr.Dataset], *args: Any, **kwargs: Dict[str, Any]) -> None:
    raise NotImplementedError("Generation of reports is not yet implemented.")
