from json import dump, JSONDecoder, JSONEncoder, load
from mchqr import DecodedList, StrFrozenSet
from mchqr.io import fopen
from pathlib import Path
from typing import Dict

Solution = Dict[str, StrFrozenSet]

def decode_solution(path: Path) -> Solution:
	with fopen(path) as file:
		return load(file, cls=SolutionDecoder)

def encode_solution(path: Path, solution: Solution):
	with fopen(path, 'w+') as file:
		return dump(solution, file, cls=SolutionEncoder, indent=4)

def extract_content(decoded_list: DecodedList) -> StrFrozenSet:
	return frozenset(
		map(
			lambda decoded: decoded.data.decode('utf-8'),
			decoded_list
		)
	)

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
