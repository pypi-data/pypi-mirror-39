import os

from Phosphorpy.data.data import DataSet
from astropy.table import Table
import numpy as np
import warnings
import time


warnings.simplefilter('ignore')


def get_test_coordinates():
    tab = Table.read('./full_phot_data.fits')
    tab = tab[['ra', 'dec']]
    return tab.to_pandas()


def test_vizier():
    d = DataSet(get_test_coordinates())
    # print(d.coordinates.to_table())
    mass = d.load_from_vizier('2mass')
    gaia = d.load_from_vizier('gaia')
    gaia = d.load_from_vizier('sdss')
    gaia = d.load_from_vizier('panstarrs')
    gaia = d.load_from_vizier('wise')
    gaia = d.load_from_vizier('galex')
    print(d.magnitudes.data[['gmag_panstarrs',
                             'rmag_panstarrs',
                             'imag_panstarrs',
                             'zmag_panstarrs',
                             'ymag_panstarrs']])
    # print(d.magnitudes._survey)

    # print(d.magnitudes._survey._properties)
    print(d.magnitudes.get_flux())
    # print(mass.magnitudes.stats())
    # print(mass.magnitudes.mag_names)
    # print(mass.magnitudes.get_flux())


def test_flux_converting():
    d = DataSet(get_test_coordinates())
    mass = d.load_from_vizier('2mass')
    gaia = d.load_from_vizier('gaia')
    gaia = d.load_from_vizier('sdss')
    gaia = d.load_from_vizier('panstarrs')
    gaia = d.load_from_vizier('ukidss')
    fl = d.magnitudes.get_flux()

    g_fl = fl._data['gmag']/fl.data['gmag_panstarrs']
    g_fl = g_fl.values-1
    r_fl = fl._data['rmag']/fl.data['rmag_panstarrs']
    r_fl = r_fl.values-1
    i_fl = fl._data['imag']/fl.data['imag_panstarrs']
    i_fl = i_fl.values-1

    mask = (np.abs(g_fl) < 0.25) & (np.abs(r_fl) < 0.25) & (np.abs(i_fl) < 0.25)
    fl.mask = mask

    # fl.fit_polynomial(4, True, True, True, True)
    for i in range(1, 50):
        try:
            fl.plot.sed(i, x_log=True, y_log=True, fit=3)
        except KeyError:
            pass
    # import pylab as pl
    #
    # pl.clf()
    # sp = pl.subplot()
    # sp.scatter(g_fl[mask], i_fl[mask], c=r_fl[mask],
    #            cmap='jet', marker='.')
    # print(len(g_fl), len(g_fl[mask]))
    # pl.show()


def test_color_converting():
    t0 = time.time()
    d = DataSet.load_coordinates('./full_phot_data.fits',
                                 format='fits',
                                 ra_name='ra',
                                 dec_name='dec')
    print('load data', time.time()-t0)
    t0 = time.time()
    print('2mass')
    d.load_from_vizier('2mass')
    # d.load_from_vizier('gaia')
    print('sdss')
    d.load_from_vizier('sdss')
    print('panstarrs')
    d.load_from_vizier('panstarrs')
    d.flux.data.to_csv('fluxes.csv')
    print(d.coordinates.data)
    # d.load_from_vizier('wise')
    # print('load from vizier', time.time()-t0)
    # t0 = time.time()
    # d.magnitudes.set_limit('rmag', 19, 14)
    # d.magnitudes.set_limit('rmag', 18.25, 14)
    # d.magnitudes.set_limit('rmag', 17, 14)
    # print('set mag limits vizier', time.time()-t0)
    # t0 = time.time()
    # d.colors.plot.color_color(['umag - gmag', 'BPmag - Gmag'])
    # d.colors.plot.color_color(['W1mag - W2mag', 'gmag - rmag'])
    #
    # print('plots', time.time()-t0)
    # t0 = time.time()
    # print(d.magnitudes.stats()['rmag'])
    #
    # print('statistics', time.time()-t0)
    # t0 = time.time()


def test_writing():

    d = DataSet.load_coordinates('./full_phot_data.fits',
                                 format='fits',
                                 ra_name='ra',
                                 dec_name='dec')
    d.load_from_vizier('2mass')
    d.colors
    d.flux
    d.write('test_zip.zip', format='zip', in_zip_format='csv')


def test_writing_reading():

    d = DataSet.load_coordinates('./full_phot_data.fits',
                                 format='fits',
                                 ra_name='ra',
                                 dec_name='dec')
    d.load_from_vizier('2mass')
    d.load_from_vizier('sdss')
    d.colors
    d.flux
    try:
        os.remove('test_zip.zip')
    except:
        pass
    d.write('test_zip.zip', format='zip', in_zip_format='csv')
    ds = DataSet.read_from_file('test_zip.zip')
    print(ds)


def test_mask_plotting():
    ds = DataSet.from_vizier('gaia', **{'pmRA': '> 300'})
    print(ds.magnitudes._survey.flux_zero('gaia', 'G'))
    ds.load_from_vizier('2mass')
    ds.magnitudes.set_limit('Gmag', 16, 14)
    # ds.plot.equatorial_coordinates()
    ds.plot.color_color(survey='2mass')
