class Expression(object):

	def evaluate(self):
		# Aca se implementa cada tipo de expresion.
		raise NotImplementedError


class Number(Expression):

	def __init__(self, value):
		self.value = value

	def evaluate(self):
		return self.value


class BinaryOperation(Expression):

	def __init__(self, left, right, operator):
		self.left = left
		self.right = right
		self.operator = operator

	def evaluate(self):
		left_evaluation = self.left.evaluate()
		right_evaluation = self.right.evaluate()
		return self.operator(left_evaluation, right_evaluation)
