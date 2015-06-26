from fractions import Fraction


class Node:
    def check_symbols(self, table): pass

class MusiLeng(Node):
    def __init__(self, tempo_dir, bar_dir, consts, voices):
        self.tempo = tempo_dir
        self.bar = bar_dir
        self.consts = consts
        self.voices = voices

    def semantically_analize(self):
        self.check_symbols()

    def check_symbols(self):
        for voice in self.voices:
            voice.check_symbols(self.consts)

    def build_midi(self):
        pass


class Number(Node):
    def __init__(self, literal):
        self.literal = literal

    def value(self, symbol_table = {}):
        return self.literal

class Const(Node):
    def __init__(self, identifier):
        self.identifier = identifier

    def value(self, symbol_table):
        return symbol_table.get(self.identifier)

    def check_symbols(self, table):
        if not self.identifier in table:
            raise UndeclaredSymbol(self.identifier)


class TempoDirective(Node):
    def __init__(self, note_value, notes_per_min):
        self.reference_note, self.notes_per_min = Duration(note_value), notes_per_min

class BarDirective(Node):
    def __init__(self, pulses, note_value):
        self.pulses, self.note_value = pulses, note_value

    def fraction(self):
        return Fraction(self.pulses, self.note_value)


class Note(Node):
    def __init__(self, pitch, octave, duration):
        self.pitch, self.octave, self.duration = pitch, octave, duration

    def __eq__(self, other):
        return (isinstance(other, Note) and self.pitch == other.pitch and self.octave == other.octave and self.duration == other.duration)

    def check_symbols(self, symbol_table):
        self.octave.check_symbols(symbol_table)

class Silence(Node):
    def __init__(self, duration):
        self.duration = duration


class Duration(Node):
    def __init__(self, note_value, dotted=False):
        self.note_value, self.dotted = note_value, dotted

    def __eq__(self, other):
        return (isinstance(other, Duration) and self.note_value == other.note_value and self.dotted == other.dotted)

class Pitch(Node):
    def __init__(self, musical_note, modifier=None):
        self.musical_note, self.modifier = musical_note, modifier

    def __eq__(self, other):
        return (isinstance(other, Pitch) and self.musical_note == other.musical_note and self.modifier == other.modifier)


class Container(Node):
    def __init__(self, childs):
        self.childs = childs

    def check_symbols(self, symbol_table):
        for child in self.childs:
            child.check_symbols(symbol_table)

class Voice(Container):
    def __init__(self, instrument, bars):
        super().__init__(bars)
        self.instrument, self.bars = instrument, bars

    def check_symbols(self, symbol_table):
        self.instrument.check_symbols(symbol_table)
        super().check_symbols(symbol_table)

class Repeat(Container):
    def __init__(self, times, childs):
        super().__init__(childs)
        self.times = times

    def check_symbols(self, symbol_table):
        self.times.check_symbols(symbol_table)
        super().check_symbols(symbol_table)

class Bar(Container):
    def __init__(self, notes):
        super().__init__(notes)
        self.notes = notes


class UndeclaredSymbol(Exception):
    def __init__(self, name):
        self.msg = "Identificador '{}' no declarado previamente".format(name)
