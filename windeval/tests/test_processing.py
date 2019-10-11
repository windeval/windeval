import math
import pytest
import inspect
import numpy as np
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
    U = np.array([3, 5.9, 6, 12, 26, 27, 1])
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
    x = processing.BulkFormula("yelland_and_taylor_1996").calculate(U=U, rho=1, u=1)
    for i, _ in enumerate(U):
        if np.isnan(y[i]):
            assert np.isnan(x[i])
        else:
            assert math.isclose(x[i], y[i] * U[i], rel_tol=accuracy)
    assert x.shape == U.shape


def test_BulkFormula_LP81(accuracy):
    U = np.array([5, 12, 1, 26])
    y = np.array([1.2e-3, 0.00127, np.nan, np.nan])
    x = processing.BulkFormula("large_and_pond_1981").calculate(U=U, rho=1, u=1)
    for i, _ in enumerate(U):
        if np.isnan(y[i]):
            assert np.isnan(x[i])
        else:
            assert math.isclose(x[i], y[i] * U[i], rel_tol=accuracy)
    assert x.shape == U.shape


def test_BulkFormula_KH07(accuracy):
    U = np.array([1, 1])
    y = 1.3e-3
    x = processing.BulkFormula("ncep_ncar_2007").calculate(U=U, rho=1, u=1)
    for i, _ in enumerate(x):
        assert x[i] == y
    assert x.shape == U.shape


def test_BulkFormula_empty(accuracy):
    U = np.array([1, 1])
    y = 1.3e-3
    x = processing.BulkFormula().calculate(U=U, rho=1, u=1)
    for i, _ in enumerate(x):
        assert x[i] == y
    assert x.shape == U.shape


def test_BulkFormula_T90(accuracy):
    U = np.array([0.5, 1.5, 3 + 1e-10, 15])
    y = np.array([0.00218, 0.00166, 0.00114, 0.001465])
    x = processing.BulkFormula("trenberth_etal_1990").calculate(U=U, rho=1, u=1)
    for i, _ in enumerate(U):
        assert math.isclose(x[i], y[i] * U[i], rel_tol=accuracy)
    assert x.shape == U.shape


def test_BulkFormula_LY04(accuracy):
    U = np.array([1, 2, 0])
    y = np.array([0.002918, 0.001644, np.nan])
    x = processing.BulkFormula("large_and_yeager_2004").calculate(U=U, rho=1, u=1)
    for i, _ in enumerate(U):
        if np.isnan(y[i]):
            assert np.isnan(x[i])
        else:
            assert math.isclose(x[i], y[i] * U[i], rel_tol=accuracy)
    assert x.shape == U.shape


def test_BulkFormula_K00(accuracy):
    U = T_s = T_a = np.array([1, 10])
    y = np.array([0.0010764375, 0.001653, np.nan])
    x = processing.BulkFormula("kara_etal_2000").calculate(
        U=U, T_s=T_s, T_a=T_a, rho=1, u=1
    )
    for i, _ in enumerate(U):
        assert math.isclose(x[i], y[i] * U[i], rel_tol=accuracy)
    assert x.shape == U.shape
