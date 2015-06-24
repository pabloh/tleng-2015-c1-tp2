from fractions import Fraction


class MusiLeng:
    def __init__(self, tempo_dir, bar_dir, consts, voices):
        self.tempo = tempo_dir
        self.bar = bar_dir
        self.consts = consts
        self.voices = voices

    def semantically_analize(self):
        self.check_symbol_use()

    def build_midi(self):
        pass


class Number:
    def __init__(self, value):
        self.value = value

    def value_for(self, symbol_table):
        return self.value

class Const:
    def __init__(self, name):
        self.name = name

    def value_for(self, symbol_table):
        return symbol_table.get(self.name)


class TempoDirective:
    def __init__(self, note_value, notes_per_min):
        self.reference_note, self.notes_per_min = Duration(note_value), notes_per_min

class BarDirective:
    def __init__(self, pulses, note_value):
        self.pulses, self.note_value = pulses, note_value

    def fraction(self):
        return Fraction(self.pulses, self.note_value)


class Note:
    def __init__(self, pitch, octave, duration):
        self.pitch, self.octave, self.duration = pitch, octave, duration

    def __eq__(self, other):
        return (self.pitch == other.pitch and self.octave == other.octave and self.duration == other.duration)

class Silence:
    def __init__(self, duration):
        self.duration = duration


class Duration:
    def __init__(self, note_value, dotted=False):
        self.note_value, self.dotted = note_value, dotted

    def __eq__(self, other):
        return (self.note_value == other.note_value and self.dotted == other.dotted)

class Pitch:
    def __init__(self, musical_note, modifier=None):
        self.musical_note, self.modifier = musical_note, modifier

    def __eq__(self, other):
        return (self.musical_note == other.musical_note and self.modifier == other.modifier)


class Bar:
    def __init__(self, notes):
        self.notes = notes

class Voice:
    def __init__(self, instrument, bars):
        self.instrument, self.bars = instrument, bars

class Repeat:
    def __init__(self, number, childs):
        self.number, self.childs = number, childs
