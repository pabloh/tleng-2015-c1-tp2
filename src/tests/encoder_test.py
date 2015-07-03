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

        self.simple_def_w_repeat = """
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

        self.simple_def_w_repeat_encoded = self.no_ident("""
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

    def tearDown(self):
        self.output.close()

    def encode(self, text):
        mus = self.parse(text)
        self.encoder.visit(mus)
        return self.output.getvalue()

    def no_ident(self, string):
        return re.sub(r'^\s+', '', string, flags=re.M)


    def test_simple_encoding(self):
        self.assertEqual(self.simple_def_encoded, self.encode(self.simple_def))

    def test_repetition(self):
        self.assertEqual(self.simple_def_w_repeat_encoded, self.encode(self.simple_def_w_repeat))


if __name__ == '__main__':
    unittest.main()
