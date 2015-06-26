import unittest
import musileng.parser
import musileng.lexer
from musileng.ast import *
from musileng.validations import *
from ply import lex, yacc

class TestMusilengParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lexer = lex.lex(module=musileng.lexer)
        cls.parser = yacc.yacc(module=musileng.parser)

    def setUp(self):
        self.lexer = type(self).lexer
        self.parser = type(self).parser
        self.symbols_checker = ValidateSymbolsReference()

        self.simple_def = """
            #tempo negra 60
            #compas 2/4

            voz(3) {
                compas {
                    nota(do, 1, blanca);
                }
            }
        """

        self.simple_def_w_consts = """
            #tempo negra 60
            #compas 2/4

            const octava1 = 1;
            const octava2 = 2;
            const piano = 23;

            voz(piano) {
                compas {
                    nota(do, octava1, blanca);
                }
            }
        """

        self.simple_def_missing_consts = """
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

    def parse(self, text):
        return self.parser.parse(text, self.lexer)

    def test_directives(self):
        mus = self.parse(self.simple_def)

        self.assertIsInstance(mus, MusiLeng)
        self.assertEqual(Fraction(2,4), mus.bar.fraction())
        self.assertEqual(60, mus.tempo.notes_per_min)
        self.assertEqual(Duration('negra'), mus.tempo.reference_note)


    def test_voice(self):
        mus = self.parse(self.simple_def)

        self.assertEqual(1, len(mus.voices))
        self.assertIsInstance(mus.voices[0], Voice)
        self.assertEqual(3, mus.voices[0].instrument.value())
        self.assertEqual(1, len(mus.voices[0].bars))
        self.assertIsInstance(mus.voices[0].bars[0], Bar)


    def test_consts(self):
        mus = self.parse(self.simple_def_w_consts)
        symbols = mus.consts

        self.assertEqual({'octava1' : 1, 'octava2' : 2, 'piano' : 23}, symbols)
        self.assertEqual(23, mus.voices[0].instrument.value(symbols))
        self.assertEqual(1, mus.voices[0].bars[0].notes[0].octave.value(symbols))

        self.symbols_checker.visit(mus)


    def test_missing_consts(self):
        mus = self.parse(self.simple_def_missing_consts)

        with self.assertRaises(UndeclaredSymbol, msg="Identificador 'octava1' no declarado previamente"):
            self.symbols_checker.visit(mus)


if __name__ == '__main__':
    unittest.main()
