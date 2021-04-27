from __future__ import annotations
from mchqr.dev import PathList
from mchqr.geometry import Style
from mchqr.image import Image
from mchqr.io import is_escape
from mchqr.platform import screen_size
from mchqr.solution import AlgoSolution, DetectedList
from typing import Iterable

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
				.resize_max(max_width=screen.width // 2, max_height=screen.height)
				.show_in_center(screen)
			):
				break

	def stroke(self, solution: AlgoSolution, style: Style) -> ImageList:
		def stroke_detected_list(image: Image, detected_list: DetectedList) -> Image:
			return image.stroke_polygons(
				list(
					map(
						lambda detected: detected.polygon,
						detected_list
					)
				),
				style
			)

		return ImageList(
			map(
				lambda zipped: stroke_detected_list(*zipped),
				zip(
					self, solution.values()
				)
			)
		)
