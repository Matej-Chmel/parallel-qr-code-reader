import cv2 as cv
from dataclasses import dataclass, field
from mchqr.dev import NdArrayList, PathList
from mchqr.geometry import Point, Size, Style
from mchqr.io import is_escape, wait_key
from mchqr.platform import screen_size
from mchqr.solution import AlgoSolution
from numpy import ndarray
from pathlib import Path
from typing import Iterable

@dataclass
class Image:
	height: int = field(init=False)
	matrix: ndarray
	path: Path
	width: int = field(init=False)

	def __post_init__(self):
		self.height, self.width = self.shape[:2]

	@staticmethod
	def from_path(path: Path):
		return Image(
			cv.imread(
				str(path)
			), path
		)

	def max_size(self, max_width: int, max_height: int = None):
		if not max_height:
			max_height = max_width

		if self.height > max_height:
			size = self.resized_same_ratio_size(new_height=max_height)
			size.width = min(size.width, max_width)
		else:
			size = self.resized_same_ratio_size(new_width=max_width)
			size.height = min(size.height, max_height)

		return size

	@property
	def name(self):
		return self.path.stem

	def new(self, matrix: ndarray):
		return Image(matrix, self.path)

	@property
	def path_as_str(self):
		return str(self.path)

	def resize_by_ratio(self, new_height: int = None, new_width: int = None):
		return self.resize_by_size(
			self.resized_same_ratio_size(new_height, new_width)
		)

	def resize_by_size(self, size: Size):
		return self.new(
			cv.resize(self.matrix, size.as_tuple, interpolation=cv.INTER_AREA)
		)

	def resize_max(self, max_width: int, max_height: int = None):
		return self.resize_by_size(
			self.max_size(max_width, max_height)
		)

	def resized_same_ratio_size(self, new_height: int = None, new_width: int = None) -> Size:
		old_height, old_width = self.height, self.width

		if not new_height and not new_width:
			return
		
		if new_height and new_width:
			return Size(new_height, new_width)
		elif not new_height:
			return Size(new_width, old_height * new_width / old_width).as_int
		else:
			return Size(old_width * new_height / old_height, new_height).as_int

	@property
	def shape(self):
		return self.matrix.shape

	def show(self, x: int = 0, y: int = 0):
		name = self.name

		cv.namedWindow(name)
		cv.moveWindow(name, x, y)
		cv.imshow(name, self.matrix)

		key = wait_key()

		cv.destroyWindow(name)
		return key

	def show_in_center(self, screen: Size):
		center = screen.center

		return self.show(
			center.x - self.width // 2,
			center.y - self.height // 2
		)

	def split(self, split_size: Size):
		return ImageList((
			self.view(
				Point(x, y),
				split_size
			)
			for y in range(0, self.height, split_size.height // 2)
			for x in range(0, self.width, split_size.width // 2)
		))

	def stroke_polygons(self, polygons: NdArrayList, style: Style):
		return self.new(
			cv.polylines(self.matrix, polygons, True, style.color, style.line_width)
		)

	def view(self, origin: Point, size: Size):
		return ImageView(
			self.matrix[self.view_index(origin, size)],
			self.path,
			origin
		)

	def view_index(self, origin: Point, size: Size):
		return (
			slice(origin.y, origin.y + size.height),
			slice(origin.x, origin.x + size.width)
		)

class ImageList(list):
	def __init__(_, images: Iterable[Image]):
		super().__init__(images)

	@staticmethod
	def from_paths(paths: PathList):
		return ImageList(
			map(Image.from_path, paths)
		)

	def show(self):
		screen = screen_size()

		for image in self:
			image: Image

			if is_escape(image
				.resize_max(screen.width // 2, screen.height)
				.show_in_center(screen)
			):
				break

	def stroke(self, solution: AlgoSolution, style: Style):
		return ImageList((
			image.stroke_polygons([
					detected.polygon
					for detected in detected_list
				],
				style
			)
			for image, detected_list in zip(
				self,
				solution.values()
			)
		))

@dataclass
class ImageView(Image):
	origin: Point

	def index(self):
		return self.view_index(
			self.origin,
			Size(self.width, self.height)
		)
