from dataclasses import dataclass
from mchqr import NotOverriden
from mchqr.image_list import ImageList
from mchqr.solution import Solution
from time import perf_counter_ns

@dataclass
class BaseAlgorithm:
	images: ImageList

	def measure(self):
		start = perf_counter_ns()
		data = self.run()
		end = perf_counter_ns()

		return end - start, data

	def run(self) -> Solution:
		raise NotOverriden(self.run.__qualname__)
