from lexer_rules import tokens
from operator import add, mul
from expressions import BinaryOperation, Number


def p_expression_plus(subexpressions):
    'expression : expression PLUS term'
    subexpressions[0] = BinaryOperation(subexpressions[1], subexpressions[3], add)


def p_expression_term(subexpressions):
    'expression : term'
    subexpressions[0] = subexpressions[1]


def p_term_times(subexpressions):
    'term : term TIMES factor'
    subexpressions[0] = BinaryOperation(subexpressions[1], subexpressions[3], mul)


def p_term_factor(subexpressions):
    'term : factor'
    subexpressions[0] = subexpressions[1]


def p_factor_number(subexpressions):
    'factor : NUMBER'
    subexpressions[0] = Number(subexpressions[1])


def p_factor_expression(subexpressions):
    'factor : LPAREN expression RPAREN'
    subexpressions[0] = subexpressions[2]


def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
