import xarray as xr
from typing import Optional
from . import processing


def ekman(
    X: xr.Dataset,
    component: str = "eastward",
    drag_coefficient: Optional[str] = None,
    bulk_formula: Optional[str] = None,
    extend_ranges: Optional[bool] = None,
) -> xr.Dataset:
    """Wrapper for Ekman transport calculations.

    Parameters
    ----------
    X : array_like
        Wind product data set.
    component : str
        Component of Ekman transport to be calculated, defaults to 'eastward'.
    drag_coefficient : str, optional
        Name of drag coefficient method, defaults to wrapped function default.
    bulk_formula : str, optional
        Name of bulk formula, defaults to wrapped function default.
    extend_ranges : bool, optional
        Fills undefined areas of the bulk formulas if `True`, returns `numpy.nan` values
        otherwise, defaults to defaults to wrapped function default.

    Returns
    -------
    array_like
        Wind product data set with added Ekman transport and required fields.

    """
    d = {}
    for x in ["drag_coefficient", "bulk_formula", "extend_ranges"]:
        if locals()[x] is None:
            continue
        d[x] = locals()[x]
    c = "northward" if component == "eastward" else "eastward"
    getattr(processing, "surface_downward_" + c + "_stress")(X, **d)
    getattr(processing, component + "_ekman_transport")(X)

    return X


def sverdrup(
    X: xr.Dataset,
    drag_coefficient: Optional[str] = None,
    bulk_formula: Optional[str] = None,
    extend_ranges: Optional[bool] = None,
) -> xr.Dataset:
    """Wrapper for Sverdrup transport calculations.

    Parameters
    ----------
    X : array_like
        Wind product data set.
    drag_coefficient : str, optional
        Name of drag coefficient method, defaults to wrapped function default.
    bulk_formula : str, optional
        Name of bulk formula, defaults to wrapped function default.
    extend_ranges : bool, optional
        Fills undefined areas of the bulk formulas if `True`, returns `numpy.nan` values
        otherwise, defaults to defaults to wrapped function default.

    Returns
    -------
    array_like
        Wind product data set with added Sverdrup transport and required fields.

    """
    d = {}
    for x in ["drag_coefficient", "bulk_formula", "extend_ranges"]:
        if locals()[x] is None:
            continue
        d[x] = locals()[x]
    processing.surface_downward_eastward_stress(X, **d)
    processing.surface_downward_northward_stress(X, **d)
    processing.sverdrup_transport(X)

    return X
