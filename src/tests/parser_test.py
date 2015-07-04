import unittest
from tests.helpers import TestMusilengBase
from musileng.ast import *
from musileng.semantic_analysis import *

class TestMusilengParser(TestMusilengBase):
    def setUp(self):
        super().setUp()

        self.def_with_empty_voice = self.simple_header + """
            voz(0) {
                compas { nota(do, 1, blanca); }
            }
            voz(23) { }
        """

        self.def_with_empty_bar = self.simple_header + """
            voz(0) {
                compas { nota(do, 1, blanca); }
            }
            voz(23) { compas {} }
        """

        self.invalid_tempo_def = """
            #tempo negra 0
            #compas 2/4

            voz(0) { compas { nota(do, 1, blanca); } }
        """

        self.invalid_bar_pulses_def = """
            #tempo negra 60
            #compas 0/4

            voz(0) { compas { nota(do, 1, blanca); } }
        """

        self.invalid_bar_base_def = """
            #tempo negra 60
            #compas 2/3

            voz(0) { compas { nota(do, 1, blanca); } }
        """

        voice = """
            voz(0) {
                compas { nota(do, 1, blanca); }
            }
        """

        self.too_many_voices_def = self.simple_header + voice * 17


    def test_valid_directives(self):
        mus = self.parse(self.simple_def)
        tempo_dur = mus.tempo.reference_note

        self.assertIsInstance(mus, MusiLeng)
        self.assertIsInstance(mus.bar, BarDirective)
        self.assertIsInstance(mus.tempo, TempoDirective)
        self.assertEqual(Fraction(2,4), mus.bar.fraction())
        self.assertEqual(60, mus.tempo.notes_per_min)
        self.assertIsInstance(tempo_dur, Duration)
        self.assertEqual('negra', tempo_dur.note_value)
        self.assertFalse(tempo_dur.dotted)

    def test_invalid_tempo(self):
        with self.assertRaises(InvalidTempo):
            self.parse(self.invalid_tempo_def)

    def test_invalid_bar_pulses(self):
        with self.assertRaises(InvalidBarPulses):
            self.parse(self.invalid_bar_pulses_def)

    def test_invalid_bar_base(self):
        with self.assertRaises(InvalidBarBase):
            self.parse(self.invalid_bar_base_def)

    def test_voice(self):
        mus = self.parse(self.simple_def)

        self.assertEqual(1, len(mus.voices))
        self.assertIsInstance(mus.voices[0], Voice)
        self.assertEqual(3, mus.voices[0].instrument.value())
        self.assertEqual(1, len(mus.voices[0].childs))
        self.assertIsInstance(mus.voices[0].childs[0], Bar)

    def test_too_many_voices(self):
        with self.assertRaises(TooManyVoices):
            self.parse(self.too_many_voices_def)

    def test_number_refs(self):
        mus = self.parse(self.simple_def_w_consts)
        symbols = self.symbol_table(mus)

        self.assertEqual(23, mus.voices[0].instrument.value(symbols))
        self.assertEqual(1, mus.voices[0].childs[0].notes[0].octave.value(symbols))
        self.assertEqual(2, mus.voices[0].childs[0].notes[1].octave.value(symbols))

    def test_no_voices(self):
        with self.assertRaises(SyntaxError):
            self.parse(self.simple_header)

    def test_empty_voice(self):
        with self.assertRaises(SyntaxError):
            self.parse(self.def_with_empty_voice)

    def test_empty_bar(self):
        with self.assertRaises(SyntaxError):
            self.parse(self.def_with_empty_bar)


if __name__ == '__main__':
    unittest.main()
