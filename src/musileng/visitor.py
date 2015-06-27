from musileng.ast import *

class Visitor:
    def visit(self, node):
        node.accept(self)

    def visit_all(self, nodes):
        for node in nodes:
            self.visit(node)

    def visit_type_MusiLeng(self, node):
        self.visit(node.tempo)
        self.visit(node.bar)
        self.visit_all(node.consts)
        self.visit_all(node.voices)

    def visit_type_TempoDirective(self, node): pass

    def visit_type_BarDirective(self, node): pass

    def visit_type_ConstDecl(self, node): pass

    def visit_type_Voice(self, node):
        self.visit(node.instrument)
        self.visit_all(node.childs)

    def visit_type_Repeat(self, node):
        self.visit(node.times)
        self.visit_all(node.childs)

    def visit_type_Bar(self, node):
        self.visit_all(node.childs)

    def visit_type_Note(self, node):
        self.visit(node.pitch)
        self.visit(node.octave)
        self.visit(node.duration)

    def visit_type_Silence(self, node):
        self.visit(node.duration)

    def visit_type_Duration(self, node): pass

    def visit_type_Pitch(self, node): pass

    def visit_type_Literal(self, node): pass

    def visit_type_ConstRef(self, node): pass
