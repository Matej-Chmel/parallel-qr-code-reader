from dataclasses import dataclass
from mchqr.detector import Detector
from mchqr.dev import NotOverriden, subclasses_dict
from mchqr.image import ImageList
from mchqr.solution import AlgoSolution
from multiprocessing import Pool
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

class ProcessPool(BaseAlgorithm):
	def run(self) -> AlgoSolution:
		with Pool(len(self.images)) as pool:
			return dict(
				pool.map(self.detector, self.images)
			)

class Sequence(BaseAlgorithm):
	def run(self) -> AlgoSolution:
		return dict(
			map(self.detector, self.images)
		)

algos = subclasses_dict(BaseAlgorithm)
