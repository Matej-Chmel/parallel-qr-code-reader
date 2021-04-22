from mchqr.algorithm import Algorithm
from mchqr.extraction import extract_content
from mchqr.typing import Solution

class SequentialAlgorithm(Algorithm):
	def run(self) -> Solution:
		return {
			image.name : extract_content(
				image.detect()
			)
			for image in self.images
		}
