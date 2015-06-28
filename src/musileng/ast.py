from fractions import Fraction

class Node:
    def accept(self, visitor):
        getattr(visitor, 'visit_type_' + type(self).__name__)(self)

class MusiLeng(Node):
    def __init__(self, tempo_dir, bar_dir, consts, voices):
        if len(voices) > 16: raise TooManyVoices
        self.tempo, self.bar, self.consts, self.voices = tempo_dir, bar_dir, consts, voices

    def voices_number(self):
        return len(self.voices)

class TooManyVoices(Exception): pass


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
        if notes_per_min == 0: raise InvalidTempo
        self.reference_note, self.notes_per_min = Duration(note_value), notes_per_min

class BarDirective(Node):
    valid_note_values = [ 2**i for i in range(0,7) ]

    def __init__(self, pulses, note_value):
        if pulses == 0: raise InvalidBarPulses
        if not note_value in self.valid_note_values: raise InvalidBarBase
        self.pulses, self.note_value = pulses, note_value

    def fraction(self):
        return Fraction(self.pulses, self.note_value)

class InvalidTempo(Exception): pass
class InvalidBarPulses(Exception): pass
class InvalidBarBase(Exception): pass


class ConstDecl(Node):
    def __init__(self, identifier, number):
        self.identifier, self.number = identifier, number


class Note(Node):
    def __init__(self, pitch, octave, duration):
        self.pitch, self.octave, self.duration = pitch, octave, duration

class Silence(Node):
    def __init__(self, duration):
        self.duration = duration


class Duration(Node):
    proportions = {
        'redonda':      Fraction(1, 1),
        'blanca':       Fraction(1, 2),
        'negra':        Fraction(1, 4),
        'corchea':      Fraction(1, 8),
        'semicorchea':  Fraction(1, 16),
        'fusa' :        Fraction(1, 32),
        'semifusa':     Fraction(1, 64),
    }

    def __init__(self, note_value, dotted=False):
        self.note_value, self.dotted = note_value, dotted

    def fraction(self):
        return self.proportions[self.note_value] * self.dot_increase()

    def dot_increase(self):
        return Fraction(3,2) if self.dotted else 1

class Pitch(Node):
    def __init__(self, musical_note, modifier=None):
        self.musical_note, self.modifier = musical_note, modifier


class Container(Node):
    def __init__(self, childs):
        self.childs = childs

class Voice(Container):
    def __init__(self, instrument, childs):
        super().__init__(childs)
        self.instrument = instrument

class Repeat(Container):
    def __init__(self, times, childs):
        super().__init__(childs)
        self.times = times

class Bar(Container):
    def __init__(self, notes):
        super().__init__(notes)
        self.notes = notes

    def duration(self):
        return sum(note.duration.fraction() for note in self.notes)
