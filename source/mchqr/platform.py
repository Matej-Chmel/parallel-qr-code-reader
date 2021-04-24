from __future__ import annotations
from mchqr.geometry import Size
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

def screen_size():
	if OS.WINDOWS:
		import ctypes
		from win32api import GetMonitorInfo, MonitorFromPoint

		ctypes.windll.shcore.SetProcessDpiAwareness(2)

		monitor_info = GetMonitorInfo(
			MonitorFromPoint((0, 0))
		)
		monitor_area = monitor_info.get("Monitor")
		work_area = monitor_info.get("Work")

		def dimension(i: int):
			monitor_dimension = monitor_area[i]
			work_dimension = work_area[i]

			return (
				work_dimension
				if monitor_dimension == work_dimension
				else work_dimension - monitor_dimension // 20
			)

		return Size(
			dimension(2),
			dimension(3)
		)

	try:
		from screeninfo import get_monitors

		screen = get_monitors()[0]
		return Size(screen.width, screen.height)
	
	except IndexError:
		from mchqr.dev import NoScreen

		raise NoScreen('No screen for displaying images found.')

OS.detect()
