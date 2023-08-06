from SearchEngine.report.Report import SourceList, Report, SourcePositionPlot, MagnitudePlot
from SearchEngine.report.source import Detail
from astropy.coordinates import SkyCoord
from astropy.table import Table, unique
from astropy import units as u
import numpy as np


def test_source_list():
    tab = Table.read('./full_phot_data.fits')
    tab['zero'] = 0

    print(tab.colnames)
    tab = unique(tab, keys='ra')
    # tab = tab[:2]
    mask = tab['UKIDSS_kmag'] > 0
    coords = SkyCoord(tab['ra'],
                      tab['dec'])
    tab['l'] = coords.galactic.l
    tab['b'] = coords.galactic.b
    # print(coords.to_string('hmsdms'))
    sl = SourceList(coords)
    spp = SourcePositionPlot(coords, projection='mollweide', mask=mask)
    spp2 = SourcePositionPlot(coords, projection='mollweide', mask=mask, galactic=True)
    mp = MagnitudePlot(tab, 'SDSS12_umag', 'SDSS12_gmag',
                       'SDSS12_gmag', 'SDSS12_rmag', mask=mask)
    mp3 = MagnitudePlot(tab, 'SDSS12_gmag', 'SDSS12_rmag',
                        'SDSS12_rmag', 'SDSS12_imag', mask=mask)
    mp4 = MagnitudePlot(tab, 'SDSS12_rmag', 'SDSS12_imag',
                        'SDSS12_imag', 'SDSS12_zmag', mask=mask)
    mp2 = MagnitudePlot(tab, '2MASS_Jmag', '2MASS_Hmag',
                        '2MASS_Hmag', '2MASS_Kmag', mask=mask)
    mp5 = MagnitudePlot(tab, 'SDSS12_gmag', 'PS_gmag',
                        'SDSS12_zmag', 'PS_zmag', mask=mask)
    mp6 = MagnitudePlot(tab, 'UKIDSS_j_1mag', 'UKIDSS_hmag',
                        'UKIDSS_hmag', 'UKIDSS_kmag', mask=mask)
    rp = Report()
    rp.add_section(spp)
    rp.add_section(spp2)
    rp.add_section(mp)
    rp.add_section(mp2)
    rp.add_section(mp3)
    rp.add_section(mp4)
    rp.add_section(mp5)
    rp.add_section(mp6)
    rp.add_section(sl)
    for c in tab:
        rp.add_section(Detail(c))
    rp.html('./test.html')
    # tab[mask].show_in_browser(jsviewer=True)
