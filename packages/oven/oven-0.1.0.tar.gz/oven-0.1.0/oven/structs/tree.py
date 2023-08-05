''' Tree. '''

__all__ = ['Tree']

from .stack import Stack
from .queue import Queue

class Tree:
	''' A node of the actual tree. '''
	
	def __init__(self, value = None):
		self.value = value
		self.children = []

	def addChild(self, value):
		if type(value) != Tree:
			raise TypeError('children of Tree must be Tree')

		self.children.append(value)

	def dfs(self) -> list:
		''' Return a list containing the tree in dfs order. '''

		out = []

		''' Circumventing StackOverflowError '''
		buffer = Stack()
		buffer.push(self)

		''' Iterate through the tree. '''
		while len(buffer) > 0:
			next = buffer.pop()
			out.append(next)

			''' Get children from left to right. '''
			for i in reversed(next.children):
				buffer.push(i)

		return out

	def bfs(self) -> list:
		''' Return a list containing the tree in bfs order. '''

		out = []

		buffer = Queue()
		buffer.push(self)

		''' Iterate through the tree. '''
		while len(buffer) > 0:
			next = buffer.pop()
			out.append(next)

			for i in next.children:

				''' Setting up for BinaryTree. '''
				if i == None:
					continue

				buffer.push(i)

		return out

	def __str__(self):
		return 'Tree(value: %s, %d children)'%(self.value, len(self.children))

	def __repr__(self):
		return 'Tree(value: %s, %d children)'%(self.value, len(self.children))