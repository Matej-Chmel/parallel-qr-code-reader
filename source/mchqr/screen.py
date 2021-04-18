from mchqr.exceptions import NoScreen
from mchqr.geometry import Size
from mchqr.platform import OS

class DesktopSize(Size):
	def __init__(self, work_size: Size, taskbar_size: Size):
		super().__init__(*work_size)
		self.taskbar = taskbar_size

	@Size.height.getter
	def height(self):
		return self._y - self.taskbar.height

def screen_size():
	if OS.WINDOWS:
		import ctypes
		from win32api import GetMonitorInfo, MonitorFromPoint

		ctypes.windll.shcore.SetProcessDpiAwareness(2)
		monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
		monitor_area = monitor_info.get("Monitor")
		work_area = monitor_info.get("Work")

		return DesktopSize(
			Size(monitor_area[2], monitor_area[3]),
			Size(work_area[2], (monitor_area[3] - work_area[3]) * 2)
		)

	from screeninfo import get_monitors

	try:
		screen = get_monitors()[0]
		return Size(screen.width, screen.height)
	
	except IndexError:
		raise NoScreen('No screen for displaying images found.')

if __name__ == '__main__':
	screen = screen_size()
	print(screen, screen.center, sep='\n')
