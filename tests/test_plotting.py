import pytest

from windeval import plotting, processing


def test_plot(X):
    plotting.plot({"ds": X}, "eastward_wind")
    with pytest.raises(NotImplementedError):
        plotting.plot(False)
    with pytest.raises(NotImplementedError):
        plotting.plot({"ds": X}, "eastward_wind", dataset=[])
    ds = processing.diagnostics({"ds": X}, "eastward_wind", "welch")
    plotting.plot(ds, "power_spectral_density")
