from argparse import ArgumentParser
from ply import lex, yacc

import musileng.parser
import musileng.lexer
from musileng.ast import MusiLengError
from musileng.semantic_analysis import MusiLengSemanticAnalizer
from musileng.encoder import SMFEncoder


if __name__ == "__main__":
    cli_parser = ArgumentParser(description='Generador de archivos SMF')
    cli_parser.add_argument('entrada', help='nombre del archivo fuente')
    cli_parser.add_argument('salida', help='nombre del archivo generado')
    args = cli_parser.parse_args()

    try:
        with open(args.entrada, 'r') as src:
            lexer = lex.lex(module=musileng.lexer)
            parser = yacc.yacc(module=musileng.parser)
            analizer = MusiLengSemanticAnalizer()

            mus = parser.parse(src.read(), lexer)
            analizer.visit(mus)

            with open(args.salida, "w") as dest:
                encoder = SMFEncoder(dest)
                encoder.visit(mus)
    except FileNotFoundError as ioe:
        exit('No se pudo acceder al archivo: ' + ioe.filename)
    except MusiLengError as me:
        exit(me.msg)
