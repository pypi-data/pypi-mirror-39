''' Stack. '''

__all__ = ['Stack']

''' Almost identical to python's list. '''
class Stack(list):

	def push(self, value):
		''' Add value to end of list. '''
		self.append(value)

	def pop(self):
		''' Return and delete the last value '''

		''' Raise EmptyStackError '''
		if len(self) == 0:
			raise EmptyStackError('pop from empty stack.')

		value = self[-1]
		del self[-1]
		return value

class EmptyStackError(IndexError):
	pass