from SearchEngine.data.sub.magnitudes import Magnitude
from astropy.table import Table
import numpy as np
import time
import pylab as pl


def get_example_data(size=1000):

    t = Table()
    t['U'] = 2*np.random.rand() * np.random.randn(size)+18
    t['B'] = 2*np.random.rand() * np.random.randn(size)+17.6
    t['V'] = 2*np.random.rand() * np.random.randn(size)+16.9
    t['R'] = 2*np.random.rand() * np.random.randn(size)+16
    return t.to_pandas()


def test_speed_magnitude():
    lin = np.logspace(2, 6, 1000, dtype=np.int32)
    o = []
    for i in lin:
        m = Magnitude(get_example_data(i))
        to = time.time()
        # print()
        m.stats()
        # m.plot.hist()
        m.get_colors()
        o.append((i, time.time()-to))
    o = Table(rows=o, names=['n', 't'])
    pl.clf()
    sp = pl.subplot()
    sp.plot(o['n'], o['t'])
    sp.set_xscale('log')
    pl.show()
    pass


def test_basic_magnitude():
    print()
    sample = get_example_data(3000)
    m = Magnitude(sample)
    print(m.stats())

    colors = m.get_colors()
    print(colors.stats())


def test_basic_color():
    print()
    sample = get_example_data(300)
    m = Magnitude(sample)
    print(m.stats())

    colors = m.get_colors()
    print(colors.stats())
    colors.plot.color_color()
