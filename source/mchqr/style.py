from dataclasses import astuple, dataclass

@dataclass
class Color:
	red: int
	green: int
	blue: int

	@property
	def as_tuple(self):
		return (self.blue, self.green, self.red)

@dataclass
class Style:
	color: Color
	line_width: int = 8
