from Phosphorpy.data.data import DataSet
from Phosphorpy.external.xmatch import xmatch
import time
import numpy as np


def test_xmatch():
    t0 = time.time()
    d = DataSet.load_coordinates('./full_phot_data.fits',
                                 format='fits',
                                 ra_name='ra',
                                 dec_name='dec')
    survey = '2MASS'
    # print('load data', time.time()-t0)
    # t0 = time.time()
    # d.load_from_vizier(survey)

    print('vizier', time.time()-t0)
    t0 = time.time()
    rs = xmatch(d.coordinates.to_table(), 'ra', 'dec', survey)
    print('xmatch', time.time()-t0)
    t0 = time.time()
    print(rs.columns)

    # print(rs[['ra', 'dec', 'e_RPmag']])