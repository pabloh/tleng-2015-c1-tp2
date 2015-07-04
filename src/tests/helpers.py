import unittest
import musileng.parser
import musileng.lexer
from musileng.ast import *
from musileng.semantic_analysis import *
from musileng.encoder import *
from ply import lex, yacc

class TestMusilengBase(unittest.TestCase):
    lexer = lex.lex(module=musileng.lexer)
    parser = yacc.yacc(module=musileng.parser)

    def setUp(self):
        self.lexer = type(self).lexer.clone()
        self.analizer = MusiLengSemanticAnalizer()

        self.simple_header = """
            #tempo negra 60
            #compas 2/4
        """

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
                    nota(do, octava1, negra);
                    nota(do, 2, negra);
                }
            }
        """

    def parse(self, text):
        return self.parser.parse(text, self.lexer)

    def symbol_table(self, mus):
        self.analizer.visit(mus)
        return self.analizer.symbol_table
    pass
