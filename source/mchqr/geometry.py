from dataclasses import astuple, dataclass
from mchqr import  static_property
import numpy as np
from pyzbar.pyzbar import Point
from typing import List

@dataclass
class Color:
	red: int
	green: int
	blue: int

	@property
	def as_tuple(self):
		return (self.blue, self.green, self.red)
	
	@static_property
	def dark_blue():
		return Color(20, 40, 240)

PointList = List[Point]

@dataclass
class Polygon:
	points: PointList

	@property
	def as_array(self):
		return np.array(self.points)

@dataclass
class Size:
	width: int
	height: int

	def __iter__(self):
		return iter(self.as_tuple)

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

@dataclass
class Style:
	color: Color
	line_width: int = 8

	@static_property
	def dark_blue(line_width: int = 8):
		return Style(Color.dark_blue, line_width)
