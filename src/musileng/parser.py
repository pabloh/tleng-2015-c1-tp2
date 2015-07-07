from musileng.lexer import tokens
from musileng.ast import *


def p_musileng(subs):
    'musileng : tempo_directive compas_directive constants voices'
    subs[0] = MusiLeng(*subs[1:5])


def p_tempo_directive(subs):
    'tempo_directive : HASH TEMPO NOTE_VALUE NUMBER'
    subs[0] = TempoDirective(subs[3], subs[4], line=subs.lineno(1))

def p_compas_directive(subs):
    'compas_directive : HASH COMPAS NUMBER SLASH NUMBER'
    subs[0] = BarDirective(subs[3], subs[5], line=subs.lineno(1))


def p_constants(subs):
    """constants : constant constants
                 | """
    subs[0] = [subs[1]] + subs[2] if len(subs) == 3 else []

def p_constant(subs):
    'constant : CONST ID EQUALS NUMBER SEMICOLON'
    subs[0] = ConstDecl(subs[2], subs[4], line=subs.lineno(1))


def p_voices(subs):
    '''voices : voice voices
              | voice'''
    subs[0] = [subs[1]] + (subs[2] if len(subs) == 3 else [])


def p_voice(subs):
    'voice : VOZ LPAREN numeric_value RPAREN LBRACKET voice_content RBRACKET'
    subs[0] = Voice(subs[3], subs[6], line=subs.lineno(1))

def p_voice_content(subs):
    '''voice_content : compas voice_content
                     | repetition voice_content
                     | compas
                     | repetition'''
    subs[0] = [subs[1]] + (subs[2] if len(subs) == 3 else [])


def p_compas(subs):
    'compas : COMPAS LBRACKET compas_content RBRACKET'
    subs[0] = Bar(subs[3], line=subs.lineno(1))


def p_compas_content(subs):
    '''compas_content : note compas_content
                      | silence compas_content
                      | note
                      | silence'''
    subs[0] = [subs[1]] + (subs[2] if len(subs) == 3 else [])

def p_note(subs):
    'note : NOTA LPAREN pitch COMMA numeric_value COMMA duration RPAREN SEMICOLON'
    subs[0] = Note(subs[3], subs[5], subs[7], line=subs.lineno(1))

def p_silence(subs):
    'silence : SILENCIO LPAREN duration RPAREN SEMICOLON'
    subs[0] = Silence(subs[3], line=subs.lineno(1))


def p_repetition(subs):
    'repetition : REPETIR LPAREN numeric_value RPAREN LBRACKET voice_content RBRACKET'
    subs[0] = Repeat(subs[3], subs[6], line=subs.lineno(1))


def p_numeric_value(subs):
    '''numeric_value : NUMBER
                     | ID'''
    if type(subs[1]) == int:
        subs[0] = Literal(subs[1], line=subs.lineno(1))
    else:
        subs[0] = ConstRef(subs[1], line=subs.lineno(1))

def p_duration(subs):
    '''duration : NOTE_VALUE
                | NOTE_VALUE POINT'''
    subs[0] = Duration(subs[1], len(subs) == 3, line=subs.lineno(1))


def p_pitch(subs):
    '''pitch : MUSICAL_NOTE
             | MUSICAL_NOTE PLUS
             | MUSICAL_NOTE MINUS'''
    if len(subs) == 3:
        subs[0] = Pitch(subs[1], subs[2], line=subs.lineno(1))
    else:
        subs[0] = Pitch(subs[1], line=subs.lineno(1))


def p_error(token):
    message = "[Error de Sintaxis]"
    if token is not None:
        message += " token " + str(token.value)
        message += " inesperado en línea " + str(token.lineno)
    else:
        message += " fin de archivo inesperado"
    raise SyntaxError(message)
