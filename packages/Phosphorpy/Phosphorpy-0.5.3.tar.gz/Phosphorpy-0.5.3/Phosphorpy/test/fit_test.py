from SearchEngine.fitting.fit import PolyFit
import numpy as np


def test_polyfit():
    x = np.array([1, 2, 3, 4, 5, 6, 7])
    y = x**2
    pf = PolyFit(2, x_log=True)
    fit = pf(x, y)
    print(fit)
