import unittest
from musileng.ast import *
from musileng.semantic_analysis import *
from tests.helpers import TestMusilengBase

class TestMusilengSemantics(TestMusilengBase):
    def setUp(self):
        super().setUp()

        self.missing_consts_def = """
            #tempo negra 60
            #compas 2/4

            const octava2 = 2;
            const piano = 23;

            voz(piano) {
                compas {
                    nota(do, octava1, blanca);
                }
            }
        """

        self.redeclared_consts_def = """
            #tempo negra 60
            #compas 2/4

            const octava2 = 2;
            const piano = 23;
            const octava2 = 4;

            voz(piano) {
                compas {
                    nota(do, octava2, blanca);
                }
            }
        """


        self.invalid_octave_def = self.simple_header + """
            voz(0) {
                compas { nota(do, 10, blanca); }
            }
        """

        self.invalid_instrument_def = self.simple_header + """
            voz(128) {
                compas { nota(do, 1, blanca); }
            }
        """

        self.invalid_repeat_def = self.simple_header + """
            voz(0) {
                repetir(0) {
                    compas { nota(do, 1, blanca); }
                }
            }
        """

        self.correct_bar_length_def = self.simple_header + """
            voz(0) {
                compas {
                    nota(do, 1, negra.);
                    silencio(corchea);
                }
            }
        """

        self.bigger_bar_length_def = self.simple_header + """
            voz(0) {
                compas {
                    nota(do, 1, negra);
                    nota(do, 1, negra);
                    nota(do, 1, negra);
                }
            }
        """

        self.smaller_bar_length_def = self.simple_header + """
            voz(0) {
                compas { nota(do, 1, negra); }
            }
        """

    def test_const_decl(self):
        mus = self.parse(self.simple_def_w_consts)
        self.analizer.visit(mus)

        self.assertEqual({'octava1' : 1, 'octava2' : 2, 'piano' : 23}, self.analizer.symbol_table)

    def test_missing_consts(self):
        mus = self.parse(self.missing_consts_def)

        with self.assertRaises(UndeclaredSymbol):
            self.analizer.visit(mus)

    def test_redeclared_consts(self):
        mus = self.parse(self.redeclared_consts_def)

        with self.assertRaises(RedeclaredSymbol):
            self.analizer.visit(mus)

    def test_invalid_octave(self):
        mus = self.parse(self.invalid_octave_def)

        with self.assertRaises(InvalidOctave):
            self.analizer.visit(mus)

    def test_invalid_instrument(self):
        mus = self.parse(self.invalid_instrument_def)

        with self.assertRaises(InvalidInstrument):
            self.analizer.visit(mus)

    def test_invalid_repeat(self):
        mus = self.parse(self.invalid_repeat_def)

        with self.assertRaises(InvalidRepeatNumber):
            self.analizer.visit(mus)

    def test_bar_lenghts(self):
        mus = self.parse(self.bigger_bar_length_def)

        with self.assertRaises(InvalidBarDuration):
            self.analizer.visit(mus)

        mus = self.parse(self.smaller_bar_length_def)

        with self.assertRaises(InvalidBarDuration):
            self.analizer.visit(mus)

        mus = self.parse(self.correct_bar_length_def)
        self.analizer.visit(mus)

if __name__ == '__main__':
    unittest.main()
