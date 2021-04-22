from __future__ import annotations
from mchqr.image import Image
from mchqr.keys import is_escape
from mchqr.screen import screen_size
from mchqr.style import Style
from mchqr.typing import DecodedMatrix, PathList
from typing import Iterable

class ImageList(list):
	def __init__(_, images: Iterable[Image]):
		super().__init__(images)

	def detect(self) -> DecodedMatrix:
		return list(
			map(Image.detect, self)
		)

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

	def stroke_decoded_matrix(self, decoded_matrix: DecodedMatrix, style: Style) -> ImageList:
		return ImageList([
			image.stroke_decoded_list(decoded_list, style)
			for image, decoded_list in zip(self, decoded_matrix)
		])

if __name__ == '__main__':
	from mchqr.test import on_first_dataset

	def show_all(image_paths: PathList):
		images = ImageList.from_paths(image_paths)

		images.stroke_decoded_matrix(
			images.detect(), Style.dark_blue
		).show()

	on_first_dataset(show_all)
