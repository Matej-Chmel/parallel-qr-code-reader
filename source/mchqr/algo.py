from dataclasses import dataclass
from mchqr.detector import Detector
from mchqr.dev import NotOverriden
from mchqr.image_list import ImageList
from mchqr.solution import AlgoSolution
from time import perf_counter_ns

@dataclass
class BaseAlgorithm:
	detector: Detector
	images: ImageList

	def measure(self):
		start = perf_counter_ns()
		data = self.run()
		end = perf_counter_ns()

		return end - start, data

	def run(self) -> AlgoSolution:
		raise NotOverriden(self.run)

class Sequence(BaseAlgorithm):
	def run(self) -> AlgoSolution:
		return dict(
			map(self.detector, self.images)
		)
