''' Handler for io_stream requests. '''

__all__ = ['FILE', 'CONSOLE']

def FILE(path: str, method: str, buffer: list = None, value: str = None):
	''' Access a new line on call. '''
	if method == 'r':

		''' Populate the buffer. '''
		if buffer == None:
			with open(path, method) as f:
				buffer = f.readlines()

		return buffer.pop(0)[:-1], buffer

	if method == 'w':

		with open(path, 'a') as f:
			f.write(value)

def CONSOLE(path: str, method: str, buffer: list = None, value: str = None):
	'''Direct IO to the console.'''
	if method == 'r':
		return input(), buffer

	if method == 'w':
		print(value,end='')