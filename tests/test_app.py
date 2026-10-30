"""Numerical checks and Streamlit execution checks, no network needed."""
import io
import unittest
from pathlib import Path
import numpy as np
import colour
from streamlit.testing.v1 import AppTest
from core import ROOT
from importlib import import_module


def exercise(number):
    path = next((ROOT / 'pages').glob(f'{number}_*.py'))
    return import_module(f'pages.{path.stem}')


read_spectrum = exercise(2).read_spectrum
spectrum_xyz = exercise(2).spectrum_xyz
band_data = exercise(7).band_data
halftone_data = exercise(6).halftone_data
trc = exercise(6).trc
predict_mix = exercise(6).predict_mix
lab_difference = exercise(8).lab_difference


class Calculations(unittest.TestCase):
    def test_srgb_white_and_roundtrip(self):
        np.testing.assert_allclose(colour.sRGB_to_XYZ([1, 1, 1])*100, [95.05, 100, 108.9], atol=.03)
        rgb = [.2, .5, .8]
        # Colour uses published sRGB matrices rounded to four decimal places.
        np.testing.assert_allclose(colour.XYZ_to_sRGB(colour.sRGB_to_XYZ(rgb)), rgb, atol=1e-4)

    def test_perfect_reflector(self):
        a = np.column_stack([np.arange(360, 831), np.ones(471)])
        self.assertAlmostEqual(spectrum_xyz(a)[1], 100, places=5)

    def test_csv_validation(self):
        for data in ['400,0.1\n410,0.2\n410,0.3\n430,0.4', '400,0.1\n410,-1\n420,0.3\n430,0.4', '400,0.1\n410,nan\n420,0.3\n430,0.4']:
            with self.assertRaises(ValueError):
                read_spectrum(io.StringIO(data))
        a = read_spectrum(io.StringIO('nm,R\n400,10\n410,20\n420,30\n430,40'), True)
        np.testing.assert_allclose(a[:, 1], [.1, .2, .3, .4])

    def test_band_exact_range(self):
        wave, xyz, rgb = band_data()
        self.assertEqual((wave[0], wave[-1], len(wave)), (400, 700, 301))
        self.assertEqual(xyz.shape, rgb.shape)
        self.assertTrue(np.all((rgb >= 0) & (rgb <= 1)))

    def test_halftone_endpoints(self):
        p, yellow, magenta = halftone_data()
        for samples in [yellow, magenta]:
            area, _ = trc(samples)
            np.testing.assert_allclose(area[[0, -1]], [0, 1], atol=1e-10)
        for mi, yi in [(0, 0), (0, 10), (10, 0), (10, 10), (5, 5)]:
            pred = predict_mix(p, mi, yi)
            self.assertTrue(np.isfinite(pred).all())
            self.assertTrue(np.all((pred >= 0) & (pred <= 1)))

    def test_delta_e_reference(self):
        # Published CIEDE2000 test pair (Sharma et al.).
        _, _, _, de = lab_difference([50, 2.6772, -79.7751], [50, 0, -82.7485])
        self.assertAlmostEqual(de, 2.0425, places=4)
        delta, dc, d76, d00 = lab_difference([0, 0, 0], [0, 0, 0])
        self.assertEqual(d76, 0)
        self.assertEqual(d00, 0)


class Pages(unittest.TestCase):
    def assert_clean(self, app):
        self.assertEqual(len(app.exception), 0, str(app.exception))
        self.assertEqual(len(app.error), 0, str(app.error))

    def test_every_page(self):
        for file in [ROOT / 'app.py', ROOT / 'Khoa học Màu sắc.py', *sorted((ROOT/'pages').glob('[1-8]_*.py'))]:
            with self.subTest(page=file.name):
                self.assert_clean(AppTest.from_file(str(file), default_timeout=40).run())

    def test_converter_inverse(self):
        app = AppTest.from_file(str(next((ROOT/'pages').glob('1_*.py')))).run()
        app.radio[0].set_value('XYZ → sRGB').run()
        self.assert_clean(app)

    def test_halftone_modes(self):
        app = AppTest.from_file(str(next((ROOT/'pages').glob('6_*.py'))), default_timeout=40).run()
        for mode in ['Phổ phản xạ', 'Đường cong tái tạo tông', 'Dự báo trộn màu']:
            app.radio[0].set_value(mode).run()
            self.assert_clean(app)

    def test_lab_d50_black(self):
        app = AppTest.from_file(str(ROOT/'pages/8_CIELab_so_sanh_mau.py'), default_timeout=40).run()
        app.selectbox[0].set_value('D50')
        for item in app.number_input:
            item.set_value(0.)
        app.run()
        self.assert_clean(app)

    def test_rgb_custom(self):
        app = AppTest.from_file(str(next((ROOT/'pages').glob('4_*.py'))), default_timeout=40).run()
        app.checkbox[0].check().run()
        app.multiselect[0].set_value(['sRGB', 'Adobe RGB (1998)', 'Display P3', 'ITU-R BT.2020']).run()
        self.assert_clean(app)


if __name__ == '__main__':
    unittest.main()
