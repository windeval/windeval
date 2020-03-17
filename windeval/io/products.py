import xarray as xr
from pathlib import Path
from typing import Any, Dict


def open_product(
    path0: str,
    path1: str,
    *args: Any,
    experimental: bool = False,
    **kwargs: Dict[str, Any]
) -> Dict[str, xr.Dataset]:
    if not args:
        names = [Path(path0).stem, Path(path1).stem]
    else:
        names = [*args]
    if experimental:
        ds = {names[0]: xr.open_dataset(path0), names[1]: xr.open_dataset(path1)}
    else:
        raise NotImplementedError(
            "Import of data through Intake is not yet implemented."
        )

    return ds


def save_product(
    ds: Dict[str, xr.Dataset],
    path: str,
    experimental: bool = False,
    **kwargs: Dict[str, Any]
) -> None:
    if experimental:
        for k, v in ds.items():
            v.to_netcdf(Path(path).joinpath(k + ".cdf"))
    else:
        raise NotImplementedError("Export of data is not yet implemented.")

    return None


def info(wndpr: Dict[str, xr.Dataset], *args: Any, **kwargs: Dict[str, Any]) -> None:
    raise NotImplementedError("Info of wind products is not yet implemented.")


def select(
    wndpr: Dict[str, xr.Dataset], *args: Any, **kwargs: Dict[str, Any]
) -> Dict[str, xr.Dataset]:
    raise NotImplementedError(
        "Selecting and slicing of dataset is not yet implemented."
    )
