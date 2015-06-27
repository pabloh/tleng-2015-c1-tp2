from fractions import Fraction

class Node:
    def accept(self, visitor):
        getattr(visitor, 'visit_type_' + type(self).__name__)(self)

class MusiLeng(Node):
    def __init__(self, tempo_dir, bar_dir, consts, voices):
        self.tempo, self.bar, self.consts, self.voices = tempo_dir, bar_dir, consts, voices

    def symbol_table(self):
        return { const.identifier : const.number for const in self.consts }

    def build_midi(self):
        pass


class Literal(Node):
    def __init__(self, number):
        self.number = number

    def value(self, symbol_table = {}):
        return self.number

class ConstRef(Node):
    def __init__(self, identifier):
        self.identifier = identifier

    def value(self, symbol_table):
        return symbol_table.get(self.identifier)


class TempoDirective(Node):
    def __init__(self, note_value, notes_per_min):
        self.reference_note, self.notes_per_min = Duration(note_value), notes_per_min

class BarDirective(Node):
    def __init__(self, pulses, note_value):
        self.pulses, self.note_value = pulses, note_value

    def fraction(self):
        return Fraction(self.pulses, self.note_value)

class ConstDecl(Node):
    def __init__(self, identifier, number):
        self.identifier, self.number = identifier, number


class Note(Node):
    def __init__(self, pitch, octave, duration):
        self.pitch, self.octave, self.duration = pitch, octave, duration

    def __eq__(self, other):
        return (isinstance(other, Note) and self.pitch == other.pitch and self.octave == other.octave and self.duration == other.duration)

class Silence(Node):
    def __init__(self, duration):
        self.duration = duration

    def __eq__(self, other):
        return (isinstance(other, Silence) and self.duration == other.duration)


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

class Voice(Container):
    def __init__(self, instrument, bars):
        super().__init__(bars)
        self.instrument, self.bars = instrument, bars

class Repeat(Container):
    def __init__(self, times, childs):
        super().__init__(childs)
        self.times = times

class Bar(Container):
    def __init__(self, notes):
        super().__init__(notes)
        self.notes = notes
