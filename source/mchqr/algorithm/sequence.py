from .base import BaseAlgorithm
from mchqr.solution import extract_content, Solution

class Sequence(BaseAlgorithm):
	def run(self) -> Solution:
		return {
			image.name : extract_content(
				image.detect()
			)
			for image in self.images
		}
