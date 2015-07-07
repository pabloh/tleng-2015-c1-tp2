from musileng.ast import *
from musileng.visitor import *

class SemanticVisitor(Visitor):
    def __init__(self):
        self.symbol_table = {}

    def visit_type_ConstDecl(self, node):
        self.symbol_table[node.identifier] = node.number

    def value(self, numeric_node):
        return numeric_node.value(self.symbol_table)


class MusiLengSemanticAnalizer(SemanticVisitor):
    def visit_type_BarDirective(self, node):
        self.bar_duration = node.fraction()

    def visit_type_ConstDecl(self, node):
        if node.identifier in self.symbol_table:
            raise RedeclaredSymbol(node)
        else:
            super().visit_type_ConstDecl(node)

    def visit_type_ConstRef(self, node):
        if not node.identifier in self.symbol_table:
            raise UndeclaredSymbol(node)

    def visit_type_Voice(self, node):
        super().visit_type_Voice(node)
        instrument = self.value(node.instrument)
        if not 0 <= instrument <= 127: raise InvalidInstrument(node.instrument, instrument)

    def visit_type_Repeat(self, node):
        super().visit_type_Repeat(node)
        if self.value(node.times) == 0: raise InvalidRepeatNumber(node.times)

    def visit_type_Bar(self, node):
        super().visit_type_Bar(node)
        if node.duration() != self.bar_duration:
            raise InvalidBarDuration(node, self.bar_duration, node.duration())

    def visit_type_Note(self, node):
        super().visit_type_Note(node)
        octave = self.value(node.octave)
        if not 1 <= octave <= 9: raise InvalidOctave(node.octave, octave)


class RedeclaredSymbol(MusiLengError):
    def __init__(self, node):
        super().__init__(node, "'{}' ya fue declarado previamente".format(node.identifier))

class UndeclaredSymbol(MusiLengError):
    def __init__(self, node):
        super().__init__(node, "'{}' no fue declarado".format(node.identifier))

class InvalidRepeatNumber(MusiLengError):
    def __init__(self, node):
        super().__init__(node, "no es válida una repetición de 0 iteraciones")


class InvalidOctave(MusiLengError):
    def __init__(self, node, number):
        super().__init__(node, "'{}' no es una octava válida".format(number))

class InvalidInstrument(MusiLengError):
    def __init__(self, node, number):
        super().__init__(node, "'{}' no es un instrumento válido".format(number))

class InvalidBarDuration(MusiLengError):
    def __init__(self, node, midi_bar, invalid_bar):
        super().__init__(node, "compás de '{invalid}' declarado pero el configurado era de {bar}".format(bar=midi_bar, invalid=invalid_bar))
