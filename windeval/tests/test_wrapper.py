import windeval


def test_ekman(X):
    windeval.ekman(X, drag_coefficient="large_and_pond_1981", extend_ranges=True)


def test_sverdrup(X):
    windeval.sverdrup(X, drag_coefficient="large_and_yeager_2004")
