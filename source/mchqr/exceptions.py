class MessageException(Exception):
	def __init__(_, message: str = ''):
		super().__init__(message)

class NoScreen(MessageException):
	pass

class NotOverriden(MessageException):
	def __init__(_, method_name: str):
		super().__init__(
			f'Method {method_name} is abstract and must be overriden.'
		)
