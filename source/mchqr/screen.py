from mchqr.exceptions import NoScreen
from mchqr.geometry import Size
from mchqr.platform import OS

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

		dimension = lambda i: monitor_area[i] - (monitor_area[i] - work_area[i]) * 2

		return Size(
			dimension(2),
			dimension(3)
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
