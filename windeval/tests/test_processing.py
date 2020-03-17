import math
import pytest
import inspect
import numpy as np
import xarray as xr
from windeval import processing


@pytest.fixture
def accuracy():
    return 1e-12


def test_BulkFormula():
    BFC = processing.BulkFormula
    assert inspect.isclass(BFC)
    BFI = processing.BulkFormula()
    assert isinstance(BFI, BFC)


def test_BulkFormula_YT96(accuracy):
    x = np.array([3, 5.9, 6, 12, 26, 27, 1])
    X = xr.Dataset({"w": (("x"), x), "air_density": (("x"), np.full(x.shape, 1))})
    y = np.array(
        [
            0.00217888888888889,
            0.001036624533180121,
            0.00102,
            0.00144,
            0.00242,
            np.nan,
            np.nan,
        ]
    )
    tau = processing.BulkFormula("yelland_and_taylor_1996").calculate(X, "w")
    for i, _ in enumerate(X.w):
        if np.isnan(y[i]):
            assert np.isnan(tau[i])
        else:
            assert math.isclose(tau[i] / np.power(X.w[i], 2), y[i], rel_tol=accuracy)
    assert tau.shape == X.w.shape


def test_BulkFormula_LP81(accuracy):
    x = np.array([5, 12, 1, 26])
    X = xr.Dataset({"w": (("x"), x), "air_density": (("x"), np.full(x.shape, 1))})
    y = np.array([1.2e-3, 0.00127, np.nan, np.nan])
    tau = processing.BulkFormula("large_and_pond_1981").calculate(X, "w")
    for i, _ in enumerate(X.w):
        if np.isnan(y[i]):
            assert np.isnan(tau[i])
        else:
            assert math.isclose(tau[i] / np.power(X.w[i], 2), y[i], rel_tol=accuracy)
    assert tau.shape == X.w.shape


def test_BulkFormula_KH07(accuracy):
    x = np.array([1, 10])
    X = xr.Dataset({"w": (("x"), x), "air_density": (("x"), np.full(x.shape, 1))})
    y = 1.3e-3
    tau = processing.BulkFormula("ncep_ncar_2007").calculate(X, "w")
    for i, _ in enumerate(X.w):
        assert math.isclose(tau[i] / np.power(X.w[i], 2), y, rel_tol=accuracy)
    assert tau.shape == X.w.shape


def test_BulkFormula_T90(accuracy):
    x = np.array([0.5, 1.5, 3 + 1e-10, 15])
    X = xr.Dataset({"w": (("x"), x), "air_density": (("x"), np.full(x.shape, 1))})
    y = np.array([0.00218, 0.00166, 0.00114, 0.001465])
    tau = processing.BulkFormula("trenberth_etal_1990").calculate(X, "w")
    for i, _ in enumerate(X.w):
        assert math.isclose(tau[i] / np.power(X.w[i], 2), y[i], rel_tol=accuracy)
    assert tau.shape == X.w.shape


def test_BulkFormula_LY04(accuracy):
    x = np.array([1, 2, 0])
    X = xr.Dataset({"w": (("x"), x), "air_density": (("x"), np.full(x.shape, 1))})
    y = np.array([0.002918, 0.001644, np.nan])
    tau = processing.BulkFormula("large_and_yeager_2004").calculate(X, "w")
    for i, _ in enumerate(X.w):
        if np.isnan(y[i]):
            assert np.isnan(tau[i])
        else:
            assert math.isclose(tau[i] / np.power(X.w[i], 2), y[i], rel_tol=accuracy)
    assert tau.shape == X.w.shape


def test_BulkFormula_K00(accuracy):
    x = np.array([1, 10])
    X = xr.Dataset(
        {
            "w": (("x"), x),
            "sea_surface_temperature": (("x"), x),
            "air_temperature": (("x"), x),
            "air_density": (("x"), np.full(x.shape, 1)),
        }
    )
    y = np.array([0.0010764375, 0.001653, np.nan])
    tau = processing.BulkFormula("kara_etal_2000").calculate(X, "w")
    for i, _ in enumerate(X.w):
        assert math.isclose(tau[i] / np.power(X.w[i], 2), y[i], rel_tol=accuracy)
    assert tau.shape == X.w.shape


def test_wind_speed(X):
    processing.wind_speed(X)
    assert X.data_vars["wind_speed"].values[0, 0, 0, 0] == 5.0
    assert np.isnan(X.data_vars["wind_speed"].values[0, 0, 0, 1])


def test_surface_downward_eastward_stress(X):
    processing.surface_downward_eastward_stress(
        X, drag_coefficient="ncep_ncar_2007", bulk_formula="generic"
    )
    y = 1.3e-3 * X.eastward_wind ** 2
    assert (
        X.data_vars["surface_downward_eastward_stress"].values[0, 0, 0, 0]
        == y[0, 0, 0, 0]
    )
    assert (
        X.data_vars["surface_downward_eastward_stress"].values[0, 0, 0, 1]
        == y[0, 0, 0, 1]
    )


def test_surface_downward_northward_stress(X):
    processing.surface_downward_northward_stress(
        X, drag_coefficient="ncep_ncar_2007", bulk_formula="generic"
    )
    y = 1.3e-3 * X.northward_wind ** 2
    assert (
        X.data_vars["surface_downward_northward_stress"].values[0, 0, 0, 0]
        == y[0, 0, 0, 0]
    )
    assert np.isnan(X.data_vars["surface_downward_northward_stress"].values[0, 0, 0, 1])


def test_northward_ekman_transport(X):
    processing.surface_downward_eastward_stress(
        X, drag_coefficient="ncep_ncar_2007", bulk_formula="generic"
    )
    processing.northward_ekman_transport(X)
    y = (
        -1.3e-3
        * X.eastward_wind.values[0, 0, 0, :2] ** 2
        / processing._Coriolis().parameter(X.latitude.values[0])
    )
    assert X.data_vars["northward_ekman_transport"].values[0, 0, 0, 0] == y[0]
    assert X.data_vars["northward_ekman_transport"].values[0, 0, 0, 1] == y[1]


def test_eastward_ekman_transport(X):
    processing.surface_downward_northward_stress(
        X, drag_coefficient="ncep_ncar_2007", bulk_formula="generic"
    )
    processing.eastward_ekman_transport(X)
    y = (
        1.3e-3
        * X.northward_wind.values[0, 0, 0, 0] ** 2
        / processing._Coriolis().parameter(X.latitude.values[0])
    )
    assert X.data_vars["eastward_ekman_transport"].values[0, 0, 0, 0] == y
    assert np.isnan(X.data_vars["eastward_ekman_transport"].values[0, 0, 0, 1])


def test_eastward_ekman_transport_v2(X):
    processing.eastward_ekman_transport(X)
    y = (
        1.3e-3
        * X.northward_wind.values[0, 0, 0, 0] ** 2
        / processing._Coriolis().parameter(X.latitude.values[0])
    )
    assert X.data_vars["eastward_ekman_transport"].values[0, 0, 0, 0] == y
    assert np.isnan(X.data_vars["eastward_ekman_transport"].values[0, 0, 0, 1])


def test_sverdrup_transport(X):
    processing.sverdrup_transport(X)
    assert math.isclose(
        X.sverdrup_transport[0, 0, 0, 0].values, -62.40566775, rel_tol=1e-7
    )
    assert np.isnan(X.data_vars["sverdrup_transport"].values[0, 0, 0, 1])


def test_conversions(X):
    with pytest.raises(NotImplementedError):
        processing.conversions({"ds": X})


def test_diagnostics(X):
    ds = processing.diagnostics({"ds": X}, "eastward_wind", "welch")
    assert isinstance(ds["ds"]["power_spectral_density"], xr.DataArray)
