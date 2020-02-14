import os
import pytest
import numpy as np
import xarray as xr


# station test data set
@pytest.fixture
def station():
    s = xr.open_dataset(
        os.path.join(
            os.path.dirname(__file__),
            "test_data/TAO_moored_buoy_data/high_resolution/cdf/hr/w10s10w_hr.cdf",
        )
    )
    s = s.rename({"lat": "latitude", "lon": "longitude", "WS_401": "wind_speed"})
    s.attrs["WindProductType"] = "Station"
    return s


@pytest.fixture
def X():
    i, j, k, t = 4, 5, 5, 6
    ds = xr.Dataset(
        {
            "eastward_wind": (
                ("time", "depth", "latitude", "longitude"),
                np.reshape(
                    np.append(np.array([3, 1]), np.ones(i * j * k * t - 2)),
                    (t, k, j, i),
                ),
            ),
            "northward_wind": (
                ("time", "depth", "latitude", "longitude"),
                np.reshape(
                    np.append(np.array([4, np.nan]), np.ones(i * j * k * t - 2)),
                    (t, k, j, i),
                ),
            ),
            "air_density": (
                ("time", "depth", "latitude", "longitude"),
                np.reshape(
                    np.append(np.array([1, 1]), np.ones(i * j * k * t - 2)),
                    (t, k, j, i),
                ),
            ),
        },
        coords={
            "longitude": xr.DataArray(np.array(range(i)), dims=("longitude",)),
            "latitude": xr.DataArray(np.array(range(j)), dims=("latitude",)),
            "depth": xr.DataArray(np.array(range(k)), dims=("depth",)),
            "time": xr.DataArray(np.array(range(t)), dims=("time",)),
        },
    )
    return ds
