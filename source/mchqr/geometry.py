from dataclasses import astuple, dataclass
import numpy as np
from pyzbar.pyzbar import Point
from typing import List

PointList = List[Point]

@dataclass
class Polygon:
	points: PointList

	@property
	def as_array(self):
		return np.array(self.points).reshape((-1, 1, 2))

@dataclass
class Size:
	width: int
	height: int

	@property
	def as_int(self):
		return Size(
			round(self.width),
			round(self.height)
		)

	@property
	def as_tuple(self):
		return astuple(self)

	@property
	def center(self):
		return Point(self.width // 2, self.height // 2)

if __name__ == '__main__':
	size = Size(100, 200)

	print(
		size,
		size.as_tuple,
		size.center,
		Size(4.1, 5.5).as_int,
		sep='\n'
	)
