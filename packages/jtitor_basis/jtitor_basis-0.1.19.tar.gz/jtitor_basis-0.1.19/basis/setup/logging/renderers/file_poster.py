'''
Defines a log renderer that performs its
rendering by writing text to a given file path.
'''

class FilePoster(object):
	'''Renders log messages as OS notifications.
	'''

	def __init__(self, filePath):
		'''Class initializer.

		:param str filePath: The path to the file to save the log text in.

		:raises: Unknown, depends on the errors file.open() raises.
		'''
		raise NotImplementedError()

	def render(self, logText):
		'''Posts the log text as
		colored text to standard output.

		:param str logText: The text to be displayed.
		'''
		raise NotImplementedError()
