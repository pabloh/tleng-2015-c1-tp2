import unittest
import musileng.parser
import musileng.lexer
from musileng.ast import *
from ply import lex, yacc

class TestMusilengParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lexer = lex.lex(module=musileng.lexer)
        cls.parser = yacc.yacc(module=musileng.parser)

    def setUp(self):
        self.lexer = self.__class__.lexer
        self.parser = self.__class__.parser

        self.simple_def = """
            #tempo negra 60
            #compas 2/4

            voz(3) {
                compas {
                    nota(do, 1, blanca);
                }
            }
        """

    def parse(self, text):
        return self.parser.parse(text, self.lexer)

    def test_header(self):
        mus = self.parse(self.simple_def)

        self.assertIsInstance(mus, MusiLeng)
        self.assertEqual(Fraction(2,4), mus.bar.fraction())
        self.assertEqual(60, mus.tempo.notes_per_min)
        self.assertEqual(Duration('negra'), mus.tempo.reference_note)


    def test_voice(self):
        mus = self.parse(self.simple_def)

        self.assertEqual(1, len(mus.voices))
        self.assertIsInstance(mus.voices[0], Voice)
        self.assertEqual(3, mus.voices[0].instrument.value_for({}))
        self.assertEqual(1, len(mus.voices[0].bars))
        self.assertIsInstance(mus.voices[0].bars[0], Bar)


if __name__ == '__main__':
    unittest.main()
