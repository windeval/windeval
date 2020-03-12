import pytest
from windeval import plotting


def test_report(X):
    with pytest.raises(NotImplementedError):
        plotting.plot({"ds": X})
