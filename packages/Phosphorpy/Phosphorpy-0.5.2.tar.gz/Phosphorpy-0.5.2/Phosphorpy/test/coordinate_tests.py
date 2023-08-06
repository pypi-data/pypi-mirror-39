import numpy as np
from Phosphorpy.data.sub.coordinates import CoordinateTable


def test_basic_coordinate_table():

    ct = CoordinateTable(np.array([[24.23, 24.22],
                                   [65.34, 1.23]]))
    # print(ct._data.shape)
    # print(ct['ra'], ct['dec'])
    # print(len(ct))


def test_coordinate_match():

    ct = CoordinateTable(np.array([[24.23, 24.22],
                                   [65.34, 1.23]]))

    ct2 = CoordinateTable(np.array([[65.34, 1.23],
                                    [24.23, 24.22]
                                    ]))
    print(ct.match(ct2))


def test_coordinate_plot():

    ct = CoordinateTable(np.array([[24.23, 24.22],
                                   [65.34, 1.23]]))
    ct.plot.equatorial()
    ct.plot.galactic()
