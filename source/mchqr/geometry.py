from dataclasses import astuple, dataclass
from mchqr.dev import static_property
from pyzbar.pyzbar import Point
from typing import NamedTuple

class color(NamedTuple):
	blue: int
	green: int
	red: int

class Color:
	@static_property
	def dark_blue():
		return color(240, 40, 20)

	@static_property
	def full_blue():
		return color(255, 0, 0)

	@static_property
	def full_green():
		return color(0, 255, 0)

	@static_property
	def full_red():
		return color(0, 0, 255)

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
