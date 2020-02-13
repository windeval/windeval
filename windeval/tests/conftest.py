import os
import pytest
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
