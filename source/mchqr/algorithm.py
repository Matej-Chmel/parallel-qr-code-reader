from dataclasses import dataclass
from mchqr.exceptions import NotOverriden
from mchqr.image_list import ImageList
from mchqr.typing import Solution
from time import perf_counter_ns

@dataclass
class Algorithm:
	images: ImageList

	def measure(self):
		start = perf_counter_ns()
		data = self.run()
		end = perf_counter_ns()

		return end - start, data

	def run(self) -> Solution:
		raise NotOverriden(self.run.__qualname__)

if __name__ == '__main__':
	class BadAlgorithm(Algorithm):
		pass

	class GoodAlgorithm(Algorithm):
		def run(_) -> Solution:
			return {
				'1.jpg': frozenset(['1a', '1b']),
				'2.jpg': frozenset(['2a', '2b'])
			}

	def print_test(*algorithm_types):
		print(
			*map(
				lambda algorithm_type: test_algorithm(
					algorithm_type(None)
				),
				algorithm_types
			),
			sep='\n'
		)

	def test_algorithm(algorithm: Algorithm):
		try:
			return algorithm.measure()
		
		except NotOverriden as e:
			return e

	print_test(BadAlgorithm, GoodAlgorithm)
