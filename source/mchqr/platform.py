from __future__ import annotations
from platform import system

class OsMetaClass(type):
	def __str__(self: OS):
		return 'Linux' if self.LINUX else 'Windows' if self.WINDOWS else 'OSX'

class OS(metaclass=OsMetaClass):
	LINUX = False
	WINDOWS = False
	X = False

	@staticmethod
	def detect():
		os_name = system().rstrip().lower()

		if os_name.startswith('linux'):
			OS.LINUX = True

		elif os_name.startswith('win'):
			OS.WINDOWS = True

		elif os_name.startswith('darwin'):
			OS.X = True

OS.detect()

if __name__ == '__main__':
	print(OS)
