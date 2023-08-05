''' BinaryTree. '''

__all__ = ['BinaryTree', 'PREORDER', 'INORDER', 'POSTORDER']

from .tree import Tree
from .stack import Stack

PREORDER = 'PREORDER'
INORDER = 'INORDER'
POSTORDER = 'POSTORDER'

class BinaryTree(Tree):

	def __init__(self, value = None):
		self.value = value
		self.children = [None, None]

	def addChild(self, value):
		raise AttributeError('\'BinaryTree\' object has no attribute \'addChild\'')

	def left(self, *args):
		''' Set value if args exists else get value. '''
		if len(args) == 0:
			return self.children[0]

		if type(args[0]) != BinaryTree:
			raise TypeError('children of BinaryTree must be BinaryTree')

		self.children[0] = args[0]

	def right(self, *args):
		''' Set value if args exists else get value. '''
		if len(args) == 0:
			return self.children[1]

		if type(args[0]) != BinaryTree:
			raise TypeError('children of BinaryTree must be BinaryTree')

		self.children[1] = args[0]

	def dfs(self, mode = 'PREORDER') -> list:
		''' Return a list containing the tree in dfs order according to the given mode. '''

		out = []

		''' Setup left and right namespace for simplicity. '''
		left = self.children[0]
		right = self.children[1]

		''' Determine output order. '''
		if mode == 'PREORDER':
			out = [self] + (left.dfs(mode) if left else []) + (right.dfs(mode) if right else [])

		if mode == 'INORDER':
			out = (left.dfs(mode) if left else []) + [self] + (right.dfs(mode) if right else [])

		if mode == 'POSTORDER':
			out = (left.dfs(mode) if left else []) + (right.dfs(mode) if right else []) + [self]

		return out

	def __str__(self):
		return 'BinaryTree(value: %s, %d children)'%(self.value, len(self.children))

	def __repr__(self):
		return 'BinaryTree(value: %s, %d children)'%(self.value, len(self.children))