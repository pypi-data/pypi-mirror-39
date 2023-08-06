'''
Defines a log renderer that performs its
rendering by HTTP POSTing the log message
to a specified address.
'''

class HttpPoster(object):
	'''HTTP POSTs text logs to a given address.
	'''

	def __init__(self, apiAddress):
		self._apiAddress = apiAddress
		raise NotImplementedError()

	def render(self, logText):
		'''POSTs the log text to the poster's API address.

		:param str logText: The text to be displayed.
		'''
		raise NotImplementedError()
