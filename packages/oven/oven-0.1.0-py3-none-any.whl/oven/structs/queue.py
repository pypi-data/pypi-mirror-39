''' Queue. '''

__all__ = ['Queue']

''' Almost identical to python's list. '''
class Queue(list):

	def push(self, value):
		''' Add value to end of list. '''
		self.append(value)

	def pop(self):
		''' Return and delete the last value '''

		''' Raise EmptyStackError '''
		if len(self) == 0:
			raise EmptyQueueError('pop from empty queue.')

		value = self[0]
		del self[0]
		return value

class EmptyQueueError(IndexError):
	pass