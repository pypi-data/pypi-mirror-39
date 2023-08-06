'''
Defines a log renderer that performs its
rendering by creating an OS notification.
'''
from .internal import postNotification

class NotificationPoster(object):
	'''Renders log messages as OS notifications.
	'''

	def __init__(self):
		raise NotImplementedError()

	def render(self, logText):
		'''Posts the log text as an OS notification.

		:param str logText: The text to be displayed.
		'''
		postNotification(logText)
