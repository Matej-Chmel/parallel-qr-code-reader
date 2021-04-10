import cv2 as cv
from dataclasses import astuple, dataclass
from pathlib import Path
from mchqr.keys import is_escape, wait_key

class Image:
	def __init__(self, path: Path):
		self.matrix = cv.imread(str(path))
		self.name = path.stem

	def get_max_size(self, max_width, max_height=None):
		if not max_height:
			max_height = max_width

		if self.height > max_height:
			size = self.get_resized_same_ratio_size(new_height=max_height)
			size.width = min(size.width, max_width)
		else:
			size = self.get_resized_same_ratio_size(new_width=max_width)
			size.height = min(size.height, max_height)

		return size

	def get_resized_same_ratio_size(self, new_height=None, new_width=None):
		old_height, old_width = self.height, self.width

		if not new_height and not new_width:
			return
		
		if new_height and new_width:
			return Size(new_height, new_width)
		elif not new_height:
			return Size(new_width, old_height * new_width / old_width)
		else:
			return Size(old_width * new_height / old_height, new_height)

	@property
	def matrix(self):
		return self.__matrix

	@matrix.setter
	def matrix(self, value):
		self.__matrix = value
		self.height, self.width = value.shape[:2]

	def resize_by_ratio(self, new_height=None, new_width=None):
		return self.resize_by_size(self.get_resized_same_ratio_size(new_height, new_width))

	def resize_by_size(self, size):
		self.matrix = cv.resize(self.matrix, astuple(size), interpolation=cv.INTER_AREA)
		return self

	def resize_max(self, max_width, max_height=None):
		return self.resize_by_size(self.get_max_size(max_width, max_height))

	def show(self, x=0, y=0):
		cv.namedWindow(self.name)
		cv.moveWindow(self.name, x, y)
		cv.imshow(self.name, self.matrix)

		key = wait_key()

		cv.destroyWindow(self.name)
		return key

class NoData(Exception):
	def __init__(self, message):
		super().__init__(message)

@dataclass
class Size:
	height: int
	width: int

	def __post_init__(self):
		self.height = int(self.height)
		self.width = int(self.width)

def show_images(paths):
	data_found = False

	for path in paths:
		data_found = True

		if is_escape(Image(path).resize_max(max_width=384).show()):
			break

	if not data_found:
		raise NoData('No images to show.')

if __name__ == '__main__':
	from mchqr.data import yield_datasets, yield_image_files

	try:
		show_images(yield_image_files(next(yield_datasets())))

	except NoData as e:
		print(e)

	except StopIteration:
		print('No available datasets.')