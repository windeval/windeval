import pytest
from windeval.io import reports


def test_report(X):
    with pytest.raises(NotImplementedError):
        reports.report({"ds": X})
