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
            00:00:000 TimeSig 2/4 24 8
            00:00:000 Tempo 1000000
            00:00:000 Meta TrkEnd
            TrkEnd
            MTrk
            00:00:000 Meta TrkName "Voz 1"
            00:00:000 ProgCh ch=1 prog=3
            00:00:000 On  ch=1 note=c1  vol=70
            01:00:000 Off ch=1 note=c1  vol=0
            01:00:000 Meta TrkEnd
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
            00:00:000 TimeSig 2/4 24 8
            00:00:000 Tempo 1000000
            00:00:000 Meta TrkEnd
            TrkEnd
            MTrk
            00:00:000 Meta TrkName "Voz 1"
            00:00:000 ProgCh ch=1 prog=23
            00:00:000 On  ch=1 note=c+1 vol=70
            00:01:000 Off ch=1 note=c+1 vol=0
            00:01:000 On  ch=1 note=d2  vol=70
            01:00:000 Off ch=1 note=d2  vol=0
            01:00:000 On  ch=1 note=f1  vol=70
            01:00:288 Off ch=1 note=f1  vol=0
            01:00:288 On  ch=1 note=g-2 vol=70
            01:01:000 Off ch=1 note=g-2 vol=0
            01:01:000 On  ch=1 note=a2  vol=70
            02:00:000 Off ch=1 note=a2  vol=0
            02:00:000 On  ch=1 note=f1  vol=70
            02:00:288 Off ch=1 note=f1  vol=0
            02:00:288 On  ch=1 note=g-2 vol=70
            02:01:000 Off ch=1 note=g-2 vol=0
            02:01:000 On  ch=1 note=a2  vol=70
            03:00:000 Off ch=1 note=a2  vol=0
            03:00:000 Meta TrkEnd
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
            00:00:000 TimeSig 3/4 24 8
            00:00:000 Tempo 600000
            00:00:000 Meta TrkEnd
            TrkEnd
            MTrk
            00:00:000 Meta TrkName "Voz 1"
            00:00:000 ProgCh ch=1 prog=23
            00:01:000 On  ch=1 note=e2  vol=70
            01:00:000 Off ch=1 note=e2  vol=0
            01:00:000 On  ch=1 note=d1  vol=70
            01:02:000 Off ch=1 note=d1  vol=0
            01:02:000 On  ch=1 note=c1  vol=70
            02:00:000 Off ch=1 note=c1  vol=0
            02:00:000 Meta TrkEnd
            TrkEnd
            MTrk
            00:00:000 Meta TrkName "Voz 2"
            00:00:000 ProgCh ch=2 prog=23
            00:00:000 On  ch=2 note=c1  vol=70
            00:00:192 Off ch=2 note=c1  vol=0
            00:00:192 On  ch=2 note=e2  vol=70
            00:02:192 Off ch=2 note=e2  vol=0
            00:02:192 On  ch=2 note=b1  vol=70
            01:00:000 Off ch=2 note=b1  vol=0
            01:00:000 On  ch=2 note=c1  vol=70
            01:00:192 Off ch=2 note=c1  vol=0
            01:00:192 On  ch=2 note=e2  vol=70
            01:02:192 Off ch=2 note=e2  vol=0
            01:02:192 On  ch=2 note=b1  vol=70
            02:00:000 Off ch=2 note=b1  vol=0
            02:00:000 Meta TrkEnd
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


if __name__ == '__main__':
    unittest.main()
