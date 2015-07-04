import unittest
import re
from musileng.ast import *
from musileng.semantic_analysis import *
from musileng.encoder import *
from tests.helpers import TestMusilengBase
from io import StringIO

class TestMusilengEncoder(TestMusilengBase):
    def setUp(self):
        super().setUp()
        self.output = StringIO()
        self.encoder = SMFEncoder(self.output)

        self.simple_def_encoded = self.no_ident("""
            MFile 1 2 384
            MTrk
            000:00:000 TimeSig 2/4 24 8
            000:00:000 Tempo 1000000
            000:00:000 Meta TrkEnd
            TrkEnd
            MTrk
            000:00:000 Meta TrkName "Voz 1"
            000:00:000 ProgCh ch=1 prog=3
            000:00:000 On  ch=1 note=c1  vol=70
            001:00:000 Off ch=1 note=c1  vol=0
            001:00:000 Meta TrkEnd
            TrkEnd
            """)

        self.def_w_repeat = """
            #tempo negra 60
            #compas 2/4

            const octava1 = 1;
            const octava2 = 2;
            const piano = 23;

            voz(piano) {
                compas {
                    nota(do+, octava1, negra);
                    nota(re, octava2, negra);
                }

                repetir(2) {
                    compas {
                        nota(fa, octava1, corchea.);
                        nota(sol-, octava2, semicorchea);
                        nota(la, octava2, negra);
                    }
                }
            }
        """

        self.def_w_repeat_encoded = self.no_ident("""
            MFile 1 2 384
            MTrk
            000:00:000 TimeSig 2/4 24 8
            000:00:000 Tempo 1000000
            000:00:000 Meta TrkEnd
            TrkEnd
            MTrk
            000:00:000 Meta TrkName "Voz 1"
            000:00:000 ProgCh ch=1 prog=23
            000:00:000 On  ch=1 note=c+1 vol=70
            000:01:000 Off ch=1 note=c+1 vol=0
            000:01:000 On  ch=1 note=d2  vol=70
            001:00:000 Off ch=1 note=d2  vol=0
            001:00:000 On  ch=1 note=f1  vol=70
            001:00:288 Off ch=1 note=f1  vol=0
            001:00:288 On  ch=1 note=g-2 vol=70
            001:01:000 Off ch=1 note=g-2 vol=0
            001:01:000 On  ch=1 note=a2  vol=70
            002:00:000 Off ch=1 note=a2  vol=0
            002:00:000 On  ch=1 note=f1  vol=70
            002:00:288 Off ch=1 note=f1  vol=0
            002:00:288 On  ch=1 note=g-2 vol=70
            002:01:000 Off ch=1 note=g-2 vol=0
            002:01:000 On  ch=1 note=a2  vol=70
            003:00:000 Off ch=1 note=a2  vol=0
            003:00:000 Meta TrkEnd
            TrkEnd
            """)

        self.def_w_many_voices = """
            #tempo negra 100
            #compas 3/4

            const octava1 = 1;
            const octava2 = 2;
            const piano = 23;

            voz(piano) {
                compas {
                    silencio(negra);
                    nota(mi, octava2, blanca);
                }
                compas {
                    nota(re, octava1, blanca);
                    nota(do, octava1, negra);
                }

            }

            voz(piano) {
                repetir(2) {
                    compas {
                        nota(do, octava1, corchea);
                        nota(mi, octava2, blanca);
                        nota(si, octava1, corchea);
                    }
                }
            }
        """

        self.def_w_many_voices_encoded = self.no_ident("""
            MFile 1 3 384
            MTrk
            000:00:000 TimeSig 3/4 24 8
            000:00:000 Tempo 600000
            000:00:000 Meta TrkEnd
            TrkEnd
            MTrk
            000:00:000 Meta TrkName "Voz 1"
            000:00:000 ProgCh ch=1 prog=23
            000:01:000 On  ch=1 note=e2  vol=70
            001:00:000 Off ch=1 note=e2  vol=0
            001:00:000 On  ch=1 note=d1  vol=70
            001:02:000 Off ch=1 note=d1  vol=0
            001:02:000 On  ch=1 note=c1  vol=70
            002:00:000 Off ch=1 note=c1  vol=0
            002:00:000 Meta TrkEnd
            TrkEnd
            MTrk
            000:00:000 Meta TrkName "Voz 2"
            000:00:000 ProgCh ch=2 prog=23
            000:00:000 On  ch=2 note=c1  vol=70
            000:00:192 Off ch=2 note=c1  vol=0
            000:00:192 On  ch=2 note=e2  vol=70
            000:02:192 Off ch=2 note=e2  vol=0
            000:02:192 On  ch=2 note=b1  vol=70
            001:00:000 Off ch=2 note=b1  vol=0
            001:00:000 On  ch=2 note=c1  vol=70
            001:00:192 Off ch=2 note=c1  vol=0
            001:00:192 On  ch=2 note=e2  vol=70
            001:02:192 Off ch=2 note=e2  vol=0
            001:02:192 On  ch=2 note=b1  vol=70
            002:00:000 Off ch=2 note=b1  vol=0
            002:00:000 Meta TrkEnd
            TrkEnd
            """)

        self.def_w_full_note_bar = """
            #tempo negra 100
            #compas 2/1

            voz(0) {
                compas {
                    nota(do, 1, semifusa);
                    nota(re, 1, semifusa);
                    nota(mi, 1, fusa);
                    nota(mi, 1, semicorchea);
                    nota(fa, 1, corchea);
                    nota(mi, 1, negra);
                    nota(si, 1, blanca);

                    nota(mi, 1, semifusa.);
                    nota(re, 1, semifusa.);
                    nota(mi, 1, semifusa);
                    nota(re, 1, corchea.);
                    nota(mi, 1, blanca.);
                }
            }
        """

        self.def_w_full_note_bar_encoded = self.no_ident("""
            MFile 1 2 384
            MTrk
            000:00:000 TimeSig 2/1 24 8
            000:00:000 Tempo 600000
            000:00:000 Meta TrkEnd
            TrkEnd
            MTrk
            000:00:000 Meta TrkName "Voz 1"
            000:00:000 ProgCh ch=1 prog=0
            000:00:000 On  ch=1 note=c1  vol=70
            000:00:006 Off ch=1 note=c1  vol=0
            000:00:006 On  ch=1 note=d1  vol=70
            000:00:012 Off ch=1 note=d1  vol=0
            000:00:012 On  ch=1 note=e1  vol=70
            000:00:024 Off ch=1 note=e1  vol=0
            000:00:024 On  ch=1 note=e1  vol=70
            000:00:048 Off ch=1 note=e1  vol=0
            000:00:048 On  ch=1 note=f1  vol=70
            000:00:096 Off ch=1 note=f1  vol=0
            000:00:096 On  ch=1 note=e1  vol=70
            000:00:192 Off ch=1 note=e1  vol=0
            000:00:192 On  ch=1 note=b1  vol=70
            000:01:000 Off ch=1 note=b1  vol=0
            000:01:000 On  ch=1 note=e1  vol=70
            000:01:009 Off ch=1 note=e1  vol=0
            000:01:009 On  ch=1 note=d1  vol=70
            000:01:018 Off ch=1 note=d1  vol=0
            000:01:018 On  ch=1 note=e1  vol=70
            000:01:024 Off ch=1 note=e1  vol=0
            000:01:024 On  ch=1 note=d1  vol=70
            000:01:096 Off ch=1 note=d1  vol=0
            000:01:096 On  ch=1 note=e1  vol=70
            001:00:000 Off ch=1 note=e1  vol=0
            001:00:000 Meta TrkEnd
            TrkEnd
            """)

    def tearDown(self):
        self.output.close()

    def encode(self, text):
        mus = self.parse(text)
        self.analizer.visit(mus)
        self.encoder.visit(mus)
        return self.output.getvalue()

    def no_ident(self, string):
        return re.sub(r'^\s+', '', string, flags=re.M)


    def test_simple_encoding(self):
        self.assertEqual(self.simple_def_encoded, self.encode(self.simple_def))

    def test_repetition(self):
        self.assertEqual(self.def_w_repeat_encoded, self.encode(self.def_w_repeat))

    def test_multiple_voices(self):
        self.assertEqual(self.def_w_many_voices_encoded, self.encode(self.def_w_many_voices))

    def test_misc_clicks(self):
        self.assertEqual(self.def_w_full_note_bar_encoded, self.encode(self.def_w_full_note_bar))


if __name__ == '__main__':
    unittest.main()
