import xarray as xr
from typing import Any, Dict


def open_product(path1, path2, **kwargs: Dict[str, Any]) -> Dict[str, xr.Dataset]:
    raise NotImplementedError("Import of data through Intake is not yet implemented.")


def info(wndpr: Dict[str, xr.Dataset], *args: Any, **kwargs: Dict[str, Any]) -> None:
    raise NotImplementedError("Info of wind products is not yet implemented.")


def select(
    wndpr: Dict[str, xr.Dataset], *args: Any, **kwargs: Dict[str, Any]
) -> Dict[str, xr.Dataset]:
    raise NotImplementedError(
        "Selecting and slicing of dataset is not yet implemented."
    )
