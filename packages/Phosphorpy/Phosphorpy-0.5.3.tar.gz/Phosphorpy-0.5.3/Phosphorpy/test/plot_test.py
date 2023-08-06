from Phosphorpy.data.data import DataSet


def get_test_dataset():
    ds = DataSet.load_coordinates('./full_phot_data.fits',
                                  format='fits',
                                  ra_name='ra',
                                  dec_name='dec')
    ds.load_from_vizier('sdss')
    ds.load_from_vizier('2mass')
    return ds


def test_sed_plot():
    ds = get_test_dataset()
    ds.plot.sed(2, x_log=True, y_log=True)


def test_color_color():
    ds = get_test_dataset()
    ds.plot.color_color(['Jmag - Hmag', 'Hmag - Kmag'])


def test_color_color_all():
    ds = get_test_dataset()
    ds.plot.color_color(['umag - gmag', 'gmag - rmag', 'Jmag - Hmag', 'Hmag - Kmag']
                        )
