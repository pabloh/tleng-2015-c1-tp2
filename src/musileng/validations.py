from musileng.ast import *
from musileng.visitor import *

class ValidateSymbolsReference(Visitor):
    def visit_type_MusiLeng(self, node):
        self.symbol_table = node.consts
        super().visit_type_MusiLeng(node)

    def visit_type_Const(self, node):
        if not node.identifier in self.symbol_table:
            raise UndeclaredSymbol(node.identifier)

class UndeclaredSymbol(Exception):
    def __init__(self, name):
        self.msg = "Identificador '{}' no declarado previamente".format(name)
