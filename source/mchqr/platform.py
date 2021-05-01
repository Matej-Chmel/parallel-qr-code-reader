from __future__ import annotations
from mchqr.dev import NoScreen, UnsupportedOS
from mchqr.geometry import Size
from platform import system

class OsMetaClass(type):
	def __str__(self: OS):
		return 'Linux' if self.LINUX else 'Windows'

class OS(metaclass=OsMetaClass):
	LINUX = False
	WINDOWS = False

	@staticmethod
	def detect():
		os_name = system().rstrip().lower()

		if os_name.startswith('linux'):
			OS.LINUX = True

		elif os_name.startswith('win'):
			OS.WINDOWS = True

		else:
			detected_name = 'OS X' if os_name.startswith('darwin') else os_name

			raise UnsupportedOS(
				f'{detected_name} is not supported.'
			)

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
		raise NoScreen('No screen for displaying images found.')

OS.detect()
