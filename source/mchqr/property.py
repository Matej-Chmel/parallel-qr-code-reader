class static_property(property):
    def __get__(self, _, owner):
        return staticmethod(self.fget).__get__(None, owner)()

if __name__ == '__main__':
	from dataclasses import dataclass

	@dataclass
	class Example:
		attribute: int

		@static_property
		def one():
			return Example(1)

	assert Example.one == Example(1)
	print('Both instances are equal.')
