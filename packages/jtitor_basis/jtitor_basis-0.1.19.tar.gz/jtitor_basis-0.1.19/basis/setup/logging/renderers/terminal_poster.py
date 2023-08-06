'''
Defines a log renderer that performs its
rendering by writing colored text to standard output.
'''

class TerminalPoster(object):
	'''Renders log messages as OS notifications.
	'''

	def __init__(self):
		raise NotImplementedError()

	def render(self, logText):
		'''Posts the log text as
		colored text to standard output.

		:param str logText: The text to be displayed.
		'''
		raise NotImplementedError()
