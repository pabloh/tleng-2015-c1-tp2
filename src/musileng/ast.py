from fractions import Fraction

class Node:
    def __init__(self, *args, line=None, **kargs):
        self.lineno = line
        self.init_subnodes(*args, **kargs)

    def accept(self, visitor):
        getattr(visitor, 'visit_type_' + type(self).__name__)(self)

    def init_subnodes(self, *args, **kargs): pass

class MusiLengError(Exception):
    def __init__(self, node, detail):
        msg = "Ocurrió un error"
        if node.lineno:
            msg += " en la línea {}".format(node.lineno)
        super().__init__(msg + ": "+ detail)


class MusiLeng(Node):
    def init_subnodes(self, tempo_dir, bar_dir, consts, voices):
        if len(voices) > 16: raise TooManyVoices(voices[16])
        self.tempo, self.bar, self.consts, self.voices = tempo_dir, bar_dir, consts, voices

    def voices_number(self):
        return len(self.voices)

class TooManyVoices(MusiLengError):
    def __init__(self, node):
        super().__init__(node, 'no se pueden definir más de 16 voces')


class Literal(Node):
    def init_subnodes(self, number):
        self.number = number

    def value(self, symbol_table = {}):
        return self.number

class ConstRef(Node):
    def init_subnodes(self, identifier):
        self.identifier = identifier

    def value(self, symbol_table):
        return symbol_table.get(self.identifier)


class TempoDirective(Node):
    def init_subnodes(self, note_value, notes_per_min):
        if notes_per_min == 0: raise InvalidTempo(self)
        self.reference_note, self.notes_per_min = Duration(note_value), notes_per_min

    def microseconds_per_quarter_note(self):
        return int((1000000 * 60 * self.reference_note.note_value_number()) /
                   (4 * self.notes_per_min))

class BarDirective(Node):
    valid_note_values = [ 2**i for i in range(0,7) ]

    def init_subnodes(self, pulses, note_value_number):
        if pulses == 0: raise InvalidBarPulses(self)
        if not note_value_number in self.valid_note_values: raise InvalidBarBase(self)
        self.pulses, self.note_value_number = pulses, note_value_number

    def pulse_duration(self):
        return Duration.from_number(self.note_value_number)

    def fraction(self):
        return Fraction(self.pulses, self.note_value_number)

    def formated(self):
        return "%d/%d" % (self.pulses, self.note_value_number)

class InvalidTempo(MusiLengError):
    def __init__(self, node):
        super().__init__(node, 'la cantidad de notas por minuto en tempo no puede ser 0')

class InvalidBarPulses(MusiLengError):
    def __init__(self, node):
        super().__init__(node, 'la cantidad de pulsos por compás no puede ser 0')

class InvalidBarBase(MusiLengError):
    def __init__(self, node):
        super().__init__(node, 'número de figura inválido para el compás')


class ConstDecl(Node):
    def init_subnodes(self, identifier, number):
        self.identifier, self.number = identifier, number


class Note(Node):
    def init_subnodes(self, pitch, octave, duration):
        self.pitch, self.octave, self.duration = pitch, octave, duration

class Silence(Node):
    def init_subnodes(self, duration):
        self.duration = duration


class Duration(Node):
    numbers = {
        'redonda':      1,
        'blanca':       2,
        'negra':        4,
        'corchea':      8,
        'semicorchea':  16,
        'fusa' :        32,
        'semifusa':     64,
    }
    proportions = { name : Fraction(1, num) for name, num in numbers.items() }

    @classmethod
    def from_number(cls, number):
        for name, num in cls.numbers.items():
            if num == number: return Duration(name)

    def init_subnodes(self, note_value, dotted=False):
        self.note_value, self.dotted = note_value, dotted

    def note_value_number(self):
        return self.numbers[self.note_value]

    def fraction(self):
        return self.proportions[self.note_value] * self.dot_increase()

    def dot_increase(self):
        return Fraction(3,2) if self.dotted else 1

class Pitch(Node):
    american_codes = {'do' : 'c', 're' : 'd', 'mi' : 'e', 'fa' : 'f', 'sol' : 'g', 'la' : 'a', 'si' : 'b'}

    def init_subnodes(self, musical_note, modifier=None):
        self.musical_note, self.modifier = musical_note, modifier

    def american(self):
        return self.american_codes[self.musical_note] + (self.modifier if self.modifier else '')

class Voice(Node):
    def init_subnodes(self, instrument, childs):
        self.instrument, self.childs = instrument, childs

class Repeat(Node):
    def init_subnodes(self, times, childs):
        self.times, self.childs = times, childs

class Bar(Node):
    def init_subnodes(self, notes):
        self.notes = notes

    def duration(self):
        return sum(note.duration.fraction() for note in self.notes)
