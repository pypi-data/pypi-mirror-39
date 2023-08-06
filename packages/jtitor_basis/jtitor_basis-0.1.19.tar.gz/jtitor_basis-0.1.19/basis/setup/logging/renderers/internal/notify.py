'''Attempts to place the given notification to the user's
screen.
'''
import sys
import os

kMacOsNotifyCommand = "osascript -e 'display notification \"{1}\" with title \"{0}\"'"

def postNotification(title, body = ""):
	'''Sends an OS notification.

	:param str title: The notification's title.
	:param str body: The notification's body. Can be empty or None.
	'''
	if sys.platform == "linux" or sys.platform == "linux2":
		raise NotImplementedError("Notifications not implemented for Linux!")
	elif sys.platform == "darwin":
		#MacOS doesn't have a no-body notification.
		os.system(kMacOsNotifyCommand.format(title, body))
	elif sys.platform == "win32":
		raise NotImplementedError("Notifications not implemented for Windows!")
