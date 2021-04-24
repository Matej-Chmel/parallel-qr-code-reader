from __future__ import annotations
import cv2 as cv
from dataclasses import dataclass
from pathlib import Path
from mchqr import DecodedList
from mchqr.geometry import Polygon, Size, Style
from mchqr.io import wait_key
from numpy import ndarray
from pyzbar.pyzbar import decode, Decoded, ZBarSymbol

@dataclass
class Image:
	matrix: ndarray
	name: str

	def __post_init__(self):
		self.height, self.width = self.matrix.shape[:2]

	def detect(self) -> DecodedList:
		return decode(self.matrix, [ZBarSymbol.QRCODE])

	@staticmethod
	def from_path(path: Path):
		return Image(
			cv.imread(
				str(path)
			), path.stem
		)

	def max_size(self, max_width: int, max_height: int = None) -> Size:
		if not max_height:
			max_height = max_width

		if self.height > max_height:
			size = self.resized_same_ratio_size(new_height=max_height)
			size.width = min(size.width, max_width)
		else:
			size = self.resized_same_ratio_size(new_width=max_width)
			size.height = min(size.height, max_height)

		return size

	def resize_by_ratio(self, new_height: int = None, new_width: int = None) -> Image:
		return self.resize_by_size(
			self.resized_same_ratio_size(new_height, new_width)
		)

	def resize_by_size(self, size: Size):
		return Image(
			cv.resize(self.matrix, size.as_tuple, interpolation=cv.INTER_AREA),
			self.name
		)

	def resize_max(self, max_width: int, max_height: int = None) -> Image:
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

	def show(self, x: int = 0, y: int = 0):
		cv.namedWindow(self.name)
		cv.moveWindow(self.name, x, y)
		cv.imshow(self.name, self.matrix)

		key: int = wait_key()

		cv.destroyWindow(self.name)
		return key

	def show_in_center(self, screen: Size):
		center = screen.center
		x = center.x - self.width // 2
		y = center.y - self.height // 2
		return self.show(x, y)

	def stroke_decoded(self, decoded: Decoded, style: Style):
		return self.stroke_polygon(
			Polygon(decoded.polygon), style
		)
	
	def stroke_decoded_list(self, decoded_list: DecodedList, style: Style):
		image = self

		for decoded in decoded_list:
			image = image.stroke_decoded(decoded, style)

		return image

	def stroke_polygon(self, polygon: Polygon, style: Style):
		return Image(
			cv.polylines(self.matrix, [polygon.as_array], True, style.color.as_tuple, style.line_width),
			self.name
		)
