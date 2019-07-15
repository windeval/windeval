"""Windeval."""


import xarray as xr


def _has_degenerate_time_dependece(dobj):

    has_deg_time_dep = any(d == "time" for d in dobj.dims)
    has_deg_time_dep &= dobj.astype("float").var("time").max() == 0.0

    return has_deg_time_dep


def convert_to_station(ds):
    """Convert ds to station representation.

    Station data have no time dependent spatial coords.
    """
    for coord in filter(_has_degenerate_time_dependece, ds.coords.values()):
        ds.coords[coord.name] = coord.mean("time")

    ds = ds.squeeze()

    return ds


def convert_to_sequence(ds):
    """Broadcast all coords to time dependent arrays."""
    ds = ds.squeeze()
    for coord in filter(lambda c: c != "time", ds.coords):
        ds.coords[coord], _ = xr.broadcast(ds.coords[coord], ds["time"])
    return ds


def load_pirata_data_set(file_name, **kwargs):
    """Load data from file_name."""
    ds = xr.open_dataset(file_name, **kwargs)
    ds = ds.squeeze()
    return ds
