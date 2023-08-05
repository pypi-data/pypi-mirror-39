''' The pointer class. '''

__all__ = ['Pointer']

class Pointer:

	def __init__(self, value = None):
		self.value = value

	def __call__(self, *args):
		''' Get or set the value. '''
		if len(args) == 0:
			return self.value
		self.value = args[0]

	def __repr__(self):
		return str(self.value)

	def __str__(self):
		return str(self.value)