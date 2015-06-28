from musileng.ast import *
from musileng.visitor import *

class SemanticVisitor(Visitor):
    def visit_type_MusiLeng(self, node):
        self.symbol_table = {}
        super().visit_type_MusiLeng(node)

    def visit_type_ConstDecl(self, node):
        self.symbol_table[node.identifier] = node.number

    def value(self, numeric_node):
        return numeric_node.value(self.symbol_table)


class MusiLengSemanticAnalizer(SemanticVisitor):
    def visit_type_BarDirective(self, node):
        self.bar_duration = node.fraction()

    def visit_type_ConstDecl(self, node):
        if node.identifier in self.symbol_table:
            raise RedeclaredSymbol(node.identifier)
        else:
            super().visit_type_ConstDecl(node)

    def visit_type_ConstRef(self, node):
        if not node.identifier in self.symbol_table:
            raise UndeclaredSymbol(node.identifier)

    def visit_type_Voice(self, node):
        super().visit_type_Voice(node)
        instrument = self.value(node.instrument)
        if not 0 <= instrument <= 127: raise InvalidInstrument(instrument)

    def visit_type_Repeat(self, node):
        super().visit_type_Repeat(node)
        if self.value(node.times) == 0: raise InvalidRepeatNumber

    def visit_type_Bar(self, node):
        super().visit_type_Bar(node)
        if node.duration() != self.bar_duration:
            raise InvalidBarDuration(self.bar_duration, node.duration())

    def visit_type_Note(self, node):
        super().visit_type_Note(node)
        octave = self.value(node.octave)
        if not 1 <= octave <= 9: raise InvalidOctave(octave)


class RedeclaredSymbol(Exception):
    def __init__(self, name):
        super().__init__("'{}' ya fue declarado previamente".format(name))

class UndeclaredSymbol(Exception):
    def __init__(self, name):
        super().__init__("'{}' no fue declarado".format(name))

class InvalidRepeatNumber(Exception): pass

class InvalidOctave(Exception):
    def __init__(self, number):
        super().__init__("'{}' no es una octava válida".format(number))

class InvalidInstrument(Exception):
    def __init__(self, number):
        super().__init__("'{}' no es un instrumento válido".format(number))

class InvalidBarDuration(Exception):
    def __init__(self, midi_bar, invalid_bar):
        super().__init__("compás de {invalid}' declarado pero el configurado era de {bar}".format(bar=midi_bar, invalid=invalid_bar))
