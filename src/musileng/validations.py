from musileng.ast import *
from musileng.visitor import *

class ValidateSymbolsReference(Visitor):
    def visit_type_MusiLeng(self, node):
        self.symbol_table = {}
        super().visit_type_MusiLeng(node)

    def visit_type_ConstDecl(self, node):
        if node.identifier in self.symbol_table:
            raise RedeclaredSymbol(node.identifier)
        else:
            self.symbol_table[node.identifier] = node.number

    def visit_type_ConstRef(self, node):
        if not node.identifier in self.symbol_table:
            raise UndeclaredSymbol(node.identifier)

class RedeclaredSymbol(Exception):
    def __init__(self, name):
        super().__init__("'{}' ya fue declarado previamente".format(name))

class UndeclaredSymbol(Exception):
    def __init__(self, name):
        super().__init__("'{}' no fue declarado".format(name))
