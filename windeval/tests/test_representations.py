"""Test data representations."""


import xarray as xr
import numpy as np

from windeval import convert_to_station, convert_to_sequence


def assert_all_vars_and_coords_equal(ds0, ds1):
    # all variables are present in both
    assert all(var in ds1.data_vars for var in ds0.data_vars)
    assert all(var in ds0.data_vars for var in ds1.data_vars)

    # all dims present in both
    assert all(dim in ds1.dims for dim in ds0.dims)
    assert all(dim in ds0.dims for dim in ds1.dims)

    # all coords present in both
    assert all(coord in ds1.coords for coord in ds0.coords)
    assert all(coord in ds0.coords for coord in ds1.coords)


def test_roundtrip_sequence_station():

    ds_station = xr.Dataset(
        coords={
            "time": xr.DataArray(
                np.datetime64("2001-01-01") + np.arange(100) * np.timedelta64(1, "D"),
                dims=("time",),
            ),
            "space": xr.DataArray(-23, dims=()),
        }
    )

    ds_sequence = convert_to_sequence(ds_station)

    assert_all_vars_and_coords_equal(ds_station, convert_to_station(ds_sequence))
