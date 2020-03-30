import pytest

from windeval.io import products


def test_open_product():
    with pytest.raises(NotImplementedError):
        products.open_product("path1", "path2", kwarg={"kwarg": "kwargs"})


def test_info(X):
    with pytest.raises(NotImplementedError):
        products.info({"ds": X})


def test_select(X):
    with pytest.raises(NotImplementedError):
        products.select({"ds": X})
