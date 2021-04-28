from __future__ import annotations
from dataclasses import dataclass
from json import dump, dumps, JSONDecoder, load
from mchqr.dev import StrList
from mchqr.io import fopen
from numpy import ndarray
from pathlib import Path
from typing import Dict, List

@dataclass
class AlgoPair:
	name: str
	detected_list: DetectedList

	def __iter__(self):
		return iter((self.name, self.detected_list))

	def encode(self):
		return (
			self.name, (
				None if not self.detected_list else
				self.detected_list[0].content if len(self.detected_list) == 1
				else [
					detected.content
					for detected in self.detected_list
				]
			)
		)

@dataclass
class Detected:
	content: str
	polygon: ndarray

def dump_solution_to_file(path: Path, solution: AlgoSolution):
	with fopen(path, 'w+') as file:
		return dump(
			prepare_solution(solution),
			file,
			indent=4
		)

def dump_solution_to_str(solution: AlgoSolution):
	return dumps(
		prepare_solution(solution),
		indent=4
	)

def load_solution(path: Path) -> Solution:
	with fopen(path) as file:
		return load(file, cls=SolutionDecoder)

def prepare_solution(solution: AlgoSolution):
	return dict((
		AlgoPair(*pair).encode()
		for pair in solution.items()
	))

Solution = Dict[str, StrList]

class SolutionDecoder(JSONDecoder):
	def __init__(self, *args, **kwargs):
		super().__init__(object_hook=self.hook, *args, **kwargs)

	def hook(_, solution: dict) -> Solution:
		return {
			key:
				[] if value is None else
				[value] if isinstance(value, str)
				else value
			for key, value in solution.items()
		}

DetectedList = List[Detected]
AlgoSolution = Dict[str, DetectedList]
