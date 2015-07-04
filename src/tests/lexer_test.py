import unittest
import musileng.lexer
from ply import lex

class TestMusilengLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = lex.lex(module=musileng.lexer)

    # Test it output
    def tokens(self, data):
        self.lexer.input(data)
        res = []

        while True:
             tok = self.lexer.token()
             if not tok:
                 break
             res.append((tok.type, tok.value))
        return res

    def assertTokens(self, data, tokens):
        self.assertEqual(tokens, self.tokens(data))

    def test_keywords(self):
        self.assertTokens('tempo const voz repetir nota silencio', [('TEMPO', 'tempo'), ('CONST', 'const'), ('VOZ', 'voz'), ('REPETIR', 'repetir'), ('NOTA', 'nota'), ('SILENCIO', 'silencio')])

    def test_invalid_token(self):
        with self.assertRaises(SyntaxError):
            self.tokens('compas []')

    def test_directives(self):
        self.assertTokens('#tempo redonda 60', [('HASH', '#'), ('TEMPO', 'tempo'), ('NOTE_VALUE', 'redonda'), ('NUMBER', 60)])
        self.assertTokens('#compas 3/4', [('HASH', '#'), ('COMPAS', 'compas'), ('NUMBER', 3), ('SLASH', '/'), ('NUMBER', 4)])
        self.assertTokens('#compas 1 / 8', [('HASH', '#'), ('COMPAS', 'compas'), ('NUMBER', 1), ('SLASH', '/'), ('NUMBER', 8)])


    def test_const_declaration(self):
        self.assertTokens('const oct = 5;', [('CONST', 'const'), ('ID', 'oct'), ('EQUALS', '='), ('NUMBER', 5), ('SEMICOLON', ';')])

    def test_ignored_chars(self):
        self.assertTokens('\tconst  octava=8 ;', [('CONST', 'const'), ('ID', 'octava'), ('EQUALS', '='), ('NUMBER', 8), ('SEMICOLON', ';')])

    def test_comments(self):
        notas = """
            nota(sol, 5, blanca);
            // Este es un comentario entre las dos notas
            nota(la, 5, negra); // Este tambien vale
        """

        self.assertTokens(notas, [('NOTA', 'nota'), ('LPAREN', '('), ('MUSICAL_NOTE', 'sol'), ('COMMA', ','), ('NUMBER', 5), ('COMMA', ','), ('NOTE_VALUE', 'blanca'), ('RPAREN', ')'), ('SEMICOLON', ';'),
            ('NOTA', 'nota'), ('LPAREN', '('), ('MUSICAL_NOTE', 'la'), ('COMMA', ','), ('NUMBER', 5), ('COMMA', ','), ('NOTE_VALUE', 'negra'), ('RPAREN', ')'), ('SEMICOLON', ';')])

    def test_compas_and_notas(self):
        notas = """
            compas
            {
                nota(sol-, octava, fusa);
                silencio(corchea.);
                nota(sol+ , octava, semifusa );
            }
        """
        self.assertTokens(notas, [('COMPAS', 'compas'), ('LBRACKET','{'),
            ('NOTA', 'nota'), ('LPAREN', '('), ('MUSICAL_NOTE', 'sol'), ('MINUS', '-'), ('COMMA', ','), ('ID', 'octava'), ('COMMA', ','), ('NOTE_VALUE', 'fusa'), ('RPAREN', ')'), ('SEMICOLON', ';'),
            ('SILENCIO', 'silencio'), ('LPAREN', '('), ('NOTE_VALUE', 'corchea'), ('POINT', '.'), ('RPAREN', ')'), ('SEMICOLON', ';'),
            ('NOTA', 'nota'), ('LPAREN', '('), ('MUSICAL_NOTE', 'sol'), ('PLUS', '+'), ('COMMA', ','), ('ID', 'octava'), ('COMMA', ','), ('NOTE_VALUE', 'semifusa'), ('RPAREN', ')'), ('SEMICOLON', ';'),
            ('RBRACKET','}')])


if __name__ == '__main__':
    unittest.main()
