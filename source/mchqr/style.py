from dataclasses import dataclass
from mchqr.property import static_property

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

@dataclass
class Style:
	color: Color
	line_width: int = 8

	@static_property
	def dark_blue(line_width: int = 8):
		return Style(Color.dark_blue, line_width)
