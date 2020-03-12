from windeval import wrapper


def test_ekman(X):
    wrapper.ekman(X, drag_coefficient="large_and_pond_1981", extend_ranges=True)


def test_sverdrup(X):
    wrapper.sverdrup(X, drag_coefficient="large_and_yeager_2004")
