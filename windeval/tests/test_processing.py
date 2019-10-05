import math
import pytest
import inspect
from windeval import processing


@pytest.fixture
def accuracy():
    return 1e-12


def test_BulkFormula():
    BFC = processing.BulkFormula
    assert inspect.isclass(BFC)
    BFI = processing.BulkFormula()
    assert isinstance(BFI, BFC)
    for method in [
        "Large_and_Pond_1981",
        "Trenberth_etal_1990",
        "Yelland_and_Taylor_1996",
        "Kara_etal_2000",
        "Large_and_Yeager_2004",
        "NCEP_NCAR_2007",
    ]:
        bulk = getattr(processing.BulkFormula(), method.lower())
        assert callable(bulk)


def test_BulkFormula_YT96(accuracy):
    U = [3, 5.9, 6, 12, 26, 27, 1]
    bulk = processing.BulkFormula().yelland_and_taylor_1996
    assert math.isclose(bulk(U[0]), 0.00217888888888889, rel_tol=accuracy)
    assert math.isclose(bulk(U[1]), 0.001036624533180121, rel_tol=accuracy)
    assert math.isclose(bulk(U[2]), 0.00102, rel_tol=accuracy)
    assert math.isclose(bulk(U[3]), 0.00144, rel_tol=accuracy)
    assert math.isclose(bulk(U[4]), 0.00242, rel_tol=accuracy)
    for u in U[-2:]:
        with pytest.raises(ValueError) as e:
            assert bulk(u)
        assert (
            str(e.value)
            == "Bulk-formula is not defined for values outside of the interval I = "
            + "[3, 26]"
        )


def test_BulkFormula_LP81(accuracy):
    U = [5, 12, 1, 26]
    bulk = processing.BulkFormula().large_and_pond_1981
    assert bulk(U[0]) == 1.2 * 1e-3
    assert math.isclose(bulk(U[1]), 0.00127, rel_tol=accuracy)
    for u in U[-2:]:
        with pytest.raises(ValueError) as e:
            assert bulk(u)
        assert (
            str(e.value)
            == "Bulk-formula is not defined for values outside of the interval I = "
            + "[4, 25]"
        )


def test_BulkFormula_KH07(accuracy):
    bulk = processing.BulkFormula().ncep_ncar_2007
    assert bulk() == 1.3 * 1e-3


def test_BulkFormula_T90(accuracy):
    U = [0.5, 1.5, 3 + 1e-10, 15]
    bulk = processing.BulkFormula().trenberth_etal_1990
    assert bulk(U[0]) == 0.00218
    assert math.isclose(bulk(U[1]), 0.00166, rel_tol=accuracy)
    assert bulk(U[2]) == 0.00114
    assert math.isclose(bulk(U[3]), 0.001465, rel_tol=accuracy)


def test_BulkFormula_LY04(accuracy):
    U = [1, 2]
    bulk = processing.BulkFormula().large_and_yeager_2004
    assert math.isclose(bulk(U[0]), 0.002918, rel_tol=accuracy)
    assert math.isclose(bulk(U[1]), 0.001644, rel_tol=accuracy)
    with pytest.raises(ValueError) as e:
        assert bulk(0)
    assert str(e.value) == "Bulk-formula is not defined for U = 0"


def test_BulkFormula_K00(accuracy):
    V_a = T_s = T_a = [1, 10]
    bulk = processing.BulkFormula.kara_etal_2000
    assert math.isclose(bulk(V_a[0], T_s[0], T_a[0]), 0.0010764375, rel_tol=accuracy)
    assert math.isclose(bulk(V_a[1], T_s[1], T_a[1]), 0.001653, rel_tol=accuracy)
