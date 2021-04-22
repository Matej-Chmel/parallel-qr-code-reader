from json import dump, JSONDecoder, JSONEncoder, load
from mchqr import fopen
from mchqr.typing import Solution
from pathlib import Path

def decode_solution(path: Path) -> Solution:
	with fopen(path) as file:
		return load(file, cls=SolutionDecoder)

def encode_solution(path: Path, solution: Solution):
	with fopen(path, 'w+') as file:
		return dump(solution, file, cls=SolutionEncoder, indent=4)

class SolutionDecoder(JSONDecoder):
	def __init__(self, *args, **kwargs):
		super().__init__(object_hook=self.hook, *args, **kwargs)

	def hook(_, solution: dict) -> Solution:
		return {
			key:
				frozenset() if value is None else
				frozenset([value]) if isinstance(value, str) else
				frozenset(value)
			for key, value in solution.items()
		}

class SolutionEncoder(JSONEncoder):
	def default(self, o):
		if isinstance(o, frozenset):
			data = list(o)

			if not data:
				return None

			if len(data) == 1:
				return data[0]

			return data

		return super().default(o)

if __name__ == '__main__':
	from mchqr.image_list import ImageList
	from mchqr.sequential_algorithm import SequentialAlgorithm
	from mchqr.test import on_first_dataset
	from mchqr.typing import PathList

	def save_decoded(path: Path, image_paths: PathList):
		elapsed, solution = SequentialAlgorithm(
			ImageList.from_paths(image_paths)
		).measure()

		encode_solution(
			path.joinpath('solution.json'), solution
		)
		print(f'Elapsed: {elapsed / 1_000_000_000 : .2f} seconds')

	on_first_dataset(save_decoded)
