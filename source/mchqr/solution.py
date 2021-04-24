from __future__ import annotations
from dataclasses import dataclass
from json import dump, JSONDecoder, load
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
				else list(
					map(
						lambda detected: detected.content,
						self.detected_list
					)
				)
			)
		)

def decode_content_solution(path: Path) -> Solution:
	with fopen(path) as file:
		return load(file, cls=SolutionDecoder)

@dataclass
class Detected:
	content: str
	polygon: ndarray

def encode_solution(path: Path, solution: AlgoSolution):
	with fopen(path, 'w+') as file:
		return dump(
			dict(
				map(
					lambda pair: AlgoPair(*pair).encode(),
					solution.items()
				)
			),
			file,
			indent=4
		)

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
