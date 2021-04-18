class Point:
	@property
	def as_tuple(self):
		return (self.x, self.y)
	
	@property
	def as_list(self):
		return [self.x, self.y]

	def __init__(self, x, y, item_type=int):
		self.item_type = item_type
		self.x = x
		self.y = y

	def __iter__(self):
		return iter((self.x, self.y, self.item_type))

	def __str__(self):
		return str(self.as_list)

	@property
	def x(self):
		return self._x
	
	@x.setter
	def x(self, value):
		self._x = self.item_type(value)
	
	@property
	def y(self):
		return self._y
	
	@y.setter
	def y(self, value):
		self._y = self.item_type(value)

class Size(Point):
	def __init__(self, width, height, item_type=int):
		super().__init__(width, height, item_type)

	@property
	def center(self):
		return Point(self.width / 2, self.height / 2, self.item_type)

	@property
	def height(self):
		return self.y

	@height.setter
	def height(self, value):
		self.y = value
	
	@property
	def width(self):
		return self.x

	@width.setter
	def width(self, value):
		self.x = value

if __name__ == '__main__':
	print('\n'.join(
		map(str, [
			Point(1, 2),
			Point(1.1, 1.9, round),
			Point(2.1, 3.5, float),
			Size(4.5, 4).center,
			Size(4, 5).as_tuple,
			Size(6, 10.1, float).as_list
		])
	))
