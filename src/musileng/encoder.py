from musileng.ast import *
from musileng.visitor import *
from musileng.semantic_analysis import SemanticVisitor

class SMFEncoder(SemanticVisitor):
    default_volume = 70

    def __init__(self, output):
        self.output = output
        super().__init__()

    def visit_type_MusiLeng(self, node):
        self.visit(node.tempo)
        self.visit(node.bar)
        self.visit_all(node.consts)
        self.output_header_track(node.voices_number())

        for number, voice in enumerate(node.voices):
            self.current_track = number + 1
            self.visit(voice)

    def visit_type_TempoDirective(self, node):
        self.quarter_note_length = node.microseconds_per_quarter_note()

    def visit_type_BarDirective(self, node):
        self.setup_midi_timer(node.pulses, node.pulse_duration())
        self.formated_bar = node.formated()

    def visit_type_Voice(self, node):
        self.timer.reset()

        self.output_track_begin()
        self.output_timestamped_line('Meta TrkName "Voz {NUMERO_DE_VOZ}"', NUMERO_DE_VOZ=self.current_track)
        self.output_timestamped_line('ProgCh ch={CANAL} prog={INSTRUMENTO}', CANAL=self.current_track, INSTRUMENTO=self.value(node.instrument))

        self.visit_all(node.childs)

        self.output_timestamped_line('Meta TrkEnd')
        self.output_track_end()

    def visit_type_Repeat(self, node):
        for n in range(self.value(node.times)):
            self.visit_all(node.childs)

    def visit_type_Note(self, node):
        self.output_timestamped_line('On  ch={CANAL} note={NOTA} vol={VOL}', CANAL=self.current_track, NOTA=self.format_note(node), VOL=self.default_volume)
        self.timer.elapse_by(node.duration)
        self.output_timestamped_line('Off ch={CANAL} note={NOTA} vol={VOL}', CANAL=self.current_track, NOTA=self.format_note(node), VOL=0)

    def visit_type_Silence(self, node):
        self.timer.elapse_by(node.duration)


    def setup_midi_timer(self, pulses, pulse_duration):
        self.timer = MidiTimer(pulses, pulse_duration)

    def output_header_track(self, voices):
        self.output_line("MFile 1 {NTRACKS} 384", NTRACKS=voices + 1)
        self.output_track_begin()
        self.output_timestamped_line("TimeSig {COMPAS} 24 8", COMPAS=self.formated_bar)
        self.output_timestamped_line("Tempo {TEMPO}", TEMPO=self.quarter_note_length)
        self.output_timestamped_line("Meta TrkEnd")
        self.output_track_end()

    def output_track_begin(self):
        self.output_line("MTrk")

    def output_track_end(self):
        self.output_line("TrkEnd")

    def output_timestamped_line(self, string, **kargs):
        self.output_line(self.timer.formated() + ' ' + string, **kargs)

    def output_line(self, string, **kargs):
        self.output.write(string.format(**kargs))
        self.output.write("\n")

    def format_note(self, note):
        return (note.pitch.american() + str(self.value(note.octave))).ljust(3)

class MidiTimer:
    clicks_per_pulse = 384

    def __init__(self, pulses, pulse_duration):
        self.clicks_per_full_note = self.clicks_per_pulse * pulse_duration.note_value_number()
        self.bar_pulses = pulses
        self.reset()

    def reset(self):
        self.bar = self.pulse = self.clicks = 0

    def elapse_by(self, duration):
        pulses, self.clicks = divmod(self.clicks + self.clicks_per_full_note * duration.fraction(), self.clicks_per_pulse)
        bars, self.pulse = divmod(self.pulse + pulses, self.bar_pulses)
        self.bar += bars

    def formated(self):
        return "%03d:%02d:%03d" % (self.bar, self.pulse, self.clicks)

class Track10MustBeAPercussionInstrument(Exception):
    def __init__(self, instrument):
        super().__init__("El instrumento número {} asignado al track 10 no es de percusión según la especificación MIDI".format(instrument))
