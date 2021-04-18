class MessageException(Exception):
	def __init__(_, message=''):
		super().__init__(message)

class NoData(MessageException):
	pass

class NoScreen(MessageException):
	pass
