import re

keywords = {
    'tempo'    : 'TEMPO',
    'compas'   : 'COMPAS',
    'const'    : 'CONST',
    'voz'      : 'VOZ',
    'repetir'  : 'REPETIR',
    'nota'     : 'NOTA',
    'silencio' : 'SILENCIO',
}

musical_notes = ['do', 're', 'mi', 'fa', 'sol', 'la', 'si']
note_values = ['redonda', 'blanca', 'negra', 'corchea', 'semicorchea', 'fusa', 'semifusa']


tokens = (
    # Operators
    'HASH',
    'EQUALS',
    'SLASH',
    'POINT',
    'PLUS',
    'MINUS',

    # Delimiters
    'SEMICOLON',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',

    # Misc
    'MUSICAL_NOTE',
    'NOTE_VALUE',
    'NUMBER',
    'ID',
) + tuple(keywords.values())


def t_NUMBER(token):
    r'[0-9]+'
    token.value = int(token.value)
    return token

def t_ID(token):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    if token.value in keywords:   # Check for keywords
        token.type = keywords.get(token.value)
    elif token.value in musical_notes:
        token.type = 'MUSICAL_NOTE'
    elif token.value in note_values:
        token.type = 'NOTE_VALUE'
    else:
        token.type = 'ID'

    return token


t_HASH   = r'\#'
t_EQUALS = r'='
t_SLASH  = r'/'
t_POINT  = r'\.'
t_PLUS   = r'\+'
t_MINUS  = r'\-'

t_SEMICOLON = r';'
t_COMMA  = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'


t_ignore = " \t"

def t_COMMENT(token):
    r'//[^\n]*\n'
    token.lexer.lineno += 1

def t_NEWLINE(token):
    r'\n+'
    token.lexer.lineno += len(token.value)


def t_error(token):
    message = "[Error de Sintaxis] Token desconocido "
    message += re.sub(r'\s+.*', '', str(token.value))
    message += " en linea " + str(token.lineno)
    raise SyntaxError(message)
