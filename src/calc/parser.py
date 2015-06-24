import lexer_rules
import parser_rules

from sys import argv, exit

from ply.lex import lex
from ply.yacc import yacc


if __name__ == "__main__":
    if len(argv) != 2:
        print("Invalid arguments.")
        print("Use:")
        print("  parser.py expression")
        exit()

    text = argv[1]

    lexer = lex(module=lexer_rules)
    parser = yacc(module=parser_rules)

    expression = parser.parse(text, lexer)

    result = expression.evaluate()
    print(result)
